"""
add_bgm.py — mix low, fading background music under a rendered video's narration.

The music is set quiet (default 10% volume), faded in at the start and out at the end,
and mixed UNDER the narration (voice stays at full level). Optional --duck makes the
music dip further whenever the narrator speaks (sidechain compression).

Usage:
  python add_bgm.py outputs/q8_4k.mp4                 # -> outputs/q8_4k_music.mp4
  python add_bgm.py --all                             # every outputs/*.mp4 (skips *_music)
  python add_bgm.py outputs/q8_4k.mp4 --volume 0.08 --duck
  python add_bgm.py outputs/q8_4k.mp4 --inplace       # overwrite the original

Music file: assets/bgm.mp3 (override with --music).
"""
import argparse
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MUSIC = os.path.join(ROOT, "assets", "bgm.mp3")


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def mix(video, music, vol, fin, fout, duck, out):
    dur = duration(video)
    fade_out_start = max(0.0, dur - fout)
    bg = (f"[1:a]volume={vol},"
          f"afade=t=in:st=0:d={fin},"
          f"afade=t=out:st={fade_out_start:.2f}:d={fout},"
          f"aresample=44100,aformat=channel_layouts=stereo[bg]")
    voice = "[0:a]aresample=44100,aformat=channel_layouts=stereo[voice]"
    # master tail: resync + gentle limiter (no loudnorm — it would pump the music-only
    # intro/outro). The sidechain duck itself makes the music louder where there's no voice
    # (intro/outro) and quieter under narration (teaching) — exactly what's wanted.
    tail = "aresample=async=1:first_pts=0,alimiter=limit=0.95"
    if duck:
        # the voice feeds TWO filters (sidechain key + final mix); a filter pad can only be
        # consumed once, so split it into [vmain] and [vkey].
        voice_split = "[0:a]aresample=44100,aformat=channel_layouts=stereo,asplit=2[vmain][vkey]"
        chain = (f"{bg};{voice_split};"
                 f"[bg][vkey]sidechaincompress=threshold=0.02:ratio=9:attack=5:release=450:makeup=1[bgd];"
                 f"[vmain][bgd]amix=inputs=2:duration=first:normalize=0,{tail}[a]")
    else:
        chain = f"{bg};{voice};[voice][bg]amix=inputs=2:duration=first:normalize=0,{tail}[a]"

    cmd = ["ffmpeg", "-y", "-i", video, "-stream_loop", "-1", "-i", music,
           "-filter_complex", chain,
           "-map", "0:v", "-map", "[a]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return False, r.stderr[-800:]
    return True, out


def main():
    ap = argparse.ArgumentParser(description="Add low, fading background music to videos.")
    ap.add_argument("videos", nargs="*", help="video files (or use --all)")
    ap.add_argument("--all", action="store_true", help="process every outputs/*.mp4")
    ap.add_argument("--music", default=DEFAULT_MUSIC)
    ap.add_argument("--volume", type=float, default=0.10, help="music level 0..1 (default 0.10)")
    ap.add_argument("--fadein", type=float, default=2.0)
    ap.add_argument("--fadeout", type=float, default=3.0)
    ap.add_argument("--duck", action="store_true", help="dip music under narration (sidechain)")
    ap.add_argument("--inplace", action="store_true", help="overwrite the original file")
    ap.add_argument("--suffix", default="_music", help="output suffix when not --inplace")
    args = ap.parse_args()

    if not os.path.exists(args.music):
        sys.exit(f"music not found: {args.music}")

    if args.all:
        vids = [v for v in sorted(glob.glob(os.path.join(ROOT, "outputs", "*.mp4")))
                if args.suffix not in os.path.basename(v)]
    else:
        vids = args.videos
    if not vids:
        sys.exit("no videos (pass files or --all)")

    ok = 0
    for v in vids:
        stem, ext = os.path.splitext(v)
        out = v if args.inplace else f"{stem}{args.suffix}{ext}"
        tmp = out + ".tmp.mp4" if args.inplace else out
        print(f"[bgm] {os.path.basename(v)} (vol={args.volume}, duck={args.duck}) ...", flush=True)
        good, msg = mix(v, args.music, args.volume, args.fadein, args.fadeout, args.duck, tmp)
        if not good:
            print("  FAILED:\n", msg)
            continue
        if args.inplace:
            os.replace(tmp, out)
        print(f"  OK -> {os.path.relpath(out, ROOT)}")
        ok += 1
    print(f"\n{ok}/{len(vids)} done")


if __name__ == "__main__":
    main()
