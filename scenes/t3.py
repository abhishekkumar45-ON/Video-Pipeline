"""
Orange Nelumbo · DEBRIEF · Thermodynamics · t3 — "Black-body plates in series" (detailed)
JEE Advanced 2025 · Paper 1 · Numerical.  Answer: W0 / Ws = 3.
Concept-first (Stefan net exchange + series-flux idea) + series-of-plates schematic +
full step-by-step derivation + step rail. No progress counter. Voice af_bella. 4K. Gate-clean.
"""
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from voice import narration_service

WORKC = LEFT * 1.15
LOGO_CLEAR = 1.7   # top-edge buff for centered headers: keeps them ~1.5 cm below the logo


class Scene_t3(VoiceoverScene):
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
        meta = Mono("JEE ADVANCED 2025 · PAPER 1", color=EMBER).scale(0.32)
        fmt = Mono("NUMERICAL", color=SIGNAL).scale(0.32)
        head = VGroup(VGroup(badge, meta).arrange(RIGHT, buff=0.35), fmt).arrange(RIGHT, buff=0.9).to_edge(UP, buff=LOGO_CLEAR)
        q = VGroup(
            Body("Two identical black-body plates P and Q in vacuum,", color=WHITE).scale(0.46),
            Body("held at fixed temperatures with T_P > T_Q.", color=WHITE).scale(0.46),
            Body("Net power per unit area from P to Q is W0.", color=WHITE).scale(0.46),
            Body("Insert two more identical plates between them", color=WHITE).scale(0.46),
            Body("(heat flows only between adjacent plates).", color=WHITE).scale(0.46),
            Body("In steady state that power becomes Ws.", color=WHITE).scale(0.46),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(head, DOWN, buff=0.5)
        target = Mono("Find  W0 / Ws", color=IGNITION).scale(0.5).next_to(q, DOWN, buff=0.45)
        with self.voiceover(text="Here's a clean radiation problem. Two identical black-body plates face each other in "
                                 "vacuum, P hot and Q cold. The net power per unit area flowing across is W-nought. Now we "
                                 "slide two more identical plates in between, so heat only hops from one plate to the next. "
                                 "In steady state that power drops to W-s. Find the ratio W-nought over W-s.") as t:
            self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.7)
            for ln in q:
                self.play(FadeIn(ln, shift=UP * 0.1), run_time=0.38, rate_func=smooth)
            self.play(FadeIn(target, shift=RIGHT * 0.1), run_time=0.5)
            self.wait(max(0.2, t.duration - 5.0))
        self.play(FadeOut(head), FadeOut(q), FadeOut(target))

        # ============ 02 · PAUSE ============
        ring = Circle(radius=1.0, color=SIGNAL, stroke_width=5).move_to(UP * 0.2)
        num = Mono("5", color=SIGNAL).scale(1.4).move_to(ring)
        plbl = Label("PAUSE & ATTEMPT IT", color=WHITE).scale(0.55).next_to(ring, DOWN, buff=0.6)
        with self.voiceover(text="Pause, and try the ratio yourself first.") as t:
            self.play(Create(ring), FadeIn(num), FadeIn(plbl), run_time=1.0)
            for k in ["4", "3", "2", "1"]:
                self.play(Transform(num, Mono(k, color=SIGNAL).scale(1.4).move_to(ring)), run_time=max(0.4, (t.duration-1.2)/4), rate_func=linear)
        self.play(FadeOut(ring), FadeOut(num), FadeOut(plbl))

        # ============ 03 · CONCEPT-FIRST ============
        head3 = Label("First — two ideas that crack this", color=WHITE).scale(0.58).to_edge(UP, buff=LOGO_CLEAR)

        def plate_icon(col, h=1.0):
            return Rectangle(width=0.16, height=h, fill_color=col, fill_opacity=0.85, stroke_width=0)
        # concept card 1 : Stefan net exchange between two black bodies
        pA = plate_icon(IGNITION); pB = plate_icon(SIGNAL)
        pair = VGroup(pA, pB).arrange(RIGHT, buff=1.1)
        arr1 = Arrow(pA.get_right(), pB.get_left(), color=EMBER, stroke_width=4, buff=0.06, tip_length=0.16)
        vis1 = VGroup(pair, arr1)
        c1 = VGroup(
            vis1,
            Label("STEFAN NET FLUX", color=IGNITION).scale(0.46),
            Body("black body to black body", color=TITANIUM).scale(0.34),
            MathTex(r"W=\sigma\,(T_h^{4}-T_c^{4})", color=IGNITION).scale(0.56),
        ).arrange(DOWN, buff=0.24)
        # concept card 2 : same net flux across every gap in series
        r1 = plate_icon(IGNITION); r2 = plate_icon(TITANIUM); r3 = plate_icon(SIGNAL)
        row = VGroup(r1, r2, r3).arrange(RIGHT, buff=0.9)
        a1 = Arrow(r1.get_right(), r2.get_left(), color=EMBER, stroke_width=3.5, buff=0.05, tip_length=0.14)
        a2 = Arrow(r2.get_right(), r3.get_left(), color=EMBER, stroke_width=3.5, buff=0.05, tip_length=0.14)
        vis2 = VGroup(row, a1, a2)
        c2 = VGroup(
            vis2,
            Label("SAME FLUX IN SERIES", color=SIGNAL).scale(0.46),
            Body("like equal current in series", color=TITANIUM).scale(0.34),
            MathTex(r"W_s\ \text{crosses every gap}", color=SIGNAL).scale(0.5),
        ).arrange(DOWN, buff=0.24)
        cards = VGroup(c1, c2).arrange(RIGHT, buff=1.6).next_to(head3, DOWN, buff=0.7)
        with self.voiceover(text="Before any numbers, two ideas. First, Stefan's law: between two black bodies the net "
                                 "flux is sigma times the fourth power of the hot temperature minus the fourth power of the "
                                 "cold one.") as t:
            self.play(Write(head3), run_time=0.8)
            self.play(FadeIn(c1, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration-1.8))
        with self.voiceover(text="Second, and this is the key: in steady state no plate stores energy, so the same net "
                                 "flux must cross every gap in the stack — exactly like equal current through resistors in "
                                 "series. The in-between temperatures quietly self-adjust to make that happen.") as t:
            self.play(FadeIn(c2, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration-1.0))
        self.play(FadeOut(head3), FadeOut(cards))

        # ============ 04 · GROUNDWORK ============
        head4 = kicker("", "THE GROUNDWORK").to_edge(UP, buff=LOGO_CLEAR)
        g = VGroup(
            MathTex(r"\text{Black bodies} \Rightarrow \text{emissivity } \varepsilon = 1", color=IGNITION).scale(0.6),
            MathTex(r"\text{Net flux (2 plates): } W_0=\sigma\,(T_P^{4}-T_Q^{4})", color=WHITE).scale(0.6),
            MathTex(r"\text{Steady state} \Rightarrow \text{no plate stores heat}", color=SIGNAL).scale(0.6),
            MathTex(r"2\ \text{inserted plates} \Rightarrow 3\ \text{gaps in series}", color=WHITE).scale(0.6),
        ).arrange(DOWN, buff=0.42).next_to(head4, DOWN, buff=0.6)
        with self.voiceover(text="Set the groundwork. The plates are perfect black bodies, so emissivity is one. Originally, "
                                 "with just P and Q, the net flux is sigma times T-P to the fourth minus T-Q to the fourth. "
                                 "In steady state no plate stores heat, and inserting two plates makes three gaps in series.") as t:
            self.play(FadeIn(head4), run_time=0.4)
            for line in g:
                self.play(Write(line), run_time=1.0)
            self.wait(max(0.1, t.duration - 4.4))
        self.play(FadeOut(head4), FadeOut(g))

        # ============ 05 · LIVE VISUAL — the four-plate series schematic ============
        head5 = Label("The stack: P — 1 — 2 — Q", color=WHITE).scale(0.5).to_edge(UP, buff=LOGO_CLEAR)

        PH = 2.4          # plate height
        cy = -0.55        # centre y of the plates
        xs = [-4.4, -2.05, 0.30, 2.65]
        cols = [IGNITION, TITANIUM, TITANIUM, SIGNAL]
        names = ["P", "1", "2", "Q"]
        tlabs = [r"T_P", r"T_1", r"T_2", r"T_Q"]
        plates, pnames, ptemps = VGroup(), VGroup(), VGroup()
        for x, col, nm, tl in zip(xs, cols, names, tlabs):
            pl = Rectangle(width=0.32, height=PH, fill_color=col, fill_opacity=0.80, stroke_color=col, stroke_width=2).move_to([x, cy, 0])
            nlab = Mono(nm, color=col).scale(0.5).next_to(pl, UP, buff=0.18)
            tlab = MathTex(tl, color=col).scale(0.52).next_to(pl, DOWN, buff=0.2)
            plates.add(pl); pnames.add(nlab); ptemps.add(tlab)
        # flux arrows across each of the three gaps
        fl_arrows, fl_labs = VGroup(), VGroup()
        for i in range(3):
            a = Arrow([xs[i] + 0.20, cy, 0], [xs[i+1] - 0.20, cy, 0], color=EMBER, stroke_width=4, buff=0.0, tip_length=0.18)
            wl = MathTex(r"W_s", color=EMBER).scale(0.5).next_to(a, UP, buff=0.12)
            fl_arrows.add(a); fl_labs.add(wl)
        schematic = VGroup(plates, pnames, ptemps, fl_arrows, fl_labs)

        with self.voiceover(text="Here's the stack. P on the left, hot, in orange; Q on the right, cold, in cyan; and the "
                                 "two inserted plates one and two in between. Their temperatures, T-one and T-two, settle "
                                 "somewhere between the two ends.") as t:
            self.play(Write(head5), run_time=0.7)
            self.play(LaggedStart(*[GrowFromCenter(p) for p in plates], lag_ratio=0.2), run_time=1.4)
            self.play(FadeIn(pnames, shift=UP*0.1), FadeIn(ptemps, shift=DOWN*0.1), run_time=0.8)
            self.wait(max(0.1, t.duration - 2.9))
        with self.voiceover(text="Now the crucial picture: in steady state the very same net flux W-s crosses each of the "
                                 "three gaps. Equal arrows, gap after gap.") as t:
            for a, wl in zip(fl_arrows, fl_labs):
                self.play(GrowArrow(a), FadeIn(wl, shift=UP*0.08), run_time=0.6)
            self.wait(max(0.1, t.duration - 1.8))

        # dock bottom-right
        self.play(FadeOut(head5), schematic.animate.scale(0.4).to_corner(DR, buff=0.4), run_time=1.0)

        # ============ 06 · STEP RAIL + DETAILED SOLVE ============
        rail = StepRail(3, top=1.3, gap=1.05, size=0.6)
        self.play(FadeIn(rail.whole()), rail.active(0), run_time=0.7)

        s1t = Label("STEP 1 — the original two-plate flux", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s1a = MathTex(r"\text{Two black bodies P, Q facing each other:}", color=WHITE).scale(0.5).move_to(WORKC + UP*0.9)
        s1b = MathTex(r"W_0 = \sigma\,(T_P^{4} - T_Q^{4})", color=IGNITION).scale(0.66).move_to(WORKC + DOWN*0.3)
        with self.voiceover(text="Step one. With just P and Q, Stefan's law gives the net flux W-nought equals sigma times "
                                 "T-P to the fourth minus T-Q to the fourth. Hold onto this expression.") as t:
            self.play(FadeIn(s1t), Write(s1a), run_time=min(1.8, t.duration))
            self.play(Write(s1b), run_time=1.0)
            add_result(r"W_0 = \sigma(T_P^{4}-T_Q^{4})", IGNITION)
            self.wait(max(0.1, t.duration - 3.0))
        self.play(FadeOut(s1t), FadeOut(s1a), FadeOut(s1b), rail.done(0), rail.active(1))

        s2t = Label("STEP 2 — same flux across all three gaps", color=WHITE).scale(0.42).move_to(WORKC + UP*2.0)
        s2a = MathTex(r"W_s = \sigma\,(T_P^{4} - T_1^{4})", color=WHITE).scale(0.56).move_to(WORKC + UP*0.85)
        s2b = MathTex(r"W_s = \sigma\,(T_1^{4} - T_2^{4})", color=WHITE).scale(0.56).move_to(WORKC + DOWN*0.05)
        s2c = MathTex(r"W_s = \sigma\,(T_2^{4} - T_Q^{4})", color=WHITE).scale(0.56).move_to(WORKC + DOWN*0.95)
        with self.voiceover(text="Step two. In steady state each plate radiates away exactly what it receives, so the same "
                                 "W-s crosses every gap. That gives three equations: sigma T-P fourth minus T-one fourth, "
                                 "then T-one fourth minus T-two fourth, then T-two fourth minus T-Q fourth — all equal to W-s.") as t:
            self.play(FadeIn(s2t), Write(s2a), run_time=min(1.8, t.duration))
            self.play(Write(s2b), run_time=1.0)
            self.play(Write(s2c), run_time=1.0)
            add_result(r"W_s\ \text{same in each gap}", SIGNAL)
            self.wait(max(0.1, t.duration - 4.0))
        self.play(FadeOut(s2t), FadeOut(s2a), FadeOut(s2b), FadeOut(s2c), rail.done(1), rail.active(2))

        s3t = Label("STEP 3 — add them: the middles cancel", color=WHITE).scale(0.42).move_to(WORKC + UP*2.0)
        s3a = MathTex(r"3W_s = \sigma\big[(T_P^{4}-T_1^{4})+(T_1^{4}-T_2^{4})+(T_2^{4}-T_Q^{4})\big]", color=WHITE).scale(0.46).move_to(WORKC + UP*0.9)
        s3b = MathTex(r"3W_s = \sigma\,(T_P^{4} - T_Q^{4}) = W_0", color=CORRECT).scale(0.58).move_to(WORKC + DOWN*0.2)
        s3c = MathTex(r"\Rightarrow\ \frac{W_0}{W_s} = 3", color=CORRECT).scale(0.66).move_to(WORKC + DOWN*1.35)
        with self.voiceover(text="Step three. Add the three equations. On the right the intermediate T-one fourth and "
                                 "T-two fourth cancel in a telescoping sum, leaving just T-P fourth minus T-Q fourth. So "
                                 "three W-s equals sigma times that difference — which is exactly W-nought. Therefore the "
                                 "ratio W-nought over W-s is three.") as t:
            self.play(FadeIn(s3t), Write(s3a), run_time=min(2.2, t.duration))
            self.play(Write(s3b), run_time=1.2)
            self.play(Write(s3c), run_time=1.0)
            add_result(r"W_0/W_s = 3", CORRECT)
            self.wait(max(0.1, t.duration - 4.6))
        self.play(FadeOut(s3t), FadeOut(s3a), FadeOut(s3b), FadeOut(s3c), rail.done(2))

        # ============ 07 · LOCK-IN ============
        gen = MathTex(r"\text{General: } m\ \text{plates inserted} \Rightarrow \frac{W_0}{W_s} = m+1", color=SIGNAL).scale(0.5).move_to(WORKC + UP*0.7)
        ans = Label("ANSWER:   W0 / Ws  =  3", color=IGNITION).scale(0.8).move_to(WORKC + DOWN*0.7)
        box = SurroundingRectangle(ans, color=CORRECT, buff=0.28, corner_radius=0.1)
        with self.voiceover(text="Worth remembering the general pattern: inserting m identical plates makes m plus one gaps "
                                 "in series, so the flux drops by a factor of m plus one. Two plates gives a factor of three.") as t:
            self.play(Write(gen), run_time=min(2.2, t.duration))
            self.wait(max(0.1, t.duration - 2.2))
        with self.voiceover(text="So the answer is three — the extra plates act like resistors in series and cut the "
                                 "radiative flow to a third. Solved, completely.") as t:
            self.play(FadeIn(ans, shift=UP*0.1), run_time=0.9)
            self.play(Create(box), run_time=0.8)
            self.wait(max(0.3, t.duration - 1.7))
        self.wait(0.6)
