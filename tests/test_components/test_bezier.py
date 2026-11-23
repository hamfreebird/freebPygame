"""Bezier 曲线绘制的兼容性测试。

标准 pygame 的 ``pygame.gfxdraw`` 没有 ``bezier`` 函数（仅 pygame-ce 提供），
因此实现必须自带采样，不能依赖 ``pygame.gfxdraw.bezier``。
"""

import math
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
import pytest

from freepygame import FreeAllCircle, FreeCircle
from freepygame.freecircle import _binomial_coefficient


def _count_non_black(surface, width, height):
    """统计 surface 左上角区域中非黑像素数量。"""
    return sum(
        1
        for x in range(width)
        for y in range(height)
        if surface.get_at((x, y))[:3] != (0, 0, 0)
    )


class TestBezierWithoutGfxdrawBezier:
    """确保绘制路径不依赖 pygame.gfxdraw.bezier。"""

    def test_instance_does_not_call_gfxdraw_bezier(self, test_screen, monkeypatch):
        def _forbidden(*args, **kwargs):
            raise AssertionError(
                "draw_bezier 不应调用 pygame.gfxdraw.bezier"
                "（标准 pygame 没有该函数）"
            )

        monkeypatch.setattr(pygame.gfxdraw, "bezier", _forbidden, raising=False)
        circle = FreeCircle(test_screen, [10, 10], 5, color=(0, 0, 0))
        circle.draw_bezier(
            test_screen,
            [(10, 10), (50, 10), (50, 50), (90, 50)],
            40,
            (255, 255, 255),
        )
        assert _count_non_black(test_screen, 100, 60) > 0

    def test_static_draws_visible_pixels(self, test_screen):
        FreeAllCircle.draw_bezier(
            test_screen,
            [(10, 10), (50, 10), (50, 50), (90, 50)],
            40,
            (0, 255, 0),
        )
        assert _count_non_black(test_screen, 100, 60) > 0

    def test_works_without_math_comb(self, test_screen, monkeypatch):
        # 模拟 Python 3.7：math 模块没有 comb
        monkeypatch.delattr(math, "comb", raising=False)
        FreeAllCircle.draw_bezier(
            test_screen,
            [(10, 10), (50, 10), (50, 50), (90, 50)],
            20,
            (255, 255, 0),
        )
        assert _count_non_black(test_screen, 100, 60) > 0


class TestBezierEdgeCases:
    def test_fewer_than_two_points_is_noop(self, test_screen):
        FreeAllCircle.draw_bezier(test_screen, [(1, 2)], 10, (255, 0, 0))
        assert _count_non_black(test_screen, 100, 60) == 0

    def test_zero_steps_does_not_raise(self, test_screen):
        FreeAllCircle.draw_bezier(test_screen, [(0, 0), (10, 10)], 0, (255, 0, 0))

    def test_accepts_float_and_vector_points(self, test_screen):
        points = [
            pygame.math.Vector2(10, 10),
            (50.5, 10.0),
            (50.0, 50.0),
            (90, 50),
        ]
        FreeAllCircle.draw_bezier(test_screen, points, 10, (255, 0, 255))
        assert _count_non_black(test_screen, 100, 60) > 0


class TestBinomialCoefficient:
    def test_known_values(self):
        assert _binomial_coefficient(0, 0) == 1
        assert _binomial_coefficient(4, 2) == 6
        assert _binomial_coefficient(4, 0) == 1
        assert _binomial_coefficient(4, 4) == 1
        assert _binomial_coefficient(10, 5) == 252
        assert _binomial_coefficient(4, 5) == 0
        assert _binomial_coefficient(4, -1) == 0
