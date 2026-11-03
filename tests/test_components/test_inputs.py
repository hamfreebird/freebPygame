"""
测试新增输入类控件：InputBox、Dropdown、Switch、RadioButton/RadioGroup，
以及 FreeFrame 对焦点/键盘/悬停的事件分发。
"""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
import pytest

from freepygame import (
    Dropdown,
    FreeFrame,
    InputBox,
    RadioButton,
    RadioGroup,
    Switch,
    get_theme,
)


class TestInputBox:
    def test_value_roundtrip(self, test_screen):
        box = InputBox(test_screen, [0, 0], width=200, value="hi")
        assert box.get_value() == "hi"
        assert box._cursor == 2
        box.set_value("")
        assert box.get_value() == "" and box._cursor == 0

    def test_focus_blur(self, test_screen):
        box = InputBox(test_screen, [0, 0], width=200)
        assert box.handle_click((10, 10)) is True
        assert box.focused is True
        box.blur()
        assert box.focused is False
        assert box.handle_click((999, 999)) is False

    def test_type_and_backspace(self, test_screen):
        changed = []
        box = InputBox(test_screen, [0, 0], width=200, on_change=lambda v: changed.append(v))
        box.focus()
        for ch in "abc":
            box.handle_key(pygame.event.Event(pygame.KEYDOWN, key=ord(ch), unicode=ch))
        assert box.get_value() == "abc"
        box.handle_key(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, unicode=""))
        assert box.get_value() == "ab"
        assert changed[-1] == "ab"

    def test_cursor_movement(self, test_screen):
        box = InputBox(test_screen, [0, 0], width=200, value="abcd")
        box.focus()
        box.handle_key(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, unicode=""))
        assert box._cursor == 3
        box.handle_key(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_HOME, unicode=""))
        assert box._cursor == 0
        box.handle_key(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_END, unicode=""))
        assert box._cursor == 4

    def test_max_length(self, test_screen):
        box = InputBox(test_screen, [0, 0], width=200, max_length=3)
        box.focus()
        for ch in "abcd":
            box.handle_key(pygame.event.Event(pygame.KEYDOWN, key=ord(ch), unicode=ch))
        assert box.get_value() == "abc"

    def test_submit_callback(self, test_screen):
        submitted = []
        box = InputBox(
            test_screen, [0, 0], width=200, value="x", on_submit=lambda v: submitted.append(v)
        )
        box.focus()
        box.handle_key(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, unicode=""))
        assert submitted == ["x"]

    def test_password_and_placeholder_draw(self, test_screen):
        box = InputBox(test_screen, [0, 0], width=200, password=True, placeholder="输入")
        box.draw()
        box.set_value("secret")
        box.focus()
        box.draw()

    def test_theme_applies(self, test_screen):
        box = InputBox(test_screen, [0, 0], width=200, theme=get_theme("dark"))
        assert box.focus_border_color == get_theme("dark").primary


class TestDropdown:
    def test_default_selection(self, test_screen):
        dd = Dropdown(test_screen, [0, 0], width=150, options=["A", "B", "C"])
        assert dd.get_selected() == (-1, None)
        dd.set_selected(1)
        assert dd.get_selected() == (1, "B")

    def test_open_and_select(self, test_screen):
        picked = []
        dd = Dropdown(
            test_screen, [0, 0], width=150, options=["A", "B", "C"], on_select=lambda i, v: picked.append((i, v))
        )
        # open via header
        assert dd.handle_click((10, 10)) is True
        assert dd.open is True
        # click on second item (panel starts at y + height; items are height tall)
        # y = 10 + 30 (header) + 31 -> 71 lands in the 2nd item band (60..90)
        assert dd.handle_click((10, 71)) is True
        assert dd.open is False
        assert dd.selected_index == 1
        assert picked == [(1, "B")]

    def test_click_outside_item_closes(self, test_screen):
        dd = Dropdown(test_screen, [0, 0], width=150, options=["A", "B", "C"])
        dd.handle_click((10, 10))
        assert dd.open is True
        # far away -> closes, not consumed
        assert dd.handle_click((999, 999)) is False
        assert dd.open is False

    def test_hover_tracking(self, test_screen):
        dd = Dropdown(test_screen, [0, 0], width=150, options=["A", "B", "C"])
        dd.open = True
        dd.on_mouse_move((10, 75))  # y=75 -> 2nd item band (60..90)
        assert dd._hover_index == 1
        dd.on_mouse_move((999, 999))
        assert dd._hover_index == -1

    def test_draw(self, test_screen):
        dd = Dropdown(test_screen, [0, 0], width=150, options=["A", "B", "C"], selected_index=0)
        dd.draw()
        dd.handle_click((10, 10))
        dd.draw()


class TestSwitch:
    def test_toggle(self, test_screen):
        changed = []
        sw = Switch(test_screen, [0, 0], on_change=lambda v: changed.append(v))
        assert sw.checked is False
        assert sw.handle_click((5, 5)) is True
        assert sw.checked is True and changed == [True]
        assert sw.handle_click((5, 5)) is True
        assert sw.checked is False and changed == [True, False]

    def test_draw(self, test_screen):
        sw = Switch(test_screen, [0, 0], checked=True)
        sw.draw()


class TestRadioGroup:
    def test_single_select(self, test_screen):
        group = RadioGroup()
        changes = []
        group.on_change = lambda b: changes.append(b.value)
        r1 = RadioButton(test_screen, [0, 0], label="One", value=1)
        r2 = RadioButton(test_screen, [0, 0], label="Two", value=2)
        group.add(r1).add(r2)
        r2.handle_click((5, 5))
        assert r2.checked is True and r1.checked is False
        assert group.get_selected() is r2
        assert changes == [2]
        r1.handle_click((5, 5))
        assert r1.checked is True and r2.checked is False


class TestFreeFrameInputIntegration:
    def test_focus_and_keyboard_dispatch(self):
        # FreeFrame.__init__ initializes Pygame itself; the session-scoped
        # pygame_init fixture handles teardown, so we don't quit here.
        app = FreeFrame(size=(400, 300), fps=60)
        box = InputBox(app.screen, [50, 50], width=200)
        app.add_widget(box)

        # Click inside the input -> gains focus through the frame dispatcher.
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(60, 60), button=1))
        # Then type "hi".
        for ch in "hi":
            pygame.event.post(
                pygame.event.Event(pygame.KEYDOWN, key=ord(ch), unicode=ch)
            )
        app.handle_events()

        assert app.focused_widget is box
        assert box.get_value() == "hi"

    def test_mouse_move_hover(self):
        app = FreeFrame(size=(400, 300), fps=60)
        dd = Dropdown(app.screen, [10, 10], width=150, options=["A", "B"])
        app.add_widget(dd)
        pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION, pos=(10, 10 + 30 + 5)))
        app.handle_events()
        assert dd.open is False
        dd.open = True
        pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION, pos=(10, 75)))
        app.handle_events()
        assert dd._hover_index == 1
