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
pip install manim manim-voiceover pillow openpyxl
deactivate

echo "==> [3/4] Kokoro voice venv (.venv-kokoro) — heavy (torch), one time ..."
if [ ! -d .venv-kokoro ]; then
  python3 -m venv .venv-kokoro
fi
.venv-kokoro/bin/pip install --upgrade pip
.venv-kokoro/bin/pip install kokoro soundfile

echo "==> [4/4] Done."
cat <<'EOF'

Setup complete.  Build a finished 4K video (render -> intro/outro -> music -> Drive) with:

  ./.venv/bin/python orchestrator.py build q10 --quality=-qk --music --drive=gdrive:JEE-Videos/Thermodynamics

(swap q10 for any id in questions.json whose scenes/<id>.py exists).
First render downloads the ~330 MB Kokoro voice model once, then it's offline.
Full guide: README.md.  Google Drive upload needs `rclone config` (remote named 'gdrive').
EOF
