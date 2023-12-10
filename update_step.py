from manim import *

class UpdateStep(Scene):
    def construct(self):
        point = Dot().move_to([-2, 4, 0])
        new_point = point.copy().shift(RIGHT*2 + DOWN*1)
        movement = Arrow(start=point.get_center(), end=new_point.get_center(), buff=0)

        self.add(point, new_point, movement)
        self.play(MoveAlongPath(point, movement))
        self.wait(2)