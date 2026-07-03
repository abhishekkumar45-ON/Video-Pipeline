import os
import json
from manim import *

HERE = os.path.dirname(os.path.abspath(__file__))
BEATS = json.load(open(os.path.join(HERE, "build", "beats.json")))


def make_element(el):
    t = el.get("type", "text")
    c = el.get("content", "")
    try:
        if t == "title":
            return Text(c, font_size=44, weight=BOLD)
        if t == "math":
            return MathTex(c, font_size=48)  # needs LaTeX
        return Text(c, font_size=30)
    except Exception:
        # if LaTeX/anything fails, degrade to plain text so render never crashes
        return Text(c, font_size=30)


class VideoScene(Scene):
    def construct(self):
        prev = None
        for beat in BEATS:
            dur = float(beat.get("duration", 3.0))
            els = [make_element(e) for e in beat.get("elements", [])] or [Text(" ")]
            group = VGroup(*els).arrange(DOWN, buff=0.6)

            if group.width > config.frame_width - 1:
                group.scale_to_fit_width(config.frame_width - 1)
            if group.height > config.frame_height - 1:
                group.scale_to_fit_height(config.frame_height - 1)
            group.move_to(ORIGIN)

            anim_t = min(1.0, max(0.4, dur * 0.4))
            if prev is not None:
                self.play(FadeOut(prev), run_time=0.3)
                dur = max(dur - 0.3, 0.3)
                anim_t = min(anim_t, dur * 0.5)

            self.play(Write(group), run_time=anim_t)
            self.wait(max(0.2, dur - anim_t))
            prev = group
