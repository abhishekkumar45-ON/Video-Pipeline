#!/usr/bin/env python3
"""
batch_build.py — UNATTENDED renderer for the Orange Nelumbo DEBRIEF pipeline.

Scene AUTHORING (writing scenes/<id>.py) is LLM work done in chat — this script
does NOT author anything. It only drives the deterministic half of the pipeline
(gate -> render 4K -> intro/outro -> ducked music -> Drive upload -> mark done)
over every question that ALREADY has a scene file. Safe to leave running for hours.

It renders WORKERS videos at a time (default 2 — right for an 8-core / 16 GB M2).
Each build's full output goes to logs/<id>.log so concurrent runs don't interleave;
this script's own stream carries only start/finish markers + a final summary.
It never stops on a single failure: orchestrator.py marks a bad scene "review" and
returns, so the batch just logs it and moves on. questions.json updates are made
under a cross-process lock by orchestrator.py, so parallel writes are safe.

Usage (normally launched for you in the background):
  .venv/bin/python batch_build.py                       # all Thermodynamics scenes not yet done, 2 at a time
  .venv/bin/python batch_build.py --workers 1           # fully sequential
  .venv/bin/python batch_build.py --chapter Kinematics
  .venv/bin/python batch_build.py --ids q11 q12 q13     # explicit list, any chapter
  .venv/bin/python batch_build.py --quality=-qm         # faster preview instead of 4K
"""
import argparse
import concurrent.futures as futures
import datetime
import json
import os
import subprocess
import sys
import threading
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = os.path.join(ROOT, ".venv", "bin", "python")
QUESTIONS = os.path.join(ROOT, "questions.json")
SCENES = os.path.join(ROOT, "scenes")
LOGS = os.path.join(ROOT, "logs")

_print_lock = threading.Lock()


def load():
    with open(QUESTIONS, encoding="utf-8") as f:
        return json.load(f)


def q_field(qid, field, default=None):
    for q in load():
        if q["id"] == qid:
            return q.get(field, default)
    return default


def log(msg):
    with _print_lock:
        print(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


def build_one(q, args, index, total):
    """Run the full pipeline for one question, streaming its output to logs/<id>.log."""
    qid = q["id"]
    chapter = q.get("chapter", "Misc")
    cmd = [PY, "orchestrator.py", "build", qid, f"--quality={args.quality}"]
    if not args.no_music:
        cmd.append("--music")
    if not args.no_drive:
        cmd.append(f"--drive={args.drive_root}/{chapter}")

    attempts = max(1, args.retries + 1)
    log(f">>> [{index}/{total}] START {qid} ({chapter}) -> logs/{qid}.log")
    t0 = time.time()
    status, url, rc = "?", None, -1
    with open(os.path.join(LOGS, f"{qid}.log"), "w", encoding="utf-8") as lf:
        for attempt in range(1, attempts + 1):
            lf.write(f"# {qid} attempt {attempt}/{attempts} :: {' '.join(cmd)}\n\n")
            lf.flush()
            rc = subprocess.run(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT).returncode
            status = q_field(qid, "status", "?")
            url = q_field(qid, "video_url")
            if status == "done":
                break
            if attempt < attempts:
                msg = f"    retry {qid}: status={status} after attempt {attempt}/{attempts} (likely transient)"
                log(msg); lf.write(f"\n{msg}\n\n"); lf.flush()
    dt = time.time() - t0

    ok = status == "done"
    log(f"<<< [{index}/{total}] {'DONE ✅' if ok else 'NEEDS REVIEW ⚠️'} {qid} "
        f"(status={status}, rc={rc}, {dt/60:.1f} min) {url or ''}")
    return qid, ok, status, url, dt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", default="Thermodynamics",
                    help="build every not-done question in this chapter that has a scene file")
    ap.add_argument("--ids", nargs="*", help="explicit ids (overrides --chapter)")
    ap.add_argument("--workers", type=int, default=2, help="videos to render at once (default 2)")
    ap.add_argument("--retries", type=int, default=1, help="re-run a build this many times if it doesn't reach 'done' (default 1)")
    ap.add_argument("--quality", default="-qk", help="-qk 4K final (default), -qm medium, -ql fast")
    ap.add_argument("--drive-root", default="gdrive:JEE-Videos",
                    help="rclone remote root; final folder is <root>/<chapter>")
    ap.add_argument("--no-music", action="store_true")
    ap.add_argument("--no-drive", action="store_true", help="render locally, skip upload")
    ap.add_argument("--include-done", action="store_true", help="re-build questions already marked done")
    args = ap.parse_args()

    os.makedirs(LOGS, exist_ok=True)
    qs = load()
    if args.ids:
        picked = [q for q in qs if q["id"] in args.ids]
    else:
        picked = [q for q in qs if q.get("chapter", "") == args.chapter]

    ready, skipped = [], []
    for q in picked:
        if not os.path.exists(os.path.join(SCENES, f"{q['id']}.py")):
            skipped.append((q["id"], "no scene file"))
        elif q.get("status") == "done" and not args.include_done:
            skipped.append((q["id"], "already done"))
        else:
            ready.append(q)

    workers = max(1, min(args.workers, len(ready) or 1))
    log(f"batch start · {len(ready)} to build · workers={workers} · quality={args.quality} "
        f"· music={not args.no_music} · drive={not args.no_drive}")
    for qid, why in skipped:
        log(f"  skip {qid}: {why}")
    log(f"  queue: {[q['id'] for q in ready]}")
    if not ready:
        log("nothing to build — exiting.")
        return

    total = len(ready)
    results = []
    with futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(build_one, q, args, i, total): q["id"]
                for i, q in enumerate(ready, 1)}
        for fut in futures.as_completed(futs):
            results.append(fut.result())

    results.sort(key=lambda r: r[0])
    log("================ BATCH SUMMARY ================")
    for qid, ok, status, url, dt in results:
        log(f"  {'✅' if ok else '⚠️ '} {qid:6} {status:8} {dt/60:5.1f} min  {url or ''}")
    done = sum(1 for r in results if r[1])
    log(f"finished {done}/{len(results)} rendered & uploaded")
    if done < len(results):
        log("  (⚠️  = failed gate/render; its scenes/<id>.py needs a fix in chat, then re-run the batch)")
    sys.exit(0 if done == len(results) else 1)


if __name__ == "__main__":
    main()
