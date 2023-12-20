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
        derivative.align_to(next_to, LEFT)
        # move a bit to left
        #derivative.shift(RIGHT*shiftFactor)
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
        derivative.align_to(next_to, LEFT)
        # move a bit to left
        #derivative.shift(RIGHT*shiftFactor)
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
        derivative.align_to(next_to, LEFT)
        # move a bit to left
       #derivative.shift(RIGHT*shiftFactor)
        return derivative, totalResult
    


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
            self.play(Write(dot))
        self.wait(2)


        # Move coordinate system to the left all at the same time
        group = VGroup(axes, x_label, y_label, *dots)
        self.play(group.animate.shift(LEFT*3))
        self.wait(3)


        # Create regression line
        slope = 1.5
        intercept = 0
        line, linetitle = self.graph(axes, f"{slope}*x + {intercept}")

        function = MathTex("y")
        function2 = MathTex("= slope \cdot x + intercept")
        function3 = MathTex(f"= {slope} \cdot x + {intercept}")
        function.next_to(axes, RIGHT)
        function.shift(UP*2)
        function.shift(LEFT*0.7)
        function2.next_to(function, RIGHT)
        function3.next_to(function2, DOWN)
        function3.align_to(function2, LEFT)
        self.play(Write(function), Write(function2))
        self.play(Write(function3))
        # Show regression line
        self.wait(3)
        self.play(Write(line), Write(linetitle))




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
            self.play(Write(connection))
        
        self.play(FadeOut(function), FadeOut(function2), FadeOut(function3))

        # Residuals sum of squares
        RSS = Tex("$RSS = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$")
        RSS.next_to(axes, RIGHT)
        RSS.shift(UP*2)
        RSS.shift(LEFT*0.7)
        self.play(Write(RSS))
        self.wait(2)
        self.play(FadeOut(RSS))

        # Derivatives of RSS
        partialSlopeText1 = self.partialDerivative1("slope", coordinates, 0, slope, axes, RIGHT)
        partialSlopeText2 = self.partialDerivative2("slope", coordinates, 0, slope, partialSlopeText1, RIGHT, 1.5)
        self.play(Write(partialSlopeText1))
        
        self.play(Write(partialSlopeText2))
        partialSlopeText3 = self.partialDerivative3("slope", coordinates, 0, slope, partialSlopeText2, DOWN, 0.75)
        self.play(Write(partialSlopeText3))
        self.wait(3)
        partialSlopeText4 = self.partialDerivative4("slope", coordinates, 0, slope, partialSlopeText2, DOWN, 3.3)
        self.play(FadeTransform(partialSlopeText3, partialSlopeText4))
        self.wait(3)
        partialSlopeText5, DERIVATIVE_SLOPE = self.partialDerivative5("slope", coordinates, 0, slope, partialSlopeText2, DOWN, 2)
        self.play(FadeTransform(partialSlopeText4, partialSlopeText5))
        self.wait(2)
        self.play(FadeOut(partialSlopeText2), partialSlopeText5.animate.shift(UP))
        self.wait(2)

        partialInterceptText1 = self.partialDerivative1("intercept", coordinates, 0, slope, partialSlopeText1, DOWN)
        partialInterceptText2 = self.partialDerivative2("slope", coordinates, 0, slope, partialInterceptText1, RIGHT, 1.5)
        self.play(Write(partialInterceptText1))
        self.play(Write(partialInterceptText2))
        partialInterceptText3 = self.partialDerivative3("intercept", coordinates, 0, slope, partialInterceptText2, DOWN, 0.25)
        self.play(Write(partialInterceptText3))
        self.wait(3)
        partialInterceptText4 = self.partialDerivative4("intercept", coordinates, 0, slope, partialInterceptText2, DOWN, 3.4)
        self.play(FadeTransform(partialInterceptText3, partialInterceptText4))
        self.wait(3)
        partialInterceptText5, DERIVATIVE_INTERCEPT = self.partialDerivative5("intercept", coordinates, 0, slope, partialInterceptText2, DOWN, 2.3)
        self.play(FadeTransform(partialInterceptText4, partialInterceptText5))
        self.wait(2)
        self.play(FadeOut(partialInterceptText2), partialInterceptText5.animate.shift(UP))
        self.wait(2)

        # clear up all objects
        objects = [axes, x_label, y_label, *dots, *newDots.values(), *connections.values(), line, linetitle]
        group = VGroup(*objects)
        self.play(FadeOut(group))
        self.wait(0.5)
        slopeGroup = [partialSlopeText1, partialSlopeText5]
        interceptGroup = [partialInterceptText1, partialInterceptText5]
        slopeGroup = VGroup(*slopeGroup)
        interceptGroup = VGroup(*interceptGroup)
        #group = VGroup(*derivatives)
        self.play(slopeGroup.animate.shift(LEFT*6))
        vertical_shift = slopeGroup[0].get_center()[1] - interceptGroup[0].get_center()[1]
        self.play(interceptGroup.animate.shift(UP*vertical_shift))
        # Animate move group to left
        
        
        # Gradient descent
        stepSizeSlope = r"stepSize_{Slope}"
        stepSizeSlope2 = r"= \dfrac{\partial RSS}{\partial slope} \cdot learningRate"
        stepSizeSlope = MathTex(rf"{stepSizeSlope}")
        stepSizeSlope.next_to(partialSlopeText1, DOWN)
        stepSizeSlope.shift(RIGHT * 1)
        stepSizeSlope2 = MathTex(rf"{stepSizeSlope2}")
        stepSizeSlope2.next_to(stepSizeSlope, RIGHT)
        self.play(Write(stepSizeSlope))
        self.play(Write(stepSizeSlope2))
        learningRate = 0.01
        stepSizeSlope3 = MathTex(rf"= {DERIVATIVE_SLOPE} \cdot {learningRate}")
        stepSizeSlope3.next_to(stepSizeSlope2, DOWN)
        stepSizeSlope3.align_to(stepSizeSlope2, LEFT)
        self.play(Write(stepSizeSlope3))

        stepSizeSlope4 = DERIVATIVE_SLOPE * learningRate
        stepSizeSlopeValue = stepSizeSlope4
        stepSizeSlope4 = MathTex(rf"= {stepSizeSlope4}")
        stepSizeSlope4.next_to(stepSizeSlope2, DOWN)
        stepSizeSlope4.align_to(stepSizeSlope2, LEFT)
        self.play(FadeTransform(stepSizeSlope3, stepSizeSlope4))
        vertical_shift = stepSizeSlope2.get_center()[1] - stepSizeSlope4.get_center()[1]
        self.play(FadeOut(stepSizeSlope2))
        self.play(stepSizeSlope4.animate.shift(UP * vertical_shift))




        # Visualize
        stepSizeIntercept = r"stepSize_{intercept}"
        stepSizeIntercept2 = r"= \dfrac{\partial RSS}{\partial intercept} \cdot learningRate"
        stepSizeIntercept = MathTex(rf"{stepSizeIntercept}")
        stepSizeIntercept.next_to(stepSizeSlope, DOWN)
        stepSizeIntercept.shift(LEFT*0.7)
        stepSizeIntercept.shift(DOWN*0.5)
        stepSizeIntercept.shift(RIGHT * 1)
        stepSizeIntercept2 = MathTex(rf"{stepSizeIntercept2}")
        stepSizeIntercept2.next_to(stepSizeIntercept, RIGHT)
        self.play(Write(stepSizeIntercept))
        self.play(Write(stepSizeIntercept2))
        learningRate = 0.01
        stepSizeIntercept3 = MathTex(rf"= {DERIVATIVE_INTERCEPT} \cdot {learningRate}")
        stepSizeIntercept3.next_to(stepSizeIntercept2, DOWN)
        stepSizeIntercept3.align_to(stepSizeIntercept2, LEFT)
        self.play(Write(stepSizeIntercept3))
        stepSizeIntercept4 = DERIVATIVE_INTERCEPT * learningRate
        stepSizeInterceptValue = stepSizeIntercept4
        stepSizeIntercept4 = MathTex(rf"= {stepSizeIntercept4}")
        stepSizeIntercept4.next_to(stepSizeIntercept2, DOWN)
        stepSizeIntercept4.align_to(stepSizeIntercept2, LEFT)
        self.play(FadeTransform(stepSizeIntercept3, stepSizeIntercept4))
        vertical_shift = stepSizeIntercept2.get_center()[1] - stepSizeIntercept4.get_center()[1]
        self.play(FadeOut(stepSizeIntercept2))
        self.play(stepSizeIntercept4.animate.shift(UP * vertical_shift))
        stepsize = [stepSizeSlope, stepSizeSlope4, stepSizeIntercept, stepSizeIntercept4]
        stepsize = VGroup(*stepsize)


        # New slopes and intercepts
        self.play(FadeOut(slopeGroup), FadeOut(interceptGroup))
        self.play(stepsize.animate.shift(UP*2))

        newSlope1 = r"slope_{new}"
        newSlope2 = r"= slope_{old} - stepSize_{slope}"
        newSlope1 = MathTex(rf"{newSlope1}")
        newSlope2 = MathTex(rf"{newSlope2}")
        newSlope1.next_to(stepsize, DOWN)
        newSlope1.shift(LEFT*2)
        newSlope2.next_to(newSlope1, RIGHT)
        self.play(Write(newSlope1))
        self.play(Write(newSlope2))
        newSlope3 = rf"= {slope} - ({stepSizeSlopeValue})"
        newSlope3 = MathTex(rf"{newSlope3}")
        newSlope3.next_to(newSlope2, DOWN)
        newSlope3.align_to(newSlope2, LEFT)
        self.play(Write(newSlope3))
        newSlope4 = slope - stepSizeSlopeValue
        newSlope4 = MathTex(rf"= {newSlope4}")
        newSlope4.next_to(newSlope2, DOWN)
        newSlope4.align_to(newSlope2, LEFT)
        self.play(FadeTransform(newSlope3, newSlope4))
        vertical_shift = newSlope2.get_center()[1] - newSlope4.get_center()[1]
        self.play(FadeOut(newSlope2))
        self.play(newSlope4.animate.shift(UP * vertical_shift))

        
        
        newintercept1 = r"intercept_{new}"
        newintercept2 = r"= intercept_{old} - stepSize_{intercept}"
        newintercept1 = MathTex(rf"{newintercept1}")
        newintercept2 = MathTex(rf"{newintercept2}")
        newintercept1.next_to(newSlope1, DOWN)
        newintercept1.align_to(newSlope1, LEFT)
        newintercept2.next_to(newintercept1, RIGHT)
        self.play(Write(newintercept1))
        self.play(Write(newintercept2))
        newintercept3 = rf"= {intercept} - ({stepSizeInterceptValue})"
        newintercept3 = MathTex(rf"{newintercept3}")
        newintercept3.next_to(newintercept2, DOWN)
        newintercept3.align_to(newintercept2, LEFT)
        self.play(Write(newintercept3))
        newintercept4 = intercept - stepSizeInterceptValue
        newintercept4 = MathTex(rf"= {newintercept4}")
        newintercept4.next_to(newintercept2, DOWN)
        newintercept4.align_to(newintercept2, LEFT)
        self.play(FadeTransform(newintercept3, newintercept4))
        vertical_shift = newintercept2.get_center()[1] - newintercept4.get_center()[1]
        self.play(FadeOut(newintercept2))
        self.play(newintercept4.animate.shift(UP * vertical_shift))








        
        #self.play(FadeIn(stepSizeIntercept4))
        #self.play(FadeTransform(stepSizeIntercept4))
        #self.play
        #horizontal_shift = stepSizeIntercept.get_center()[0] - stepSizeIntercept2.get_center()[0]
        #stepSizeIntercept2.shift(RIGHT * horizontal_shift)
        #self.play(FadeIn(stepSizeIntercept2))

        """
        stepSizeSlope = r"stepSize_{slope} = \dfrac{\partial RSS}{\partial intercept} \cdot learningRate"
        stepSizeSlope = MathTex(rf"{stepSizeSlope}")
        stepSizeSlope.next_to(stepSizeIntercept, DOWN)
        vertical_shift = partialSlopeText5.get_center()[1] - stepSizeSlope.get_center()[1]
        #stepSizeSlope.shift(UP * vertical_shift)
        self.play(Write(stepSizeSlope))
        self.wait(3)
        """

        
        
        
        