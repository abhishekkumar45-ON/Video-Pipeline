import os
import subprocess


def tts(text, out_mp3):
    """Make an mp3 for `text`. Tries gTTS (needs internet); if that fails,
    falls back to the macOS built-in `say` command (offline, always works on Mac)."""
    try:
        from gtts import gTTS
        gTTS(text=text, lang="en").save(out_mp3)
        if os.path.getsize(out_mp3) > 0:
            return out_mp3
    except Exception as e:
        print(f"  gTTS failed ({e}); using macOS 'say' instead")

    aiff = out_mp3.replace(".mp3", ".aiff")
    subprocess.run(["say", "-o", aiff, text], check=True)
    subprocess.run(["ffmpeg", "-y", "-i", aiff, out_mp3],
                   check=True, capture_output=True)
    os.remove(aiff)
    return out_mp3
