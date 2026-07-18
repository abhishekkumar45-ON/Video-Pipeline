"""
Orange Nelumbo · DEBRIEF · Thermodynamics · t4 — "Soap bubble excess pressure"
JEE Advanced 2024 · Paper 2 · Numerical.  Answer: ΔP = 96 Pa.
Concept-first (excess pressure ΔP = 4S/r ⇒ ΔP ∝ 1/r; Boyle on trapped air) + LIVE bubble
that GROWS as the chamber pressure drops, with live P and ΔP readouts (144 → 96) + step rail.
No progress counter. Voice af_bella. Gate-clean.
"""
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from voice import narration_service

WORKC = LEFT * 1.15
LOGO_CLEAR = 1.7   # top-edge buff for centered headers: keeps them ~1.5 cm below the logo


class Scene_t4(VoiceoverScene):
    def construct(self):
        background(self)
        self.set_speech_service(narration_service(kokoro_voice="af_bella"))

        logo = on_logo(0.5).to_corner(UL, buff=0.45)
        chapter = Body("Thermodynamics", color=TITANIUM).scale(0.4).to_corner(DL, buff=0.45)
        self.add(logo, chapter)

        self._ri = 0
        RAIL_X, RAIL_Y = 5.05, [2.4, 1.75, 1.1, 0.45, -0.2]
        def add_result(latex, color=SIGNAL):
            c = mchip(latex, color=color, tscale=0.36).move_to(RIGHT * RAIL_X + UP * RAIL_Y[self._ri])
            self._ri += 1
            self.play(FadeIn(c, shift=LEFT * 0.15), run_time=0.5, rate_func=smooth)
            return c

        # ============ 01 · QUESTION ============
        bt = Mono("1", color=OBSIDIAN).scale(0.5)
        badge = VGroup(SurroundingRectangle(bt, color=SIGNAL, fill_color=SIGNAL, fill_opacity=1, buff=0.13, corner_radius=0.06), bt)
        meta = Mono("JEE ADVANCED 2024 · PAPER 2", color=EMBER).scale(0.32)
        fmt = Mono("NUMERICAL", color=SIGNAL).scale(0.32)
        head = VGroup(VGroup(badge, meta).arrange(RIGHT, buff=0.35), fmt).arrange(RIGHT, buff=0.9).to_edge(UP, buff=LOGO_CLEAR)
        q = VGroup(
            Body("A soap bubble sits in an air chamber at P₀ = 10⁵ Pa.", color=WHITE).scale(0.46),
            Body("Its excess pressure is ΔP = 144 Pa.", color=WHITE).scale(0.46),
            Body("The chamber pressure is lowered to 8P₀/27  (T constant).", color=WHITE).scale(0.46),
            Body("With ΔP ≪ chamber pressure, find the new ΔP.", color=WHITE).scale(0.46),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.55)
        ask = Mono("ΔP = ?  Pa", color=TITANIUM).scale(0.5).next_to(q, DOWN, buff=0.5)
        with self.voiceover(text="A neat surface-tension problem. A soap bubble floats inside an air chamber. "
                                 "Its excess pressure is one hundred forty-four pascals. Now we slowly drop the "
                                 "chamber pressure to eight twenty-sevenths of its start, keeping temperature fixed. "
                                 "Find the bubble's new excess pressure.") as t:
            self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.7)
            for ln in q:
                self.play(FadeIn(ln, shift=UP * 0.1), run_time=0.45, rate_func=smooth)
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.4)
            self.wait(max(0.2, t.duration - 4.6))
        self.play(FadeOut(head), FadeOut(q), FadeOut(ask))

        # ============ 02 · PAUSE ============
        ring = Circle(radius=1.0, color=SIGNAL, stroke_width=5).move_to(UP * 0.2)
        num = Mono("5", color=SIGNAL).scale(1.4).move_to(ring)
        plbl = Label("PAUSE & ATTEMPT IT", color=WHITE).scale(0.55).next_to(ring, DOWN, buff=0.6)
        with self.voiceover(text="Pause, and think about what pins the bubble's size.") as t:
            self.play(Create(ring), FadeIn(num), FadeIn(plbl), run_time=1.0)
            for k in ["4", "3", "2", "1"]:
                self.play(Transform(num, Mono(k, color=SIGNAL).scale(1.4).move_to(ring)), run_time=max(0.4, (t.duration-1.2)/4), rate_func=linear)
        self.play(FadeOut(ring), FadeOut(num), FadeOut(plbl))

        # ============ 03 · CONCEPT-FIRST ============
        head3 = Label("First — two laws in play", color=WHITE).scale(0.58).to_edge(UP, buff=LOGO_CLEAR)
        def bubble_icon(r, color):
            outer = Circle(radius=r, color=color, stroke_width=3.5)
            inner = Circle(radius=r*0.62, color=color, stroke_width=1.6).set_opacity(0.5)
            return VGroup(outer, inner)
        def ccard(title, sub, rel, relcol, icon):
            return VGroup(icon,
                          VGroup(Label(title, color=IGNITION).scale(0.5), Body(sub, color=TITANIUM).scale(0.35),
                                 MathTex(rel, color=relcol).scale(0.58)).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.32)
        c1 = ccard("EXCESS PRESSURE", "surface tension fixed", r"\Delta P=\tfrac{4S}{r}\ \Rightarrow\ \Delta P\propto\tfrac{1}{r}",
                   IGNITION, bubble_icon(0.5, IGNITION))
        c2 = ccard("BOYLE'S LAW", "isothermal trapped air", r"P\,V=\text{const},\ \ V\propto r^{3}",
                   SIGNAL, bubble_icon(0.65, SIGNAL))
        cards = VGroup(c1, c2).arrange(RIGHT, buff=1.6).next_to(head3, DOWN, buff=0.75)
        with self.voiceover(text="Two ideas do all the work. First, a soap bubble's excess pressure is four S over r, "
                                 "where S is the surface tension. Surface tension doesn't change, so the excess pressure "
                                 "is simply inversely proportional to the radius.") as t:
            self.play(Write(head3), run_time=0.8); self.play(FadeIn(c1, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration-1.8))
        with self.voiceover(text="Second, the air trapped in the bubble is squeezed slowly at constant temperature, so "
                                 "Boyle's law holds — pressure times volume is constant — and the volume goes as the "
                                 "radius cubed.") as t:
            self.play(FadeIn(c2, shift=UP*0.15), run_time=1.0); self.wait(max(0.1, t.duration-1.0))
        self.play(FadeOut(head3), FadeOut(cards))

        # ============ 04 · GROUNDWORK ============
        head4 = kicker("", "THE GROUNDWORK").to_edge(UP, buff=LOGO_CLEAR)
        g = VGroup(
            MathTex(r"\Delta P=\tfrac{4S}{r},\quad S\ \text{fixed}\ \Rightarrow\ \Delta P\propto \tfrac{1}{r}", color=IGNITION).scale(0.6),
            MathTex(r"\Delta P\ll\text{chamber}\ \Rightarrow\ P_{\text{gas}}\approx P_{\text{chamber}}", color=WHITE).scale(0.6),
            MathTex(r"\text{isothermal}:\ P_1V_1=P_2V_2,\quad V\propto r^{3}", color=SIGNAL).scale(0.6),
            MathTex(r"P_1=P_0,\quad P_2=\tfrac{8P_0}{27},\quad \Delta P_1=144\,\mathrm{Pa}", color=WHITE).scale(0.6),
        ).arrange(DOWN, buff=0.42).next_to(head4, DOWN, buff=0.6)
        with self.voiceover(text="Set the groundwork. Excess pressure is four S over r, so it scales as one over the "
                                 "radius. Because the excess pressure is tiny next to the chamber pressure, the gas inside "
                                 "sits at essentially the chamber pressure. The process is isothermal, so P-one V-one "
                                 "equals P-two V-two, with volume as r cubed. Our data: start at P-nought, drop to eight "
                                 "twenty-sevenths P-nought, with a starting excess of one hundred forty-four pascals.") as t:
            self.play(FadeIn(head4), run_time=0.4)
            for line in g:
                self.play(Write(line), run_time=1.0)
            self.wait(max(0.1, t.duration - 4.4))
        self.play(FadeOut(head4), FadeOut(g))

        # ============ 05 · WORKING VISUALISATION with LIVE P, ΔP (bubble grows) ============
        CHX, CHY = -3.9, -0.55          # chamber centre
        chw, chh = 2.7, 3.1
        chamber = RoundedRectangle(width=chw, height=chh, corner_radius=0.22,
                                   stroke_color=SIGNAL, stroke_width=4, fill_opacity=0).move_to([CHX, CHY, 0])
        ch_lbl = Mono("air chamber", color=TITANIUM).scale(0.32).next_to(chamber, DOWN, buff=0.18)

        r1, r2 = 0.62, 0.93             # 3/2 growth in radius
        rt = ValueTracker(r1)
        bubble = always_redraw(lambda: VGroup(
            Circle(radius=rt.get_value(), color=IGNITION, stroke_width=3.5, fill_color=IGNITION, fill_opacity=0.12),
            Circle(radius=rt.get_value()*0.6, color=IGNITION, stroke_width=1.4).set_opacity(0.45),
        ).move_to([CHX, CHY, 0]))

        pt_ = ValueTracker(1.0)         # chamber pressure in units of P₀
        dpt = ValueTracker(144.0)       # excess pressure in Pa
        def stat(name, tr, unit, col, dec):
            lbl = Mono(name, color=TITANIUM).scale(0.44)
            n = DecimalNumber(tr.get_value(), num_decimal_places=dec, color=col, font_size=38)
            n.add_updater(lambda m, tr=tr: m.set_value(tr.get_value()))
            u = Mono(unit, color=col).scale(0.4)
            return VGroup(lbl, n, u).arrange(RIGHT, buff=0.13), n
        sP, nP = stat("P =", pt_, "P₀", SIGNAL, 3)
        sDP, nDP = stat("ΔP =", dpt, "Pa", IGNITION, 0)
        readout = VGroup(sP, sDP).arrange(RIGHT, buff=0.9).to_edge(UP, buff=LOGO_CLEAR)

        with self.voiceover(text="Watch it live. On the left the air chamber with the soap bubble inside; up top, the "
                                 "chamber pressure in units of P-nought and the excess pressure in pascals. We start at "
                                 "P-nought, excess one hundred forty-four.") as t:
            self.play(Create(chamber), FadeIn(ch_lbl), run_time=1.0)
            self.play(FadeIn(bubble), run_time=0.6)
            self.play(FadeIn(readout, shift=DOWN*0.15), run_time=0.8)
            self.wait(max(0.1, t.duration - 2.4))

        with self.voiceover(text="Now lower the chamber pressure to eight twenty-sevenths of P-nought — about zero point "
                                 "two nine six. The trapped air expands, so the bubble grows: its radius climbs by a "
                                 "factor of three-halves. And since excess pressure goes as one over r, it falls from "
                                 "one hundred forty-four all the way down to ninety-six pascals.") as t:
            self.play(pt_.animate.set_value(8/27), dpt.animate.set_value(96), rt.animate.set_value(r2),
                      run_time=min(3.4, max(2.0, t.duration-1.2)), rate_func=smooth)
            self.wait(max(0.1, t.duration - 3.6))

        nP.clear_updaters(); nDP.clear_updaters()
        bubble.clear_updaters()
        diagram = VGroup(chamber, ch_lbl, bubble)
        self.play(FadeOut(readout),
                  diagram.animate.scale(0.4).to_corner(DR, buff=0.4), run_time=1.0)

        # ============ 06 · STEP RAIL + DETAILED SOLVE ============
        rail = StepRail(3, top=1.5, gap=0.95, size=0.60)
        self.play(FadeIn(rail.whole()), rail.active(0), run_time=0.7)

        s1t = Label("STEP 1 — excess pressure sets the radius", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s1a = MathTex(r"\Delta P=\frac{4S}{r},\qquad S=\text{const}", color=WHITE).scale(0.62).move_to(WORKC + UP*0.9)
        s1b = MathTex(r"\Rightarrow\ \Delta P\propto \frac{1}{r}", color=IGNITION).scale(0.66).move_to(WORKC + DOWN*0.2)
        s1c = MathTex(r"\frac{\Delta P_2}{\Delta P_1}=\frac{r_1}{r_2}", color=IGNITION).scale(0.62).move_to(WORKC + DOWN*1.3)
        with self.voiceover(text="Step one. The excess pressure is four S over r, and the surface tension is fixed, so "
                                 "the excess pressure is inversely proportional to the radius. That means the ratio of "
                                 "new to old excess pressure is just the inverse ratio of the radii.") as t:
            self.play(FadeIn(s1t), Write(s1a), run_time=min(1.9, t.duration))
            self.play(Write(s1b), run_time=1.0)
            self.play(Write(s1c), run_time=0.9)
            add_result(r"\Delta P\propto \tfrac{1}{r}", IGNITION)
            self.wait(max(0.1, t.duration - 3.8))
        self.play(FadeOut(s1t), FadeOut(s1a), FadeOut(s1b), FadeOut(s1c), rail.done(0), rail.active(1))

        s2t = Label("STEP 2 — Boyle's law fixes the radius ratio", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s2a = MathTex(r"P_1V_1=P_2V_2,\qquad V\propto r^{3}", color=WHITE).scale(0.56).move_to(WORKC + UP*0.85)
        s2b = MathTex(r"P_0\,r_1^{3}=\tfrac{8P_0}{27}\,r_2^{3}\ \Rightarrow\ \left(\tfrac{r_2}{r_1}\right)^{3}=\tfrac{27}{8}", color=WHITE).scale(0.52).move_to(WORKC + DOWN*0.3)
        s2c = MathTex(r"\Rightarrow\ \frac{r_2}{r_1}=\frac{3}{2}", color=SIGNAL).scale(0.64).move_to(WORKC + DOWN*1.4)
        with self.voiceover(text="Step two. The trapped air is isothermal, so P-one V-one equals P-two V-two, and volume "
                                 "goes as r cubed. Substituting: P-nought r-one cubed equals eight twenty-sevenths "
                                 "P-nought r-two cubed. The P-noughts cancel, so r-two over r-one cubed is twenty-seven "
                                 "over eight, and the radius ratio is three-halves.") as t:
            self.play(FadeIn(s2t), Write(s2a), run_time=min(1.9, t.duration))
            self.play(Write(s2b), run_time=1.3)
            self.play(Write(s2c), run_time=0.9)
            add_result(r"\tfrac{r_2}{r_1}=\tfrac{3}{2}", SIGNAL)
            self.wait(max(0.1, t.duration - 4.1))
        self.play(FadeOut(s2t), FadeOut(s2a), FadeOut(s2b), FadeOut(s2c), rail.done(1), rail.active(2))

        s3t = Label("STEP 3 — the new excess pressure", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s3a = MathTex(r"\Delta P_2=\Delta P_1\cdot\frac{r_1}{r_2}=144\cdot\frac{2}{3}", color=WHITE).scale(0.58).move_to(WORKC + UP*0.75)
        s3b = MathTex(r"\Delta P_2 = 96\ \mathrm{Pa}", color=CORRECT).scale(0.7).move_to(WORKC + DOWN*0.5)
        with self.voiceover(text="Step three. Combine them. The new excess pressure is the old one times r-one over "
                                 "r-two — that's one hundred forty-four times two-thirds, which is exactly ninety-six "
                                 "pascals.") as t:
            self.play(FadeIn(s3t), Write(s3a), run_time=min(2.0, t.duration))
            self.play(Write(s3b), run_time=1.0)
            add_result(r"\Delta P = 96\ \mathrm{Pa}", CORRECT)
            self.wait(max(0.1, t.duration - 3.2))
        self.play(FadeOut(s3t), FadeOut(s3a), rail.done(2))

        # ============ 07 · ANSWER LOCK-IN ============
        ans = Label("ANSWER:   ΔP = 96 Pa", color=IGNITION).scale(0.8).move_to(WORKC + UP*0.1)
        box = SurroundingRectangle(ans, color=CORRECT, buff=0.28, corner_radius=0.1)
        with self.voiceover(text="So the new excess pressure is ninety-six pascals. Lower the chamber pressure, the "
                                 "bubble swells, and its excess pressure drops in step. Solved.") as t:
            self.play(FadeOut(s3b), run_time=0.4)
            self.play(FadeIn(ans, shift=UP*0.1), run_time=0.9); self.play(Create(box), run_time=0.8)
            self.wait(max(0.3, t.duration - 2.1))
        self.wait(0.6)
