"""
测试 freepygame 中的按钮组件
包括 FreeButton 和 CircleButton
"""

import pygame
import pytest

from freepygame import CircleButton, FreeButton, position_button, position_button_class


class TestPositionButtonFunctions:
    """测试位置判断函数"""

    def test_position_button_inside(self):
        """测试点在矩形内部"""
        rect = (100, 200, 150, 250)  # x1, x2, y1, y2
        pos = (150, 180)
        assert position_button(rect, pos) is True

    def test_position_button_outside(self):
        """测试点在矩形外部"""
        rect = (100, 200, 150, 250)
        pos = (50, 180)
        assert position_button(rect, pos) is False

    def test_position_button_on_edge(self):
        """测试点在矩形边缘"""
        rect = (100, 200, 150, 250)
        pos = (100, 150)
        assert position_button(rect, pos) is True

    def test_position_button_with_list(self):
        """测试使用列表作为矩形参数"""
        rect = [100, 200, 150, 250]
        pos = (150, 180)
        assert position_button(rect, pos) is True


class TestFreeButton:
    """测试 FreeButton 类"""

    def test_button_creation(self, test_screen, default_button_params):
        """测试按钮创建"""
        button = FreeButton(test_screen, **default_button_params)
        assert button is not None
        assert button.msg == "测试按钮"
        assert button.width == 200
        assert button.height == 50
        assert button.coordinates == [100, 100]

    def test_button_get_attribute(self, test_screen, default_button_params):
        """测试获取按钮属性"""
        button = FreeButton(test_screen, **default_button_params)
        attributes = button.get_attribute()

        assert isinstance(attributes, dict)
        assert attributes["msg"] == "测试按钮"
        assert attributes["button_size"] == [200, 50]
        assert attributes["coordinates"] == [100, 100]
        assert attributes["draw_border"] is True
        assert attributes["draw_line"] is False

    def test_button_get_coordinates(self, test_screen, default_button_params):
        """测试获取按钮坐标"""
        button = FreeButton(test_screen, **default_button_params)
        coords = button.get_coordinates()

        assert isinstance(coords, list)
        assert len(coords) == 4
        # 左上角
        assert coords[0] == [100, 100]
        # 右上角
        assert coords[1] == [300, 100]
        # 右下角
        assert coords[2] == [300, 150]
        # 左下角
        assert coords[3] == [100, 150]

    def test_button_set_msg(self, test_screen, default_button_params):
        """测试设置按钮文本"""
        button = FreeButton(test_screen, **default_button_params)
        new_msg = "新文本"
        button.set_msg(new_msg)

        assert button.msg == new_msg

    def test_button_set_colors(self, test_screen, default_button_params):
        """测试设置按钮颜色"""
        button = FreeButton(test_screen, **default_button_params)

        # 测试设置按钮颜色
        new_button_color = (255, 0, 0)
        button.set_button_color(new_button_color)
        assert button.button_color == new_button_color

        # 测试设置文本颜色
        new_text_color = (0, 255, 0)
        button.set_text_color(new_text_color)

        # 测试设置边框颜色
        new_border_color = (0, 0, 255)
        button.set_border_color(new_border_color)
        assert button.border[1] == new_border_color

        # 测试设置线颜色
        new_line_color = (255, 255, 0)
        button.set_line_color(new_line_color)
        assert button.line[1] == new_line_color

    def test_button_set_dimensions(self, test_screen, default_button_params):
        """测试设置按钮尺寸相关属性"""
        button = FreeButton(test_screen, **default_button_params)

        # 测试设置边框宽度
        new_border_width = 3
        button.set_border_width(new_border_width)
        assert button.border[0] == new_border_width

        # 测试设置线宽度
        new_line_width = 2
        button.set_line_width(new_line_width)
        assert button.line[0] == new_line_width

    def test_button_toggle_features(self, test_screen, default_button_params):
        """测试切换按钮特性"""
        button = FreeButton(test_screen, **default_button_params)

        # 测试切换边框显示
        button.open_border(False)
        assert button.draw_border is False
        button.open_border(True)
        assert button.draw_border is True

        # 测试切换线显示
        button.open_line(True)
        assert button.draw_line is True
        button.open_line(False)
        assert button.draw_line is False

    def test_button_set_msg_tran(self, test_screen, default_button_params):
        """测试设置文本透明"""
        button = FreeButton(test_screen, **default_button_params)

        button.set_msg_tran(True)
        assert button.msg_tran is True

        button.set_msg_tran(False)
        assert button.msg_tran is False

    def test_button_draw_no_error(self, test_screen, default_button_params):
        """测试绘制按钮不抛出错误"""
        button = FreeButton(test_screen, **default_button_params)

        # 绘制应该不抛出异常
        try:
            button.draw()
        except Exception as e:
            pytest.fail(f"绘制按钮时抛出异常: {e}")

    def test_button_str_representation(self, test_screen, default_button_params):
        """测试按钮的字符串表示"""
        button = FreeButton(test_screen, **default_button_params)

        assert str(button) == "基础按钮类"
        assert repr(button) == "基础按钮类"

    def test_button_with_dsm(self, test_screen):
        """测试带缩放系数的按钮"""
        params = {
            "coordinates": [100, 100],
            "button_size": [200, 50],
            "msg": "缩放按钮",
            "dsm": 2,  # 2倍缩放
        }

        button = FreeButton(test_screen, **params)
        assert button.dsm == 2
        assert button.width == 400  # 200 * 2
        assert button.height == 100  # 50 * 2
        assert button.coordinates == [200, 200]  # 100 * 2


class TestCircleButton:
    """测试 CircleButton 类"""

    def test_circle_button_creation(self, test_screen):
        """测试圆形按钮创建"""
        params = {
            "coordinates": [400, 300],
            "radius": 50,
            "msg": "圆形按钮",
        }

        button = CircleButton(test_screen, **params)
        assert button is not None
        assert button.msg == "圆形按钮"
        assert button.radius == 50
        assert button.coordinates == [400, 300]

    def test_circle_button_inheritance(self, test_screen):
        """测试圆形按钮继承关系"""
        params = {
            "coordinates": [400, 300],
            "radius": 50,
            "msg": "测试",
        }

        button = CircleButton(test_screen, **params)
        assert isinstance(button, CircleButton)
        # CircleButton 应该继承自 FreeCircle
        from freepygame import FreeCircle

        assert isinstance(button, FreeCircle)

    def test_circle_button_set_msg(self, test_screen):
        """测试设置圆形按钮文本"""
        params = {
            "coordinates": [400, 300],
            "radius": 50,
            "msg": "原始文本",
        }

        button = CircleButton(test_screen, **params)
        new_msg = "新文本"
        button.set_msg(new_msg)

        assert button.msg == new_msg

    def test_circle_button_set_colors(self, test_screen):
        """测试设置圆形按钮颜色"""
        params = {
            "coordinates": [400, 300],
            "radius": 50,
            "msg": "测试",
            "button_color": (0, 0, 0),
            "msg_color": (255, 255, 255),
        }

        button = CircleButton(test_screen, **params)

        # 测试设置按钮颜色
        new_button_color = (255, 0, 0)
        button.set_button_color(new_button_color)
        assert button.button_color == new_button_color
        assert button.color == new_button_color  # 应该同时设置父类的颜色

        # 测试设置消息颜色
        new_msg_color = (0, 255, 0)
        button.set_msg_color(new_msg_color)
        assert button.msg_color == new_msg_color

    def test_circle_button_set_msg_tran(self, test_screen):
        """测试设置圆形按钮文本透明"""
        params = {
            "coordinates": [400, 300],
            "radius": 50,
            "msg": "测试",
            "msg_tran": False,
        }

        button = CircleButton(test_screen, **params)

        button.set_msg_tran(True)
        assert button.msg_tran is True

        button.set_msg_tran(False)
        assert button.msg_tran is False

    def test_circle_button_draw_no_error(self, test_screen):
        """测试绘制圆形按钮不抛出错误"""
        params = {
            "coordinates": [400, 300],
            "radius": 50,
            "msg": "测试",
        }

        button = CircleButton(test_screen, **params)

        # 绘制应该不抛出异常
        try:
            button.draw()
        except Exception as e:
            pytest.fail(f"绘制圆形按钮时抛出异常: {e}")

    def test_circle_button_with_dsm(self, test_screen):
        """测试带缩放系数的圆形按钮"""
        params = {
            "coordinates": [400, 300],
            "radius": 50,
            "msg": "缩放圆形按钮",
            "dsm": 2,
        }

        button = CircleButton(test_screen, **params)
        assert button.dsm == 2


class TestPositionButtonClass:
    """测试 position_button_class 函数"""

    def test_position_button_class_with_freebutton(
        self, test_screen, default_button_params
    ):
        """测试 position_button_class 与 FreeButton"""
        button = FreeButton(test_screen, **default_button_params)

        # 测试按钮内部点
        inside_pos = (200, 125)  # 按钮中心附近
        assert position_button_class(button, inside_pos) is True

        # 测试按钮外部点
        outside_pos = (50, 50)
        assert position_button_class(button, outside_pos) is False

        # 测试按钮边缘点
        edge_pos = (100, 100)  # 左上角
        assert position_button_class(button, edge_pos) is True

    def test_position_button_class_with_circlebutton(self, test_screen):
        """测试 position_button_class 与 CircleButton"""
        params = {
            "coordinates": [400, 300],
            "radius": 50,
            "msg": "测试",
        }

        button = CircleButton(test_screen, **params)

        # 注意：position_button_class 对圆形按钮使用外切矩形坐标
        # 外切矩形应该是 [350, 450, 250, 350] (x1, x2, y1, y2)

        # 测试外切矩形内部点
        inside_pos = (400, 300)  # 圆心
        assert position_button_class(button, inside_pos) is True

        # 测试外切矩形外部点
        outside_pos = (200, 200)
        assert position_button_class(button, outside_pos) is False
