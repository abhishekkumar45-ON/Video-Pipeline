import os
import hashlib
import subprocess
from pathlib import Path

from manim_voiceover.services.base import SpeechService


class MacSayService(SpeechService):
    """Text-to-speech using the macOS built-in `say` command.
    Free, offline, no API key. Voices: run `say -v ?` in a terminal to list them.

    Default is 'Tara' — a natural, neural-quality Indian-English (en_IN) voice.
    Other good Indian options: 'Aman' (male, natural), 'Rishi' (male, robotic).
    """

    def __init__(self, voice="Tara", rate=None, **kwargs):
        self.voice = voice
        self.rate = rate
        super().__init__(**kwargs)

    def generate_from_text(self, text, cache_dir=None, path=None):
        if cache_dir is None:
            cache_dir = self.cache_dir
        if path is None:
            key = f"{self.voice}-{self.rate}-{text}".encode()
            audio_path = "macsay-" + hashlib.sha256(key).hexdigest()[:20] + ".mp3"
        else:
            audio_path = path

        full = Path(cache_dir) / audio_path
        if not full.exists():
            aiff = str(full) + ".aiff"
            cmd = ["say", "-o", aiff]
            if self.voice:
                cmd += ["-v", self.voice]
            if self.rate:
                cmd += ["-r", str(self.rate)]
            cmd += [text]
            subprocess.run(cmd, check=True)
            subprocess.run(["ffmpeg", "-y", "-i", aiff, str(full)],
                           check=True, capture_output=True)
            os.remove(aiff)

        return {"input_text": text, "original_audio": audio_path}
