from manim import *

class GradientCalculation(Scene):
    def construct(self):
        point = Dot().move_to([-2, 4, 0])
        gradient = Arrow(start=point.get_center(), end=point.get_center() + RIGHT*2)

        self.add(point, gradient)
        self.play(Create(gradient))
        self.wait(2)