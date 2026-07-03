"""
GCloudTTSService — a manim-voiceover SpeechService using Google Cloud Text-to-Speech.
Default voice: en-IN-Chirp3-HD-Autonoe — a natural, Indian-accent English HD voice.
This is currently the best natural+Indian+free-tier option (1M chars/month free).

CLOUD service — must be online when rendering. Auth via a service-account JSON key:
  - set GOOGLE_APPLICATION_CREDENTIALS to the key path, OR
  - drop the key at ~/.gcp_tts_key.json (this file is read automatically).
Never paste the key contents into chat.

Other en-IN Chirp3-HD voices: Callirrhoe, Despina, Erinome, Gacrux, Kore (female);
Charon, Enceladus, Fenrir, Iapetus (male). Just change `voice`.
Same sha256 caching as the other services -> each unique line synthesized/billed once.
"""
import hashlib
import os
from pathlib import Path

from google.cloud import texttospeech

from manim_voiceover.services.base import SpeechService

_DEFAULT_KEY = Path.home() / ".gcp_tts_key.json"


class GCloudTTSService(SpeechService):
    def __init__(self, voice="en-IN-Chirp3-HD-Autonoe", language_code="en-IN", **kwargs):
        self.voice = voice
        self.language_code = language_code
        if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            self.client = texttospeech.TextToSpeechClient()
        elif _DEFAULT_KEY.exists():
            self.client = texttospeech.TextToSpeechClient.from_service_account_file(str(_DEFAULT_KEY))
        else:
            raise RuntimeError(
                "No Google credentials. Set GOOGLE_APPLICATION_CREDENTIALS or place the "
                "service-account JSON at ~/.gcp_tts_key.json")
        super().__init__(**kwargs)

    def generate_from_text(self, text, cache_dir=None, path=None):
        if cache_dir is None:
            cache_dir = self.cache_dir
        if path is None:
            key = f"gtts-{self.voice}-{text}".encode()
            audio_path = "gtts-" + hashlib.sha256(key).hexdigest()[:20] + ".mp3"
        else:
            audio_path = path

        full = Path(cache_dir) / audio_path
        if not full.exists():
            resp = self.client.synthesize_speech(
                input=texttospeech.SynthesisInput(text=text),
                voice=texttospeech.VoiceSelectionParams(
                    language_code=self.language_code, name=self.voice),
                audio_config=texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3),
            )
            tmp = full.with_suffix(".part")
            with open(tmp, "wb") as f:
                f.write(resp.audio_content)
            tmp.rename(full)   # atomic: only a complete file lands in the cache

        return {"input_text": text, "original_audio": audio_path}
