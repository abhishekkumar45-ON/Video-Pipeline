"""
Chatterbox TTS CLI — runs inside .venv-chatterbox (torch + chatterbox-tts).
Reads narration text from STDIN, clones the voice in --reference, writes a wav to --out.

Called by chatterbox_service.py (which lives in the manim venv) via subprocess,
so the heavy torch/chatterbox stack stays isolated from manim. Mirrors kokoro_tts.py.

Standalone test:
  echo "Hello, this is my cloned voice." | \
    .venv-chatterbox/bin/python chatterbox_tts.py --reference assets/my_voice.wav --out /tmp/t.wav
"""
import argparse
import sys

import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS


def pick_device():
    if torch.cuda.is_available():
        return "cuda"                      # NVIDIA GPU (render box) — fastest
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"                       # Apple Silicon
    return "cpu"                           # always works, slower


def main():
    ap = argparse.ArgumentParser(description="Chatterbox voice-clone TTS -> wav")
    ap.add_argument("--reference", required=True, help="reference voice clip (wav/mp3), 10-30s")
    ap.add_argument("--out", required=True, help="output .wav path")
    ap.add_argument("--exaggeration", type=float, default=0.5,
                    help="emotion intensity (0.3-0.7 typical; higher = more expressive)")
    ap.add_argument("--cfg", type=float, default=0.5,
                    help="cfg/pace weight (lower = slower, more deliberate)")
    args = ap.parse_args()

    text = sys.stdin.read().strip()
    if not text:
        sys.exit("chatterbox_tts: no text on stdin")

    device = pick_device()
    model = ChatterboxTTS.from_pretrained(device=device)

    wav = model.generate(
        text,
        audio_prompt_path=args.reference,
        exaggeration=args.exaggeration,
        cfg_weight=args.cfg,
    )

    ta.save(args.out, wav, model.sr)


if __name__ == "__main__":
    main()
