"""
测试配置文件 conftest.py
为 freepygame 库提供测试配置和共享的测试工具
"""

import os
import sys

import pygame
import pytest

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def pygame_init():
    """初始化 Pygame 用于测试"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def test_screen(pygame_init):
    """创建一个测试用的 Pygame 屏幕"""
    # 使用虚拟显示模式进行测试
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    screen = pygame.Surface((800, 600))
    yield screen
    # 清理


@pytest.fixture
def default_button_params():
    """返回默认的按钮参数"""
    return {
        "coordinates": [100, 100],
        "button_size": [200, 50],
        "msg": "测试按钮",
        "font": None,  # 使用默认字体
        "size": 24,
        "border_width": 1,
        "draw_border": True,
        "draw_line": False,
        "msg_tran": False,
        "line_width": 1,
        "button_color": (0, 0, 0),
        "text_color": (255, 255, 255),
        "border_color": (0, 0, 0),
        "line_color": (255, 255, 255),
        "dsm": 1,
    }


@pytest.fixture
def default_circle_params():
    """返回默认的圆形参数"""
    return {
        "coordinates": [400, 300],
        "radius": 50,
        "width": 1,
        "rect": (0, 0),
        "angle": (0, 360),
        "aa": True,
        "draw_border": False,
        "border_width": 1,
        "color": (0, 0, 0),
        "border_color": (0, 0, 0),
    }


@pytest.fixture
def default_text_params():
    """返回默认的文本参数"""
    return {
        "coordinates": [200, 200],
        "msg": "测试文本",
        "font": None,  # 使用默认字体
        "size": 24,
        "color": (0, 0, 0),
    }


@pytest.fixture
def mock_font():
    """创建一个模拟的字体对象"""

    class MockFont:
        def __init__(self, font_path=None, size=24):
            self.size = size
            self.font_path = font_path

        def render(self, text, antialias, color, background=None):
            # 创建一个简单的表面来模拟字体渲染
            surface = pygame.Surface((len(text) * 10, self.size))
            if background:
                surface.fill(background)
            return surface

    return MockFont


def pytest_configure(config):
    """Pytest 配置钩子"""
    # 设置测试标记
    config.addinivalue_line("markers", "slow: 标记为慢速测试（需要实际渲染）")
    config.addinivalue_line("markers", "visual: 标记为视觉测试（需要人工验证）")
    config.addinivalue_line("markers", "integration: 标记为集成测试")


def pytest_collection_modifyitems(config, items):
    """修改测试收集"""
    # 如果设置了快速测试模式，跳过慢速测试
    if config.getoption("--quick"):
        skip_slow = pytest.mark.skip(reason="在快速测试模式下跳过")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)


def pytest_addoption(parser):
    """添加自定义命令行选项"""
    parser.addoption(
        "--quick", action="store_true", default=False, help="快速测试模式：跳过慢速测试"
    )
    parser.addoption(
        "--visual", action="store_true", default=False, help="运行视觉测试（需要显示）"
    )
