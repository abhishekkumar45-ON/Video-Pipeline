from manim import *


class SampleSilent(Scene):
    def construct(self):
        title = Text("Sum of roots", font_size=44).to_edge(UP)
        self.play(Write(title))

        eq = MathTex(r"2x^2 - 8x + 6 = 0", font_size=50)
        self.play(Write(eq))
        self.wait(0.5)

        res = MathTex(r"\text{Sum} = -\frac{b}{a} = \frac{8}{2} = 4",
                      font_size=46).next_to(eq, DOWN, buff=0.8)
        self.play(Write(res))
        self.wait(1)
