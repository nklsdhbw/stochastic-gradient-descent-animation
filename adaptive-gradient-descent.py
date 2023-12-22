from manim import Scene, Text, Write, FadeOut, FadeIn, Axes, Dot, Transform, MathTex, GREEN, WHITE, RED, YELLOW, BLUE, PINK, UP, RIGHT, LEFT, DOWN, VGroup, Arrow, Create, Indicate, SurroundingRectangle, GrowArrow, GrowFromCenter, DrawBorderThenFill, BLACK
import numpy as np

class AdaGrad(Scene):
    def construct(self):
        # first scene with the title
        title_text = Text("Adaptive Gradient Descent", font_size=48, color=RED)
        title_background = SurroundingRectangle(title_text, color=WHITE, fill_color=BLACK, fill_opacity=0.5)
        title_group = VGroup(title_background, title_text)

        self.play(GrowFromCenter(title_background), DrawBorderThenFill(title_text))
        self.wait(1)
        self.play(title_group.animate.scale(1.2).set_opacity(1.2))
        self.wait(2)
        self.play(FadeOut(title_group))

        # Mach erst mal die Basics
        basic_title = Text("Basics of AdaGrad", font_size=36)
        self.play(Write(basic_title))
        self.wait(2)
        self.play(FadeOut(basic_title))

        adagrad_formula = MathTex(
            r"AdaGrad \text{ automatically adjusts the learning rate: }",
            r"\eta_{t,i} = \frac{\eta}{\sqrt{\sum_{\tau=1}^t g_{\tau,i}^2 + \epsilon}}",
            font_size=30)
        adagrad_formula_box = SurroundingRectangle(adagrad_formula, color=BLUE)
        self.play(Write(adagrad_formula), Create(adagrad_formula_box))
        self.wait(2)
        self.play(FadeOut(adagrad_formula), FadeOut(adagrad_formula_box))

        # split to transform 'AdaGrad' into 'AdaGrad learning rate adjustment'
        adagrad_teil1 = adagrad_formula[0][0:7]
        new_title = MathTex(
            r"AdaGrad \text{ learning rate adjustment}",
            font_size=36
        ).to_edge(UP)

        # tranform into next scene
        self.play(Transform(adagrad_teil1, new_title))
        self.remove(adagrad_formula)
        self.add(new_title)
        self.wait(2)

        # more details about the formula of adagrad
        title = MathTex(
            r"AdaGrad \text{ learning rate adjustment}",
            font_size=36
        ).to_edge(UP)
        self.play(Write(new_title))

        # create variables for the explanation
        adagrad_formula = MathTex(
            r"\eta_{t,i} = \frac{\eta}{\sqrt{\sum_{\tau=1}^t g_{\tau,i}^2 + \epsilon}}",
            font_size=30
        ).shift(UP)

        learning_rate_desc = MathTex(
            r"\text{Initial learning rate } \eta",
            font_size=24
        ).next_to(adagrad_formula, DOWN, aligned_edge=LEFT)

        sqrt_desc = MathTex(
            r"\text{Adjustment based on historical gradients}",
            font_size=24
        ).next_to(adagrad_formula, DOWN, buff=1)

        gradient_sum_desc = MathTex(
            r"\sum_{\tau=1}^t g_{\tau,i}^2 \text{: Sum of the squared gradients}",
            font_size=24
        ).next_to(sqrt_desc, DOWN, aligned_edge=LEFT)

        epsilon_desc = MathTex(
            r"\epsilon \text{: Small value to avoid division by zero}",
            font_size=24
        ).next_to(gradient_sum_desc, DOWN, aligned_edge=LEFT)

        # animation of the variables
        self.play(Write(adagrad_formula))
        self.wait(2)
        self.play(Write(learning_rate_desc))
        self.wait(2)
        self.play(Write(sqrt_desc))
        self.wait(2)
        self.play(Write(gradient_sum_desc))
        self.wait(2)
        self.play(Write(epsilon_desc))
        self.wait(2)

        # group all elements together to let them all fade out at once
        all_elements = VGroup(adagrad_formula, learning_rate_desc, sqrt_desc, gradient_sum_desc, epsilon_desc)
        self.play(FadeOut(all_elements))
        self.play(FadeOut(title), FadeOut(new_title), FadeOut(adagrad_teil1))

        # animation of the AdaGrad-Algorithm
        example_text = Text("AdaGrad sample application", font_size=36)
        self.play(Write(example_text))
        self.wait(2)
        self.play(FadeOut(example_text))

        # sample application of AdaGrad
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-5, 5],
            axis_config={"color": WHITE}
        )
        function_curve = axes.plot(lambda x: x**2, color=GREEN)
        function_label = MathTex("f(x) = x^2", color=GREEN).next_to(function_curve, UP)

        self.play(Write(axes), Write(function_curve), Write(function_label))

       # starting point
        start_x = 2
        start_dot = Dot(axes.c2p(start_x, start_x**2), color=RED)
        self.play(FadeIn(start_dot))

        # initialise the explanation text
        explanation_text = MathTex("", font_size=24).to_edge(UP)
        self.play(Write(explanation_text))

        # loop for the 10 steps
        learning_rate = 1.0
        historical_gradient = 0
        epsilon = 1e-8

        for _ in range(10):
            gradient = 2 * start_x
            historical_gradient += gradient ** 2
            adjusted_learning_rate = learning_rate / (np.sqrt(historical_gradient) + epsilon)
            start_x = start_x - adjusted_learning_rate * gradient
            new_dot = Dot(axes.c2p(start_x, start_x**2), color=RED)

            # update the explanation text
            new_explanation_text = MathTex(
                f"Gradient: {gradient:.2f}",
                f"\\quad Angepasste Lernrate: {adjusted_learning_rate:.2f}",
                f"\\quad Position: ({start_x:.2f}, {start_x**2:.2f})",
                font_size=24
            ).to_edge(UP)

            # dot and text animation at the same time
            self.play(Transform(start_dot, new_dot), Transform(explanation_text, new_explanation_text))

        self.wait(2)
        self.play(FadeOut(function_curve), FadeOut(axes), FadeOut(start_dot), FadeOut(function_label), FadeOut(explanation_text))

        self.explain_adagrad()

    def explain_adagrad(self):
        title_explanation = Text("Explanation of the AdaGrad-animation", font_size=36)
        self.play(Write(title_explanation))
        self.wait(2)
        self.play(title_explanation.animate.to_edge(UP))

        learning_rate_text = Text("AdaGrad automatically adjusts the learning rate:", font_size=24).shift(UP * 2)
        self.play(Write(learning_rate_text))
        self.wait(2)

        # example of a learning rate formula
        learning_rate_formula = MathTex(r"\eta_{t} = \frac{\eta}{\sqrt{G_{t} + \epsilon}}", font_size=24).next_to(learning_rate_text, DOWN, buff=0.5)
        self.play(Write(learning_rate_formula))
        self.wait(2)

        # move the learning rate explanation
        lr_group = VGroup(learning_rate_text, learning_rate_formula)
        self.play(lr_group.animate.next_to(title_explanation, DOWN, buff=0.5))

        # explanation of the gradient
        gradient_text = Text("The gradient influences the direction of the optimisation", font_size=24).shift(UP)
        self.play(Write(gradient_text))
        self.wait(2)

        # visualisation of the gradient with an arrow
        arrow = Arrow(RIGHT, LEFT, buff=0).next_to(gradient_text, DOWN, buff=0.5)
        arrow_text = Text("Direction of the gradient", font_size=24).next_to(arrow, DOWN)
        self.play(GrowArrow(arrow), Write(arrow_text))
        self.wait(2)

        # move the explanation
        gradient_group = VGroup(gradient_text, arrow, arrow_text)
        self.play(gradient_group.animate.next_to(lr_group, DOWN, buff=0.5))

        # end of the scene
        end_text = Text("That's the Adaptive Gradient Descent!", font_size=36, color=GREEN).next_to(gradient_group, DOWN, buff=0.5)
        self.play(Write(end_text))
        self.wait(2)

        self.play(FadeOut(lr_group), FadeOut(gradient_group), FadeOut(end_text))