"""
orchestrator.py — assisted question -> narrated Manim video pipeline (ZERO cost).

Your org blocked headless `claude -p`, and you won't pay the API. So the LLM step
(writing the Manim code) stays in THIS chat, which is free on your subscription.
The orchestrator automates everything around it: question tracking, the paste-ready
prompt, the compile+render gate, Drive upload, and resumable state.

Two-step loop per question:

  1) python orchestrator.py next
        Selector picks the next `pending` question, builds the full prompt
        (brand_system.md + q1.py exemplar + the question), writes it to
        prompts/<id>.txt AND copies it to your clipboard.
        -> Paste it into the Claude chat. Save the ```python reply to scenes/<id>.py.

  2) python orchestrator.py build <id> [--quality=-qh] [--drive=gdrive:JEE-Videos/Kinematics]
        Gate (py_compile) -> render -> copy to outputs/<id>.mp4 -> upload to Drive
        -> mark the question done (+url) in questions.json.
        If the render fails, it writes prompts/<id>_repair.txt (traceback + your code)
        and copies it to the clipboard -> paste that, re-save scenes/<id>.py, build again.

  python orchestrator.py status         # table of every question + its state

Prereqs in the shell:
  source .venv/bin/activate
  eval "$(/usr/libexec/path_helper)"    # so latex/MathTex resolves

Phase-2 (when you fund an API key, these become real autonomous agents):
  script_judge(), visual_qc(), caption_writer() hooks are stubbed below.
"""
import argparse
import contextlib
import fcntl
import glob
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
QUESTIONS = os.path.join(ROOT, "questions.json")
BRAND = os.path.join(ROOT, "guidelines", "masterclass", "03_video_guidelines.txt")
EXEMPLAR = os.path.join(ROOT, "scenes", "t1.py")    # current gold example (Masterclass format)
SCENES_DIR = os.path.join(ROOT, "scenes")
PROMPTS_DIR = os.path.join(ROOT, "prompts")
OUT_DIR = os.path.join(ROOT, "outputs")
MEDIA = os.path.join(ROOT, "build", "media")


# ---------------- state ----------------
def load_questions():
    with open(QUESTIONS, encoding="utf-8") as f:
        return json.load(f)


def save_questions(qs):
    with open(QUESTIONS, "w", encoding="utf-8") as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)
        f.write("\n")


def find_q(qs, qid):
    for q in qs:
        if q["id"] == qid:
            return q
    return None


# Cross-process lock so parallel `build`s never clobber each other's status in questions.json.
_QLOCK = os.path.join(ROOT, ".questions.lock")


@contextlib.contextmanager
def questions_lock():
    with open(_QLOCK, "w") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def update_question(qid, **fields):
    """Re-read questions.json fresh, patch ONLY this id, write back — all under an
    exclusive lock. Safe when several builds finish at once (avoids stale-snapshot clobber)."""
    with questions_lock():
        qs = load_questions()
        q = find_q(qs, qid)
        if q is None:
            return
        q.update(fields)
        save_questions(qs)


def class_name_for(qid):
    """Deterministic, valid-identifier class name the agent must use and we render."""
    return "Scene_" + re.sub(r"\W", "_", qid)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def to_clipboard(text):
    try:
        p = subprocess.run(["pbcopy"], input=text, text=True)
        return p.returncode == 0
    except FileNotFoundError:
        return False


# ---------------- the prompt (what you paste into chat) ----------------
def build_prompt(q, cls, prior_code=None, error=None):
    brand = read(BRAND)
    exemplar = read(EXEMPLAR)
    task = f"""# TASK
Write the complete Manim scene for this question, saved as scenes/{q['id']}.py.

- id: {q['id']}
- chapter: {q.get('chapter', '')}
- question: {q['question']}
- options: {q.get('options', '(none)')}
- KNOWN CORRECT ANSWER (anchor the whole explanation to this, never contradict it): {q['answer']}

Requirements:
- The class MUST be named EXACTLY: {cls}
- Top-left chapter tag: // {q.get('chapter', 'JEE').upper()}
- Follow every rule in the BRAND + CODING SYSTEM above. Teaching-style narration,
  af_nova Kokoro voice, brand colours, MathTex basictex-safe.
- Return ONLY the file content in ONE ```python block.
"""
    if error:
        task += f"""
# THE PREVIOUS VERSION FAILED THE RENDER GATE
Error:

{error}

Your previous code:
```python
{prior_code}
```
Fix it and return the FULL corrected file in one ```python block. Keep the class name {cls}.
"""
    return brand + "\n" + exemplar + "\n" + task


# ---------------- deterministic gates + render ----------------
def render_env():
    """Self-contained env: project root on PYTHONPATH; venv bin + Homebrew + LaTeX on PATH.
    Lets `.venv/bin/python orchestrator.py build ...` run from any cwd with no `source`/`export`."""
    env = dict(os.environ)
    env["PYTHONPATH"] = ROOT + os.pathsep + env.get("PYTHONPATH", "")
    extra = [os.path.dirname(sys.executable),   # the venv's bin (manim lives here)
             "/opt/homebrew/bin",               # ffmpeg, ffprobe, rclone
             "/Library/TeX/texbin"]             # latex for MathTex
    path = env.get("PATH", "")
    for d in extra:
        if os.path.isdir(d) and d not in path:
            path = d + os.pathsep + path
    env["PATH"] = path
    return env


def py_compile_check(path):
    proc = subprocess.run([sys.executable, "-m", "py_compile", path],
                          capture_output=True, text=True)
    return (proc.returncode == 0, (proc.stderr or proc.stdout).strip())


def layout_check(path, cls):
    """Deterministic overlap / off-frame gate. Returns (ok, report)."""
    proc = subprocess.run([sys.executable, "layout_check.py", path, cls],
                          cwd=ROOT, env=render_env(), capture_output=True, text=True)
    if proc.returncode == 0:
        return True, ""
    # keep only the violation lines for the repair prompt
    lines = [ln.strip() for ln in proc.stdout.splitlines()
             if "OVERLAP" in ln or "OFF-FRAME" in ln or "violation" in ln]
    return False, "\n".join(lines) or proc.stdout[-1500:]


def burn_captions(video, srt):
    """Burn the auto-generated narration SRT into the scene video, in the bottom caption band
    (white with a black outline, centred). Returns the captioned path, or the original on failure.
    Captions go on the SCENE only, before intro/outro are wrapped around it (guideline: never over
    the sting or outro)."""
    if not (srt and os.path.exists(srt)):
        return video
    out = os.path.splitext(video)[0] + "_cc.mp4"
    # libass scales Fontsize/margins by the ASS script height (SRT default PlayResY=288),
    # NOT the output resolution — so these values are resolution-independent (Fontsize 12 renders
    # ~90px at 2160p). Do NOT use output-pixel numbers here.
    # Caption look: SMALL, brand off-white text, in the SAME font the scene body renders in
    # (Manrope/Space Grotesk fall back to Noto Sans on this box), NO background band — just text
    # at the very bottom with a hairline outline for legibility.
    style = ("Fontname=Noto Sans,Fontsize=12,"
             "PrimaryColour=&H00E8EFF1&,"          # brand WHITE #F1EFE8 (ASS is BGR)
             "OutlineColour=&H00141414&,"          # near-obsidian hairline (not a box)
             "BorderStyle=1,Outline=1,Shadow=0,"
             "Alignment=2,MarginV=14,MarginL=150,MarginR=150")   # MarginV small -> hug the very bottom
    # escape the srt path for the ffmpeg filter
    srt_esc = srt.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
    cmd = ["ffmpeg", "-y", "-i", video,
           "-vf", f"subtitles='{srt_esc}':force_style='{style}'",
           "-c:a", "copy", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", out]
    r = subprocess.run(cmd, cwd=ROOT, env=render_env(), capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(out):
        return out
    print(f"  (caption burn failed: {(r.stderr or '')[-300:]})")
    return video


def render(path, cls, quality, media=MEDIA):
    """Render <cls> from <path>. Returns (ok, mp4_path_or_error_tail).
    `media` can be a per-build dir so parallel renders never share the LaTeX cache."""
    proc = subprocess.run(
        ["manim", quality, "--media_dir", media, path, cls],
        cwd=ROOT, env=render_env(), capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return False, (proc.stdout + "\n" + proc.stderr)[-2500:]
    stem = os.path.splitext(os.path.basename(path))[0]
    hits = glob.glob(os.path.join(media, "videos", stem, "*", cls + ".mp4"))
    if not hits:
        hits = glob.glob(os.path.join(media, "videos", "**", cls + ".mp4"), recursive=True)
    if not hits:
        return False, "render succeeded but mp4 not found"
    return True, sorted(hits, key=os.path.getmtime)[-1]


def wrap_intro_outro(video, qid):
    """Prepend assets/intro.mp4 and append assets/outro.mp4 (both silent 4K/30) to the video.
    Returns the wrapped path, or None if the bumpers are missing / it fails."""
    intro = os.path.join(ROOT, "assets", "intro.mp4")
    outro = os.path.join(ROOT, "assets", "outro.mp4")
    if not (os.path.exists(intro) and os.path.exists(outro)):
        return None

    def dur(p):
        o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1", p],
                           capture_output=True, text=True)
        return float(o.stdout.strip())

    idur, odur = dur(intro), dur(outro)
    out = os.path.join(OUT_DIR, f"{qid}_wrapped.mp4")
    vf = "scale=3840:2160,setsar=1,fps=30,format=yuv420p"
    fc = (f"[0:v]{vf}[v0];[1:v]{vf}[v1];[2:v]{vf}[v2];"
          f"[3:a]aresample=48000,aformat=channel_layouts=stereo[a0];"
          f"[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];"
          f"[4:a]aresample=48000,aformat=channel_layouts=stereo[a2];"
          f"[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]")
    cmd = ["ffmpeg", "-y", "-i", intro, "-i", video, "-i", outro,
           "-f", "lavfi", "-t", str(idur), "-i", "anullsrc=r=48000:cl=stereo",
           "-f", "lavfi", "-t", str(odur), "-i", "anullsrc=r=48000:cl=stereo",
           "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", out]
    r = subprocess.run(cmd, cwd=ROOT, env=render_env(), capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(out):
        return out
    print(f"  (intro/outro wrap failed: {(r.stderr or '')[-300:]})")
    return None


def upload_to_drive(local_path, remote_dir):
    fname = os.path.basename(local_path)
    remote_file = remote_dir.rstrip("/") + "/" + fname
    try:
        subprocess.run(["rclone", "copy", local_path, remote_dir],
                       check=True, capture_output=True, text=True)
        out = subprocess.run(["rclone", "link", remote_file],
                             check=True, capture_output=True, text=True)
        return out.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"    (drive upload skipped: {getattr(e, 'stderr', e)})")
        return None


# ---------------- phase-2 agent hooks (stubbed until an API key exists) ----------------
def script_judge(code, q):   return True, []   # TODO rubric gate
def visual_qc(mp4, q):       return True, []   # TODO geometry + multimodal keyframes
def caption_writer(q, code): return None       # TODO YouTube metadata


# ---------------- commands ----------------
def emit_prompt(q, error=None, prior_code=None, tag=""):
    cls = class_name_for(q["id"])
    prompt = build_prompt(q, cls, prior_code=prior_code, error=error)
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    name = f"{q['id']}{'_repair' if tag == 'repair' else ''}.txt"
    path = os.path.join(PROMPTS_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(prompt)
    copied = to_clipboard(prompt)
    print(f"  prompt -> {os.path.relpath(path, ROOT)}"
          + ("  (copied to clipboard ✅)" if copied else "  (pbcopy unavailable)"))
    print(f"  NEXT: paste it into the Claude chat, save the ```python reply to "
          f"scenes/{q['id']}.py, then:  python orchestrator.py build {q['id']}")


def cmd_prompt(args):
    qs = load_questions()
    if args.id:
        q = find_q(qs, args.id)
        if not q:
            sys.exit(f"no question with id {args.id}")
    else:
        pend = [x for x in qs if x.get("status", "pending") == "pending"]
        if not pend:
            print("No pending questions. (use --id to force one)")
            return
        q = pend[0]
    print(f"=== {q['id']} ({q.get('chapter','')}) ===")
    emit_prompt(q)
    q["status"] = "prompted"
    save_questions(qs)


def cmd_build(args):
    qs = load_questions()
    q = find_q(qs, args.id)
    if not q:
        sys.exit(f"no question with id {args.id}")
    cls = class_name_for(q["id"])
    scene_path = os.path.join(SCENES_DIR, f"{q['id']}.py")
    if not os.path.exists(scene_path):
        sys.exit(f"{scene_path} not found — run `prompt`, paste into chat, save the reply there first.")

    print(f"=== build {q['id']} ({cls}) ===")
    ok, msg = py_compile_check(scene_path)
    if not ok:
        print("  py_compile FAILED:")
        print("   ", msg.splitlines()[-1] if msg else "")
        emit_prompt(q, error=msg, prior_code=read(scene_path), tag="repair")
        update_question(q["id"], status="review"); return

    if getattr(args, "skip_gate", False):
        print("  layout gate SKIPPED (--skip-gate; scene pre-verified)")
    else:
        print("  layout gate (overlap / off-frame) ...", flush=True)
        ok, report = layout_check(scene_path, cls)
        if not ok:
            print("  LAYOUT FAILED:")
            for ln in report.splitlines():
                print("   ", ln)
            emit_prompt(q, error="Layout gate failed — FIX THESE overlaps/clipping:\n" + report,
                        prior_code=read(scene_path), tag="repair")
            update_question(q["id"], status="review"); return

    media_dir = getattr(args, "media", "") or MEDIA
    print(f"  rendering {args.quality} (media={os.path.relpath(media_dir, ROOT)}) ...", flush=True)
    ok, msg = render(scene_path, cls, args.quality, media=media_dir)
    if not ok:
        print("  render FAILED — writing repair prompt")
        emit_prompt(q, error=msg, prior_code=read(scene_path), tag="repair")
        update_question(q["id"], status="review"); return

    os.makedirs(OUT_DIR, exist_ok=True)
    solo = os.path.join(OUT_DIR, f"{q['id']}.mp4")
    shutil.copy(msg, solo)
    print(f"  OK -> {os.path.relpath(solo, ROOT)}")

    # 0) burn narration subtitles into the scene (before wrapping, so they cover the scene
    #    only, never the sting/outro). The SRT sits next to the rendered mp4.
    if getattr(args, "captions", False):
        srt = os.path.splitext(msg)[0] + ".srt"
        print("  burning captions ...", flush=True)
        capped = burn_captions(solo, srt)
        if capped != solo:
            shutil.copy(capped, solo)   # keep the wrap step pointed at outputs/<id>.mp4
            print(f"  + captions -> {os.path.relpath(solo, ROOT)}")

    # 1) wrap intro + outro (silent bumpers) around the voice-only solution
    print("  wrapping intro + outro ...", flush=True)
    base = wrap_intro_outro(solo, q["id"]) or solo
    if base != solo:
        print(f"  + intro/outro -> {os.path.relpath(base, ROOT)}")

    # 2) background music across the WHOLE video, ducked under the voice — so it plays
    #    a touch louder over the silent intro/outro and dips under the teaching narration.
    final = base
    if args.music:
        print("  adding background music (whole video, ducked) ...", flush=True)
        r = subprocess.run(
            [sys.executable, os.path.join(ROOT, "add_bgm.py"), base,
             "--volume", str(args.music_vol), "--fadein", "1.5", "--fadeout", "3",
             "--duck", "--suffix", "_final"],
            cwd=ROOT, env=render_env(), capture_output=True, text=True)
        mout = os.path.splitext(base)[0] + "_final.mp4"
        if r.returncode == 0 and os.path.exists(mout):
            final = mout
            print(f"  + music -> {os.path.relpath(final, ROOT)}")
        else:
            print(f"  (music step failed — shipping no-music version)\n{(r.stderr or '')[-300:]}")

    url = upload_to_drive(final, args.drive) if args.drive else None
    fields = {"status": "done"}
    if url:
        print(f"  Drive: {url}")
        fields["video_url"] = url
    update_question(q["id"], **fields)
    print(f"  {q['id']} DONE ✅")


def cmd_status(args):
    qs = load_questions()
    icon = {"done": "✅", "pending": "· ", "prompted": "✍️", "review": "⚠️"}
    print(f"{'id':6} {'status':10} {'chapter':16} question")
    for q in qs:
        s = q.get("status", "pending")
        print(f"{q['id']:6} {icon.get(s,'? ')} {s:8} {q.get('chapter','')[:15]:16} "
              f"{q['question'][:60]}")


def main():
    ap = argparse.ArgumentParser(description="Assisted Manim video pipeline (free).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("next", help="build the prompt for the next pending question")
    p.add_argument("--id", default="", help="force a specific question id")
    p.set_defaults(func=cmd_prompt)

    p = sub.add_parser("prompt", help="alias of next; --id targets a specific question")
    p.add_argument("--id", default="")
    p.set_defaults(func=cmd_prompt)

    p = sub.add_parser("build", help="gate + render + music + upload a saved scene")
    p.add_argument("id", help="question id whose scenes/<id>.py to build")
    p.add_argument("--quality", default="-ql", help="-ql fast, -qm medium, -qk 4K final")
    p.add_argument("--drive", default="", metavar="REMOTE:FOLDER",
                   help="rclone remote for finals, e.g. gdrive:JEE-Videos/Kinematics")
    p.add_argument("--music", action="store_true", help="mix in assets/bgm.mp3 (ducked)")
    p.add_argument("--music-vol", type=float, default=0.08, dest="music_vol")
    p.add_argument("--skip-gate", action="store_true", dest="skip_gate",
                   help="skip the layout gate (use only for pre-verified scenes / parallel batches)")
    p.add_argument("--media", default="", help="per-build media dir (isolates the LaTeX cache in parallel runs)")
    p.add_argument("--captions", action="store_true", help="burn the narration SRT into the scene (Masterclass)")
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("status", help="show all questions + states")
    p.set_defaults(func=cmd_status)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
