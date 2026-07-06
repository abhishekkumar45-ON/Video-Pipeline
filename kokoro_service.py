"""
KokoroService — a manim-voiceover SpeechService using Kokoro (open-weight neural TTS).
Free, fully offline after the one-time model download. Much more natural than macOS `say`.

Runs Kokoro in an isolated venv (.venv-kokoro, Python 3.12) via subprocess so the heavy
torch stack never touches the manim venv. Mirrors mac_say_service.py:
sha256 filename caching, `say/kokoro -> wav -> ffmpeg -> mp3`.

Voices (accent is American/British — Kokoro has no native Indian voice):
  af_nova   (US female, bright/lively — teaching voice)   <- default
  af_heart  (US female, flagship, warm)   af_bella (US female, warm)
  am_michael (US male)   bf_emma (UK female)   bm_george (UK male)
Default speed is 0.9 (slightly slow, for a deliberate teaching cadence).
Full list: https://huggingface.co/hexgrad/Kokoro-82M  (VOICES.md)
"""
import os
import hashlib
import subprocess
from pathlib import Path

from manim_voiceover.services.base import SpeechService

ROOT = Path(__file__).resolve().parent
KOKORO_PY = ROOT / ".venv-kokoro" / "bin" / "python"
KOKORO_SCRIPT = ROOT / "kokoro_tts.py"


class KokoroService(SpeechService):
    def __init__(self, voice="af_bella", lang="a", speed=0.9, **kwargs):
        self.voice = voice
        self.lang = lang
        self.speed = speed
        super().__init__(**kwargs)

    def generate_from_text(self, text, cache_dir=None, path=None):
        if cache_dir is None:
            cache_dir = self.cache_dir
        if path is None:
            key = f"kokoro-{self.voice}-{self.speed}-{text}".encode()
            audio_path = "kokoro-" + hashlib.sha256(key).hexdigest()[:20] + ".mp3"
        else:
            audio_path = path

        full = Path(cache_dir) / audio_path
        if not full.exists():
            wav = str(full) + ".wav"
            try:
                subprocess.run(
                    [str(KOKORO_PY), str(KOKORO_SCRIPT),
                     "--voice", self.voice, "--lang", self.lang,
                     "--speed", str(self.speed), "--out", wav],
                    input=text, text=True, check=True, capture_output=True,
                )
            except subprocess.CalledProcessError as e:
                raise RuntimeError(
                    f"Kokoro TTS failed for voice={self.voice!r}:\n{(e.stderr or e.stdout or '').strip()}"
                ) from e
            subprocess.run(["ffmpeg", "-y", "-i", wav, str(full)],
                           check=True, capture_output=True)
            os.remove(wav)

        return {"input_text": text, "original_audio": audio_path}
