"""
ChatterboxService — a manim-voiceover SpeechService that clones YOUR voice.

Zero-shot voice cloning via Chatterbox: it reads a short reference clip of your
voice (config.CLONE_REFERENCE, 10-30s) and speaks any text in that voice. No
training, no dataset.

Mirrors kokoro_service.py exactly: runs the heavy torch/Chatterbox stack in an
isolated venv (.venv-chatterbox) via subprocess so it never touches the manim
venv. Same sha256 filename caching and `generate -> wav -> ffmpeg -> mp3` flow.

Setup on the render machine (one time):
    python3 -m venv .venv-chatterbox
    .venv-chatterbox/bin/pip install chatterbox-tts torchaudio
    # place your reference clip at assets/my_voice.wav

Then flip the pipeline to your voice via config.py (VOICE_ENGINE = "clone")
or per render:  VOICE_ENGINE=clone python batch_render.py ...
"""
import os
import hashlib
import subprocess
from pathlib import Path

from manim_voiceover.services.base import SpeechService

ROOT = Path(__file__).resolve().parent
CHATTERBOX_PY = ROOT / ".venv-chatterbox" / "bin" / "python"
CHATTERBOX_SCRIPT = ROOT / "chatterbox_tts.py"


class ChatterboxService(SpeechService):
    def __init__(self, reference="assets/my_voice.wav", **kwargs):
        # Resolve the reference clip relative to the project root.
        ref = Path(reference)
        self.reference = str(ref if ref.is_absolute() else ROOT / ref)
        super().__init__(**kwargs)

    def generate_from_text(self, text, cache_dir=None, path=None):
        if cache_dir is None:
            cache_dir = self.cache_dir

        # Cache key includes the reference clip's identity so re-recording your
        # voice invalidates old audio automatically.
        ref_tag = hashlib.sha256(self.reference.encode()).hexdigest()[:8]
        if path is None:
            key = f"chatterbox-{ref_tag}-{text}".encode()
            audio_path = "chatterbox-" + hashlib.sha256(key).hexdigest()[:20] + ".mp3"
        else:
            audio_path = path

        full = Path(cache_dir) / audio_path
        if not full.exists():
            if not CHATTERBOX_PY.exists():
                raise RuntimeError(
                    f"Cloning venv not found at {CHATTERBOX_PY}. Create it with:\n"
                    f"  python3 -m venv .venv-chatterbox && "
                    f".venv-chatterbox/bin/pip install chatterbox-tts torchaudio"
                )
            if not Path(self.reference).exists():
                raise RuntimeError(
                    f"Reference voice clip not found at {self.reference}. "
                    f"Place a 10-30s WAV of the target voice there (see config.CLONE_REFERENCE)."
                )

            wav = str(full) + ".wav"
            try:
                subprocess.run(
                    [str(CHATTERBOX_PY), str(CHATTERBOX_SCRIPT),
                     "--reference", self.reference, "--out", wav],
                    input=text, text=True, check=True, capture_output=True,
                )
            except subprocess.CalledProcessError as e:
                raise RuntimeError(
                    f"Chatterbox TTS failed:\n{(e.stderr or e.stdout or '').strip()}"
                ) from e
            subprocess.run(["ffmpeg", "-y", "-i", wav, str(full)],
                           check=True, capture_output=True)
            os.remove(wav)

        return {"input_text": text, "original_audio": audio_path}
