from manim import *

class FunctionPlot(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        function = axes.plot(lambda x: x**2, x_range=[-3, 3], color=BLUE)

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes, function)
        self.wait(2)