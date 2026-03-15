# freepygame

一个为 Pygame 游戏开发提供 UI 控件和工具的 Python 库。

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-orange)](https://www.pygame.org/)

## 特性

- 🎨 **丰富的 UI 组件**: 按钮、文本、圆形、图标等
- 🖌️ **抗锯齿支持**: 高质量图形渲染
- 🔧 **易于使用**: 简单的 API 和直观的接口
- 🎯 **灵活配置**: 支持颜色、大小、位置等属性动态调整
- ✨ **特效支持**: 粒子系统、图像处理等高级功能
- 📱 **缩放支持**: 支持高DPI显示和界面缩放

## 安装

```bash
pip install freepygame
```

或者从源代码安装:

```bash
git clone https://github.com/yourusername/freepygame.git
cd freepygame
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

### 烟花效果
```python
from freepygame import explode, Fireworks

# 创建爆炸效果
particles = explode(x, y)

# 更新和绘制烟花
for particle in particles:
    particle.update()
    particle.draw(screen)
```

## 示例

查看 `examples/` 目录获取完整示例：

- `basic_demo.py` - 基础演示程序
- `particle_demo.py` - 粒子系统演示
- `ui_demo.py` - 完整UI界面演示

运行示例：
```bash
cd examples
python basic_demo.py
```

## API 文档

### FreeButton 类

#### 方法
- `get_attribute()` - 获取按钮所有属性
- `get_coordinates()` - 获取按钮四个角的坐标
- `set_msg(msg)` - 设置按钮文本
- `set_button_color(color)` - 设置按钮背景色
- `set_text_color(color)` - 设置文本颜色
- `open_border(enable)` - 显示/隐藏边框
- `open_line(enable)` - 显示/隐藏对角线
- `draw()` - 绘制按钮

### FreeCircle 类

#### 方法
- `get_attribute()` - 获取圆形所有属性
- `get_center_coordinates()` - 获取圆心坐标
- `get_coordinates()` - 获取外切矩形坐标
- `set_radius(radius)` - 设置半径
- `set_color(color)` - 设置颜色
- `set_angle(angle)` - 设置角度范围
- `open_border(enable)` - 显示/隐藏边框
- `draw()` - 绘制圆形

## 开发指南

### 运行测试
```bash
# 安装测试依赖
pip install pytest

# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_components/test_buttons.py

# 快速测试（跳过慢速测试）
pytest tests/ --quick
```

### 代码规范
- 使用类型注解
- 遵循 PEP 8 代码风格
- 添加中文和英文文档字符串
- 编写单元测试

### 项目结构
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

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 作者

freebird

## 致谢

- [Pygame](https://www.pygame.org/) - 游戏开发库
- 所有贡献者和用户

---

**注意**: 本库仍在积极开发中，API 可能会有变动。建议在生产环境中使用时锁定版本号。