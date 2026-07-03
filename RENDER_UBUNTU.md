# Rendering on Ubuntu — quick start

The Mac is the "brain" (writes + overlap-checks the Manim scenes). Ubuntu is the render
farm. You only need this repo + system deps + a voice backend. Everything below is copy-paste.

---

## 0. Clone
```bash
git clone https://github.com/abhishekkumar45-ON/Video-Pipeline.git
cd Video-Pipeline
```

## 1. One-shot setup
```bash
bash setup_ubuntu.sh
```
This installs the system deps (cairo, pango, ffmpeg, LaTeX, fonts), a `.venv` with
Manim + manim-voiceover, and a `.venv-kokoro` with the Kokoro neural voice (so the
scenes render exactly like the Mac previews, no code edits). First render downloads the
~330 MB Kokoro model once, then it's offline.

## 2. Render in 4K — run each in its own terminal (parallel)
Each terminal needs the project root on PYTHONPATH so scenes can import the voice service:
```bash
source .venv/bin/activate
export PYTHONPATH="$PWD"                                   # REQUIRED (import kokoro_service)
manim -qk --media_dir build/media scenes/q5.py Scene_q5   # terminal 1
manim -qk --media_dir build/media scenes/q6.py Scene_q6   # terminal 2
manim -qk --media_dir build/media scenes/q7.py Scene_q7   # terminal 3
```
(Or skip the PYTHONPATH line and use `python batch_render.py --quality=-qk`, which sets it for you.)
`-qk` = 2160p (4K). Output lands at:
```
build/media/videos/q5/2160p60/Scene_q5.mp4
build/media/videos/q6/2160p60/Scene_q6.mp4
build/media/videos/q7/2160p60/Scene_q7.mp4
```

Batch-render everything in `scenes/` instead (resumable, skips done, logs failures):
```bash
python batch_render.py --quality=-qk
```

---

## Voice options

**Default = Kokoro (US accent, offline).** Set up by `setup_ubuntu.sh`, no edits needed —
this is what the Mac previews used.

**Upgrade = Google Chirp3-HD (Indian accent, en-IN).** Lighter than Kokoro (no torch):
```bash
source .venv/bin/activate
pip install google-cloud-texttospeech
# copy your service-account key to the box securely, then place it at:
#   ~/.gcp_tts_key.json           (NEVER commit this file)
```
Then in each `scenes/qN.py`, swap the two voice lines:
```python
# from:
from kokoro_service import KokoroService
self.set_speech_service(KokoroService())
# to:
from gcloud_tts_service import GCloudTTSService
self.set_speech_service(GCloudTTSService())   # en-IN-Chirp3-HD-Autonoe
```

---

## Guarantee: no overlap
Before rendering (or after editing a scene), lint it — fails if any text overlaps or
leaves the frame:
```bash
source .venv/bin/activate
python layout_check.py scenes/q5.py Scene_q5     # prints CLEAN or the violations
```
The Mac already ran this on q5/q6/q7 (all CLEAN), so you can render straight away.

## Troubleshooting
- `latex` not found / MathTex fails: re-run the LaTeX line in `setup_ubuntu.sh`
  (`sudo apt install texlive texlive-latex-extra texlive-fonts-extra dvisvgm`).
- 4K is CPU-heavy: 3 parallel is a good balance; add more only if the box has spare cores.
- Font "JetBrains Mono not found": harmless (falls back); `sudo apt install fonts-jetbrains-mono` for the exact brand font.
