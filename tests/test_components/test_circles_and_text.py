"""
测试 freepygame 中的圆形和文本组件
包括 FreeCircle, SuperCircle, FreeAllCircle, FreeText, SuperText 等
"""

import pygame
import pytest

from freepygame import (
    FreeAllCircle,
    FreeCircle,
    FreeText,
    SuperCircle,
    SuperText,
    _degree_to_radians,
)


class TestDegreeToRadians:
    """测试角度转弧度函数"""

    def test_degree_to_radians_zero(self):
        """测试0度转弧度"""
        assert _degree_to_radians(0) == 0.0

    def test_degree_to_radians_90(self):
        """测试90度转弧度"""
        result = _degree_to_radians(90)
        expected = 90 * 6.283185307179586 / 360
        assert abs(result - expected) < 1e-10

    def test_degree_to_radians_180(self):
        """测试180度转弧度"""
        result = _degree_to_radians(180)
        expected = 180 * 6.283185307179586 / 360
        assert abs(result - expected) < 1e-10

    def test_degree_to_radians_360(self):
        """测试360度转弧度"""
        result = _degree_to_radians(360)
        expected = 360 * 6.283185307179586 / 360
        assert abs(result - expected) < 1e-10

    def test_degree_to_radians_negative(self):
        """测试负角度转弧度"""
        result = _degree_to_radians(-45)
        expected = -45 * 6.283185307179586 / 360
        assert abs(result - expected) < 1e-10


class TestFreeAllCircle:
    """测试 FreeAllCircle 静态方法类"""

    def test_draw_circle_static(self, test_screen):
        """测试静态绘制普通圆"""
        # 这个方法应该不抛出异常
        try:
            FreeAllCircle.draw_circle(test_screen, (100, 100), 50, 2, (255, 0, 0))
        except Exception as e:
            pytest.fail(f"draw_circle 抛出异常: {e}")

    def test_draw_aacircle_static(self, test_screen):
        """测试静态绘制抗锯齿空心圆"""
        try:
            FreeAllCircle.draw_aacircle(test_screen, (200, 200), 30, (0, 255, 0))
        except Exception as e:
            pytest.fail(f"draw_aacircle 抛出异常: {e}")

    def test_draw_saacircle_static(self, test_screen):
        """测试静态绘制实心圆"""
        try:
            FreeAllCircle.draw_saacircle(test_screen, (300, 300), 40, (0, 0, 255))
        except Exception as e:
            pytest.fail(f"draw_saacircle 抛出异常: {e}")

    def test_draw_advanced_circle_static(self, test_screen):
        """测试静态绘制高级空心圆"""
        try:
            FreeAllCircle.draw_advanced_circle(
                test_screen, (400, 400), 50, 2, (0, 0), (0, 180), (255, 255, 0)
            )
        except Exception as e:
            pytest.fail(f"draw_advanced_circle 抛出异常: {e}")

    def test_draw_advanced_aacircle_static(self, test_screen):
        """测试静态绘制高级抗锯齿空心圆"""
        try:
            FreeAllCircle.draw_advanced_aacircle(
                test_screen, (500, 500), 60, (90, 270), (255, 0, 255)
            )
        except Exception as e:
            pytest.fail(f"draw_advanced_aacircle 抛出异常: {e}")

    def test_draw_advanced_aaellipse_static(self, test_screen):
        """测试静态绘制高级抗锯齿空心椭圆"""
        try:
            FreeAllCircle.draw_advanced_aaellipse(
                test_screen, (600, 600), (70, 35), (0, 255, 255)
            )
        except Exception as e:
            pytest.fail(f"draw_advanced_aaellipse 抛出异常: {e}")

    def test_draw_bezier_static(self, test_screen):
        """测试静态绘制贝塞尔曲线"""
        points = [(100, 100), (200, 50), (300, 150), (400, 100)]
        try:
            FreeAllCircle.draw_bezier(test_screen, points, 100, (128, 128, 128))
        except Exception as e:
            pytest.fail(f"draw_bezier 抛出异常: {e}")


class TestFreeCircle:
    """测试 FreeCircle 类"""

    def test_circle_creation(self, test_screen, default_circle_params):
        """测试圆形创建"""
        circle = FreeCircle(test_screen, **default_circle_params)
        assert circle is not None
        assert circle.coordinates == [400, 300]
        assert circle.radius == 50
        assert circle.width == 1
        assert circle.aa is True

    def test_circle_get_attribute(self, test_screen, default_circle_params):
        """测试获取圆形属性"""
        circle = FreeCircle(test_screen, **default_circle_params)
        attributes = circle.get_attribute()

        assert isinstance(attributes, dict)
        assert attributes["coordinates"] == [400, 300]
        assert attributes["radius"] == 50
        assert attributes["width"] == 1
        assert attributes["aa"] is True
        assert attributes["color"] == (0, 0, 0)

    def test_circle_get_center_coordinates(self, test_screen, default_circle_params):
        """测试获取圆心坐标"""
        circle = FreeCircle(test_screen, **default_circle_params)
        center = circle.get_center_coordinates()
        assert center == [400, 300]

    def test_circle_get_coordinates(self, test_screen, default_circle_params):
        """测试获取圆形矩形范围坐标"""
        circle = FreeCircle(test_screen, **default_circle_params)
        coords = circle.get_coordinates()

        assert isinstance(coords, list)
        assert len(coords) == 4
        # 左上角
        assert coords[0] == [350, 250]  # 400-50, 300-50
        # 右上角
        assert coords[1] == [450, 250]  # 400+50, 300-50
        # 右下角
        assert coords[2] == [450, 350]  # 400+50, 300+50
        # 左下角
        assert coords[3] == [350, 350]  # 400-50, 300+50

    def test_circle_set_properties(self, test_screen, default_circle_params):
        """测试设置圆形属性"""
        circle = FreeCircle(test_screen, **default_circle_params)

        # 测试设置坐标
        new_coords = [500, 400]
        circle.set_coordinates(new_coords)
        assert circle.coordinates == new_coords

        # 测试设置半径
        new_radius = 75
        circle.set_radius(new_radius)
        assert circle.radius == new_radius

        # 测试设置宽度
        new_width = 3
        circle.set_width(new_width)
        assert circle.width == new_width

        # 测试设置长短半轴
        new_rect = (60, 40)
        circle.set_rect(new_rect)
        assert circle.rect == new_rect

        # 测试设置角度
        new_angle = (45, 270)
        circle.set_angle(new_angle)
        assert circle.angle == new_angle

        # 测试设置抗锯齿
        circle.set_aa(False)
        assert circle.aa is False

        # 测试设置颜色
        new_color = (255, 0, 0)
        circle.set_color(new_color)
        assert circle.color == new_color

    def test_circle_border_properties(self, test_screen, default_circle_params):
        """测试圆形边框属性"""
        circle = FreeCircle(test_screen, **default_circle_params)

        # 测试切换边框显示
        circle.open_border(True)
        assert circle.draw_border is True
        circle.open_border(False)
        assert circle.draw_border is False

        # 测试设置边框宽度
        new_border_width = 3
        circle.set_border_width(new_border_width)
        assert circle.border_width == new_border_width

        # 测试设置边框颜色
        new_border_color = (0, 255, 0)
        circle.set_border_color(new_border_color)
        assert circle.border_color == new_border_color

        # 测试设置边框角度
        border_angle = (90, 180)
        circle._open_border_angle(border_angle)
        assert circle._border_angle == list(border_angle)

    def test_circle_draw_no_error(self, test_screen, default_circle_params):
        """测试绘制圆形不抛出错误"""
        circle = FreeCircle(test_screen, **default_circle_params)

        try:
            circle.draw()
        except Exception as e:
            pytest.fail(f"绘制圆形时抛出异常: {e}")

    def test_circle_draw_bezier(self, test_screen, default_circle_params):
        """测试绘制贝塞尔曲线"""
        circle = FreeCircle(test_screen, **default_circle_params)
        points = [(100, 100), (150, 50), (200, 150), (250, 100)]

        try:
            circle.draw_bezier(test_screen, points, 50, (255, 0, 0))
        except Exception as e:
            pytest.fail(f"绘制贝塞尔曲线时抛出异常: {e}")

    def test_circle_str_representation(self, test_screen, default_circle_params):
        """测试圆形的字符串表示"""
        circle = FreeCircle(test_screen, **default_circle_params)

        assert str(circle) == "自定义圆，弧，曲线类"
        assert repr(circle) == "自定义圆，弧，曲线类"

    def test_circle_different_configurations(self, test_screen):
        """测试不同配置的圆形绘制"""
        test_cases = [
            # (参数, 描述)
            (
                {
                    "coordinates": [400, 300],
                    "radius": 50,
                    "width": 0,  # 实心
                    "aa": True,
                    "angle": (0, 360),
                },
                "实心抗锯齿圆",
            ),
            (
                {
                    "coordinates": [400, 300],
                    "radius": 50,
                    "width": 2,
                    "aa": False,
                    "angle": (0, 360),
                },
                "非抗锯齿空心圆",
            ),
            (
                {
                    "coordinates": [400, 300],
                    "radius": 50,
                    "width": 2,
                    "aa": True,
                    "angle": (45, 270),  # 弧
                },
                "抗锯齿弧",
            ),
            (
                {
                    "coordinates": [400, 300],
                    "radius": 50,
                    "width": 2,
                    "rect": (60, 40),  # 椭圆
                    "aa": False,
                    "angle": (0, 360),
                },
                "椭圆",
            ),
        ]

        for params, description in test_cases:
            circle = FreeCircle(test_screen, **params)
            try:
                circle.draw()
            except Exception as e:
                pytest.fail(f"绘制{description}时抛出异常: {e}")


class TestSuperCircle:
    """测试 SuperCircle 类"""

    def test_super_circle_creation(self, test_screen, default_circle_params):
        """测试超级圆形创建"""
        circle = SuperCircle(test_screen, **default_circle_params)
        assert circle is not None
        assert isinstance(circle, SuperCircle)
        assert isinstance(circle, FreeCircle)

    def test_super_circle_lshift_operator(self, test_screen, default_circle_params):
        """测试 << 操作符快捷设置"""
        circle = SuperCircle(test_screen, **default_circle_params)

        # 测试设置半径
        circle << (75,)
        assert circle.radius == 75

        # 测试设置长短半轴
        circle << ((80, 60),)
        assert circle.rect == (80, 60)

        # 测试设置颜色
        circle << ((255, 0, 0),)
        assert circle.color == (255, 0, 0)

        # 测试冗余参数
        with pytest.raises(AssertionError):
            circle << (1, 2, 3, 4)

    def test_super_circle_open_border_angle(self, test_screen, default_circle_params):
        """测试开启弧边缘边框"""
        circle = SuperCircle(test_screen, **default_circle_params)

        angle = (45, 180)
        circle.open_border_angle(angle)
        assert circle._border_angle == list(angle)

    def test_super_circle_draw_scircle_static(self, test_screen):
        """测试静态绘制普通圆"""
        try:
            SuperCircle.draw_scircle(test_screen, (100, 100), 50, 2, (255, 0, 0))
        except Exception as e:
            pytest.fail(f"draw_scircle 抛出异常: {e}")

    def test_super_circle_inheritance(self, test_screen, default_circle_params):
        """测试继承关系"""
        circle = SuperCircle(test_screen, **default_circle_params)

        # 应该继承自 FreeCircle 和 FreeAllCircle
        assert isinstance(circle, FreeCircle)
        # 检查是否可以通过 SuperCircle 调用 FreeAllCircle 的静态方法
        try:
            SuperCircle.draw_circle(test_screen, (100, 100), 50, 2, (255, 0, 0))
        except Exception as e:
            pytest.fail(f"通过 SuperCircle 调用静态方法时抛出异常: {e}")


class TestFreeText:
    """测试 FreeText 类"""

    def test_text_creation(self, test_screen, default_text_params):
        """测试文本创建"""
        text = FreeText(test_screen, **default_text_params)
        assert text is not None
        assert text.msg == "测试文本"
        assert text.x == 200
        assert text.y == 200
        assert text.color == (0, 0, 0)

    def test_text_get_attribute(self, test_screen, default_text_params):
        """测试获取文本属性"""
        text = FreeText(test_screen, **default_text_params)
        attributes = text.get_attribute()

        assert isinstance(attributes, dict)
        assert attributes["msg"] == "测试文本"
        assert attributes["coordinates"] == [200, 200]
        assert attributes["color"] == (0, 0, 0)
        assert attributes["size"] == 24

    def test_text_get_coordinates(self, test_screen, default_text_params):
        """测试获取文本坐标"""
        text = FreeText(test_screen, **default_text_params)
        coords = text.get_coordinates()
        assert coords == [200, 200]

    def test_text_set_properties(self, test_screen, default_text_params):
        """测试设置文本属性"""
        text = FreeText(test_screen, **default_text_params)

        # 测试设置颜色
        new_color = (255, 0, 0)
        text.set_color(new_color)
        assert text.color == new_color

        # 测试设置字体
        new_font = None  # 使用默认字体
        text.set_fout(new_font)

        # 测试设置大小
        new_size = 36
        text.set_size(new_size)
        assert text.size == new_size

        # 测试设置消息
        new_msg = "新消息"
        text.set_msg(new_msg)
        assert text.msg == new_msg

        # 测试设置坐标
        new_coords = [300, 400]
        text.set_coordinates(new_coords)
        assert text.x == 300
        assert text.y == 400

    def test_text_draw_no_error(self, test_screen, default_text_params):
        """测试绘制文本不抛出错误"""
        text = FreeText(test_screen, **default_text_params)

        try:
            text.draw()
        except Exception as e:
            pytest.fail(f"绘制文本时抛出异常: {e}")

    def test_text_str_representation(self, test_screen, default_text_params):
        """测试文本的字符串表示"""
        text = FreeText(test_screen, **default_text_params)

        assert str(text) == "自定义文本类"
        assert repr(text) == "自定义文本类"

    def test_text_with_pygame_font_object(self, test_screen):
        """测试使用 Pygame 字体对象"""
        pygame_font = pygame.font.Font(None, 24)
        text = FreeText(test_screen, [100, 100], "测试", pygame_font, 24, (0, 0, 0))

        assert text.font == pygame_font
        try:
            text.draw()
        except Exception as e:
            pytest.fail(f"使用 Pygame 字体对象绘制时抛出异常: {e}")
