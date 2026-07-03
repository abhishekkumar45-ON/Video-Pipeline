"""
Kokoro TTS CLI — runs inside .venv-kokoro (Python 3.12 + torch + kokoro).
Reads the narration text from STDIN, writes a 24 kHz wav to --out.

Called by kokoro_service.py (which lives in the manim venv) via subprocess,
so the heavy torch/kokoro stack stays isolated from manim.

Standalone test:
  echo "Hello from Kokoro" | .venv-kokoro/bin/python kokoro_tts.py --out /tmp/t.wav
"""
import argparse
import sys

import numpy as np
import soundfile as sf
from kokoro import KPipeline

SAMPLE_RATE = 24000  # Kokoro's native output rate


def main():
    ap = argparse.ArgumentParser(description="Kokoro TTS -> wav")
    ap.add_argument("--voice", default="af_heart", help="e.g. af_heart, am_michael, bf_emma")
    ap.add_argument("--lang", default="a", help="a=American, b=British English")
    ap.add_argument("--speed", type=float, default=1.0, help="1.0 normal; <1 slower")
    ap.add_argument("--out", required=True, help="output .wav path")
    args = ap.parse_args()

    text = sys.stdin.read().strip()
    if not text:
        sys.exit("kokoro_tts: no text on stdin")

    pipeline = KPipeline(lang_code=args.lang)

    chunks = []
    for _, _, audio in pipeline(text, voice=args.voice, speed=args.speed):
        # audio may be a torch tensor or numpy array depending on version
        arr = audio.detach().cpu().numpy() if hasattr(audio, "detach") else np.asarray(audio)
        chunks.append(arr)

    if not chunks:
        sys.exit("kokoro_tts: pipeline produced no audio")

    audio = np.concatenate(chunks) if len(chunks) > 1 else chunks[0]
    sf.write(args.out, audio, SAMPLE_RATE)


if __name__ == "__main__":
    main()
