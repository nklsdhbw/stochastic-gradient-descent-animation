from manim import Create, Write, FadeIn, Axes, UP, Tex, WHITE, GREEN, Scene, Dot, DashedLine, YELLOW, RED, BLUE
import sympy as sp

class PlotParabola(Scene):
    def graph(self, axes, formula, title=""):
        x = sp.symbols('x')
        formula = sp.sympify(formula)
        function = sp.lambdify(x, formula, 'numpy')
        graph = axes.plot(function, color=BLUE)

        title = Tex(title)
        title.next_to(axes, UP)
        return graph, title
    
    def dot(self, axes, x, y):
        dot = Dot(axes.c2p(x, y))
        return dot

    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-4, 4],
            y_range=[-4, 4],
            axis_config={"color": WHITE,},
            
        )
        # Add labels to the axes
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        # Create a dots
        dot = self.dot(axes, 1, 2)
        dot2 = self.dot(axes, 2, 4)
        dot3 = self.dot(axes, 2.5, 3)
        dots = [dot, dot2, dot3]

        # Create regression line
        slope = 1.5
        line, linetitle = self.graph(axes, f"{slope}*x")

        # Create orthogonal lines
        perpendicular_slope = -1 / slope
        newDots = {}
        for dot_obj in [dot, dot2, dot3]:
            # y = mx + b
            x = dot_obj.get_center()[0]
            y = dot_obj.get_center()[1]
            b = y - x*(perpendicular_slope)
            
            m1, b1 = (slope, 0)
            m2, b2 = (perpendicular_slope, b)
            x_value = (b2 - b1) / (m1 - m2)
            y_value = m2 * x_value + b2
            new_dot = self.dot(axes, x_value, y_value)
            newDots[dot_obj] = new_dot
            print("Dot: ", x_value, y_value)

        # draw line from dot to first dot of newDots and then to second dot of newDots
        connections = {}
        for dot_obj, new_dot in newDots.items():
            connections[dot_obj] = DashedLine(dot_obj.get_center(), new_dot.get_center(), color=RED)

        


        # Show axes and the parabola curve
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(FadeIn(dot), FadeIn(dot2), FadeIn(dot3))
        self.play(FadeIn(line), FadeIn(linetitle))
        for connection in connections.values():
            self.play(FadeIn(connection))


        self.wait(3)

