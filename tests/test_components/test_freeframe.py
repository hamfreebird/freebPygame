"""FreeFrame 主循环与交互测试（headless）。

注意：``run()`` 结尾会调用 ``quit()`` -> ``pygame.quit()``。测试中用
monkeypatch 替换 ``quit``，避免关闭全局 Pygame 状态而污染后续测试。
"""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from freepygame import FreeButton, FreeFrame, InputBox


def _make_frame(**kwargs):
    kwargs.setdefault("size", (240, 160))
    kwargs.setdefault("fps", 240)
    return FreeFrame(**kwargs)


def _post_click(pos):
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1))


class TestFreeFrameLoop:
    def test_run_processes_frame_and_exits_on_quit(self, monkeypatch):
        app = _make_frame()
        monkeypatch.setattr(app, "quit", lambda: None)
        calls = []
        app.update = lambda: calls.append("update")
        app.draw = lambda: calls.append("draw")

        pygame.event.clear()
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        app.run()

        assert calls == ["update", "draw"]
        assert app.running is False

    def test_run_stops_when_running_set_false(self, monkeypatch):
        app = _make_frame()
        monkeypatch.setattr(app, "quit", lambda: None)
        frames = []

        def update():
            frames.append(1)
            if len(frames) >= 3:
                app.running = False

        app.update = update
        app.draw = lambda: None
        pygame.event.clear()
        app.run()

        assert len(frames) == 3

    def test_run_calls_quit_on_exit(self, monkeypatch):
        app = _make_frame()
        called = []
        monkeypatch.setattr(app, "quit", lambda: called.append(True))

        def update():
            app.running = False

        app.update = update
        app.draw = lambda: None
        pygame.event.clear()
        app.run()

        assert called == [True]


class TestFreeFrameApi:
    def test_str_repr_and_setters(self):
        app = _make_frame(title="before")
        assert "FreeFrame" in str(app)
        assert repr(app) == str(app)
        app.set_title("after")
        assert app.title == "after"
        app.set_background_color((1, 2, 3))
        assert app.background_color == (1, 2, 3)
        assert app.get_fps() >= 0

    def test_add_widget_is_chainable(self):
        app = _make_frame()
        button = FreeButton(app.screen, [10, 10], [60, 24], msg="x")
        assert app.add_widget(button) is button
        assert button in app.widgets


class TestFreeFrameInteraction:
    def test_focus_moves_between_inputs(self):
        app = _make_frame()
        first = InputBox(app.screen, [10, 10], width=80)
        second = InputBox(app.screen, [10, 50], width=80)
        app.add_widget(first)
        app.add_widget(second)

        _post_click((20, 20))
        app.handle_events()
        assert app.focused_widget is first
        assert first.focused is True and second.focused is False

        _post_click((20, 60))
        app.handle_events()
        assert app.focused_widget is second
        assert first.focused is False and second.focused is True

    def test_click_empty_area_blurs_focus(self):
        app = _make_frame()
        box = InputBox(app.screen, [10, 10], width=80)
        app.add_widget(box)

        _post_click((20, 20))
        app.handle_events()
        assert app.focused_widget is box

        _post_click((220, 150))
        app.handle_events()
        assert app.focused_widget is None
        assert box.focused is False

    def test_keydown_without_focus_is_safe(self):
        app = _make_frame()
        pygame.event.clear()
        pygame.event.post(
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a, unicode="a")
        )
        app.handle_events()
        assert app.focused_widget is None

    def test_keydown_reaches_focused_input(self):
        app = _make_frame()
        box = InputBox(app.screen, [10, 10], width=80)
        app.add_widget(box)

        _post_click((20, 20))
        app.handle_events()
        assert app.focused_widget is box

        pygame.event.clear()
        pygame.event.post(
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_x, unicode="x")
        )
        app.handle_events()
        assert box.get_value() == "x"

    def test_topmost_widget_wins_overlapping_click(self):
        app = _make_frame()
        bottom = FreeButton(app.screen, [10, 10], [80, 30], msg="b")
        top = FreeButton(app.screen, [10, 10], [80, 30], msg="t")
        hits = []
        bottom.set_callback(lambda _w: hits.append("bottom"))
        top.set_callback(lambda _w: hits.append("top"))
        app.add_widget(bottom)
        app.add_widget(top)

        _post_click((20, 20))
        app.handle_events()
        assert hits == ["top"]
