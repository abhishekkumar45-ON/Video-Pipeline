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


# Type floors (never scale below these): MathTex >= 40pt long-form, >= 56pt Shorts.
MATHTEX_FLOOR_LONG  = 40
MATHTEX_FLOOR_SHORT = 56

# Buffers (collision law): >=0.4 Manim units between any two mobjects; nothing within
# ~0.35 units (48px @1080p) of the frame edge. Text never shrinks or spills.
MIN_BUFFER = 0.4
EDGE_SAFE  = 0.35
