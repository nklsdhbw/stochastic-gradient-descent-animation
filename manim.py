from manim import Create, Write, FadeIn, Axes, UP, Tex, WHITE, GREEN, Scene, Dot, DashedLine, YELLOW, RED, BLUE, DOWN, LEFT, VGroup, RIGHT, FadeOut, MathTex, Transform, FadeTransform, ReplacementTransform
import sympy as sp

class Visualize(Scene):
    ####* Functions
    def partialDerivative1(self,wrt, coordinates, intercept, slope, next_to, direction):
        if wrt == "slope":
            derivative = r"\dfrac{\partial RSS}{\partial slope}"
            derivative = MathTex(rf"{derivative}")
            derivative.next_to(next_to, direction)
            # move a bit to left
            derivative.shift(UP*2)
            derivative.shift(LEFT*0.7)
        elif wrt == "intercept":
            derivative = r"\dfrac{\partial RSS}{\partial intercept}"
            derivative = MathTex(rf"{derivative}")
            derivative.next_to(next_to, direction)
            derivative.shift(DOWN*1)

        return derivative
    
    def partialDerivative2(self, wrt, coordinates, intercept, slope, next_to, direction, shiftFactor):
        if wrt == "slope":
            derivative = r"& = -2 \sum_{i=1}^{n} x_i(y_i - \hat{y}_i) \\ &"
            derivative = MathTex(rf"{derivative}")
            derivative.next_to(next_to, direction)
            # move a bit to left
        elif wrt == "intercept":
            derivative = r"\dfrac{\partial RSS}{\partial intercept}  = -2 \sum_{i=1}^{n} (y_i - \hat{y}_i) \\ &"
            derivative = MathTex(rf"{derivative}")
            derivative.next_to(next_to, direction)
        return derivative

    def partialDerivative3(self, wrt, coordinates, intercept, slope, next_to, direction, shiftFactor):
        derivative = r"&"
        for cords in coordinates:
            if cords == coordinates[0]:
                derivative += r"="
            x, y = cords
            if wrt == "slope":
                derivative += rf"(-2) \cdot {x} \cdot ({intercept} + {slope} \cdot {x}) \\ & +"
            elif wrt == "intercept":
                derivative += rf"(-2) \cdot ({intercept} + {slope} \cdot {x}) \\ & +"
        # Remove last plus sign
        derivative = derivative[:-1]
        
        derivative = MathTex(rf"{derivative}")
        derivative.next_to(next_to, direction)
        # move a bit to left
        derivative.shift(RIGHT*shiftFactor)
        return derivative
    
    def partialDerivative4(self, wrt, coordinates, intercept, slope, next_to, direction, shiftFactor):
        derivative = r"&"
        for cords in coordinates:
            if cords == coordinates[0]:
                derivative += r"="
            x, y = cords
            if wrt == "slope":
                result = (-2) * x * (intercept + slope * x)
            elif wrt == "intercept":
                result = (-2) * (intercept + slope * x)
            derivative = derivative + rf"{result} +"
        # Remove last plus sign
        derivative = derivative[:-1]
         # replace +- with -
        derivative = derivative.replace("+-", "-")
        print(derivative)
        derivative = MathTex(rf"{derivative}")
        derivative.next_to(next_to, direction)
        # move a bit to left
        derivative.shift(RIGHT*shiftFactor)
        return derivative
    
    def partialDerivative5(self, wrt, coordinates, intercept, slope, next_to, direction, shiftFactor):
        totalResult = 0
        derivative = r"&"
        for cords in coordinates:
            if cords == coordinates[0]:
                derivative += r"="
            x, y = cords
            if wrt == "slope":
                totalResult += (-2) * x * (intercept + slope * x)
            elif wrt == "intercept":
                totalResult += (-2) * (intercept + slope * x)
        derivative = derivative + rf"{totalResult}"
        derivative = MathTex(rf"{derivative}")
        derivative.next_to(next_to, direction)
        # move a bit to left
        derivative.shift(RIGHT*shiftFactor)
        return derivative
    


    def graph(self, axes, formula, title=""):
        x = sp.symbols('x')
        formula = sp.sympify(formula)
        function = sp.lambdify(x, formula, 'numpy')
        graph = axes.plot(function, x_range=[0, 3.1],color=BLUE)

        title = Tex(title)
        title.next_to(axes, UP)
        return graph, title
    
    def dot(self, axes, x, y):
        dot = Dot(axes.c2p(x, y), color=RED)
        return dot

    ####* Construct
    def construct(self):
        title = Tex("Gradient Descent")
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
        self.wait(2)

        # Create axes
        axes = Axes(
            x_range=[0, 5],
            y_range=[0, 5],
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
        


        # Show coordinate system and dots
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(2)
        for dot in dots:
            self.play(FadeIn(dot))
        self.wait(2)


        # Move coordinate system to the left all at the same time
        group = VGroup(axes, x_label, y_label, *dots)
        self.play(group.animate.shift(LEFT*3))
        self.wait(3)


        # Create regression line
        slope = 1.5
        line, linetitle = self.graph(axes, f"{slope}*x")

        function = MathTex("y = slope \cdot x + intercept")
        function2 = MathTex("= 1.5 \cdot x + 0")
        function.next_to(axes, RIGHT)
        function.shift(UP*2)
        function.shift(LEFT*0.7)
        function2.next_to(function, DOWN)
        function2.shift(LEFT*0.9)
        self.play(FadeIn(function))
        self.play(FadeIn(function2))
        # Show regression line
        self.wait(3)
        self.play(FadeIn(line), FadeIn(linetitle))




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

        # Draw loss function lines
        connections = {}
        for dot_obj, new_dot in newDots.items():
            connections[dot_obj] = DashedLine(dot_obj.get_center(), new_dot.get_center(), color=RED)

        for connection in connections.values():
            self.play(FadeIn(connection))
        
        self.play(FadeOut(function), FadeOut(function2))

        # Residuals sum of squares
        RSS = Tex("$RSS = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$")
        RSS.next_to(axes, RIGHT)
        RSS.shift(UP*2)
        RSS.shift(LEFT*0.7)
        self.play(FadeIn(RSS))
        self.wait(2)
        self.play(FadeOut(RSS))

        # Derivatives of RSS
        partialSlopeText1 = self.partialDerivative1("slope", coordinates, 0, slope, axes, RIGHT)
        self.play(FadeIn(partialSlopeText1))
        self.wait(3)
        partialSlopeText2 = self.partialDerivative2("slope", coordinates, 0, slope, partialSlopeText1, RIGHT, 1.5)
        self.play(FadeIn(partialSlopeText2))
        partialSlopeText3 = self.partialDerivative3("slope", coordinates, 0, slope, partialSlopeText2, DOWN, 0.75)
        self.play(FadeIn(partialSlopeText3))
        self.wait(3)
        partialSlopeText4 = self.partialDerivative4("slope", coordinates, 0, slope, partialSlopeText1, DOWN, 3.3)
        self.play(FadeTransform(partialSlopeText3, partialSlopeText4))
        self.wait(3)
        partialSlopeText5 = self.partialDerivative5("slope", coordinates, 0, slope, partialSlopeText1, DOWN, 2)
        self.play(FadeTransform(partialSlopeText4, partialSlopeText5))
        self.wait(2)
        self.play(FadeOut(partialSlopeText2), partialSlopeText5.animate.shift(UP))
        self.wait(2)

        partialInterceptText1 = self.partialDerivative1("intercept", coordinates, 0, slope, partialSlopeText1, DOWN)
        self.play(FadeIn(partialInterceptText1))
        self.wait(3)
        partialInterceptText2 = self.partialDerivative2("slope", coordinates, 0, slope, partialInterceptText1, RIGHT, 1.5)
        self.play(FadeIn(partialInterceptText2))
        partialInterceptText3 = self.partialDerivative3("intercept", coordinates, 0, slope, partialInterceptText2, DOWN, 0.25)
        self.play(FadeIn(partialInterceptText3))
        self.wait(3)
        partialInterceptText4 = self.partialDerivative4("intercept", coordinates, 0, slope, partialInterceptText1, DOWN, 3.4)
        self.play(FadeTransform(partialInterceptText3, partialInterceptText4))
        self.wait(3)
        partialInterceptText5 = self.partialDerivative5("intercept", coordinates, 0, slope, partialInterceptText1, DOWN, 2.3)
        self.play(FadeTransform(partialInterceptText4, partialInterceptText5))
        self.wait(2)
        self.play(FadeOut(partialInterceptText2), partialInterceptText5.animate.shift(UP))
        self.wait(2)

        # clear up all objects
        objects = [axes, x_label, y_label, *dots, *newDots.values(), *connections.values(), line, linetitle]
        group = VGroup(*objects)
        self.play(FadeOut(group))
        self.wait(0.5)
        derivatives = [partialSlopeText1, partialSlopeText5, partialInterceptText1, partialInterceptText5]
        group = VGroup(*derivatives)
        self.play(group.animate.shift(LEFT*6))
        # Animate move group to left

        
        # Gradient descent
        # Visualize
        """
        stepSizeIntercept = r"stepSize_{intercept} = slope \cdot learningRate"
        stepSizeIntercept = MathTex(rf"{stepSizeIntercept}")
        stepSizeIntercept.next_to(partialInterceptText4, RIGHT)
        stepSizeIntercept.shift(UP*2)
        self.play(FadeIn(stepSizeIntercept))
        """
        
        
        
