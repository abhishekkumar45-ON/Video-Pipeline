"""
nelumbo.py — the ONE shared brand module. Every DEBRIEF scene imports from here.
Palette, fonts and helpers are defined ONCE (per Brand Guidelines ch.03/04 and
DEBRIEF Guidelines ch.11). No scene defines its own colours or fonts.

    from nelumbo import *

Semantic colour layer (FIXED in every chapter, every subject — never repurpose):
  OBSIDIAN  background (never pure black)
  IGNITION  the active move / target / emphasis — ONE at a time
  EMBER     secondary warm, trick flags, gradients
  SIGNAL    givens, telemetry, timers, hack mode  (the ONLY place cyan lives)
  TITANIUM  scaffold, axes, ghosts (use at 45% / 30%)
  AMBER     trigger words — READ beat ONLY, nowhere else
  CORRECT   the final answer, once
  ERROR     misfire, trap, eliminations
  GRAPHITE  cards & chips
"""
from manim import *

# ---- palette (Brand Guidelines / nelumbo.py spec) ----
OBSIDIAN = "#0E0D10"   # background — never pure black
CARBON   = "#161418"   # primary surface
GRAPHITE = "#1E1B20"   # cards & chips
STEEL    = "#2A262E"
IGNITION = "#FF5A1F"   # active move / target / emphasis — ONE at a time
EMBER    = "#FF8A3D"   # secondary warm, trick flags, gradients
SIGNAL   = "#3DE0D0"   # givens, telemetry, timers, hack mode (cyan lives ONLY here)
TITANIUM = "#C7C5CC"   # scaffold, axes, ghosts (45% / 30%)
AMBER    = "#F6C344"   # trigger words — READ beat ONLY
CORRECT  = "#3DE08A"   # final answer, once
ERROR    = "#E0483C"   # misfire, trap, eliminations
WHITE    = "#F1EFE8"   # working math / body text

# ---- fonts (three families, one job each) ----
F_DISPLAY = "Space Grotesk"   # headlines, titles, takeaway lines
F_BODY    = "Manrope"         # body copy, captions
F_MONO    = "JetBrains Mono"  # telemetry, labels, // NN markers, ALL numbers


def Label(s, **kw):
    """Space Grotesk BOLD — headlines, titles, the takeaway line."""
    kw.setdefault("color", WHITE)
    return Text(s, font=F_DISPLAY, weight=BOLD, **kw)


def Body(s, **kw):
    """Manrope — body copy, captions, explanations."""
    kw.setdefault("color", TITANIUM)
    return Text(s, font=F_BODY, **kw)


def Mono(s, **kw):
    """JetBrains Mono — labels, telemetry, // NN kickers, numbers & units."""
    kw.setdefault("color", SIGNAL)
    return Text(s, font=F_MONO, **kw)


def apply_bg(scene):
    """Set the obsidian background. Call first in every construct()."""
    scene.camera.background_color = OBSIDIAN


def kicker(nn, section, color=IGNITION):
    """A small mono section label (no '//' — the brand tag lives only in the top-left logo)."""
    return Mono(section, color=color).scale(0.44)


import numpy as np


_OUTLINE = "#17151A"
_TAN     = "#C88A4A"
_PEACH   = "#E0965A"
_RUST    = "#C7440E"
_PAGE    = "#EFE6CE"
_COVER   = "#3A2418"


def _petal(length=0.5, width=0.32, fill=IGNITION, sw=2.4):
    """A single smooth lotus petal, base at origin, pointing up (+y)."""
    w, L = width, length
    pts = [[0, 0.0, 0], [w * 0.52, L * 0.28, 0], [w * 0.40, L * 0.74, 0],
           [0, L, 0], [-w * 0.40, L * 0.74, 0], [-w * 0.52, L * 0.28, 0], [0, 0.0, 0]]
    p = VMobject(fill_color=fill, fill_opacity=1, stroke_color=_OUTLINE, stroke_width=sw)
    p.set_points_smoothly([np.array(x) for x in pts])
    return p


def _book():
    """A small open book beneath the lotus."""
    cover = Polygon([-0.66, -0.20, 0], [0.66, -0.20, 0], [0.58, -0.34, 0], [-0.58, -0.34, 0],
                    fill_color=_COVER, fill_opacity=1, stroke_color=_OUTLINE, stroke_width=2.4)
    lp = Polygon([0, -0.02, 0], [-0.70, 0.10, 0], [-0.66, -0.20, 0], [0, -0.22, 0],
                 fill_color=_PAGE, fill_opacity=1, stroke_color=_OUTLINE, stroke_width=2.4)
    rp = Polygon([0, -0.02, 0], [0.70, 0.10, 0], [0.66, -0.20, 0], [0, -0.22, 0],
                 fill_color=_PAGE, fill_opacity=1, stroke_color=_OUTLINE, stroke_width=2.4)
    spine = Line([0, -0.02, 0], [0, -0.22, 0], color=_OUTLINE, stroke_width=2.2)
    return VGroup(cover, lp, rp, spine)


def on_mark():
    """The Orange Nelumbo symbol: a lotus (tan base leaves, peach mid, ignition front petals)
    resting on an open book. Built natively so it renders crisp at 4K."""
    b = UP * 0.10   # base point of the petals, sitting on the book
    # crown (small petals peeking at the very top, drawn first so mains overlap their base)
    crown = VGroup(
        _petal(0.34, 0.22, _PEACH, sw=2.0).rotate(-16 * DEGREES, about_point=ORIGIN).shift(UP * 0.66),
        _petal(0.40, 0.22, _PEACH, sw=2.0).shift(UP * 0.70),
        _petal(0.34, 0.22, _PEACH, sw=2.0).rotate(16 * DEGREES, about_point=ORIGIN).shift(UP * 0.66),
    )
    base_leaves = VGroup(   # wide outer leaves, nearly horizontal — the bloom
        _petal(0.56, 0.52, _TAN).rotate(-74 * DEGREES, about_point=ORIGIN),
        _petal(0.56, 0.52, _TAN).rotate(74 * DEGREES, about_point=ORIGIN),
    )
    mid = VGroup(
        _petal(0.64, 0.34, _PEACH).rotate(-40 * DEGREES, about_point=ORIGIN),
        _petal(0.64, 0.34, _PEACH).rotate(40 * DEGREES, about_point=ORIGIN),
    )
    front = VGroup(
        _petal(0.74, 0.32, _RUST).rotate(-18 * DEGREES, about_point=ORIGIN),
        _petal(0.74, 0.32, _RUST).rotate(18 * DEGREES, about_point=ORIGIN),
        _petal(0.86, 0.34, IGNITION),   # tall centre petal, brightest, in front
    )
    lotus = VGroup(crown, base_leaves, mid, front).shift(b)
    orbit = ArcBetweenPoints([-1.55, 0.62, 0], [1.55, 0.62, 0], angle=-0.55,
                             color=IGNITION, stroke_width=2)
    return VGroup(orbit, _book(), lotus)


def on_logo(scale=0.5):
    """Top-left video lockup: the mark + 'ORANGE NELUMBO' wordmark (Space Grotesk bold)."""
    mark = on_mark().scale(0.34)
    word = Text("ORANGE NELUMBO", font=F_DISPLAY, weight=BOLD, color=WHITE).scale(0.30)
    return VGroup(mark, word).arrange(RIGHT, buff=0.24).scale(scale / 0.5)


def mchip(latex, color=SIGNAL, tscale=0.40):
    """A small graphite result chip (LaTeX) for the right-side results rail — proper subscripts."""
    m = MathTex(latex, color=color).scale(tscale)
    box = RoundedRectangle(width=m.width + 0.34, height=m.height + 0.26, corner_radius=0.08,
                           color=GRAPHITE, fill_color=GRAPHITE, fill_opacity=0.92,
                           stroke_color=color, stroke_width=1.2)
    return VGroup(box, m)


# Type floors (never scale below these): MathTex >= 40pt long-form, >= 56pt Shorts.
MATHTEX_FLOOR_LONG  = 40
MATHTEX_FLOOR_SHORT = 56

# Buffers (collision law): >=0.4 Manim units between any two mobjects; nothing within
# ~0.35 units (48px @1080p) of the frame edge. Text never shrinks or spills.
MIN_BUFFER = 0.4
EDGE_SAFE  = 0.35
