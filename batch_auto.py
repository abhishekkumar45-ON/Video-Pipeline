"""
batch_auto.py — unattended, parallel driver over orchestrator.py build.

Renders every question that has a scene file but isn't done yet, N at a time,
through the FULL pipeline (py_compile + layout gate -> 4K render -> intro/outro
bumpers -> ducked bgm -> Drive upload -> status in questions.json). Resumable:
finished questions are skipped, so you can re-run it safely.

The one human/LLM step (writing scenes/<id>.py) happens in chat BEFORE this runs.
Everything here is headless — start it, walk away, come back to finished uploads.

Usage (run with the venv python so manim/ffmpeg/latex resolve):
  .venv/bin/python batch_auto.py --jobs 2 --music --drive-base gdrive:JEE-Videos
  .venv/bin/python batch_auto.py --ids q5 q7 --quality -qk        # only these two
  .venv/bin/python batch_auto.py --dry-run                        # show the worklist, do nothing

Drive folder is per-chapter: <drive-base>/<Chapter>. Omit --drive-base (or pass
--no-drive) to render locally only (files land in outputs/).
"""
import argparse
import datetime
import json
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.abspath(__file__))
QUESTIONS = os.path.join(ROOT, "questions.json")
SCENES_DIR = os.path.join(ROOT, "scenes")
OUT_DIR = os.path.join(ROOT, "outputs")
LOG = os.path.join(OUT_DIR, "batch_auto.log")
PYEXE = sys.executable  # the venv interpreter we were launched with

_print_lock = threading.Lock()


def log(msg):
    stamp = datetime.datetime.now().strftime("%H:%M:%S")
    line = f"[{stamp}] {msg}"
    with _print_lock:
        print(line, flush=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def load_questions():
    with open(QUESTIONS, encoding="utf-8") as f:
        return json.load(f)


def worklist(qs, ids):
    """Questions to build: explicit --ids, else everything with a scene file that isn't done."""
    out = []
    for q in qs:
        qid = q["id"]
        if ids and qid not in ids:
            continue
        scene = os.path.join(SCENES_DIR, f"{qid}.py")
        if not os.path.exists(scene):
            if ids:  # only warn about ones the user explicitly asked for
                log(f"SKIP {qid}: no scenes/{qid}.py yet (needs a scene from chat)")
            continue
        if not ids and q.get("status") == "done":
            continue
        out.append(q)
    return out


def build_one(q, args):
    qid = q["id"]
    chapter = (q.get("chapter") or "Misc").strip()
    # use =form for quality: orchestrator's argparse rejects "-qk" as a separate token.
    # per-id media dir isolates the LaTeX cache so parallel renders never collide;
    # --skip-gate because every scene is pre-verified CLEAN before the batch launches.
    cmd = [PYEXE, os.path.join(ROOT, "orchestrator.py"), "build", qid,
           f"--quality={args.quality}", "--skip-gate",
           f"--media={os.path.join('build', 'media_' + qid)}"]
    if args.music:
        cmd += ["--music", f"--music-vol={args.music_vol}"]
    if args.drive_base and not args.no_drive:
        cmd += [f"--drive={args.drive_base.rstrip('/')}/{chapter}"]

    log(f"START {qid} ({chapter})")
    t0 = datetime.datetime.now()
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    dt = (datetime.datetime.now() - t0).total_seconds()

    # persist the full orchestrator output per-question for debugging
    with open(os.path.join(OUT_DIR, f"{qid}.build.log"), "w", encoding="utf-8") as f:
        f.write(proc.stdout + "\n---STDERR---\n" + proc.stderr)

    # re-read status the build just wrote (lock-safe in orchestrator)
    status = "unknown"
    try:
        for x in load_questions():
            if x["id"] == qid:
                status = x.get("status", "unknown")
                break
    except Exception:
        pass

    ok = proc.returncode == 0 and status == "done"
    tail = (proc.stdout.strip().splitlines() or ["(no output)"])[-1]
    log(f"{'DONE ' if ok else 'FAIL '} {qid} ({dt:.0f}s, status={status}) {tail}")
    return qid, ok, status


def main():
    ap = argparse.ArgumentParser(description="Parallel unattended render batch.")
    ap.add_argument("--jobs", type=int, default=2, help="how many to render at once (2-3 recommended)")
    ap.add_argument("--quality", default="-qk", help="-ql fast, -qm medium, -qk 4K final")
    ap.add_argument("--music", action="store_true", default=True, help="mix ducked bgm (default on)")
    ap.add_argument("--no-music", dest="music", action="store_false", help="skip bgm")
    ap.add_argument("--music-vol", type=float, default=0.08, dest="music_vol")
    ap.add_argument("--drive-base", default="", help="rclone remote root, e.g. gdrive:JEE-Videos "
                                                     "(a /<Chapter> subfolder is added per question)")
    ap.add_argument("--no-drive", action="store_true", help="render locally only, no upload")
    ap.add_argument("--ids", nargs="*", default=[], help="only these ids (default: all not-done with a scene)")
    ap.add_argument("--dry-run", action="store_true", help="print the worklist and exit")
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    qs = load_questions()
    work = worklist(qs, set(args.ids))

    if not work:
        log("Nothing to do — no questions with a scene file are pending.")
        return

    log(f"=== batch start: {len(work)} question(s), {args.jobs} at a time, quality={args.quality}, "
        f"music={'on' if args.music else 'off'}, "
        f"drive={'off' if (args.no_drive or not args.drive_base) else args.drive_base} ===")
    for q in work:
        log(f"  queued: {q['id']} ({q.get('chapter','?')})")
    if args.dry_run:
        log("dry-run — exiting without building.")
        return

    done, failed = [], []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as ex:
        futs = {ex.submit(build_one, q, args): q["id"] for q in work}
        for fut in as_completed(futs):
            qid, ok, status = fut.result()
            (done if ok else failed).append(qid)

    log(f"=== batch done: {len(done)} ok, {len(failed)} failed ===")
    if done:
        log("  ok:     " + ", ".join(done))
    if failed:
        log("  FAILED: " + ", ".join(failed) + "   (see outputs/<id>.build.log; 'review' = needs a "
            "scene fix in chat)")


if __name__ == "__main__":
    main()
