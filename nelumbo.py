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
    """The mono '// NN — SECTION' kicker that opens a block."""
    return Mono(f"// {nn} — {section}", color=color).scale(0.4)


import numpy as np


def on_mark():
    """The Orange Nelumbo symbol, built in Manim: a lotus of five ignition petals in a
    launch cradle, wrapped by an orbital ring with a single satellite."""
    petals = VGroup()
    base = np.array([0.0, -0.04, 0.0])
    for ang, h, col in [(-40, 0.26, EMBER), (-20, 0.40, IGNITION), (0, 0.50, IGNITION),
                        (20, 0.40, IGNITION), (40, 0.26, EMBER)]:
        a = np.deg2rad(90 + ang)
        tip = base + h * np.array([np.cos(a), np.sin(a), 0.0])
        perp = 0.055 * np.array([np.cos(a - np.pi / 2), np.sin(a - np.pi / 2), 0.0])
        petals.add(Polygon(base + perp, tip, base - perp,
                           fill_color=col, fill_opacity=1, stroke_width=0))
    cradle = Arc(radius=0.30, start_angle=PI + 0.5, angle=PI - 1.0,
                 color=EMBER, stroke_width=3).move_to(base + DOWN * 0.16)
    ring = Ellipse(width=1.05, height=0.40, color=IGNITION, stroke_width=2.5).rotate(-0.2)
    ring.move_to(base + DOWN * 0.02)
    sat = Dot(color=EMBER, radius=0.045).move_to(ring.point_from_proportion(0.07))
    return VGroup(ring, cradle, petals, sat)


def on_logo(scale=0.5):
    """Top-left video lockup: the mark + 'ORANGE NELUMBO' wordmark (Space Grotesk bold)."""
    mark = on_mark().scale(0.62)
    word = Text("ORANGE NELUMBO", font=F_DISPLAY, weight=BOLD, color=WHITE).scale(0.30)
    return VGroup(mark, word).arrange(RIGHT, buff=0.22).scale(scale / 0.5)


def chip(text, color=SIGNAL, tscale=0.34):
    """A small graphite result chip for the right-side results rail."""
    t = Mono(text, color=color).scale(tscale)
    box = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.22, corner_radius=0.07,
                           color=GRAPHITE, fill_color=GRAPHITE, fill_opacity=0.92,
                           stroke_color=color, stroke_width=1.2)
    return VGroup(box, t)


# Type floors (never scale below these): MathTex >= 40pt long-form, >= 56pt Shorts.
MATHTEX_FLOOR_LONG  = 40
MATHTEX_FLOOR_SHORT = 56

# Buffers (collision law): >=0.4 Manim units between any two mobjects; nothing within
# ~0.35 units (48px @1080p) of the frame edge. Text never shrinks or spills.
MIN_BUFFER = 0.4
EDGE_SAFE  = 0.35
