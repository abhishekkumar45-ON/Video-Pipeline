# Which Claude model the agents use. Swap to a stronger one for better quality.
MODEL = "claude-sonnet-5"

# Manim quality: -ql = fast/low (use today). -qh = high (use once it works).
QUALITY = "-ql"

# ---------------------------------------------------------------------------
# Narration voice
# ---------------------------------------------------------------------------
# "kokoro" -> preset neural voices (af_bella etc.). Cannot sound like a person.
# "clone"  -> YOUR cloned voice via Chatterbox, using CLONE_REFERENCE below.
#
# This is the ONE switch for the whole pipeline. Every scene calls
# voice.narration_service(), which reads this value.
#
# You can also override per render without editing this file:
#     VOICE_ENGINE=clone python batch_render.py ...
VOICE_ENGINE = "kokoro"

# Reference clip for cloning (only used when VOICE_ENGINE == "clone").
# 10-30 seconds of clean speech of the target voice. WAV, 44.1/48 kHz, mono is fine.
# Path is relative to the project root.
CLONE_REFERENCE = "assets/my_voice.wav"
