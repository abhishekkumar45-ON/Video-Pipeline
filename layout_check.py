"""
layout_check.py — deterministic OVERLAP / OFF-FRAME linter for a Manim scene.

This is the anti-overlap guarantee. It runs the scene in-process at low quality with a
MOCK (instant, silent) speech service — so no TTS cost — and hooks every self.wait().
At each hold point it inspects every visible Text / MathTex / Tex object and fails if:
  - any two of them overlap by more than THRESH of the smaller one's area, or
  - any of them extends beyond the frame (clipped).

A generated scene is only shipped/rendered if this passes. If it fails, the specific
overlaps are printed and fed back to regenerate the code.

Usage:
  python layout_check.py scenes/q3.py Scene_q3
Exit code 0 = clean, 1 = violations found (printed).
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

import numpy as np
import manim
from manim import config, tempconfig, Text, MarkupText, MathTex, Tex
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.base import SpeechService

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

LABELS = (Text, MarkupText, MathTex, Tex)
OVERLAP_FRAC = 0.15   # flag if intersection > 15% of the smaller label's area
EDGE_TOL = 0.05       # units a label may poke past the frame before it's "clipped"


# ---- mock voice: no TTS, just a short silent clip so timing/layout still runs ----
class _MockSpeech(SpeechService):
    def generate_from_text(self, text, cache_dir=None, path=None):
        if cache_dir is None:
            cache_dir = self.cache_dir
        fn = "mock_silent.mp3"
        full = Path(cache_dir) / fn
        if not full.exists():
            subprocess.run(
                ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                 "-t", "0.3", str(full)], check=True, capture_output=True)
        return {"input_text": text, "original_audio": fn}


def _bbox(m):
    """(left, right, bottom, top) or None if degenerate/empty."""
    try:
        ul = m.get_corner([-1, 1, 0]); dr = m.get_corner([1, -1, 0])
    except Exception:
        return None
    left, top = ul[0], ul[1]
    right, bottom = dr[0], dr[1]
    if right - left < 1e-3 or top - bottom < 1e-3:
        return None
    return (left, right, bottom, top)


def _visible(m):
    # check the family: a MathTex group reports 0 fill on the container itself,
    # but its glyphs carry the real opacity — so inspect the leaves.
    fam = m.family_members_with_points() if hasattr(m, "family_members_with_points") else [m]
    if not fam:
        return False
    for s in fam:
        try:
            if s.get_fill_opacity() > 0.05 or s.get_stroke_opacity() > 0.05:
                return True
        except Exception:
            return True
    return False


def _labels(scene):
    """Every top-level Text/MathTex/Tex currently on screen (treated as one box each)."""
    out = []
    def visit(m):
        if isinstance(m, LABELS):
            if _visible(m):
                out.append(m)
            return                      # don't split a label into glyphs
        for s in m.submobjects:
            visit(s)
    for top in scene.mobjects:
        visit(top)
    return out


def _overlap(a, b):
    ox = max(0.0, min(a[1], b[1]) - max(a[0], b[0]))
    oy = max(0.0, min(a[3], b[3]) - max(a[2], b[2]))
    inter = ox * oy
    if inter <= 0:
        return 0.0
    area_a = (a[1] - a[0]) * (a[3] - a[2])
    area_b = (b[1] - b[0]) * (b[3] - b[2])
    return inter / max(1e-6, min(area_a, area_b))


def check(scene_path, cls):
    violations = []
    halfW = config.frame_width / 2
    halfH = config.frame_height / 2
    counter = {"i": 0}

    def inspect(scene):
        counter["i"] += 1
        i = counter["i"]
        mobs = _labels(scene)
        boxes = [(m, _bbox(m)) for m in mobs]
        boxes = [(m, b) for m, b in boxes if b]
        # off-frame (clipped)
        for m, b in boxes:
            if (b[0] < -halfW - EDGE_TOL or b[1] > halfW + EDGE_TOL or
                    b[2] < -halfH - EDGE_TOL or b[3] > halfH + EDGE_TOL):
                violations.append(f"[hold {i}] OFF-FRAME: {_txt(m)!r}")
        # pairwise overlap
        for x in range(len(boxes)):
            for y in range(x + 1, len(boxes)):
                (ma, ba), (mb, bb) = boxes[x], boxes[y]
                frac = _overlap(ba, bb)
                if frac > OVERLAP_FRAC:
                    violations.append(
                        f"[hold {i}] OVERLAP {int(frac*100)}%: {_txt(ma)!r}  <->  {_txt(mb)!r}")

    # hook wait() so we inspect every held state
    orig_wait = manim.Scene.wait
    def hooked_wait(self, *a, **k):
        try:
            inspect(self)
        except Exception as e:
            print(f"  (inspect warning: {e})")
        return orig_wait(self, *a, **k)
    manim.Scene.wait = hooked_wait

    # force the mock voice regardless of what the scene asks for
    orig_set = VoiceoverScene.set_speech_service
    VoiceoverScene.set_speech_service = lambda self, *a, **k: orig_set(self, _MockSpeech())

    SceneClass = _load(scene_path, cls)
    with tempconfig({"quality": "low_quality", "disable_caching": True,
                     "media_dir": str(ROOT / "build" / "_layoutcheck")}):
        SceneClass().render()

    manim.Scene.wait = orig_wait
    VoiceoverScene.set_speech_service = orig_set
    return violations


def _txt(m):
    for attr in ("text", "tex_string"):
        v = getattr(m, attr, None)
        if v:
            return v[:40]
    return type(m).__name__


def _load(path, cls):
    spec = importlib.util.spec_from_file_location("scene_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["scene_under_test"] = mod
    spec.loader.exec_module(mod)
    return getattr(mod, cls)


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: python layout_check.py scenes/<id>.py <ClassName>")
    path, cls = sys.argv[1], sys.argv[2]
    print(f"layout_check: {path} :: {cls}")
    v = check(path, cls)
    if not v:
        print("  CLEAN ✅  no overlap / off-frame")
        sys.exit(0)
    print(f"  {len(v)} violation(s):")
    for line in v:
        print("   -", line)
    sys.exit(1)


if __name__ == "__main__":
    main()
