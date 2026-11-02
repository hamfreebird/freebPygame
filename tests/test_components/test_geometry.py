"""
测试 freepygame 中的几何图元：FreeAARectangle 与 Point。
"""

import pygame
import pytest

from freepygame import FreeAARectangle, Point


class TestFreeAARectangle:
    """测试抗锯齿矩形图元。"""

    def test_creation(self, test_screen):
        r = FreeAARectangle(test_screen, [10, 20], [80, 40], (200, 0, 0))
        assert r.coordinates == [10, 20]
        assert r.size == [80, 40]
        assert r.color == (200, 0, 0)

    def test_attributes(self, test_screen):
        r = FreeAARectangle(test_screen, [0, 0], [50, 30])
        attr = r.get_attribute()
        assert attr["size"] == [50, 30]
        assert r.get_center_coordinates() == [25, 15]
        coords = r.det_coordinates()
        assert coords[0] == [0, 0]
        assert coords[2] == [50, 30]

    def test_setters_and_draw(self, test_screen):
        r = FreeAARectangle(test_screen, [0, 0], [50, 30])
        r.set_coordinates([5, 5])
        assert r.coordinates == [5, 5]
        r.set_size([10, 10])
        assert r.size == [10, 10]
        r.set_color((1, 2, 3))
        assert r.color == (1, 2, 3)
        try:
            r.draw()
        except Exception as e:
            pytest.fail(f"绘制 FreeAARectangle 时抛出异常: {e}")


class TestPoint:
    """测试点图元。"""

    def test_creation_and_draw(self, test_screen):
        p = Point(test_screen, [5, 5], 3, (255, 0, 0))
        assert p.coordinates == [5, 5]
        assert p.r == 3
        assert p.color == (255, 0, 0)
        p.move([10, 10])
        assert p.coordinates == [10, 10]
        try:
            p.draw()
        except Exception as e:
            pytest.fail(f"绘制 Point 时抛出异常: {e}")
