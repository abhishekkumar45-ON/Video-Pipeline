"""
Orange Nelumbo · DEBRIEF · Thermodynamics · t2 — "Spring-loaded conducting piston"
JEE Advanced 2025 · Paper 2 · Numerical.  Answer: alpha = 0.2.
Concept-first (conducting piston ⇒ shared T, ideal gas, spring force balance) +
labelled force-balance diagram + full step-by-step derivation + step rail.
No progress counter. Voice af_bella. 4K. Gate-clean.
"""
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from kokoro_service import KokoroService

WORKC = LEFT * 1.15
LOGO_CLEAR = 1.7   # top-edge buff for centered headers: keeps them ~1.5 cm below the logo


class Scene_t2(VoiceoverScene):
    def construct(self):
        background(self)
        self.set_speech_service(KokoroService(voice="af_bella"))

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
        meta = Mono("JEE ADVANCED 2025 · PAPER 2", color=EMBER).scale(0.32)
        fmt = Mono("NUMERICAL", color=SIGNAL).scale(0.32)
        head = VGroup(VGroup(badge, meta).arrange(RIGHT, buff=0.35), fmt).arrange(RIGHT, buff=0.9).to_edge(UP, buff=LOGO_CLEAR)
        q = VGroup(
            Body("A thermally isolated tube of length L is split by a conducting,", color=WHITE).scale(0.46),
            Body("movable piston of area A. Left: 3/2 mol; right: 1 mol ideal gas.", color=WHITE).scale(0.46),
            Body("A spring (constant k, natural length 2L/5) ties the piston to the", color=WHITE).scale(0.46),
            Body("left wall. At equilibrium the piston sits L/2 from each edge.", color=WHITE).scale(0.46),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).next_to(head, DOWN, buff=0.55)
        ask = MathTex(r"\text{Right-side pressure } P_R = \tfrac{kL}{A}\,\alpha.\quad \text{Find } \alpha.", color=IGNITION).scale(0.55).next_to(q, DOWN, buff=0.5)
        with self.voiceover(text="Here's a neat thermodynamics problem. A sealed tube is divided by a movable, "
                                 "heat-conducting piston. On the left, three-halves of a mole; on the right, one "
                                 "mole of ideal gas. A spring ties the piston to the left wall, and at equilibrium "
                                 "the piston sits exactly in the middle. We must find alpha in the right-side "
                                 "pressure formula.") as t:
            self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.7)
            for ln in q:
                self.play(FadeIn(ln, shift=UP * 0.1), run_time=0.45, rate_func=smooth)
            self.play(Write(ask), run_time=1.0)
            self.wait(max(0.2, t.duration - 5.0))
        self.play(FadeOut(head), FadeOut(q), FadeOut(ask))

        # ============ 02 · PAUSE ============
        ring = Circle(radius=1.0, color=SIGNAL, stroke_width=5).move_to(UP * 0.2)
        num = Mono("5", color=SIGNAL).scale(1.4).move_to(ring)
        plbl = Label("PAUSE & ATTEMPT IT", color=WHITE).scale(0.55).next_to(ring, DOWN, buff=0.6)
        with self.voiceover(text="Pause, and set up the force balance on the piston yourself first.") as t:
            self.play(Create(ring), FadeIn(num), FadeIn(plbl), run_time=1.0)
            for k in ["4", "3", "2", "1"]:
                self.play(Transform(num, Mono(k, color=SIGNAL).scale(1.4).move_to(ring)), run_time=max(0.4, (t.duration-1.2)/4), rate_func=linear)
        self.play(FadeOut(ring), FadeOut(num), FadeOut(plbl))

        # ============ 03 · CONCEPT-FIRST ============
        head3 = Label("First — the three ideas we need", color=WHITE).scale(0.58).to_edge(UP, buff=LOGO_CLEAR)
        def ccard(title, sub, rel, relcol, icol):
            chip = Rectangle(width=0.9, height=0.9, fill_color=icol, fill_opacity=0.28, stroke_color=icol, stroke_width=3, )
            return VGroup(chip,
                          VGroup(Label(title, color=IGNITION).scale(0.5), Body(sub, color=TITANIUM).scale(0.33),
                                 MathTex(rel, color=relcol).scale(0.55)).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.32)
        c1 = ccard("CONDUCTING", "heat crosses → same T", r"T_L = T_R = T", IGNITION, IGNITION)
        c2 = ccard("IDEAL GAS", "each side V = A·L/2", r"P = \tfrac{nRT}{V}", SIGNAL, SIGNAL)
        c3 = ccard("EQUILIBRIUM", "net force on piston = 0", r"\Sigma F = 0", EMBER, EMBER)
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=1.05).next_to(head3, DOWN, buff=0.7)
        with self.voiceover(text="Before any numbers, three ideas. First, the piston conducts heat — so both gases "
                                 "settle to the same temperature T.") as t:
            self.play(Write(head3), run_time=0.8); self.play(FadeIn(c1, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration-1.8))
        with self.voiceover(text="Second, each gas is ideal, and since the piston sits in the middle, each side has "
                                 "the same volume — area A times L over two.") as t:
            self.play(FadeIn(c2, shift=UP*0.15), run_time=1.0); self.wait(max(0.1, t.duration-1.0))
        with self.voiceover(text="Third, the piston is in mechanical equilibrium — the net force on it, from both "
                                 "gas pressures and the spring, must add to zero.") as t:
            self.play(FadeIn(c3, shift=UP*0.15), run_time=1.0); self.wait(max(0.1, t.duration-1.0))
        self.play(FadeOut(head3), FadeOut(cards))

        # ============ 04 · GROUNDWORK ============
        head4 = kicker("", "THE GROUNDWORK").to_edge(UP, buff=LOGO_CLEAR)
        g = VGroup(
            MathTex(r"\text{conducting piston} \ \Rightarrow\ T_L = T_R = T", color=IGNITION).scale(0.6),
            MathTex(r"n_L = \tfrac{3}{2}\ \text{mol},\quad n_R = 1\ \text{mol}", color=SIGNAL).scale(0.6),
            MathTex(r"V_L = V_R = A\cdot\tfrac{L}{2}", color=WHITE).scale(0.6),
            MathTex(r"\text{spring: } k,\ \ \ell_0 = \tfrac{2L}{5},\quad \text{piston at } \tfrac{L}{2}", color=WHITE).scale(0.6),
        ).arrange(DOWN, buff=0.42).next_to(head4, DOWN, buff=0.6)
        with self.voiceover(text="Set the groundwork. The conducting piston gives a shared temperature T. We have "
                                 "three-halves of a mole on the left, one mole on the right, equal volumes of A times "
                                 "L over two, and a spring of natural length two-fifths L with the piston resting at "
                                 "L over two.") as t:
            self.play(FadeIn(head4), run_time=0.4)
            for line in g:
                self.play(Write(line), run_time=1.0)
            self.wait(max(0.1, t.duration - 4.4))
        self.play(FadeOut(head4), FadeOut(g))

        # ============ 05 · FORCE-BALANCE DIAGRAM ============
        head5 = Label("The force balance on the piston", color=WHITE).scale(0.52).to_edge(UP, buff=LOGO_CLEAR)
        # tube geometry, centred and slightly left
        TX, TY = -0.4, -0.4          # centre of the tube
        TW, TH = 5.2, 1.7            # tube width / height
        left_x, right_x = TX - TW/2, TX + TW/2
        top_y, bot_y = TY + TH/2, TY - TH/2
        pist_x = TX                  # piston in the middle

        tube = Rectangle(width=TW, height=TH, stroke_color=TITANIUM, stroke_width=4, fill_opacity=0).move_to([TX, TY, 0])
        gasL = Rectangle(width=TW/2 - 0.05, height=TH - 0.08, fill_color=IGNITION, fill_opacity=0.22, stroke_width=0).move_to([(left_x + pist_x)/2, TY, 0])
        gasR = Rectangle(width=TW/2 - 0.05, height=TH - 0.08, fill_color=SIGNAL, fill_opacity=0.20, stroke_width=0).move_to([(pist_x + right_x)/2, TY, 0])
        piston = Rectangle(width=0.16, height=TH - 0.02, fill_color=TITANIUM, fill_opacity=1, stroke_width=0).move_to([pist_x, TY, 0])

        # spring: zig-zag from left wall to piston
        def spring(x0, x1, y, coils=7, amp=0.22):
            n = coils * 2
            pts = [[x0, y, 0]]
            for i in range(1, n):
                fx = x0 + (x1 - x0) * i / n
                pts.append([fx, y + (amp if i % 2 else -amp), 0])
            pts.append([x1, y, 0])
            m = VMobject(stroke_color=EMBER, stroke_width=3.5)
            m.set_points_as_corners([np.array(p) for p in pts])
            return m
        spr = spring(left_x, pist_x - 0.08, TY)

        lblL = Mono("3/2 mol", color=IGNITION).scale(0.4).move_to([(left_x + pist_x)/2, TY + 0.42, 0])
        lblR = Mono("1 mol", color=SIGNAL).scale(0.4).move_to([(pist_x + right_x)/2, TY + 0.42, 0])
        lblLen = Mono("L", color=TITANIUM).scale(0.4).next_to(tube, DOWN, buff=0.18)

        # force arrows ON the piston
        arrL = Arrow([pist_x - 0.9, TY, 0], [pist_x - 0.12, TY, 0], color=IGNITION, buff=0, stroke_width=5, tip_length=0.2)
        arrR = Arrow([pist_x + 0.9, TY, 0], [pist_x + 0.12, TY, 0], color=SIGNAL, buff=0, stroke_width=5, tip_length=0.2)
        arrS = Arrow([pist_x - 0.12, TY - 0.55, 0], [pist_x - 0.9, TY - 0.55, 0], color=EMBER, buff=0, stroke_width=5, tip_length=0.2)
        fLl = MathTex(r"P_L A", color=IGNITION).scale(0.5).next_to(arrL, UP, buff=0.12).shift(LEFT*0.1)
        fRl = MathTex(r"P_R A", color=SIGNAL).scale(0.5).next_to(arrR, UP, buff=0.12).shift(RIGHT*0.1)
        fSl = MathTex(r"kx", color=EMBER).scale(0.5).next_to(arrS, DOWN, buff=0.12)

        diagram = VGroup(tube, gasL, gasR, piston, spr, lblL, lblR, lblLen,
                         arrL, arrR, arrS, fLl, fRl, fSl)

        with self.voiceover(text="Here it is. The tube, split by the piston in the middle. Orange gas on the left, "
                                 "cyan on the right, and the spring — in amber — tying the piston to the left wall.") as t:
            self.play(Write(head5), run_time=0.7)
            self.play(Create(tube), FadeIn(gasL), FadeIn(gasR), FadeIn(piston), run_time=1.2)
            self.play(Create(spr), FadeIn(lblL), FadeIn(lblR), FadeIn(lblLen), run_time=1.0)
            self.wait(max(0.1, t.duration - 2.9))
        with self.voiceover(text="Three forces act on the piston. The left gas pushes it right with P-L times A. "
                                 "The right gas pushes it left with P-R times A. And the stretched spring pulls it "
                                 "back toward the wall with k times x.") as t:
            self.play(GrowArrow(arrL), FadeIn(fLl), run_time=0.8)
            self.play(GrowArrow(arrR), FadeIn(fRl), run_time=0.8)
            self.play(GrowArrow(arrS), FadeIn(fSl), run_time=0.8)
            self.wait(max(0.1, t.duration - 2.4))
        self.play(diagram.animate.scale(0.4).to_corner(DR, buff=0.4), FadeOut(head5), run_time=1.0)

        # ============ 06 · STEP RAIL + DETAILED SOLVE ============
        rail = StepRail(4, top=1.5, gap=0.95, size=0.6)
        self.play(FadeIn(rail.whole()), rail.active(0), run_time=0.7)

        s1t = Label("STEP 1 — the two gas pressures", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s1a = MathTex(r"P_L = \frac{n_L RT}{V_L} = \frac{\tfrac{3}{2}RT}{A L/2} = \frac{3RT}{AL}", color=WHITE).scale(0.55).move_to(WORKC + UP*0.85)
        s1b = MathTex(r"P_R = \frac{n_R RT}{V_R} = \frac{RT}{A L/2} = \frac{2RT}{AL}", color=WHITE).scale(0.55).move_to(WORKC + DOWN*0.35)
        s1c = MathTex(r"P_L - P_R = \frac{RT}{AL}", color=IGNITION).scale(0.6).move_to(WORKC + DOWN*1.4)
        with self.voiceover(text="Step one, the pressures. Ideal gas, P equals n R T over V, with the same T and the "
                                 "same volume A L over two on each side. The left gives three R T over A L, the right "
                                 "gives two R T over A L, so their difference is R T over A L.") as t:
            self.play(FadeIn(s1t), Write(s1a), run_time=min(2.0, t.duration))
            self.play(Write(s1b), run_time=1.3)
            self.play(Write(s1c), run_time=0.9)
            add_result(r"P_L - P_R = \tfrac{RT}{AL}", IGNITION)
            self.wait(max(0.1, t.duration - 4.2))
        self.play(FadeOut(s1t), FadeOut(s1a), FadeOut(s1b), FadeOut(s1c), rail.done(0), rail.active(1))

        s2t = Label("STEP 2 — the spring force", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s2a = MathTex(r"x = \frac{L}{2} - \ell_0 = \frac{L}{2} - \frac{2L}{5} = \frac{L}{10}", color=WHITE).scale(0.55).move_to(WORKC + UP*0.6)
        s2b = MathTex(r"F_{\text{spring}} = kx = \frac{kL}{10}", color=EMBER).scale(0.6).move_to(WORKC + DOWN*0.6)
        with self.voiceover(text="Step two, the spring. Its natural length is two-fifths L, but the piston sits at L "
                                 "over two, so the extension x is L over two minus two-fifths L — that's L over ten. "
                                 "The spring force is k times that, k L over ten.") as t:
            self.play(FadeIn(s2t), Write(s2a), run_time=min(2.0, t.duration))
            self.play(Write(s2b), run_time=1.1)
            add_result(r"kx = \tfrac{kL}{10}", EMBER)
            self.wait(max(0.1, t.duration - 3.1))
        self.play(FadeOut(s2t), FadeOut(s2a), FadeOut(s2b), rail.done(1), rail.active(2))

        s3t = Label("STEP 3 — force balance on the piston", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s3a = MathTex(r"P_L A = P_R A + kx \ \Rightarrow\ (P_L - P_R)A = \frac{kL}{10}", color=WHITE).scale(0.52).move_to(WORKC + UP*0.7)
        s3b = MathTex(r"\frac{RT}{AL}\cdot A = \frac{kL}{10} \ \Rightarrow\ \frac{RT}{L} = \frac{kL}{10}", color=WHITE).scale(0.55).move_to(WORKC + DOWN*0.45)
        s3c = MathTex(r"RT = \frac{kL^2}{10}", color=IGNITION).scale(0.62).move_to(WORKC + DOWN*1.55)
        with self.voiceover(text="Step three, the force balance. The left push equals the right push plus the spring "
                                 "pull, so the pressure difference times A equals k L over ten. Substituting our "
                                 "difference, R T over L equals k L over ten — which gives R T equals k L squared "
                                 "over ten.") as t:
            self.play(FadeIn(s3t), Write(s3a), run_time=min(2.2, t.duration))
            self.play(Write(s3b), run_time=1.3)
            self.play(Write(s3c), run_time=0.9)
            add_result(r"RT = \tfrac{kL^2}{10}", IGNITION)
            self.wait(max(0.1, t.duration - 4.4))
        self.play(FadeOut(s3t), FadeOut(s3a), FadeOut(s3b), FadeOut(s3c), rail.done(2), rail.active(3))

        s4t = Label("STEP 4 — solve for alpha", color=WHITE).scale(0.44).move_to(WORKC + UP*2.0)
        s4a = MathTex(r"P_R = \frac{2RT}{AL} = \frac{2}{AL}\cdot\frac{kL^2}{10} = \frac{kL}{5A}", color=WHITE).scale(0.55).move_to(WORKC + UP*0.6)
        s4b = MathTex(r"P_R = \frac{kL}{A}\cdot\frac{1}{5} = \frac{kL}{A}\,\alpha \ \Rightarrow\ \alpha = \frac{1}{5}", color=WHITE).scale(0.55).move_to(WORKC + DOWN*0.6)
        with self.voiceover(text="Step four, solve for alpha. Take the right-side pressure, two R T over A L, and plug "
                                 "in R T equals k L squared over ten. That collapses to k L over five A — which is k L "
                                 "over A times one-fifth. Matching the given form, alpha is one over five.") as t:
            self.play(FadeIn(s4t), Write(s4a), run_time=min(2.2, t.duration))
            self.play(Write(s4b), run_time=1.3)
            add_result(r"\alpha = 0.2", CORRECT)
            self.wait(max(0.1, t.duration - 3.5))
        self.play(FadeOut(s4t), FadeOut(s4a), FadeOut(s4b), rail.done(3))

        # ============ 07 · ANSWER LOCK-IN ============
        ans = Label("ANSWER:   α = 0.2", color=IGNITION).scale(0.85).move_to(WORKC + UP*0.15)
        box = SurroundingRectangle(ans, color=CORRECT, buff=0.3, corner_radius=0.1)
        take = Body("Same T from the conducting piston, then just balance forces.", color=TITANIUM).scale(0.42).next_to(box, DOWN, buff=0.55)
        with self.voiceover(text="So alpha equals one-fifth, or zero point two.") as t:
            self.play(FadeIn(ans, shift=UP*0.1), run_time=0.9); self.play(Create(box), run_time=0.8)
            self.wait(max(0.1, t.duration - 1.7))
        with self.voiceover(text="The whole trick was seeing that a conducting piston forces one shared temperature — "
                                 "after that, it's pure force balance. Solved, completely.") as t:
            self.play(Write(take), run_time=1.2)
            self.wait(max(0.3, t.duration - 1.2))
        self.wait(0.6)
