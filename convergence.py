from manim import *

class Convergence(Scene):
    def construct(self):
        point = Dot().move_to([-2, 0, 0])
        self.add(point)

        for i in range(10):  # Anzahl der Iterationen erhöhen
            gradient = 2 * point.get_x()  # Ableitung von x^2
            step_size = 0.2 / (1 + 0.1 * i)  # Langsamere Lernrate mit jeder Iteration
            new_x = point.get_x() - step_size * gradient
            new_point = Dot().move_to([new_x, 0, 0])

            self.play(MoveAlongPath(point, Line(start=point.get_center(), end=new_point.get_center())))
            point.move_to(new_point.get_center())

        self.wait(2)