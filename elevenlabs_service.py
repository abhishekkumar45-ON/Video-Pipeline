"""
ElevenLabsService — a manim-voiceover SpeechService using ElevenLabs TTS.
Top-tier naturalness. Default voice 'Anika' (Indian-accent English) via the
multilingual model. CLOUD service — must be online when rendering.

Auth: set ELEVENLABS_API_KEY in your environment (never paste it in chat).
The voice must exist in your ElevenLabs account ("My Voices") — add 'Anika'
from the Voice Library first, or pass an explicit voice_id.

Same sha256 filename caching as the other services, so each unique narration line
is only synthesized (and billed) once.
"""
import hashlib
import os
from pathlib import Path

from elevenlabs.client import ElevenLabs

from manim_voiceover.services.base import SpeechService


class ElevenLabsService(SpeechService):
    def __init__(self, voice_name="Anika", voice_id=None,
                 model="eleven_multilingual_v2", output_format="mp3_44100_128",
                 api_key=None, **kwargs):
        key = (api_key or os.environ.get("ELEVENLABS_API_KEY")
               or os.environ.get("ELEVEN_API_KEY") or self._key_from_file())
        if not key:
            raise RuntimeError(
                "No ElevenLabs API key. Put it in ~/.elevenlabs_key or set ELEVENLABS_API_KEY.")
        self.client = ElevenLabs(api_key=key)
        self.model = model
        self.output_format = output_format
        self.voice_name = voice_name
        self.voice_id = voice_id or self._resolve_voice_id(voice_name)
        super().__init__(**kwargs)

    @staticmethod
    def _key_from_file():
        f = Path.home() / ".elevenlabs_key"
        if f.exists():
            return f.read_text().strip()
        return None

    def _resolve_voice_id(self, name):
        """Find the voice_id for a voice named `name` in the account."""
        resp = self.client.voices.get_all()
        voices = getattr(resp, "voices", resp)
        q = name.lower().strip()
        # match exact, or the label before " - ", or substring (e.g. "Anika - Sweet and Lively")
        for v in voices:
            vn = getattr(v, "name", "").lower()
            if vn == q or vn.split(" - ")[0].strip() == q or q in vn:
                return v.voice_id
        available = ", ".join(getattr(v, "name", "?") for v in voices)
        raise RuntimeError(
            f"Voice {name!r} not in your ElevenLabs account. "
            f"Add it from the Voice Library first. Available: {available}")

    def generate_from_text(self, text, cache_dir=None, path=None):
        if cache_dir is None:
            cache_dir = self.cache_dir
        if path is None:
            key = f"11l-{self.voice_id}-{self.model}-{text}".encode()
            audio_path = "11l-" + hashlib.sha256(key).hexdigest()[:20] + ".mp3"
        else:
            audio_path = path

        full = Path(cache_dir) / audio_path
        if not full.exists():
            tmp = full.with_suffix(".part")
            try:
                stream = self.client.text_to_speech.convert(
                    voice_id=self.voice_id, text=text,
                    model_id=self.model, output_format=self.output_format,
                )
                with open(tmp, "wb") as f:
                    for chunk in stream:
                        f.write(chunk)
                tmp.rename(full)   # atomic: only a complete file lands in the cache
            finally:
                if tmp.exists():
                    tmp.unlink()

        return {"input_text": text, "original_audio": audio_path}
