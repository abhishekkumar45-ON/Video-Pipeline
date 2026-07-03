#!/usr/bin/env bash
# One-shot Ubuntu setup for the Manim render farm.
# Installs system deps + a manim venv + the Kokoro voice venv.
# Re-runnable. Run from the repo root:  bash setup_ubuntu.sh
set -euo pipefail

echo "==> [1/4] System dependencies (apt) ..."
sudo apt-get update
sudo apt-get install -y \
  python3-venv python3-pip git ffmpeg pkg-config build-essential \
  libcairo2-dev libpango1.0-dev \
  texlive texlive-latex-extra texlive-fonts-extra dvisvgm \
  fonts-jetbrains-mono espeak-ng

echo "==> [2/4] Manim venv (.venv) ..."
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install manim manim-voiceover
deactivate

echo "==> [3/4] Kokoro voice venv (.venv-kokoro) — heavy (torch), one time ..."
if [ ! -d .venv-kokoro ]; then
  python3 -m venv .venv-kokoro
fi
.venv-kokoro/bin/pip install --upgrade pip
.venv-kokoro/bin/pip install kokoro soundfile

echo "==> [4/4] Done."
cat <<'EOF'

Setup complete. To render in 4K (each in its own terminal, in parallel):

  source .venv/bin/activate
  manim -qk --media_dir build/media scenes/q5.py Scene_q5
  manim -qk --media_dir build/media scenes/q6.py Scene_q6
  manim -qk --media_dir build/media scenes/q7.py Scene_q7

First render downloads the ~330 MB Kokoro model once, then it's offline.
For the Indian-accent Google voice instead, see RENDER_UBUNTU.md (Voice options).
EOF
