from manim import Create, Write, FadeIn, Axes, UP, Tex, WHITE, GREEN, Scene, Dot, DashedLine, YELLOW, RED, BLUE, DOWN
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
            x_range=[0, 4],
            y_range=[0, 4],
            axis_config={"color": WHITE,},
            x_length = 6,
            y_length = 6,
            
        )
        # Add labels to the axes
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        # Create a dots
        dots = []
        coordinates = [(1, 2), (2, 4), (2.5, 3)]
        for x, y in coordinates:
            dots.append(self.dot(axes, x, y))
        

        # Create regression line
        slope = 1.5
        line, linetitle = self.graph(axes, f"{slope}*x")

        # Create orthogonal lines
        perpendicular_slope = -1 / slope
        newDots = {}
        for dot_obj, cords in zip(dots, coordinates):
            # y = mx + b
            x, y = cords
            b = y - x*(perpendicular_slope)
            
            m1, b1 = (slope, 0)
            m2, b2 = (perpendicular_slope, b)
            x_value = (b2 - b1) / (m1 - m2)
            y_value = m2 * x_value + b2
            new_dot = self.dot(axes, x_value, y_value)
            newDots[dot_obj] = new_dot

        # draw line from dot to first dot of newDots and then to second dot of newDots
        connections = {}
        for dot_obj, new_dot in newDots.items():
            connections[dot_obj] = DashedLine(dot_obj.get_center(), new_dot.get_center(), color=RED)

        


        # Show axes and the parabola curve
        self.play(Create(axes), Write(x_label), Write(y_label))
        for dot in dots:
            self.play(FadeIn(dot))
        #self.play(FadeIn(dot), FadeIn(dot2), FadeIn(dot3))
        self.play(FadeIn(line), FadeIn(linetitle))
        for connection in connections.values():
            self.play(FadeIn(connection))


        # Residuals sum of squares
        RSS = Tex("$RSS = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$")
        RSS.next_to(linetitle, DOWN)
        self.play(FadeIn(RSS))

        self.wait(3)

