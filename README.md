# freepygame

一个为 Pygame 游戏开发提供 UI 控件和工具的 Python 库。

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/freepygame.svg)](https://badge.fury.io/py/freepygame)
[![PyPI downloads](https://img.shields.io/pypi/dm/freepygame.svg)](https://pypi.org/project/freepygame/)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-orange)](https://www.pygame.org/)

## 特性

- 🎨 **丰富的 UI 组件**: 按钮、文本、圆形、图标等
- 🔧 **易于使用**: 简单的 API 和直观的接口
- 🎯 **灵活配置**: 支持颜色、大小、位置等属性动态调整
- ✨ **特效支持**: 粒子系统、图像处理等高级功能

## 安装

```bash
pip install freepygame
```

或者从源代码安装:

```bash
git clone https://github.com/freebird/freebPygame.git
cd freebPygame
pip install -e .
```

## 快速开始

```python
import pygame
from freepygame import FreeButton, FreeText, position_button_class

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 创建按钮
button = FreeButton(
    screen=screen,
    coordinates=[100, 100],
    button_size=[200, 50],
    msg="点击我",
    button_color=(70, 130, 180),
    text_color=(255, 255, 255)
)

# 创建文本
text = FreeText(
    screen=screen,
    coordinates=[100, 170],
    msg="欢迎使用 freepygame!",
    color=(0, 0, 0)
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if position_button_class(button, pygame.mouse.get_pos()):
                text.set_msg("按钮被点击了!")
    
    # 绘制
    screen.fill((240, 240, 245))
    button.draw()
    text.draw()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

## 主要组件

### 按钮组件

#### FreeButton - 矩形按钮
```python
button = FreeButton(
    screen=screen,
    coordinates=[x, y],          # 左上角坐标
    button_size=[width, height], # 按钮尺寸
    msg="按钮文本",              # 显示文本
    button_color=(r, g, b),      # 按钮背景色
    text_color=(r, g, b),        # 文本颜色
    draw_border=True,            # 是否显示边框
    border_width=2,              # 边框宽度
    dsm=1                        # 缩放系数
)
```

#### CircleButton - 圆形按钮
```python
circle_btn = CircleButton(
    screen=screen,
    coordinates=[x, y],          # 圆心坐标
    radius=50,                   # 半径
    msg="圆形按钮",              # 显示文本
    button_color=(r, g, b),      # 按钮颜色
    msg_color=(r, g, b)          # 文本颜色
)
```

### 文本组件

#### FreeText - 基础文本
```python
text = FreeText(
    screen=screen,
    coordinates=[x, y],          # 文本位置
    msg="文本内容",              # 显示文本
    font=None,                   # 字体文件路径或 Pygame 字体对象
    size=24,                     # 字体大小
    color=(r, g, b)              # 文本颜色
)
```

#### SuperText - 超级文本（支持缩放）
```python
super_text = SuperText(
    screen=screen,
    coordinates=[x, y],
    msg="支持缩放的文本",
    size=24,
    color=(r, g, b),
    dsm=1.5  # 1.5倍缩放
)
```

### 图形组件

#### FreeCircle - 圆形/弧形
```python
circle = FreeCircle(
    screen=screen,
    coordinates=[x, y],          # 圆心坐标
    radius=50,                   # 半径
    width=2,                     # 线宽（0为实心）
    angle=(0, 360),              # 角度范围（用于绘制弧）
    aa=True,                     # 是否抗锯齿
    color=(r, g, b)              # 颜色
)
```

#### FreeAllCircle - 静态绘图方法
```python
# 绘制抗锯齿圆
FreeAllCircle.draw_aacircle(screen, (x, y), radius, color)

# 绘制贝塞尔曲线
points = [(100, 100), (200, 50), (300, 150), (400, 100)]
FreeAllCircle.draw_bezier(screen, points, steps=100, color=(128, 128, 128))
```

### 其他组件

#### FreeIcon - 图标
```python
icon = FreeIcon(
    screen=screen,
    coordinates=[x, y],          # 图标位置
    image_1=normal_image,        # 正常状态图像
    image_2=hover_image          # 悬停状态图像
)

# 切换图标状态
icon.set_index(0)  # 显示 image_1
icon.set_index(1)  # 显示 image_2
```

#### ParticleEngine - 粒子系统
```python
engine = ParticleEngine()

# 生成粒子
engine.generate_particles(50, (x, y))

# 更新粒子
engine.update_particles()

# 绘制粒子
engine.draw_particles(screen)
```

### 图像处理

```python
from freepygame import image_blur_processing, array_mean_rgba

# 图像模糊处理
blurred_image = image_blur_processing(image, level=2)

# 计算图像区域的平均颜色
avg_color = array_mean_rgba(pixel_data)
```

## 实用函数

### 点击检测
```python
# 检测点是否在按钮内
if position_button(rect, pos):
    print("点在矩形内")

# 检测点是否在按钮对象内
if position_button_class(button, pos):
    print("点在按钮内")
```

## 高级特性

### 操作符重载

#### SuperText 的操作符
```python
text = SuperText(screen, [100, 100], "Hello")

# << 操作符快捷设置属性
text << (36,)           # 设置字体大小
text << (200, 150)      # 设置位置
text << (255, 0, 0)     # 设置颜色

# + 操作符拼接文本
text + " World!"        # 文本变为 "Hello World!"
```

#### SuperCircle 的操作符
```python
circle = SuperCircle(screen, [400, 300], 50)

circle << (75,)         # 设置半径
circle << ((80, 60),)   # 设置长短半轴
circle << ((255, 0, 0),) # 设置颜色
```

## 项目结构
```
freepygame/
├── freepygame/          # 主包目录
│   ├── __init__.py     # 包初始化
│   ├── freebutton.py   # 按钮组件
│   ├── freecircle.py   # 圆形组件
│   ├── freetext.py     # 文本组件
│   ├── freeicon.py     # 图标组件
│   ├── freeparticle.py # 粒子系统
│   ├── freetransformation.py # 图像处理
│   └── freepygamelib.py # 单文件版本
├── tests/              # 测试目录
│   ├── conftest.py    # 测试配置
│   ├── test_components/ # 组件测试
│   └── test_integration/ # 集成测试
├── examples/           # 示例目录
├── setup.py           # 安装配置
├── README.md          # 本文档
└── LICENSE.txt        # 许可证文件
```

## 许可证

本项目采用 Apache License 2.0 许可证。详见 [LICENSE.txt](LICENSE.txt)。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

freebird

## 致谢

- [Pygame](https://www.pygame.org/) - 游戏开发库

---

**注意**: 本库仍在积极开发中，API 可能会有变动。
