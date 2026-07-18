"""
narration_service() — the single place that decides which TTS voice the whole
pipeline uses. Every scene calls this instead of instantiating a service directly:

    from voice import narration_service
    ...
    self.set_speech_service(narration_service(kokoro_voice="af_bella"))

Switch the whole pipeline between the Kokoro preset voice and YOUR cloned voice by
editing VOICE_ENGINE in config.py, or per-render with an env var:

    VOICE_ENGINE=clone python batch_render.py ...

Both services expose the same manim-voiceover SpeechService interface, so scenes
don't care which one they get.
"""
import os

from config import CLONE_REFERENCE, VOICE_ENGINE

_CLONE_ALIASES = {"clone", "chatterbox", "mine", "me"}


def narration_service(kokoro_voice="af_bella", speed=0.9):
    """Return the configured SpeechService.

    kokoro_voice — preset voice name, used only when the engine is Kokoro.
    speed        — speaking speed (Kokoro honours this; the clone keeps natural pace).
    """
    engine = os.environ.get("VOICE_ENGINE", VOICE_ENGINE).strip().lower()

    if engine in _CLONE_ALIASES:
        # Lazy import so the heavy path is only touched when actually cloning.
        from chatterbox_service import ChatterboxService
        return ChatterboxService(reference=CLONE_REFERENCE)

    from kokoro_service import KokoroService
    return KokoroService(voice=kokoro_voice, speed=speed)
