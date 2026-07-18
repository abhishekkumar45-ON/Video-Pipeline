"""
Orange Nelumbo · PYQ MASTERCLASS · Thermodynamics · t1 — "Adiabatic + isobaric cycle"
JEE Advanced 2025 · Paper 2 · Numerical.  Answer: Q_XY = 1.6 J.

The FULL masterclass lesson (question card · attempt pause · decode+agenda · concept block C1
adiabatic-law · concept block C2 constant-pressure+heat · guard carrybacks · how-JEE-varies-this ·
30-second read · one-screen recap) — with the requested VISUALISATION improvements layered in,
nothing removed:
  · the graph is DRAWN with animation next to a piston; givens are LaTeX (V_X = 64 …)
  · NO dark panel/agenda boxes — teaching sits on the clean background
  · each concept block SHOWS the physics on a small piston (expands / cools / heat-in)
  · the SOLUTION is a LIVE RIG: piston (left) + V-T graph (centre) + live V,T readouts (top),
    the 4 steps dock TOP-RIGHT and appear as each leg physically animates
  · captions capped to <= 2 lines (max_subcaption_len = 34)
"""
from manim import *
from nelumbo import *
from manim_voiceover import VoiceoverScene
from voice import narration_service

K = 8.0 / 1080.0
def UX(px): return (px - 960) * K
def UY(px): return (540 - px) * K
CAP_TOP = UY(905)
PANEL_C = -0.35
GUARD = "#F2B21C"


class Scene_t1(VoiceoverScene):
    def construct(self):
        background(self)
        self.set_speech_service(narration_service(kokoro_voice="af_bella"))

        from pathlib import Path
        badge = ImageMobject(str(Path("assets/on_logo.png").resolve())); badge.height = 0.5
        badge.move_to([UX(150), UY(140), 0]); self.add(badge)

        # captions <= 2 lines: cap every subcaption chunk (M=34 -> worst cue ~38 chars)
        def vo(text):
            return self.voiceover(text=text, max_subcaption_len=34)

        # ---------------- helpers ----------------
        def chip(txt, fill=False, col=EMBER):
            t = Mono(txt, color=(OBSIDIAN if fill else col)).scale(0.3)
            box = SurroundingRectangle(t, color=col, fill_color=col,
                                       fill_opacity=1 if fill else 0.0, buff=0.12, corner_radius=0.05, stroke_width=2)
            return VGroup(box, t)

        def fitw(mob, w):
            if mob.width > w: mob.scale_to_fit_width(w)
            return mob

        # piston-cylinder primitives (shared by concept minis and the solution rig)
        def walls_of(cx, by, fh, cw):
            m = VMobject(stroke_color=TITANIUM, stroke_width=4)
            m.set_points_as_corners([[cx-cw/2, by+fh+0.45, 0], [cx-cw/2, by, 0],
                                     [cx+cw/2, by, 0], [cx+cw/2, by+fh+0.45, 0]])
            return m
        def gas_rect(vol, col, cx, by, fh, cw):
            h = vol*fh
            return Rectangle(width=cw-0.06, height=h, fill_color=col, fill_opacity=0.30, stroke_width=0).move_to([cx, by+h/2, 0])
        def piston_g(vol, cx, by, fh, cw):
            h = vol*fh
            bar = Rectangle(width=cw+0.14, height=0.12, fill_color=TITANIUM, fill_opacity=1, stroke_width=0).move_to([cx, by+h+0.05, 0])
            rod = Rectangle(width=0.11, height=0.36, fill_color=TITANIUM, fill_opacity=1, stroke_width=0).move_to([cx, by+h+0.05+0.24, 0])
            return VGroup(bar, rod)

        # borderless guard carryback (amber text + thin amber rule — NO dark box)
        def guard_card(text_str, src):
            head = Mono(src + " · GUARD", color=GUARD).scale(0.26)
            body = Body(text_str, color=WHITE).scale(0.3); fitw(body, 2.7)
            txt = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            rule = Rectangle(width=0.06, height=txt.height+0.06, fill_color=GUARD, fill_opacity=1, stroke_width=0)
            rule.next_to(txt, LEFT, buff=0.16)
            return VGroup(rule, txt)

        # V-T cycle diagram (question card) — returned in parts so it can be DRAWN in stages
        def vtdiag(scale=1.0):
            ox, oy = -1.55, -1.35
            def P(T, V): return np.array([ox + T * 0.92, oy + V * 1.28, 0])
            xax = Arrow(P(0, 0), P(3.15, 0), buff=0, stroke_width=3, color=TITANIUM, tip_length=0.16)
            yax = Arrow(P(0, 0), P(0, 2.45), buff=0, stroke_width=3, color=TITANIUM, tip_length=0.16)
            xlab = MathTex("T", color=TITANIUM).scale(0.5).next_to(xax, RIGHT, buff=0.08)
            ylab = MathTex("V", color=TITANIUM).scale(0.5).next_to(yax, UP, buff=0.06)
            W, X, Y, Z = P(1.0, 0.85), P(1.5, 0.90), P(2.85, 1.71), P(1.9, 1.62)
            rayA = Line(P(0, 0), P(2.45, 2.08), color=TITANIUM, stroke_width=1.4).set_opacity(0.28)
            rayB = Line(P(0, 0), P(3.0, 1.80), color=TITANIUM, stroke_width=1.4).set_opacity(0.28)
            isoXY = Line(X, Y, color=SIGNAL, stroke_width=3.5)
            isoZW = Line(Z, W, color=SIGNAL, stroke_width=3.5)
            adiaWX = ArcBetweenPoints(W, X, angle=-0.55, color=EMBER, stroke_width=3.5)
            adiaYZ = ArcBetweenPoints(Y, Z, angle=-0.55, color=EMBER, stroke_width=3.5)
            def node(p, nm, dr):
                d = Dot(p, color=IGNITION, radius=0.065)
                return VGroup(d, MathTex(nm, color=WHITE).scale(0.5).next_to(d, dr, buff=0.07))
            axesg = VGroup(xax, yax, xlab, ylab, rayA, rayB)
            legsg = VGroup(adiaWX, isoXY, adiaYZ, isoZW)
            nodesg = VGroup(node(W, "W", DL), node(X, "X", DR), node(Y, "Y", UR), node(Z, "Z", UL))
            whole = VGroup(axesg, legsg, nodesg).scale(scale)
            return whole, axesg, legsg, nodesg

        # ================= SEG 2 · QUESTION CARD (graph DRAWN in stages + piston) =================
        chips = VGroup(chip("JEE ADVANCED", fill=True, col=IGNITION), chip("2025 · P2"),
                       chip("NUMERICAL"), chip("THERMODYNAMICS", col=TITANIUM)).arrange(RIGHT, buff=0.25)
        figw, faxes, flegs, fnodes = vtdiag(0.62)
        # small piston preview beside the graph
        pcx, pby, pfh, pcw = 0, -0.9, 1.7, 0.8
        pic = VGroup(walls_of(pcx, pby, pfh, pcw), gas_rect(0.45, IGNITION, pcx, pby, pfh, pcw),
                     piston_g(0.45, pcx, pby, pfh, pcw), Mono("gas", color=TITANIUM).scale(0.28).move_to([pcx, pby+0.4, 0]))
        figure = VGroup(pic, figw).arrange(RIGHT, buff=0.6)
        qtext = VGroup(
            Body("Monatomic ideal gas, cycle W-X-Y-Z of adiabatic + isobaric steps.", color=WHITE).scale(0.4),
            MathTex(r"V_W=64,\quad V_X=125,\quad V_Y=250\ \text{cm}^3", color=WHITE).scale(0.46),
            MathTex(r"nRT_W = 1\ \text{J}", color=SIGNAL).scale(0.46),
            MathTex(r"\text{Heat absorbed along } X\!\to\!Y\ ?", color=WHITE).scale(0.46),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        split = VGroup(figure, qtext).arrange(RIGHT, buff=0.7)
        find_q = MathTex(r"\text{Find } Q_{XY}", color=IGNITION).scale(0.5)
        find_b = SurroundingRectangle(find_q, color=IGNITION, buff=0.18, corner_radius=0.08, stroke_width=2, fill_opacity=0)
        find_g = VGroup(find_b, find_q)
        qbody = VGroup(chips, split, find_g).arrange(DOWN, buff=0.4).move_to([0, -0.32, 0])
        qborder = SurroundingRectangle(qbody, color=STEEL, buff=0.42, corner_radius=0.16, stroke_width=1.5, fill_opacity=0)
        with vo("J E E Advanced twenty twenty five, paper two. A monatomic gas runs a cycle.") as t:
            self.play(FadeIn(qborder), FadeIn(chips, shift=DOWN*0.1), run_time=0.6)
            self.play(FadeIn(pic, shift=RIGHT*0.1), run_time=0.6)
            self.play(Create(faxes), run_time=0.8)
            self.play(Create(flegs), run_time=1.2)
            self.play(FadeIn(fnodes, lag_ratio=0.2), run_time=0.9)
            self.wait(max(0.1, t.duration - 4.1))
        with vo("The steps alternate adiabatic and isobaric. The volumes at W, X, Y are given.") as t:
            for ln in qtext: self.play(FadeIn(ln, shift=UP*0.1), run_time=0.5)
            self.wait(max(0.1, t.duration - 2.0))
        with vo("With n R T at W equal to one joule, find the heat absorbed from X to Y.") as t:
            self.play(FadeIn(find_g, shift=UP*0.1), run_time=0.7); self.wait(max(0.1, t.duration - 0.7))

        # ================= SEG 3 · ATTEMPT PAUSE =================
        bar_bg = Rectangle(width=8.0, height=0.13, fill_color=STEEL, fill_opacity=1, stroke_width=0).move_to([0, CAP_TOP, 0])
        bar_fg = Rectangle(width=8.0, height=0.13, fill_color=SIGNAL, fill_opacity=1, stroke_width=0).move_to([0, CAP_TOP, 0]).align_to(bar_bg, LEFT)
        pdig = Mono("5", color=SIGNAL).scale(0.5).next_to(bar_bg, LEFT, buff=0.25)
        plbl = Mono("TRY IT FIRST", color=EMBER).scale(0.34).next_to(bar_bg, UP, buff=0.18)
        with vo("Pause here and try it first.") as t:
            self.play(FadeIn(bar_bg), FadeIn(bar_fg), FadeIn(pdig), FadeIn(plbl), run_time=0.6)
            stp = max(0.4, (t.duration-0.6)/5)
            for kk in ["4", "3", "2", "1", "0"]:
                self.play(bar_fg.animate.stretch_to_fit_width(8.0*int(kk)/5).align_to(bar_bg, LEFT),
                          Transform(pdig, Mono(kk, color=SIGNAL).scale(0.5).move_to(pdig)), run_time=stp, rate_func=linear)
        self.play(FadeOut(qborder), FadeOut(qbody), FadeOut(bar_bg), FadeOut(bar_fg), FadeOut(pdig), FadeOut(plbl))

        # ================= SEG 4 · DECODE + AGENDA (no boxes; LaTeX givens) =================
        g_title = Mono("GIVEN", color=SIGNAL).scale(0.32)
        givens = VGroup(
            MathTex(r"V_W = 64\ \text{cm}^3", color=WHITE).scale(0.5),
            MathTex(r"V_X = 125\ \text{cm}^3", color=WHITE).scale(0.5),
            MathTex(r"V_Y = 250\ \text{cm}^3", color=WHITE).scale(0.5),
            MathTex(r"nRT_W = 1\ \text{J},\quad \gamma = \tfrac53", color=SIGNAL).scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        gcol = VGroup(g_title, givens).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        f_title = Mono("FIND", color=IGNITION).scale(0.32)
        fbody = MathTex(r"Q_{XY}\ \ (X\!\to\!Y)", color=WHITE).scale(0.5)
        fcol = VGroup(f_title, fbody).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        a_title = Mono("PLAN", color=TITANIUM).scale(0.32)
        ag1 = VGroup(Dot(radius=0.09, color=EMBER), Mono("ADIABATIC →", color=WHITE).scale(0.3), MathTex(r"T_X", color=EMBER).scale(0.5)).arrange(RIGHT, buff=0.16)
        ag2 = VGroup(Dot(radius=0.09, color=SIGNAL), Mono("ISOBARIC →", color=WHITE).scale(0.3), MathTex(r"T_Y,\ Q", color=SIGNAL).scale(0.5)).arrange(RIGHT, buff=0.16)
        acol = VGroup(a_title, ag1, ag2).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        decode = VGroup(gcol, fcol, acol).arrange(RIGHT, buff=1.15, aligned_edge=UP).move_to([0, -0.15, 0])
        head3 = Mono("DECODE", color=EMBER).scale(0.34).to_edge(UP, buff=0.9)
        with vo("Read it cleanly. Three volumes, and n R T at W is one joule.") as t:
            self.play(FadeIn(head3), run_time=0.4)
            self.play(FadeIn(g_title), run_time=0.3)
            for gg in givens: self.play(FadeIn(gg, shift=RIGHT*0.08), run_time=0.4)
            self.wait(max(0.1, t.duration - 2.3))
        with vo("We want the heat from X to Y. The plan has two moves.") as t:
            self.play(FadeIn(fcol, shift=RIGHT*0.1), run_time=0.7); self.wait(max(0.1, t.duration - 0.7))
        with vo("Adiabatic gives T X. Isobaric gives T Y and the heat.") as t:
            self.play(FadeIn(a_title), run_time=0.3)
            self.play(FadeIn(ag1, shift=LEFT*0.1), run_time=0.6)
            self.play(FadeIn(ag2, shift=LEFT*0.1), run_time=0.6)
            self.wait(max(0.1, t.duration - 1.5))
        self.play(FadeOut(head3), FadeOut(decode))

        # persistent left-side agenda (no box) + carryback stack
        ag_title = Mono("AGENDA", color=TITANIUM).scale(0.3)
        def ag_entry(txt):
            return VGroup(Circle(radius=0.1, color=TITANIUM, stroke_width=3), Mono(txt, color=TITANIUM).scale(0.28)).arrange(RIGHT, buff=0.16)
        agA = ag_entry("ADIABATIC"); agB = ag_entry("ISOBARIC")
        agenda = VGroup(ag_title, agA, agB).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(LEFT, buff=0.5).shift(UP*1.4)
        strip = VGroup(Mono("GIVEN", color=SIGNAL).scale(0.26),
                       MathTex(r"V=64,125,250,\ nRT_W=1\,\text{J}", color=TITANIUM).scale(0.32),
                       Mono("· FIND", color=IGNITION).scale(0.26),
                       MathTex(r"Q_{XY}", color=TITANIUM).scale(0.32)).arrange(RIGHT, buff=0.26).to_edge(UP, buff=0.42)
        self.play(FadeIn(agenda), FadeIn(strip), run_time=0.5)

        self.cbacks = []
        def carryback(text_str, src):
            cb = guard_card(text_str, src)
            cb.to_edge(LEFT, buff=0.5).shift(DOWN*(0.6 + 1.15*len(self.cbacks)))
            self.cbacks.append(cb); return cb
        def base_dim(op):
            return [m.animate.set_opacity(op) for m in ([agenda, strip] + self.cbacks)]

        # ---------------- concept-block machinery (NO dark panel) ----------------
        def phase_rail():
            names = ["REACT", "RESULTS", "EDGES", "JEE"]
            items = VGroup()
            for n in names:
                tx = Mono(n, color=TITANIUM).scale(0.26)
                bx = RoundedRectangle(width=tx.width + 0.3, height=tx.height + 0.22, corner_radius=0.06,
                                      stroke_color=STEEL, stroke_width=1.5, fill_opacity=0).move_to(tx)
                items.add(VGroup(bx, tx))
            items.arrange(RIGHT, buff=0.22).move_to([PANEL_C, 1.7, 0]); return items
        def phase_to(rail, idx):
            a = []
            for i, ch in enumerate(rail):
                if i == idx:   a += [ch[0].animate.set_fill(IGNITION, 1).set_stroke(IGNITION, opacity=1), ch[1].animate.set_color(OBSIDIAN)]
                elif i < idx:  a += [ch[0].animate.set_fill(EMBER, 0.16).set_stroke(EMBER, opacity=1), ch[1].animate.set_color(EMBER)]
                else:          a += [ch[0].animate.set_fill(STEEL, 0).set_stroke(STEEL, opacity=1), ch[1].animate.set_color(TITANIUM)]
            return a
        def open_block(agdot, cnum):
            clabel = Mono(f"CONCEPT · C{cnum}", color=EMBER).scale(0.24).move_to([PANEL_C - 3.0, 1.7, 0])
            self.play(*base_dim(0.4), FadeIn(clabel), run_time=0.5)
            self.play(agdot[0].animate.set_stroke(IGNITION, width=3, opacity=1).set_fill(IGNITION, 1), run_time=0.35)
            self._chrome = VGroup(clabel); return clabel
        def close_block(rail, agdot):
            self.play(FadeOut(rail), FadeOut(self._chrome), *base_dim(1.0), run_time=0.6)
            self.play(agdot[0].animate.set_fill(CORRECT, 1).set_stroke(CORRECT, width=3, opacity=1), run_time=0.3)
        def bc(mob, y, w=6.4):
            fitw(mob, w); mob.move_to([PANEL_C, y, 0]); return mob

        # ================= MOTIVATION -> BLOCK C1 (adiabatic law) =================
        with vo("The heat we want is n C P times the temperature change from X to Y.") as t:
            mot = MathTex(r"Q_{XY}=nC_P\,\Delta T\ \Rightarrow\ \text{need } T_X,\ T_Y", color=WHITE).scale(0.56).move_to([PANEL_C, 0.3, 0])
            self.play(Write(mot), run_time=1.2); self.wait(max(0.1, t.duration - 1.2))
        self.play(FadeOut(mot))
        with vo("First, what do we know about an adiabatic process?") as t:
            clabel = open_block(agA, 1); rail = phase_rail()
            blk = bc(Label("The adiabatic law", color=IGNITION).scale(0.5), 1.05)
            self.play(FadeIn(rail), Write(blk), run_time=0.9)
            self.wait(max(0.1, t.duration - 1.6))
        # physical mini-piston (right) — adiabatic expansion cools the gas
        mcx, mby, mfh, mcw = 4.4, -1.35, 1.9, 0.8
        mwalls = walls_of(mcx, mby, mfh, mcw)
        mgas = gas_rect(0.35, EMBER, mcx, mby, mfh, mcw); mpist = piston_g(0.35, mcx, mby, mfh, mcw)
        q0 = Mono("Q = 0", color=IGNITION).scale(0.34).next_to(mwalls, UP, buff=0.18)
        tdrop = VGroup(MathTex(r"T\!\downarrow", color=EMBER).scale(0.5)).next_to(mwalls, DOWN, buff=0.2)
        noq = bc(MathTex(r"Q=0\ \Rightarrow\ TV^{\gamma-1}=\text{const}", color=IGNITION).scale(0.52), -0.15)
        self.play(*phase_to(rail, 0), run_time=0.3)
        with vo("An adiabatic process exchanges no heat. Expanding gas cools.") as t:
            self.play(FadeIn(mwalls), FadeIn(mgas), FadeIn(mpist), FadeIn(q0), run_time=0.7)
            self.play(Transform(mgas, gas_rect(0.7, EMBER, mcx, mby, mfh, mcw)),
                      Transform(mpist, piston_g(0.7, mcx, mby, mfh, mcw)), FadeIn(tdrop), run_time=1.4)
            self.play(Write(noq), run_time=1.0)
            self.wait(max(0.1, t.duration - 3.1))
        self.play(FadeOut(noq), *phase_to(rail, 1))
        r1 = bc(MathTex(r"T_W\,V_W^{\,2/3}=T_X\,V_X^{\,2/3},\quad \gamma-1=\tfrac23", color=WHITE).scale(0.5), 0.35)
        r2 = bc(MathTex(r"64^{2/3}=16,\ \ 125^{2/3}=25\ \Rightarrow\ T_X=\tfrac{16}{25}T_W", color=SIGNAL).scale(0.5), -0.55)
        with vo("Apply T V to the two thirds is constant across W to X. Sixty four gives sixteen, one twenty five gives twenty five. So T X is sixteen twenty-fifths of T W.") as t:
            self.play(Write(r1), run_time=1.3); self.play(Write(r2), run_time=1.3)
            self.wait(max(0.1, t.duration - 2.6))
        self.play(FadeOut(r1), FadeOut(r2), *phase_to(rail, 2))
        trap = bc(MathTex(r"\text{reflex: } V\propto T\ \text{on adiabatic}", color=EMBER).scale(0.5), 0.5)
        brk = bc(MathTex(r"\text{adiabatic uses } TV^{\gamma-1},\ \text{not } V\propto T", color=ERROR).scale(0.46), -0.2)
        with vo("The slip is to use volume proportional to temperature everywhere. That rule is only for constant pressure. On an adiabatic leg use T V to the gamma minus one.") as t:
            self.play(Write(trap), run_time=1.0); self.play(Write(brk), run_time=1.1)
            x1 = Cross(trap, stroke_color=ERROR, stroke_width=5); self.play(Create(x1), run_time=0.5)
            self.wait(max(0.1, t.duration - 2.6))
        jee = VGroup(Mono("JEE ANGLE", color=EMBER).scale(0.26), Body("Perfect powers 64, 125 flag the exponent.", color=WHITE).scale(0.34)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        jee.move_to([PANEL_C, -1.15, 0]); fitw(jee, 6.2)
        self.play(*phase_to(rail, 3))
        with vo("Examiners pick sixty four and one twenty five so the two thirds powers are clean.") as t:
            self.play(FadeIn(jee, shift=UP*0.1), run_time=1.0); self.wait(max(0.1, t.duration - 1.0))
        with vo("Back to our question, one line.") as t:
            self.play(FadeOut(blk), FadeOut(trap), FadeOut(brk), FadeOut(x1), FadeOut(jee),
                      FadeOut(mwalls), FadeOut(mgas), FadeOut(mpist), FadeOut(q0), FadeOut(tdrop), run_time=0.4)
            cb1 = carryback("Adiabatic: T V^(2/3) = const", "C1")
            close_block(rail, agA)
            self.play(FadeIn(cb1, shift=RIGHT*0.1), run_time=0.5)
            self.wait(max(0.1, t.duration - 1.5))

        # ================= BLOCK C2 (constant pressure + heat) =================
        with vo("Next, a constant pressure step and the heat in it.") as t:
            clabel2 = open_block(agB, 2); rail2 = phase_rail()
            blk2 = bc(Label("Constant pressure + heat", color=IGNITION).scale(0.5), 1.05)
            self.play(FadeIn(rail2), Write(blk2), run_time=0.9)
            self.wait(max(0.1, t.duration - 1.6))
        m2walls = walls_of(mcx, mby, mfh, mcw)
        m2gas = gas_rect(0.45, SIGNAL, mcx, mby, mfh, mcw); m2pist = piston_g(0.45, mcx, mby, mfh, mcw)
        harr = VGroup(*[Arrow([mcx-1.15, mby+0.3+0.5*i, 0], [mcx-0.55, mby+0.3+0.5*i, 0], buff=0, color=ERROR, stroke_width=3, tip_length=0.11) for i in range(3)])
        trise = MathTex(r"T\!\uparrow", color=SIGNAL).scale(0.5).next_to(m2walls, DOWN, buff=0.2)
        vt = bc(MathTex(r"P=\text{const}\ \Rightarrow\ \tfrac{V}{T}=\text{const}", color=IGNITION).scale(0.52), -0.15)
        self.play(*phase_to(rail2, 0), run_time=0.3)
        with vo("At constant pressure, volume over temperature is fixed. Heat flows in and the gas expands.") as t:
            self.play(FadeIn(m2walls), FadeIn(m2gas), FadeIn(m2pist), run_time=0.6)
            self.play(LaggedStart(*[GrowArrow(a) for a in harr], lag_ratio=0.3), run_time=0.7)
            self.play(Transform(m2gas, gas_rect(0.9, SIGNAL, mcx, mby, mfh, mcw)),
                      Transform(m2pist, piston_g(0.9, mcx, mby, mfh, mcw)), FadeIn(trise), run_time=1.3)
            self.play(Write(vt), run_time=0.9)
            self.wait(max(0.1, t.duration - 3.5))
        self.play(FadeOut(vt), *phase_to(rail2, 1))
        rr1 = bc(MathTex(r"\tfrac{V_X}{T_X}=\tfrac{V_Y}{T_Y}\ \Rightarrow\ T_Y=2T_X=\tfrac{32}{25}T_W", color=WHITE).scale(0.48), 0.35)
        rr2 = bc(MathTex(r"C_P=\tfrac52 R,\qquad Q=nC_P\,\Delta T", color=SIGNAL).scale(0.5), -0.55)
        with vo("V Y is twice V X, so T Y is twice T X, thirty two twenty-fifths of T W. And the heat is n C P delta T, with C P five halves R.") as t:
            self.play(Write(rr1), run_time=1.3); self.play(Write(rr2), run_time=1.2)
            self.wait(max(0.1, t.duration - 2.5))
        self.play(FadeOut(rr1), FadeOut(rr2), *phase_to(rail2, 2))
        trap2 = bc(MathTex(r"\text{reflex: use } C_V=\tfrac32 R", color=EMBER).scale(0.5), 0.5)
        brk2 = bc(MathTex(r"\text{const } P\Rightarrow\text{gas does work}\Rightarrow C_P", color=ERROR).scale(0.46), -0.2)
        with vo("The classic slip reaches for C V. At constant pressure the gas also does work, so you use C P, not C V.") as t:
            self.play(Write(trap2), run_time=1.0); self.play(Write(brk2), run_time=1.1)
            x2 = Cross(trap2, stroke_color=ERROR, stroke_width=5); self.play(Create(x2), run_time=0.5)
            self.wait(max(0.1, t.duration - 2.6))
        jee2 = VGroup(Mono("JEE ANGLE", color=EMBER).scale(0.26), Body("C_P vs C_V is the most-tested trap here.", color=WHITE).scale(0.34)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        jee2.move_to([PANEL_C, -1.15, 0]); fitw(jee2, 6.2)
        self.play(*phase_to(rail2, 3))
        with vo("Wrong heat capacity is the top mark-loser. Constant pressure means C P.") as t:
            self.play(FadeIn(jee2, shift=UP*0.1), run_time=1.0); self.wait(max(0.1, t.duration - 1.0))
        with vo("Now watch the whole cycle live.") as t:
            self.play(FadeOut(blk2), FadeOut(trap2), FadeOut(brk2), FadeOut(x2), FadeOut(jee2),
                      FadeOut(m2walls), FadeOut(m2gas), FadeOut(m2pist), FadeOut(harr), FadeOut(trise), run_time=0.4)
            cb2 = carryback("Constant-P heat uses C_P = 5/2 R", "C2")
            close_block(rail2, agB)
            self.play(FadeIn(cb2, shift=RIGHT*0.1), run_time=0.5)
            self.wait(max(0.1, t.duration - 1.5))

        # ================= SOLUTION · LIVE RIG (piston + graph + readouts + top-right steps) =================
        # the piston needs the left column, so retire the agenda + carrybacks here (guards return in the recap)
        self.play(FadeOut(agenda), FadeOut(strip), FadeOut(cb1), FadeOut(cb2), run_time=0.5)
        head4 = Mono("THE CYCLE, LIVE", color=EMBER).scale(0.34).to_edge(UP, buff=0.62)
        self.play(FadeIn(head4), run_time=0.35)

        CX, base_y, full_h, cw = -5.35, -2.35, 3.0, 1.25
        rig_walls = walls_of(CX, base_y, full_h, cw)
        vW, vX, vY = 64/250.0, 125/250.0, 250/250.0
        gas = gas_rect(vW, EMBER, CX, base_y, full_h, cw); pist = piston_g(vW, CX, base_y, full_h, cw)
        cyl_lbl = Mono("piston", color=TITANIUM).scale(0.3).next_to(rig_walls, DOWN, buff=0.16)

        Vtr = ValueTracker(64.0); Ttr = ValueTracker(1.00)
        def stat(name, tr, unit_mob, col, dec):
            lbl = Mono(name, color=TITANIUM).scale(0.42)
            n = DecimalNumber(tr.get_value(), num_decimal_places=dec, color=col, font_size=36, edge_to_fix=LEFT)
            n.add_updater(lambda m, tr=tr: m.set_value(tr.get_value()))
            grp = VGroup(lbl, n, unit_mob).arrange(RIGHT, buff=0.14)
            unit_mob.add_updater(lambda m, n=n: m.next_to(n, RIGHT, buff=0.14))
            return grp, n
        sV, nV = stat("V =", Vtr, Body("cm³", color=SIGNAL).scale(0.42), SIGNAL, 0)
        sT, nT = stat("T =", Ttr, MathTex(r"T_W", color=IGNITION).scale(0.5), IGNITION, 2)
        readout = VGroup(sV, sT).arrange(RIGHT, buff=0.8).move_to([-2.7, 2.05, 0])

        Ox, Oy = -3.5, -2.45
        def GP(T, V): return np.array([Ox + T*1.85, Oy + V*0.0130, 0])
        vax = Arrow(GP(0, 0), GP(2.2, 0), buff=0, stroke_width=3, color=TITANIUM, tip_length=0.15)
        pax = Arrow(GP(0, 0), GP(0, 265), buff=0, stroke_width=3, color=TITANIUM, tip_length=0.15)
        vlab = MathTex("T", color=TITANIUM).scale(0.5).next_to(vax, RIGHT, buff=0.07)
        plab = MathTex("V", color=TITANIUM).scale(0.5).next_to(pax, UP, buff=0.05)
        Wp, Xp, Yp = GP(1.0, 64), GP(0.64, 125), GP(1.28, 250)
        rayW = DashedLine(GP(0, 0), GP(1.2, 76.8), color=TITANIUM, stroke_width=1.3).set_opacity(0.28)
        rayX = DashedLine(GP(0, 0), GP(1.35, 264), color=TITANIUM, stroke_width=1.3).set_opacity(0.28)
        dW = Dot(Wp, color=WHITE, radius=0.06); lW = MathTex("W", color=WHITE).scale(0.46).next_to(dW, DR, buff=0.05)
        dX = Dot(Xp, color=WHITE, radius=0.06); lX = MathTex("X", color=WHITE).scale(0.46).next_to(dX, LEFT, buff=0.06)
        dY = Dot(Yp, color=WHITE, radius=0.06); lY = MathTex("Y", color=WHITE).scale(0.46).next_to(dY, UP, buff=0.06)
        gaxes = VGroup(vax, pax, vlab, plab, rayW, rayX)
        moving = Dot(Wp, color=IGNITION, radius=0.10)

        def stepcard(num, eq_latex, sc=0.44):
            b = VGroup(RoundedRectangle(width=0.44, height=0.44, corner_radius=0.08, stroke_color=IGNITION,
                                        stroke_width=2, fill_color=IGNITION, fill_opacity=0.15),
                       Mono(str(num), color=IGNITION).scale(0.34))
            return VGroup(b, MathTex(eq_latex, color=WHITE).scale(sc)).arrange(RIGHT, buff=0.2, aligned_edge=UP)
        s1 = stepcard(1, r"W\!\to\!X\ \text{adiab.},\ X\!\to\!Y\ \text{isob.}", 0.34)
        s2 = stepcard(2, r"T_X=\tfrac{16}{25}T_W", 0.46)
        s3 = stepcard(3, r"T_Y=2T_X=\tfrac{32}{25}T_W", 0.42)
        s4 = stepcard(4, r"Q_{XY}=\tfrac52 nR\,(T_Y-T_X)", 0.42)
        stepcol = VGroup(s1, s2, s3, s4).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_corner(UR, buff=0.55).shift(DOWN*0.35)
        steps_lbl = Mono("SOLUTION", color=EMBER).scale(0.28).next_to(stepcol, UP, buff=0.25).align_to(stepcol, LEFT)
        ansm = MathTex(r"Q_{XY}=\tfrac{8}{5}(nRT_W)=1.6\ \text{J}", color=CORRECT).scale(0.5)
        abox = SurroundingRectangle(ansm, color=CORRECT, buff=0.2, corner_radius=0.1, stroke_width=2.5, fill_opacity=0)
        answer = VGroup(abox, ansm).next_to(stepcol, DOWN, buff=0.5).align_to(stepcol, RIGHT)

        with vo("Gas in a cylinder on the left, the V-T graph in the centre.") as t:
            self.play(Create(rig_walls), FadeIn(gas), FadeIn(pist), FadeIn(cyl_lbl), run_time=1.0)
            self.play(Create(gaxes), run_time=1.0)
            self.play(FadeIn(dW), FadeIn(lW), FadeIn(moving), FadeIn(readout, shift=DOWN*0.1), run_time=0.8)
            self.wait(max(0.1, t.duration - 2.8))
        with vo("We start at W. Volume sixty four, temperature one T W.") as t:
            self.play(FadeIn(steps_lbl), FadeIn(s1, shift=LEFT*0.1), run_time=0.8)
            self.wait(max(0.1, t.duration - 0.8))

        head4b = Mono("ADIABATIC  W → X   (no heat)", color=EMBER).scale(0.34).move_to(head4)
        adWX = VMobject(color=EMBER, stroke_width=4); adWX.set_points_smoothly([Wp, GP(0.80, 92), Xp])
        with vo("First leg is adiabatic. The gas expands and cools.") as t:
            self.play(Transform(head4, head4b), run_time=0.5)
            self.play(Vtr.animate.set_value(125), Ttr.animate.set_value(0.64),
                      Transform(gas, gas_rect(vX, EMBER, CX, base_y, full_h, cw)), Transform(pist, piston_g(vX, CX, base_y, full_h, cw)),
                      MoveAlongPath(moving, adWX), Create(adWX), run_time=min(3.0, max(1.8, t.duration-1.0)))
            self.play(FadeIn(dX), FadeIn(lX), run_time=0.4)
            self.wait(max(0.1, t.duration - 3.5))
        with vo("By T V to the two thirds, T X is sixteen twenty-fifths of T W.") as t:
            self.play(FadeIn(s2, shift=LEFT*0.1), run_time=0.8); self.wait(max(0.1, t.duration - 0.8))

        head4c = Mono("ISOBARIC  X → Y   (heat in)", color=SIGNAL).scale(0.34).move_to(head4)
        isoXY = Line(Xp, Yp, color=SIGNAL, stroke_width=4)
        arrows = VGroup(*[Arrow(GP(0.30, 40+40*i), GP(0.44, 40+40*i), buff=0, color=ERROR, stroke_width=3, tip_length=0.12) for i in range(3)])
        with vo("Second leg is isobaric. Heat flows in.") as t:
            self.play(Transform(head4, head4c), run_time=0.5)
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=0.7)
            self.wait(max(0.1, t.duration - 1.2))
        with vo("Volume doubles to two fifty, so the temperature doubles too.") as t:
            self.play(Vtr.animate.set_value(250), Ttr.animate.set_value(1.28),
                      Transform(gas, gas_rect(vY, SIGNAL, CX, base_y, full_h, cw)), Transform(pist, piston_g(vY, CX, base_y, full_h, cw)),
                      MoveAlongPath(moving, isoXY), Create(isoXY), run_time=min(3.0, max(1.8, t.duration-0.7)))
            self.play(FadeIn(dY), FadeIn(lY), run_time=0.4)
            self.wait(max(0.1, t.duration - 3.5))
        with vo("So T Y is thirty two twenty-fifths of T W.") as t:
            self.play(FadeIn(s3, shift=LEFT*0.1), run_time=0.8); self.wait(max(0.1, t.duration - 0.8))
        with vo("At constant pressure the heat is five halves n R delta T.") as t:
            self.play(FadeIn(s4, shift=LEFT*0.1), run_time=0.8); self.wait(max(0.1, t.duration - 0.8))
        self.play(FadeOut(arrows), run_time=0.3)

        with vo("The rise is sixteen twenty-fifths of T W, so the heat is eight fifths of n R T W. That is one point six joules.") as t:
            self.play(Indicate(s2[1], color=IGNITION), Indicate(s3[1], color=IGNITION), run_time=1.0)
            for n in (nV, nT): n.clear_updaters()
            self.play(FadeIn(ansm, shift=UP*0.1), Create(abox), run_time=1.0)
            self.wait(max(0.1, t.duration - 2.0))
        self.wait(0.4)
        rig = VGroup(rig_walls, gas, pist, cyl_lbl, readout, gaxes, adWX, isoXY,
                     dW, dX, dY, lW, lX, lY, moving)
        self.play(FadeOut(rig), FadeOut(head4), FadeOut(steps_lbl), FadeOut(stepcol), FadeOut(answer), run_time=0.7)

        # ================= SEG 6 · HOW JEE VARIES THIS (borderless) =================
        vhead = Mono("HOW JEE VARIES THIS", color=EMBER).scale(0.34).to_edge(UP, buff=0.9)
        def vrow(txt):
            return VGroup(Dot(radius=0.07, color=EMBER), Body(txt, color=TITANIUM).scale(0.42)).arrange(RIGHT, buff=0.22)
        vs = VGroup(vrow("Diatomic gas → γ = 7/5, C_P = 7/2 R"),
                    vrow("Ask heat along an adiabatic leg (it is zero)"),
                    vrow("Ask the net work over the whole cycle"),
                    vrow("Give the temperatures, ask for a volume")).arrange(DOWN, aligned_edge=LEFT, buff=0.34).next_to(vhead, DOWN, buff=0.55)
        with vo("Expect the same cycle worn four ways. Diatomic gas changes gamma and C P. Heat on an adiabatic leg is zero. Or they ask net work, or a volume from temperatures.") as t:
            self.play(FadeIn(vhead), run_time=0.5)
            for v in vs: self.play(FadeIn(v, shift=RIGHT*0.1), run_time=0.55)
            self.wait(max(0.1, t.duration - 2.7))
        self.play(FadeOut(vhead), FadeOut(vs))

        # ================= SEG 7 · THE 30-SECOND READ (borderless) =================
        chead = Mono("THE 30-SECOND READ", color=EMBER).scale(0.34).to_edge(UP, buff=0.85)
        def cell(tag, body):
            return VGroup(Mono(tag, color=EMBER).scale(0.26), body).arrange(DOWN, buff=0.16)
        cells = VGroup(cell("ADIABATIC", MathTex(r"T_X=\tfrac{16}{25}T_W", color=SIGNAL).scale(0.42)),
                       cell("ISOBARIC", MathTex(r"T_Y=\tfrac{32}{25}T_W", color=SIGNAL).scale(0.42)),
                       cell("Δ T", MathTex(r"\tfrac{16}{25}T_W", color=SIGNAL).scale(0.44)),
                       cell("ANSWER", MathTex(r"1.6\,\text{J}", color=CORRECT).scale(0.46))).arrange(RIGHT, buff=0.7).next_to(chead, DOWN, buff=0.7)
        arows = VGroup(*[MathTex(r"\rightarrow", color=TITANIUM).scale(0.5) for _ in range(3)])
        for i, a in enumerate(arows): a.move_to((cells[i].get_right() + cells[i+1].get_left())/2)
        sanity = VGroup(Mono("SANITY", color=CORRECT).scale(0.26), Body("Only the isobaric leg absorbs heat; 8/5 is clean. ✓", color=WHITE).scale(0.34)).arrange(RIGHT, buff=0.25).next_to(cells, DOWN, buff=0.8)
        with vo("The thirty second version. Adiabatic gives T X. Isobaric doubles it. The rise is sixteen twenty-fifths of T W, and five halves n R times that is one point six joules.") as t:
            self.play(FadeIn(chead), run_time=0.5)
            for i, c in enumerate(cells):
                self.play(FadeIn(c, shift=RIGHT*0.1), *([GrowFromCenter(arows[i-1])] if i > 0 else []), run_time=0.55)
            self.play(FadeIn(sanity, shift=UP*0.1), run_time=0.7)
            self.wait(max(0.1, t.duration - 3.6))
        self.play(FadeOut(chead), FadeOut(cells), FadeOut(arows), FadeOut(sanity))

        # ================= SEG 8 · ONE-SCREEN RECAP =================
        shead = Label("One screen", color=WHITE).scale(0.5).to_edge(UP, buff=0.9)
        summ = VGroup(Body("Adiabatic sets the temperature; isobaric brings the heat.", color=WHITE).scale(0.4),
                      MathTex(r"T_X=\tfrac{16}{25}T_W,\quad T_Y=\tfrac{32}{25}T_W", color=SIGNAL).scale(0.5),
                      MathTex(r"Q_{XY}=\tfrac52 nR\,(T_Y-T_X)=\tfrac{8}{5}\,nRT_W=1.6\,\text{J}", color=SIGNAL).scale(0.5),
                      MathTex(r"\text{GUARD: constant-}P\text{ heat uses }C_P,\ \text{not }C_V", color=GUARD).scale(0.44)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).next_to(shead, DOWN, buff=0.55)
        with vo("One screen. Adiabatic sets the temperature, isobaric brings the heat.") as t:
            self.play(Write(shead), run_time=0.6)
            self.play(FadeIn(summ[0], shift=UP*0.08), run_time=0.6)
            self.wait(max(0.1, t.duration - 1.2))
        with vo("T X is sixteen twenty-fifths, T Y is thirty two twenty-fifths of T W.") as t:
            self.play(FadeIn(summ[1], shift=UP*0.08), run_time=0.6); self.wait(max(0.1, t.duration - 0.6))
        with vo("Five halves n R times the rise is one point six joules.") as t:
            self.play(FadeIn(summ[2], shift=UP*0.08), run_time=0.6); self.wait(max(0.1, t.duration - 0.6))
        with vo("The guard: constant pressure heat uses C P, not C V.") as t:
            self.play(FadeIn(summ[3], shift=UP*0.08), run_time=0.6); self.wait(max(0.1, t.duration - 0.6))
        with vo("The next question is on your screen now. Keep going.") as t:
            self.wait(min(t.duration, 2.8))
        self.play(FadeOut(shead), FadeOut(summ)); self.wait(0.3)
