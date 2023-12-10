from manim import *

class Initialization(Scene):
    def construct(self):
        point = Dot().move_to([-2, 4, 0])
        text = Text("Starting Point").next_to(point, UP)
        
        self.add(point, text)
        self.wait(2)