import os
import sys
import json
import glob
import subprocess

from scriptwriter import write_scene
from tts import tts
from config import QUALITY

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")


def run(cmd, **kw):
    print("+ " + " ".join(cmd))
    return subprocess.run(cmd, check=True, **kw)


def ffprobe_dur(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def main():
    qid = sys.argv[1] if len(sys.argv) > 1 else None
    questions = json.load(open(os.path.join(HERE, "questions.json")))
    q = next((x for x in questions if x["id"] == qid), questions[0])
    print(f"\n=== Building video for: {q['id']} — {q.get('chapter','')} ===\n")
    os.makedirs(BUILD, exist_ok=True)

    print("[1/5] Scriptwriter agent...")
    scene = write_scene(q)
    beats = scene["beats"]
    print(f"      {len(beats)} beats written")

    print("[2/5] Voice (per beat)...")
    audios = []
    for i, b in enumerate(beats):
        mp3 = os.path.join(BUILD, f"audio_{i}.mp3")
        tts(b["narration"], mp3)
        b["duration"] = ffprobe_dur(mp3)
        audios.append(mp3)
        print(f"      beat {i}: {b['duration']:.1f}s")
    json.dump(beats, open(os.path.join(BUILD, "beats.json"), "w"))

    print("[3/5] Render (Manim)...")
    media = os.path.join(BUILD, "media")
    run(["manim", QUALITY, "--media_dir", media,
         os.path.join(HERE, "scene.py"), "VideoScene"], cwd=HERE)
    vids = sorted(
        glob.glob(os.path.join(media, "videos", "**", "*.mp4"), recursive=True),
        key=os.path.getmtime,
    )
    if not vids:
        sys.exit("ERROR: no video produced by Manim")
    video = vids[-1]

    print("[4/5] Stitch narration...")
    listf = os.path.join(BUILD, "list.txt")
    with open(listf, "w") as f:
        for a in audios:
            f.write(f"file '{a}'\n")
    narration = os.path.join(BUILD, "narration.mp3")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf,
         "-c:a", "libmp3lame", narration], capture_output=True)

    print("[5/5] Mux video + audio...")
    final = os.path.join(BUILD, f"final_{q['id']}.mp4")
    run(["ffmpeg", "-y", "-i", video, "-i", narration,
         "-c:v", "copy", "-c:a", "aac", "-shortest", final], capture_output=True)

    print(f"\n✅ DONE  ->  {final}\n")


if __name__ == "__main__":
    main()
