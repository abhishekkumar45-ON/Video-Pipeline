"""
Orange Nelumbo · Electrostatics · Q7 — "Equal Potential Locus"
JEE Adv 2026 P2 Q7 (multi-correct). |V1| = |V2| for Q1=q at P1(a,b), Q2=mq at P2(ma,mb).
Master eq: (m+1)(x^2+y^2) - 2m(ax+by) = 0 -> line if m=-1, else circle.  Answer: A, B, C.
"""
from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_service import KokoroService

BG       = "#0E0D10"
IGNITION = "#FF5A1F"
EMBER    = "#FF7A2E"
CYAN     = "#3DE0D0"
TXT      = "#E8E6EC"
MUTED    = "#8A8A93"
REDX     = "#E0483C"
GOOD     = "#3DE0D0"
MONO = "JetBrains Mono"


class Scene_q7(VoiceoverScene):
    def construct(self):
        self.camera.background_color = BG
        self.set_speech_service(KokoroService())

        tag  = Text("// ELECTROSTATICS", font=MONO, color=IGNITION).scale(0.30)
        mark = Text("ORANGE NELUMBO", font=MONO, color=MUTED).scale(0.24)
        tag.to_corner(UL, buff=0.4)
        mark.next_to(tag, DOWN, aligned_edge=LEFT, buff=0.12)
        prog = Text("01 / 07", font=MONO, color=MUTED).scale(0.24).to_corner(UR, buff=0.4)
        self.add(tag, mark, prog)

        def set_prog(n):
            new = Text(f"0{n} / 07", font=MONO, color=MUTED).scale(0.24).move_to(prog)
            self.play(Transform(prog, new), run_time=0.4)

        # ---------- 01 HOOK ----------
        title = Text("EQUAL POTENTIAL", font=MONO, color=TXT, weight=BOLD).scale(0.95)
        sub   = Text("where do two charges tie?", font=MONO, color=MUTED).scale(0.4)
        sub.next_to(title, DOWN, buff=0.3)
        with self.voiceover(text="Two charges sit in a plane. The question — "
                                 "where is the potential from one... exactly equal in magnitude... "
                                 "to the potential from the other?") as t:
            self.play(Write(title), run_time=min(2.0, t.duration))
            self.play(FadeIn(sub, shift=UP*0.2), run_time=0.7)
            self.wait(max(0.1, t.duration - 2.7))
        self.play(FadeOut(title), FadeOut(sub))

        # ---------- 02 SETUP ----------
        set_prog(2)
        c1 = MathTex(r"Q_1 = q \ \text{at}\ P_1(a,\,b)", color=CYAN).scale(0.8)
        c2 = MathTex(r"Q_2 = m q \ \text{at}\ P_2(m a,\,m b)", color=EMBER).scale(0.8)
        cond = MathTex(r"\text{find locus of }\ |V_1| = |V_2|", color=IGNITION).scale(0.8)
        setup = VGroup(c1, c2, cond).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN)
        with self.voiceover(text="Charge q sits at point P one. A second charge — m times q — "
                                 "sits at P two, at m times those coordinates.") as t:
            self.play(Write(c1), run_time=1.0)
            self.play(Write(c2), run_time=1.0)
            self.wait(max(0.1, t.duration - 2.0))
        with self.voiceover(text="We want every point where the two potentials are equal in size.") as t:
            self.play(Write(cond), run_time=1.0)
            self.wait(max(0.1, t.duration - 1.0))
        self.play(FadeOut(setup))

        # ---------- 03 EQUATION ----------
        set_prog(3)
        v = MathTex(r"V_1 = \frac{kq}{r_1}", r"\qquad V_2 = \frac{k m q}{r_2}",
                    color=TXT).scale(0.85)
        step = MathTex(r"\frac{|q|}{r_1} = \frac{|mq|}{r_2}", color=TXT).scale(0.9)
        res  = MathTex(r"r_2^{\,2} = m^2\, r_1^{\,2}", color=IGNITION).scale(1.0)
        col = VGroup(v, step, res).arrange(DOWN, buff=0.55).move_to(ORIGIN)
        with self.voiceover(text="Potential is k q over r. So the two potentials are k q over r one, "
                                 "and k m q over r two.") as t:
            self.play(Write(v), run_time=min(1.8, t.duration))
            self.wait(max(0.1, t.duration - 1.8))
        with self.voiceover(text="Set the magnitudes equal. The k's cancel. Cross-multiply... "
                                 "and squaring both sides gives r two squared equals m squared r one squared.") as t:
            self.play(Write(step), run_time=1.3)
            self.play(TransformFromCopy(step, res), run_time=1.3)
            self.wait(max(0.1, t.duration - 2.6))
        self.play(FadeOut(v), FadeOut(step), res.animate.to_edge(UP, buff=1.3))

        # ---------- 04 EXPAND -> MASTER ----------
        set_prog(4)
        exp = MathTex(r"(x-ma)^2+(y-mb)^2 = m^2\big[(x-a)^2+(y-b)^2\big]",
                      color=MUTED).scale(0.62)
        master = MathTex(r"(m+1)(x^2+y^2) - 2m(ax+by) = 0", color=IGNITION).scale(0.9)
        mlab = Text("master equation", font=MONO, color=MUTED).scale(0.34)
        grp = VGroup(exp, master, mlab).arrange(DOWN, buff=0.5).next_to(res, DOWN, buff=0.7)
        with self.voiceover(text="Write the distances in coordinates and expand. "
                                 "Watch — every constant term cancels.") as t:
            self.play(Write(exp), run_time=min(2.2, t.duration))
            self.wait(max(0.1, t.duration - 2.2))
        with self.voiceover(text="Collect the x and y terms, divide by m minus one... "
                                 "and it collapses into one clean master equation.") as t:
            self.play(TransformFromCopy(exp, master), run_time=1.6)
            self.play(FadeIn(mlab), run_time=0.4)
            self.wait(max(0.1, t.duration - 2.0))
        self.play(FadeOut(res), FadeOut(exp), FadeOut(mlab),
                  master.animate.to_edge(UP, buff=1.2))

        # ---------- 05 READ THE SHAPE ----------
        set_prog(5)
        caseA = VGroup(
            MathTex(r"m = -1", color=CYAN).scale(0.8),
            MathTex(r"ax + by = 0 \quad (\text{a line})", color=TXT).scale(0.7),
        ).arrange(DOWN, buff=0.2)
        caseB = VGroup(
            MathTex(r"m \neq -1", color=EMBER).scale(0.8),
            MathTex(r"\text{circle, center}\ \left(\tfrac{ma}{m+1},\ \tfrac{mb}{m+1}\right)", color=TXT).scale(0.6),
            MathTex(r"\text{radius}\ \tfrac{|m|}{|m+1|}\sqrt{a^2+b^2}", color=TXT).scale(0.6),
        ).arrange(DOWN, buff=0.2)
        cases = VGroup(caseA, caseB).arrange(RIGHT, buff=1.6).next_to(master, DOWN, buff=0.8)
        with self.voiceover(text="Now just read it off. If m is minus one, the squared terms vanish — "
                                 "you're left with a straight line through the origin.") as t:
            self.play(FadeIn(caseA, shift=UP*0.2), run_time=1.2)
            self.wait(max(0.1, t.duration - 1.2))
        with self.voiceover(text="For any other m, divide through, and it's a circle — "
                                 "with this center... and this radius.") as t:
            self.play(FadeIn(caseB, shift=UP*0.2), run_time=1.2)
            self.wait(max(0.1, t.duration - 1.2))
        self.play(FadeOut(master), FadeOut(cases))

        # ---------- 06 OPTIONS ----------
        set_prog(6)
        def row(letter, tex, ok):
            badge = Text(letter, font=MONO, color=(GOOD if ok else REDX), weight=BOLD).scale(0.5)
            body  = MathTex(tex, color=TXT).scale(0.55)
            mark_ = Text("✓" if ok else "✗", color=(GOOD if ok else REDX)).scale(0.55)
            return VGroup(badge, body, mark_).arrange(RIGHT, buff=0.35)
        rows = VGroup(
            row("A", r"m=-1:\ ax+by=0\ \text{(line)}", True),
            row("B", r"m=2:\ \text{circle }(\tfrac{2a}{3},\tfrac{2b}{3}),\ r=\tfrac{2}{3}\sqrt{a^2+b^2}", True),
            row("C", r"m=-2:\ \text{circle }(2a,2b),\ r=2\sqrt{a^2+b^2}", True),
            row("D", r"m=-3:\ \text{circle, NOT a line}", False),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN)
        with self.voiceover(text="Test the options. A — m is minus one, a line. Correct. "
                                 "B — m is two, a circle with center two-thirds a, two-thirds b. Correct.") as t:
            self.play(FadeIn(rows[0], shift=RIGHT*0.2), run_time=0.8)
            self.play(FadeIn(rows[1], shift=RIGHT*0.2), run_time=0.8)
            self.wait(max(0.1, t.duration - 1.6))
        with self.voiceover(text="C — m is minus two, center at two a, two b, radius two root a squared plus b squared. "
                                 "Correct. But D claims a line for m equals minus three — "
                                 "and minus three is not minus one, so it's a circle. D is wrong.") as t:
            self.play(FadeIn(rows[2], shift=RIGHT*0.2), run_time=0.8)
            self.play(FadeIn(rows[3], shift=RIGHT*0.2), run_time=0.8)
            self.wait(max(0.1, t.duration - 1.6))
        self.play(FadeOut(rows))

        # ---------- 07 ANSWER ----------
        set_prog(7)
        ans = VGroup(
            Text("ANSWER", font=MONO, color=MUTED).scale(0.4),
            Text("A ,  B ,  C", font=MONO, color=IGNITION, weight=BOLD).scale(0.9),
        ).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        box = SurroundingRectangle(ans[1], color=IGNITION, buff=0.3, corner_radius=0.1)
        with self.voiceover(text="So three of them hold. The answer... is A, B, and C.") as t:
            self.play(FadeIn(ans, shift=DOWN*0.2), run_time=1.0)
            self.play(Create(box), run_time=0.8)
            self.wait(max(0.3, t.duration - 1.8))
        self.wait(0.6)
