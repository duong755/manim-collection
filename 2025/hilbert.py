import math
from typing import List
from manim import *
import numpy as np

Point = List[float]

flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]

def make_barycenter(points: List[Point], weights: List[float]) -> Point:
    assert len(points) > 0 and len(weights) > 0, "list of points and list of weights must be non-empty"
    assert len(points) == len(weights), "list of points and list of weights must have same length"
    assert sum(weights) != 0.0, "sum of weights must be non-zero"

    _points = np.array(points)
    _weights = np.array(weights)

    barycenter = np.sum(_points * _weights[:, np.newaxis], axis=0) / np.sum(_weights)
    return barycenter


def make_centroid(points: List[Point]) -> Point:
    assert len(points) > 0, "list of points must be non-empty"
    return make_barycenter(points, weights=[1] * len(points))


def make_hilbert_curve(quadrangle: List[Point], number_of_iterations: int) -> List[List[Point]]:
    assert number_of_iterations >= 0, "number of iterations must be greater than or equal to 0"

    def hilbert_step(_quadrangle: List[Point]) -> List[List[Point]]:
        return [
            [make_barycenter(_quadrangle, [0, 0, 1, 1]), make_barycenter(_quadrangle, [1, 1, 1, 1]),
             make_barycenter(_quadrangle, [1, 0, 0, 1]), make_barycenter(_quadrangle, [0, 0, 0, 1])],
            [make_barycenter(_quadrangle, [1, 0, 0, 0]), make_barycenter(_quadrangle, [1, 1, 0, 0]),
             make_barycenter(_quadrangle, [1, 1, 1, 1]), make_barycenter(_quadrangle, [1, 0, 0, 1])],
            [make_barycenter(_quadrangle, [1, 1, 0, 0]), make_barycenter(_quadrangle, [0, 1, 0, 0]),
             make_barycenter(_quadrangle, [0, 1, 1, 0]), make_barycenter(_quadrangle, [1, 1, 1, 1])],
            [make_barycenter(_quadrangle, [1, 1, 1, 1]), make_barycenter(_quadrangle, [0, 0, 1, 1]),
             make_barycenter(_quadrangle, [0, 0, 1, 0]), make_barycenter(_quadrangle, [0, 1, 1, 0])]
        ]

    def recur(result: List[List[Point]], step: int) -> List[List[Point]]:
        if step >= number_of_iterations:
            return result

        return recur(flat_map(hilbert_step, result), step + 1)

    return recur(hilbert_step(quadrangle), 0)


class HilbertCurve2D(Scene):
    def construct(self):
        w, h = 6.0, 6.0

        groups = []
        iteration_no = 7

        for n in range(iteration_no):
            quadrangles = make_hilbert_curve([[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2, h / 2]], n)
            centroids = [make_centroid(quadrangle) for quadrangle in quadrangles]
            begin_color = PURE_RED
            end_color = PURE_GREEN
            lines = VGroup()
            length = len(centroids) - 1
            for i in range(len(centroids) - 1):
                start_point = np.append(centroids[i], [0.0])
                end_point = np.append(centroids[i + 1], [0.0])

                line = Line(start_point, end_point, stroke_width=1.0)
                line.set_color_by_gradient(interpolate_color(begin_color, end_color, i / length),
                                           interpolate_color(begin_color, end_color, (i + 1) / length))
                lines.add(line)

            groups.append(lines)

        for i in range(len(groups)):
            if i == 0:
                self.play(FadeIn(groups[i]))
                self.wait()
            else:
                self.play(ReplacementTransform(groups[i - 1], groups[i]))
                self.wait()
