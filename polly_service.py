"""
PollyService — a manim-voiceover SpeechService using Amazon Polly.
Natural + Indian-accent English via the neural voice 'Kajal' (en-IN).

Needs AWS credentials on this machine (via `aws configure` or ~/.aws/credentials or
env vars AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY). NOTE: this is a CLOUD service —
you must be online when rendering, unlike Kokoro/Tara. Polly returns mp3 directly,
so no ffmpeg step. Same sha256 filename caching as the other services, so each unique
narration line is only ever synthesized (and billed) once.

Indian-English voices: Kajal (neural, best), Aditi (standard), Raveena (standard).
Requires the IAM permission `polly:SynthesizeSpeech` (AmazonPollyReadOnlyAccess is enough).
"""
import hashlib
import os
from pathlib import Path

import boto3

from manim_voiceover.services.base import SpeechService


class PollyService(SpeechService):
    def __init__(self, voice="Kajal", engine="neural",
                 region=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"), **kwargs):
        self.voice = voice
        self.engine = engine
        self._client = boto3.client("polly", region_name=region)
        super().__init__(**kwargs)

    def generate_from_text(self, text, cache_dir=None, path=None):
        if cache_dir is None:
            cache_dir = self.cache_dir
        if path is None:
            key = f"polly-{self.voice}-{self.engine}-{text}".encode()
            audio_path = "polly-" + hashlib.sha256(key).hexdigest()[:20] + ".mp3"
        else:
            audio_path = path

        full = Path(cache_dir) / audio_path
        if not full.exists():
            resp = self._client.synthesize_speech(
                Text=text, VoiceId=self.voice, Engine=self.engine, OutputFormat="mp3",
            )
            with open(full, "wb") as f:
                f.write(resp["AudioStream"].read())

        return {"input_text": text, "original_audio": audio_path}
