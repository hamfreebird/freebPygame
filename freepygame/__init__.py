# pygame控件合集   by freebird

__version__ = "0.1.0"
__author__ = "freebird"
__license__ = "Apache License 2.0"

# 导出主要类
from .freebutton import CircleButton, FreeButton, position_button, position_button_class
from .freecircle import FreeAllCircle, FreeCircle, SuperCircle
from .freeicon import FreeIcon
from .freeparticle import Fireworks, Particle, ParticleEngine, explode

# 导出 freepygamelib 中的所有内容
from .freepygamelib import *
from .freetext import FreeMsg, FreeText, MidSuperText, NaSuperText, SuperText
from .freetransformation import array_mean_rgba, image_blur_processing, map_to_rgba

# 定义 __all__ 以便 from freepygame import * 时只导入这些
__all__ = [
    # 按钮相关
    "FreeButton",
    "CircleButton",
    "position_button",
    "position_button_class",
    # 圆形相关
    "FreeCircle",
    "SuperCircle",
    "FreeAllCircle",
    # 文本相关
    "FreeText",
    "SuperText",
    "NaSuperText",
    "MidSuperText",
    "FreeMsg",
    # 其他组件
    "FreeIcon",
    # 粒子系统
    "Particle",
    "ParticleEngine",
    "Fireworks",
    "explode",
    # 图像处理
    "image_blur_processing",
    "array_mean_rgba",
    "map_to_rgba",
    # 版本信息
    "__version__",
    "__author__",
    "__license__",
]
