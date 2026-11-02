"""
测试 SuperCircle 的操作符重载，以及 FreeAllCircle 的静态绘图方法。
"""

import pygame
import pytest

from freepygame import FreeAllCircle, SuperCircle


class TestSuperCircleOperators:
    """测试 SuperCircle 的 << 操作符。"""

    def test_lshift_radius(self, test_screen):
        sc = SuperCircle(test_screen, [100, 100], 50)
        sc << (75,)
        assert sc.radius == 75

    def test_lshift_rect(self, test_screen):
        sc = SuperCircle(test_screen, [100, 100], 50)
        sc << ((80, 60),)
        assert sc.rect == (80, 60)

    def test_lshift_color(self, test_screen):
        sc = SuperCircle(test_screen, [100, 100], 50)
        sc << ((255, 0, 0),)
        assert sc.color == (255, 0, 0)

    def test_lshift_redundant_raises(self, test_screen):
        sc = SuperCircle(test_screen, [100, 100], 50)
        with pytest.raises(AssertionError):
            sc << (1, 2, 3, 4)


class TestFreeAllCircleStatics:
    """测试 FreeAllCircle 的静态绘图辅助函数（无异常即视为通过）。"""

    def test_draw_circle(self, test_screen):
        FreeAllCircle.draw_circle(test_screen, (10, 10), 5, 1, (255, 0, 0))

    def test_draw_aacircle(self, test_screen):
        FreeAllCircle.draw_aacircle(test_screen, (10, 10), 5, (0, 255, 0))

    def test_draw_saacircle(self, test_screen):
        FreeAllCircle.draw_saacircle(test_screen, (10, 10), 5, (0, 0, 255))

    def test_draw_advanced_aacircle(self, test_screen):
        FreeAllCircle.draw_advanced_aacircle(
            test_screen, (10, 10), 5, (0, 359), (255, 255, 0)
        )

    def test_draw_advanced_aaellipse(self, test_screen):
        FreeAllCircle.draw_advanced_aaellipse(
            test_screen, (10, 10), (5, 8), (255, 0, 255)
        )

    def test_draw_bezier(self, test_screen):
        pts = [(0, 0), (10, 20), (20, 0), (30, 20)]
        FreeAllCircle.draw_bezier(test_screen, pts, 20, (128, 128, 128))
