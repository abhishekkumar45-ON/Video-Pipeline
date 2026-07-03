import argparse
import os
import re
import sys
import glob
import shutil
import subprocess
import time

ROOT = os.path.dirname(os.path.abspath(__file__))


def find_scene_classes(path):
    """Return every class in the file whose base looks like a Manim Scene."""
    text = open(path, encoding="utf-8").read()
    return re.findall(r"class\s+(\w+)\s*\([^)]*Scene[^)]*\)", text)


def upload_to_drive(local_path, remote_dir):
    """Upload a file to Google Drive via rclone and return a shareable link (or None)."""
    fname = os.path.basename(local_path)
    remote_file = remote_dir.rstrip("/") + "/" + fname
    try:
        subprocess.run(["rclone", "copy", local_path, remote_dir],
                       check=True, capture_output=True, text=True)
        out = subprocess.run(["rclone", "link", remote_file],
                             check=True, capture_output=True, text=True)
        return out.stdout.strip()
    except FileNotFoundError:
        print("        (rclone not installed — skipping upload)")
        return None
    except subprocess.CalledProcessError as e:
        print(f"        (Drive upload failed: {(e.stderr or '').strip()[:200]})")
        return None


def main():
    ap = argparse.ArgumentParser(description="Batch-render Manim scene files.")
    ap.add_argument("--scenes", default="scenes", help="folder with your .py scene files")
    ap.add_argument("--out", default="outputs", help="where finished mp4s go")
    ap.add_argument("--quality", default="-qh", help="-ql fast/low, -qm medium, -qh final")
    ap.add_argument("--force", action="store_true", help="re-render even if output exists")
    ap.add_argument("--drive", default="", metavar="REMOTE:FOLDER",
                    help="upload each finished mp4 to this rclone remote, "
                         "e.g. gdrive:manim-videos")
    args = ap.parse_args()

    scenes_dir = os.path.join(ROOT, args.scenes)
    out_dir = os.path.join(ROOT, args.out)
    media = os.path.join(ROOT, "build", "media")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(media, exist_ok=True)

    files = sorted(glob.glob(os.path.join(scenes_dir, "*.py")))
    if not files:
        sys.exit(f"No .py files found in {scenes_dir}/ — put your scene files there.")

    # let scene files import helpers (e.g. mac_say_service) from the project root
    env = dict(os.environ)
    env["PYTHONPATH"] = ROOT + os.pathsep + env.get("PYTHONPATH", "")

    logf = open(os.path.join(out_dir, "render_log.txt"), "a")
    ok, fail, links = [], [], []
    total = len(files)
    print(f"Found {total} scene file(s) in {args.scenes}/\n")

    for i, path in enumerate(files, 1):
        stem = os.path.splitext(os.path.basename(path))[0]
        classes = find_scene_classes(path)
        if not classes:
            print(f"[{i}/{total}] {stem}: no Scene class found — skipping")
            fail.append(stem + " (no Scene class)")
            continue

        for cls in classes:
            name = stem if len(classes) == 1 else f"{stem}__{cls}"
            final = os.path.join(out_dir, name + ".mp4")

            if os.path.exists(final) and not args.force:
                print(f"[{i}/{total}] {name}: already rendered — skip")
                ok.append(name)
                continue

            print(f"[{i}/{total}] {name}: rendering...", flush=True)
            t0 = time.time()
            try:
                subprocess.run(
                    ["manim", args.quality, "--media_dir", media, path, cls],
                    cwd=ROOT, env=env, check=True,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                )
            except subprocess.CalledProcessError as e:
                dt = time.time() - t0
                print(f"        FAILED ({dt:.1f}s) — logged")
                logf.write(f"\n==== {name} FAILED ====\n{(e.output or '')[-3000:]}\n")
                logf.flush()
                fail.append(name)
                continue

            hits = glob.glob(os.path.join(media, "videos", stem, "*", cls + ".mp4"))
            if not hits:
                hits = glob.glob(os.path.join(media, "videos", "**", cls + ".mp4"),
                                 recursive=True)
            if not hits:
                print("        rendered but mp4 not found")
                fail.append(name + " (mp4 missing)")
                continue

            shutil.copy(sorted(hits, key=os.path.getmtime)[-1], final)
            dt = time.time() - t0
            print(f"        OK ({dt:.1f}s) -> {os.path.relpath(final, ROOT)}")
            ok.append(name)

            if args.drive:
                link = upload_to_drive(final, args.drive)
                if link:
                    print(f"        Drive: {link}")
                    links.append(f"{name}\t{link}")

    print(f"\n=== DONE: {len(ok)} ok, {len(fail)} failed ===")
    if fail:
        print("Failed:", ", ".join(fail))
        print(f"Errors written to {os.path.join(args.out, 'render_log.txt')}")
    if links:
        with open(os.path.join(out_dir, "drive_links.txt"), "w") as f:
            f.write("\n".join(links) + "\n")
        print(f"Drive links saved to {os.path.join(args.out, 'drive_links.txt')}")


if __name__ == "__main__":
    main()