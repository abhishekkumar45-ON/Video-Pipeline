"""
Orange Nelumbo · DEBRIEF · Thermodynamics · t7 — "Match the black-body temperatures" (detailed)
JEE Advanced 2023 · Paper 1 · Single correct (List-match).  Answer: (C) P→3, Q→4, R→2, S→1.
Concept-first (Wien's law + Stefan T^4 + photoemission) + black-body spectra shifting LEFT as T
rises + full step-by-step matching + step rail. No progress counter. Voice af_bella. 4K. Gate-clean.
"""
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from kokoro_service import KokoroService

WORKC = LEFT * 1.15
LOGO_CLEAR = 1.7   # top-edge buff for centered headers: keeps them ~1.5 cm below the logo


class Scene_t7(VoiceoverScene):
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
        meta = Mono("JEE ADVANCED 2023 · PAPER 1", color=EMBER).scale(0.32)
        fmt = Mono("SINGLE CORRECT · LIST MATCH", color=SIGNAL).scale(0.32)
        head = VGroup(VGroup(badge, meta).arrange(RIGHT, buff=0.35), fmt).arrange(RIGHT, buff=0.9).to_edge(UP, buff=LOGO_CLEAR)

        intro = Body("Match each black-body temperature to a statement.", color=WHITE).scale(0.44).next_to(head, DOWN, buff=0.45)
        li = VGroup(
            Mono("(P)  2000 K", color=WHITE).scale(0.40),
            Mono("(Q)  3000 K", color=WHITE).scale(0.40),
            Mono("(R)  5000 K", color=WHITE).scale(0.40),
            Mono("(S)  10000 K", color=WHITE).scale(0.40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        li_h = Mono("LIST-I", color=SIGNAL).scale(0.36)
        listI = VGroup(li_h, li).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        lii = VGroup(
            Body("(1) peak ejects photoelectrons from a 4 eV metal", color=TITANIUM).scale(0.34),
            Body("(2) peak is visible to the eye", color=TITANIUM).scale(0.34),
            Body("(3) peak gives the widest single-slit central max", color=TITANIUM).scale(0.34),
            Body("(4) power/area = 1/16 of a body at 6000 K", color=TITANIUM).scale(0.34),
            Body("(5) peak can image bones", color=TITANIUM).scale(0.34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        lii_h = Mono("LIST-II", color=EMBER).scale(0.36)
        listII = VGroup(lii_h, lii).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        lists = VGroup(listI, listII).arrange(RIGHT, buff=1.1, aligned_edge=UP).next_to(intro, DOWN, buff=0.5)
        const = Mono("b = 2.9×10⁻³ m·K,   hc/e = 1.24×10⁻⁶ V·m", color=SIGNAL).scale(0.34).next_to(lists, DOWN, buff=0.5)
        with self.voiceover(text="Here's a matching problem. We're given four black-body temperatures in List-one — "
                                 "two thousand, three thousand, five thousand and ten thousand kelvin — and five "
                                 "statements in List-two about their peak radiation. Using Wien's constant and h-c over "
                                 "e, match each temperature to the correct statement.") as t:
            self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.7)
            self.play(FadeIn(intro, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(listI, shift=RIGHT * 0.1), run_time=0.7)
            self.play(FadeIn(listII, shift=RIGHT * 0.1), run_time=0.7)
            self.play(FadeIn(const, shift=UP * 0.1), run_time=0.5)
            self.wait(max(0.2, t.duration - 5.6))
        self.play(FadeOut(head), FadeOut(intro), FadeOut(lists), FadeOut(const))

        # ============ 02 · PAUSE ============
        ring = Circle(radius=1.0, color=SIGNAL, stroke_width=5).move_to(UP * 0.2)
        num = Mono("5", color=SIGNAL).scale(1.4).move_to(ring)
        plbl = Label("PAUSE & ATTEMPT IT", color=WHITE).scale(0.55).next_to(ring, DOWN, buff=0.6)
        with self.voiceover(text="Pause, and try to match them yourself first.") as t:
            self.play(Create(ring), FadeIn(num), FadeIn(plbl), run_time=1.0)
            for k in ["4", "3", "2", "1"]:
                self.play(Transform(num, Mono(k, color=SIGNAL).scale(1.4).move_to(ring)), run_time=max(0.4, (t.duration-1.2)/4), rate_func=linear)
        self.play(FadeOut(ring), FadeOut(num), FadeOut(plbl))

        # ============ 03 · CONCEPT-FIRST ============
        head3 = Label("First — three ideas that crack this", color=WHITE).scale(0.58).to_edge(UP, buff=LOGO_CLEAR)

        def hump(cx, col, w=0.9, h=0.9):
            crv = VMobject(color=col, stroke_width=4)
            crv.set_points_smoothly([[cx-w, -0.5, 0], [cx-w*0.4, 0.1, 0], [cx, h-0.5, 0],
                                     [cx+w*0.5, 0.0, 0], [cx+w*1.3, -0.42, 0]])
            return crv
        # concept card 1 : Wien — hotter shifts the peak left
        w1 = hump(-0.45, EMBER); w2 = hump(0.35, IGNITION)
        vis1 = VGroup(w1, w2)
        c1 = VGroup(
            vis1,
            Label("WIEN'S LAW", color=IGNITION).scale(0.46),
            Body("hotter ⇒ shorter peak λ", color=TITANIUM).scale(0.34),
            MathTex(r"\lambda_{\text{peak}}=\dfrac{b}{T}", color=IGNITION).scale(0.56),
        ).arrange(DOWN, buff=0.24)
        # concept card 2 : Stefan — power scales as T^4
        bars = VGroup(*[Rectangle(width=0.22, height=hh, fill_color=SIGNAL, fill_opacity=0.8, stroke_width=0)
                        for hh in (0.3, 0.6, 1.05)]).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        c2 = VGroup(
            bars,
            Label("STEFAN'S LAW", color=SIGNAL).scale(0.46),
            Body("emitted power per area", color=TITANIUM).scale(0.34),
            MathTex(r"\dfrac{P}{A}=\sigma T^{4}", color=SIGNAL).scale(0.56),
        ).arrange(DOWN, buff=0.24)
        # concept card 3 : photoemission threshold
        arrp = Arrow([-0.5, -0.15, 0], [0.5, 0.15, 0], color=EMBER, stroke_width=4, buff=0, tip_length=0.16)
        dote = Dot([0.6, 0.2, 0], color=CORRECT).scale(0.7)
        vis3 = VGroup(arrp, dote)
        c3 = VGroup(
            vis3,
            Label("PHOTOEMISSION", color=EMBER).scale(0.46),
            Body("needs enough energy", color=TITANIUM).scale(0.34),
            MathTex(r"\lambda \le \dfrac{hc}{e\phi}", color=EMBER).scale(0.56),
        ).arrange(DOWN, buff=0.24)
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.95).next_to(head3, DOWN, buff=0.7)
        with self.voiceover(text="Before the numbers, three ideas. First, Wien's law: the peak wavelength equals b over "
                                 "T, so a hotter body peaks at a shorter wavelength — the whole curve slides left.") as t:
            self.play(Write(head3), run_time=0.8)
            self.play(FadeIn(c1, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration-1.8))
        with self.voiceover(text="Second, Stefan's law: the power radiated per unit area goes as T to the fourth, so "
                                 "temperature ratios turn into fourth-power ratios of power.") as t:
            self.play(FadeIn(c2, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration-1.0))
        with self.voiceover(text="Third, photoemission: to eject an electron the peak wavelength must be short enough — "
                                 "at or below h-c over e times the work function.") as t:
            self.play(FadeIn(c3, shift=UP*0.15), run_time=1.0)
            self.wait(max(0.1, t.duration-1.0))
        self.play(FadeOut(head3), FadeOut(cards))

        # ============ 04 · GROUNDWORK ============
        head4 = kicker("", "THE GROUNDWORK").to_edge(UP, buff=LOGO_CLEAR)
        g = VGroup(
            MathTex(r"\lambda_{\text{peak}}=\dfrac{b}{T},\quad b=2.9\times10^{-3}\ \mathrm{m\,K}", color=IGNITION).scale(0.58),
            MathTex(r"\text{Visible band: } 400\ \mathrm{nm}\ \text{to}\ 700\ \mathrm{nm}", color=WHITE).scale(0.58),
            MathTex(r"\dfrac{P}{A}\propto T^{4}\ \ (\text{Stefan})", color=SIGNAL).scale(0.58),
            MathTex(r"\text{Photoemission: } \lambda \le \dfrac{hc}{e\phi},\quad \dfrac{hc}{e}=1.24\times10^{-6}\ \mathrm{V\,m}", color=WHITE).scale(0.54),
        ).arrange(DOWN, buff=0.40).next_to(head4, DOWN, buff=0.6)
        with self.voiceover(text="Set the groundwork. Wien's law with b equal to two point nine times ten to the minus "
                                 "three. The visible band runs from about four hundred to seven hundred nanometres. Stefan's "
                                 "power per area goes as T to the fourth. And photoemission needs the wavelength at or below "
                                 "h-c over e phi, with h-c over e equal to one point two four microvolt-metres.") as t:
            self.play(FadeIn(head4), run_time=0.4)
            for line in g:
                self.play(Write(line), run_time=1.0)
            self.wait(max(0.1, t.duration - 4.4))
        self.play(FadeOut(head4), FadeOut(g))

        # ============ 05 · LIVE VISUAL — black-body spectra shifting LEFT as T rises ============
        head5 = Label("Peaks shift left as T rises", color=WHITE).scale(0.5).to_edge(UP, buff=LOGO_CLEAR)

        Ox, Oy = -5.0, -2.3
        AX_W, AX_H = 8.4, 3.6
        def AX(x, y): return np.array([Ox + x, Oy + y, 0])
        lax = Arrow(AX(0, 0), AX(AX_W, 0), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.16)
        iax = Arrow(AX(0, 0), AX(0, AX_H), color=TITANIUM, stroke_width=3, buff=0, tip_length=0.16)
        lax_lbl = Mono("λ (nm)", color=TITANIUM).scale(0.4).next_to(lax, RIGHT, buff=0.1)
        iax_lbl = Mono("intensity", color=TITANIUM).scale(0.36).next_to(iax, UP, buff=0.1)

        # map wavelength (nm) -> x on axis; smaller λ (hotter) sits further LEFT.
        LMAX = 1600.0
        def wx(nm):  # nm 0..1600 -> 0.4..AX_W-0.4
            return 0.4 + (nm / LMAX) * (AX_W - 0.9)
        # each body: (temp, peak_nm, colour, tag). Amplitude ~ T^4 but clamped so curves fit the box.
        bodies = [
            (2000, 1450, EMBER,    "P"),
            (3000, 967,  IGNITION, "Q"),
            (5000, 580,  CORRECT,  "R"),
            (10000, 290, SIGNAL,   "S"),
        ]
        amps = [1.35, 1.9, 2.6, 3.1]
        def spectrum(peak_nm, amp, col):
            px = wx(peak_nm)
            left = wx(max(30.0, peak_nm * 0.35))
            right = wx(min(LMAX, peak_nm * 3.0))
            crv = VMobject(color=col, stroke_width=4)
            crv.set_points_smoothly([
                AX(left, 0.02),
                AX(px - (px-left)*0.45, amp*0.55),
                AX(px, amp),
                AX(px + (right-px)*0.35, amp*0.5),
                AX(right, 0.04),
            ])
            return crv

        curves, peakdots, peaklabs, tlabs = [], [], [], []
        for (T, pk, col, tag), amp in zip(bodies, amps):
            crv = spectrum(pk, amp, col)
            pd = Dot(AX(wx(pk), amp), color=col).scale(0.6)
            plb = Mono(f"{pk} nm", color=col).scale(0.30).next_to(pd, UP, buff=0.08)
            tlb = Mono(f"{tag}: {T} K", color=col).scale(0.30)
            curves.append(crv); peakdots.append(pd); peaklabs.append(plb); tlabs.append(tlb)
        legend = VGroup(*tlabs).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_corner(UR, buff=0.6).shift(DOWN*0.9)
        visual = VGroup(lax, iax, lax_lbl, iax_lbl, *curves, *peakdots, *peaklabs, legend)

        with self.voiceover(text="Now watch the spectra. Here's wavelength across the bottom, intensity up the side. As "
                                 "the temperature climbs from two thousand to ten thousand kelvin, the whole hump grows "
                                 "taller and its peak marches to the left — toward shorter wavelengths.") as t:
            self.play(Create(lax), Create(iax), FadeIn(lax_lbl), FadeIn(iax_lbl), run_time=1.0)
            for i in range(4):
                self.play(Create(curves[i]), FadeIn(peakdots[i]), FadeIn(peaklabs[i]),
                          FadeIn(tlabs[i], shift=LEFT*0.1), run_time=0.9)
            self.wait(max(0.1, t.duration - 4.6))
        with self.voiceover(text="So P at two thousand kelvin peaks in the infrared at fourteen fifty nanometres; Q near "
                                 "the infrared at nine sixty-seven; R right in the visible at five eighty; and S deep in the "
                                 "ultraviolet at two ninety.") as t:
            self.wait(max(0.2, t.duration))

        # dock bottom-right
        self.play(FadeOut(head5), visual.animate.scale(0.4).to_corner(DR, buff=0.4), run_time=1.0)

        # ============ 06 · STEP RAIL + DETAILED SOLVE ============
        rail = StepRail(5, top=1.5, gap=0.86, size=0.56)
        self.play(FadeIn(rail.whole()), rail.active(0), run_time=0.7)

        # STEP 1 — peak wavelengths
        s1t = Label("STEP 1 — peak wavelengths via λ = b/T", color=WHITE).scale(0.42).move_to(WORKC + UP*2.05)
        s1a = MathTex(r"\lambda_{\text{peak}}=\dfrac{b}{T}=\dfrac{2.9\times10^{-3}}{T}", color=WHITE).scale(0.54).move_to(WORKC + UP*0.9)
        s1b = MathTex(r"P{:}\,1450,\ \ Q{:}\,967,\ \ R{:}\,580,\ \ S{:}\,290\ \ (\mathrm{nm})", color=IGNITION).scale(0.50).move_to(WORKC + DOWN*0.4)
        s1c = MathTex(r"\text{IR}\ \to\ \text{near-IR}\ \to\ \text{visible}\ \to\ \text{UV}", color=SIGNAL).scale(0.5).move_to(WORKC + DOWN*1.4)
        with self.voiceover(text="Step one. Divide b by each temperature. P gives fourteen hundred fifty nanometres, "
                                 "Q gives nine sixty-seven, R gives five eighty, and S gives two ninety. That's infrared, "
                                 "near-infrared, visible, and ultraviolet, in order.") as t:
            self.play(FadeIn(s1t), Write(s1a), run_time=min(1.8, t.duration))
            self.play(Write(s1b), run_time=1.2)
            self.play(Write(s1c), run_time=1.0)
            add_result(r"\lambda_P=1450,\ \lambda_S=290", SIGNAL)
            self.wait(max(0.1, t.duration - 4.0))
        self.play(FadeOut(s1t), FadeOut(s1a), FadeOut(s1b), FadeOut(s1c), rail.done(0), rail.active(1))

        # STEP 2 — P -> 3 widest central max
        s2t = Label("STEP 2 — widest single-slit central max", color=WHITE).scale(0.42).move_to(WORKC + UP*2.05)
        s2a = MathTex(r"\text{Central max width}\ \propto \lambda", color=WHITE).scale(0.56).move_to(WORKC + UP*0.9)
        s2b = MathTex(r"\text{Largest } \lambda = 1450\ \mathrm{nm}\ (P)", color=WHITE).scale(0.54).move_to(WORKC + DOWN*0.2)
        s2c = MathTex(r"\Rightarrow\ P \to 3\ \checkmark", color=CORRECT).scale(0.62).move_to(WORKC + DOWN*1.3)
        with self.voiceover(text="Step two. The width of a single-slit central maximum is proportional to wavelength, so "
                                 "the widest one comes from the longest peak wavelength. That's P at fourteen fifty "
                                 "nanometres. So P matches statement three.") as t:
            self.play(FadeIn(s2t), Write(s2a), run_time=min(1.8, t.duration))
            self.play(Write(s2b), run_time=1.1)
            self.play(Write(s2c), run_time=0.9)
            add_result(r"P \to 3", CORRECT)
            self.wait(max(0.1, t.duration - 4.0))
        self.play(FadeOut(s2t), FadeOut(s2a), FadeOut(s2b), FadeOut(s2c), rail.done(1), rail.active(2))

        # STEP 3 — Q -> 4 Stefan ratio
        s3t = Label("STEP 3 — power ratio 1/16 vs 6000 K", color=WHITE).scale(0.42).move_to(WORKC + UP*2.05)
        s3a = MathTex(r"\dfrac{P/A}{(P/A)_{6000}}=\left(\dfrac{T}{6000}\right)^{4}=\dfrac{1}{16}", color=WHITE).scale(0.52).move_to(WORKC + UP*0.8)
        s3b = MathTex(r"\left(\dfrac{T}{6000}\right)=\left(\dfrac{1}{16}\right)^{1/4}=\dfrac{1}{2}\ \Rightarrow\ T=3000\ \mathrm{K}", color=WHITE).scale(0.5).move_to(WORKC + DOWN*0.4)
        s3c = MathTex(r"\Rightarrow\ Q \to 4\ \checkmark", color=CORRECT).scale(0.62).move_to(WORKC + DOWN*1.4)
        with self.voiceover(text="Step three. Stefan's law: the power ratio is the fourth power of the temperature ratio. "
                                 "Setting that to one-sixteenth, the fourth root of one-sixteenth is one-half, so T is half "
                                 "of six thousand — three thousand kelvin. That's Q, so Q matches statement four.") as t:
            self.play(FadeIn(s3t), Write(s3a), run_time=min(2.0, t.duration))
            self.play(Write(s3b), run_time=1.2)
            self.play(Write(s3c), run_time=0.9)
            add_result(r"Q \to 4", CORRECT)
            self.wait(max(0.1, t.duration - 4.1))
        self.play(FadeOut(s3t), FadeOut(s3a), FadeOut(s3b), FadeOut(s3c), rail.done(2), rail.active(3))

        # STEP 4 — R -> 2 visible
        s4t = Label("STEP 4 — which peak is visible", color=WHITE).scale(0.42).move_to(WORKC + UP*2.05)
        s4a = MathTex(r"\text{Visible: } 400\ \mathrm{nm} \le \lambda \le 700\ \mathrm{nm}", color=WHITE).scale(0.54).move_to(WORKC + UP*0.8)
        s4b = MathTex(r"\lambda_R = 580\ \mathrm{nm}\ \in\ [400,700]", color=WHITE).scale(0.54).move_to(WORKC + DOWN*0.3)
        s4c = MathTex(r"\Rightarrow\ R \to 2\ \checkmark", color=CORRECT).scale(0.62).move_to(WORKC + DOWN*1.4)
        with self.voiceover(text="Step four. The visible band runs from four hundred to seven hundred nanometres. Only "
                                 "R, at five hundred eighty nanometres, falls inside it. So R matches statement two.") as t:
            self.play(FadeIn(s4t), Write(s4a), run_time=min(1.8, t.duration))
            self.play(Write(s4b), run_time=1.1)
            self.play(Write(s4c), run_time=0.9)
            add_result(r"R \to 2", CORRECT)
            self.wait(max(0.1, t.duration - 3.8))
        self.play(FadeOut(s4t), FadeOut(s4a), FadeOut(s4b), FadeOut(s4c), rail.done(3), rail.active(4))

        # STEP 5 — S -> 1 photoemission
        s5t = Label("STEP 5 — photoelectrons from a 4 eV metal", color=WHITE).scale(0.40).move_to(WORKC + UP*2.05)
        s5a = MathTex(r"\lambda \le \dfrac{hc}{e\phi}=\dfrac{1.24\times10^{-6}}{4}=310\ \mathrm{nm}", color=WHITE).scale(0.52).move_to(WORKC + UP*0.8)
        s5b = MathTex(r"\text{Only } \lambda_S = 290\ \mathrm{nm} \le 310\ \mathrm{nm}", color=WHITE).scale(0.52).move_to(WORKC + DOWN*0.3)
        s5c = MathTex(r"\Rightarrow\ S \to 1\ \checkmark", color=CORRECT).scale(0.62).move_to(WORKC + DOWN*1.4)
        with self.voiceover(text="Step five. To eject electrons from a four electron-volt metal, the wavelength must be at "
                                 "or below h-c over e times four — that's three hundred ten nanometres. Only S, at two "
                                 "ninety, clears that threshold. So S matches statement one.") as t:
            self.play(FadeIn(s5t), Write(s5a), run_time=min(2.0, t.duration))
            self.play(Write(s5b), run_time=1.1)
            self.play(Write(s5c), run_time=0.9)
            add_result(r"S \to 1", CORRECT)
            self.wait(max(0.1, t.duration - 4.1))
        self.play(FadeOut(s5t), FadeOut(s5a), FadeOut(s5b), FadeOut(s5c), rail.done(4))

        # ============ 07 · LOCK-IN ============
        matches = MathTex(r"P\to 3,\quad Q\to 4,\quad R\to 2,\quad S\to 1", color=WHITE).scale(0.58).move_to(WORKC + UP*0.7)
        ans = Label("ANSWER:   (C)   P→3, Q→4, R→2, S→1", color=IGNITION).scale(0.62).move_to(WORKC + DOWN*0.7)
        box = SurroundingRectangle(ans, color=CORRECT, buff=0.28, corner_radius=0.1)
        with self.voiceover(text="Collect the matches: P to three, Q to four, R to two, S to one.") as t:
            self.play(Write(matches), run_time=min(2.0, t.duration))
            self.wait(max(0.1, t.duration - 2.0))
        with self.voiceover(text="That's option C. Wien's law sorts the peaks, Stefan handles the power, and the "
                                 "photoemission threshold pins down S. Solved, completely.") as t:
            self.play(FadeIn(ans, shift=UP*0.1), run_time=0.9)
            self.play(Create(box), run_time=0.8)
            self.wait(max(0.3, t.duration - 1.7))
        self.wait(0.6)
