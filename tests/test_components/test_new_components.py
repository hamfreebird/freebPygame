"""
测试新增能力：按钮点击回调、主题、控件（ProgressBar/Slider/CheckBox）、
布局管理器（VBox/HBox/AnchorLayout）、以及 FreeFrame 的控件承载与事件分发。
"""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
import pytest

from freepygame import (
    AnchorLayout,
    CheckBox,
    CircleButton,
    FreeButton,
    FreeFrame,
    HBox,
    ProgressBar,
    Slider,
    VBox,
    apply_theme,
    get_theme,
)


class TestClickable:
    """测试按钮的点击回调。"""

    def test_freebutton_callback(self, test_screen):
        hits = []
        b = FreeButton(test_screen, [10, 10], [100, 40], msg="OK")
        b.set_callback(lambda self: hits.append(self.msg))
        assert b.handle_click((50, 30)) is True
        assert hits == ["OK"]
        assert b.handle_click((300, 300)) is False
        assert hits == ["OK"]

    def test_disabled_ignores(self, test_screen):
        b = FreeButton(test_screen, [10, 10], [100, 40], msg="OK")
        b.enabled = False
        assert b.handle_click((50, 30)) is False

    def test_circlebutton_callback(self, test_screen):
        hits = []
        cb = CircleButton(test_screen, [200, 150], 30, msg="C")
        cb.set_callback(lambda self: hits.append(1))
        assert cb.handle_click((200, 150)) is True
        assert hits == [1]


class TestTheme:
    """测试主题系统。"""

    def test_get_theme_fallback(self):
        assert get_theme("nope").name == "light"
        assert get_theme("dark").name == "dark"

    def test_apply_theme(self, test_screen):
        b = FreeButton(test_screen, [0, 0], [80, 30], msg="x")
        apply_theme(b, get_theme("dark"))
        assert b.button_color == get_theme("dark").primary


class TestWidgets:
    """测试新控件。"""

    def test_progressbar(self, test_screen):
        pb = ProgressBar(test_screen, [0, 0], width=100, value=0.5)
        assert pb.get_value() == 0.5
        pb.set_value(1.5)
        assert pb.get_value() == 1.0
        pb.set_value(-1)
        assert pb.get_value() == 0.0
        pb.draw()

    def test_slider(self, test_screen):
        sl = Slider(
            test_screen, [0, 0], width=100, min_value=0, max_value=100, value=20
        )
        assert sl.get_value() == 20
        assert sl.contains((50, 8)) is True
        assert sl.set_from_pos((50, 8)) is True
        sl.set_value(75)
        assert sl.get_value() == 75
        sl.draw()

    def test_slider_outside(self, test_screen):
        sl = Slider(test_screen, [0, 0], width=100, value=0)
        assert sl.set_from_pos((500, 500)) is False

    def test_checkbox(self, test_screen):
        toggled = []
        ck = CheckBox(test_screen, [0, 0], size=20, checked=False)
        ck.on_toggle = lambda v: toggled.append(v)
        assert ck.handle_click((10, 10)) is True
        assert ck.checked is True and toggled == [True]
        assert ck.handle_click((200, 200)) is False
        ck.draw()


class TestLayout:
    """测试布局管理器。"""

    def test_vbox(self, test_screen):
        pb = ProgressBar(test_screen, [0, 0], width=50, height=10)
        sl = Slider(test_screen, [0, 0], width=50, height=10)
        v = VBox([pb, sl], spacing=5, padding=0)
        v.arrange(origin=(0, 0))
        assert pb.coordinates == [0, 0]
        assert sl.coordinates == [0, 15]

    def test_hbox(self, test_screen):
        pb = ProgressBar(test_screen, [0, 0], width=50, height=10)
        sl = Slider(test_screen, [0, 0], width=50, height=10)
        h = HBox([pb, sl], spacing=5, padding=0)
        h.arrange(origin=(0, 0))
        assert pb.coordinates == [0, 0]
        assert sl.coordinates == [55, 0]

    def test_anchor_center(self, test_screen):
        pb = ProgressBar(test_screen, [0, 0], width=50, height=10)
        a = AnchorLayout([pb], align="center")
        a.arrange(origin=(100, 100))
        assert pb.coordinates == [75, 95]


class TestFreeFrameWidgets:
    """测试 FreeFrame 承载控件并分发点击事件。"""

    def test_add_widget_and_dispatch(self):
        # FreeFrame.__init__ initializes Pygame itself; the session-scoped
        # pygame_init fixture handles teardown, so we don't quit here.
        app = FreeFrame(size=(300, 200), fps=60)
        hits = []
        btn = FreeButton(app.screen, [20, 20], [80, 30], msg="X")
        btn.set_callback(lambda self: hits.append(1))
        app.add_widget(btn)
        assert btn in app.widgets
        # 在按钮中心模拟一次鼠标按下事件
        ev = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(60, 35), button=1)
        pygame.event.post(ev)
        app.handle_events()
        assert hits == [1]
