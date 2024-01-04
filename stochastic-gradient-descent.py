from manim import Create, Arrow, GrowArrow, Write, FadeIn, Axes, UP, Tex, WHITE, GREY, GREEN, Scene, Dot, DashedLine, YELLOW, RED, ORANGE,  BLUE, DOWN, LEFT, VGroup, RIGHT, FadeOut, MathTex, Transform, FadeTransform, ReplacementTransform
import sympy as sp

class Visualize(Scene):
    ####* Functions
    def why_sgd(self):
        #* Why SGD?
        why_sgd = Tex(r"Why Stochastic Gradient Descent?", color=WHITE)
        self.play(Create(why_sgd))
        self.wait(1)
        self.play(FadeOut(why_sgd))
    
    def explain_sgd(self):
        set1 = Tex(r"Imagine we had a more complicated model, like a Logistic Regression that used 23,000 genes to predict if someone will have a disease?").scale(0.8)
        set2 = Tex(r"Then we would have 23,000 derivatives to plug the data into.").scale(0.8)
        set3 = Tex(r"And what if we had data from 1,000,000 samples?").scale(0.8)

        VGroup(set1, set2, set3).arrange(DOWN)
        self.play(Write(set1))
        self.wait(2)
        self.play(FadeIn(set2, shift=DOWN))
        self.wait(2)
        self.play(FadeIn(set3, shift=DOWN))
        self.wait(2)
        self.play(FadeOut(set1), FadeOut(set2), FadeOut(set3))
        self.wait(1)
        set4 = Tex(r"Then we would have to calculate 1,000,000 terms for each of the 23,000 derivatives.").scale(0.8)
        set5 = Tex(r"In other words, we'd have to calculate 23,000,000,000 terms for each step.").scale(0.8)
        set6 = Tex(r"And since it is common to take at least 1,000 steps, we would calculate at least 2,300,000,000,000 terms.").scale(0.8) 
        VGroup(set4, set5, set6).arrange(DOWN)
        self.play(Write(set4))
        self.wait(2)
        self.play(FadeIn(set5, shift=DOWN))
        self.wait(2)
        self.play(FadeIn(set6, shift=DOWN))
        self.wait(2)
        self.play(FadeOut(set4), FadeOut(set5), FadeOut(set6))
        self.wait(1)
        set7 = Tex(r"So, for BIG DATA, Gradient Descent is slow.").scale(0.8)
        set8 = Tex(r"This is where Stochastic Gradient Descent comes in handy.").scale(0.8)
        VGroup(set7, set8).arrange(DOWN)
        self.play(Write(set7))
        self.wait(2)
        self.play(FadeIn(set8, shift=DOWN))
        self.wait(2)
        self.play(FadeOut(set7), FadeOut(set8))
        self.wait(1)



    def drawCoordinateSystem2(self, x_range, y_range, size):
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            axis_config={"color": WHITE,},
            x_length = size,
            y_length = size,
            
        )
        # Add labels to the axes
        x_label = axes.get_x_axis_label("weight")
        y_label = axes.get_y_axis_label("height")
        return axes, x_label, y_label

    def drawLoss2(self, dots, coordinates, axes, slope, intercept):
        perpendicular_slope = -1 / slope
        newDots = {}
        newDotsCoordinates = []
        for dot_obj, cords in zip(dots, coordinates):
            # y = mx + b
            x, y = cords
            b = y - x*(perpendicular_slope)
            
            m1, b1 = (slope, intercept)
            m2, b2 = (perpendicular_slope, b)
            x_value = (b2 - b1) / (m1 - m2)
            y_value = m2 * x_value + b2
            new_dot = self.dot(axes, x_value, y_value)
            newDots[dot_obj] = new_dot
            newDotsCoordinates.append((x_value, y_value))

    def dot2(self, axes, x, y):
        dot = Dot(axes.c2p(x, y), color=RED)
        return dot

    def example1(self):
        # Create axes
        axes, x_label, y_label = self.drawCoordinateSystem2(x_range=[0, 5], y_range=[0, 5], size=6)

        # Create dots
        dots = []
        coordinates = [(1, 2), (2, 4), (3, 3)]
        for x, y in coordinates:
            dots.append(self.dot2(axes, x, y))

        # Create a title for the coordinate system
        title = Tex("Simple Example", color=BLUE).scale(0.8)
        title.next_to(axes, UP, buff=0.5)

        # Show coordinate system and dots
        self.play(Create(axes), Write(x_label), Write(y_label), Write(title))
        for dot in dots:
            self.play(Write(dot))
        self.wait(2)

        # Move coordinate system to the left all at the same time
        group = VGroup(axes, x_label, y_label, *dots)
        group.scale(0.6)
        self.play(group.animate.shift(DOWN, LEFT*3))
        self.wait(3)

        # Example: Add an arrow pointing to the first dot with explanation
        target_dot = dots[0]

        # Grey out other dots
        for dot in dots:
            if dot != target_dot:
                dot.set_color(GREY)

        # Create an arrow
        arrow = Arrow(start=2*UP+2*LEFT, end=target_dot.get_center(), buff=0.1, color=BLUE)

        # Create explanatory text
        explanation = Tex(r"Stochastic Gradient Descent would randomly pick one sample for each step…", color=WHITE).scale(0.5)
        explanation.next_to(arrow.get_start(), UP, buff=0.1)

        # Add the arrow and text to the scene
        self.play(GrowArrow(arrow), Write(explanation))
        self.wait(2)

        # Optional: Additional explanatory text
        explanation2 = Tex(r"...and just use that one sample to calculate the derivatives.", color=WHITE).scale(0.5)
        explanation2.next_to(arrow.get_start(), UP, buff=0.1)
        self.play(FadeOut(explanation))
        self.play(Write(explanation2))
        self.wait(2)
        self.play(FadeOut(explanation2), FadeOut(arrow))

        # Create the derivative equation parts
        equation_part1 = MathTex(
            r"\frac{d}{d \text{intercept}}",
            r"\text{ Sum of squared residuals}",
            r"=",
            font_size=24
        )
        equation_part2 = MathTex(
            r"-2(\text{Height} - (\text{intercept} + \text{slope} \times \text{Weight}))",
            font_size=24
        )

        # Position the equation parts
        equation_part1.next_to(group, RIGHT, buff=0.5)
        equation_part1.shift(UP*2)
        equation_part2.next_to(equation_part1, DOWN, aligned_edge=LEFT)

        # Display the equation parts
        self.play(Write(equation_part1))
        self.play(Write(equation_part2))
        self.wait(2)

        # Create arrows
        # Since we cannot target the exact submobject, we will approximate the position manually
        # Adjust the arrow's end positions as needed to accurately point to 'Height' and 'Weight'
        arrow_to_height_end = equation_part2.get_center() + LEFT * 1.8   # These values are examples; adjust as needed
        arrow_to_weight_end = equation_part2.get_center() + RIGHT * 2 + DOWN * 0.2   # These values are examples; adjust as needed

        arrow_to_height = Arrow(start=dots[0].get_center(), end=arrow_to_height_end, buff=0.1, color=BLUE)
        arrow_to_weight = Arrow(start=dots[0].get_center(), end=arrow_to_weight_end, buff=0.1, color=BLUE)

        # Display the arrows
        self.play(GrowArrow(arrow_to_height), GrowArrow(arrow_to_weight))
        self.wait(2)
        self.play(FadeOut(arrow_to_height), FadeOut(arrow_to_weight))


    def construct(self):
        self.why_sgd()  # Call the why_sgd function within the construct method
        self.explain_sgd()
        self.example1()