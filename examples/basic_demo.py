"""
freepygame 基础演示示例
展示如何使用 freepygame 库创建基本的 UI 界面
"""

import random
import sys

import pygame

# 导入 freepygame 库
from freepygame import (
    CircleButton,
    FreeButton,
    FreeCircle,
    FreeIcon,
    FreeText,
    ParticleEngine,
    SuperCircle,
    SuperText,
    position_button_class,
)

# 初始化 Pygame
pygame.init()

# 设置窗口
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("freepygame 基础演示")
clock = pygame.time.Clock()

# 颜色定义
BACKGROUND = (240, 240, 245)
TITLE_COLOR = (30, 60, 120)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (90, 150, 200)
CIRCLE_BUTTON_COLOR = (180, 70, 130)
TEXT_COLOR = (50, 50, 50)
PARTICLE_COLORS = [
    (255, 100, 100),  # 红色
    (100, 255, 100),  # 绿色
    (100, 100, 255),  # 蓝色
    (255, 255, 100),  # 黄色
    (255, 100, 255),  # 紫色
]

# 创建标题
title = SuperText(
    screen=screen,
    coordinates=[SCREEN_WIDTH // 2 - 150, 30],
    msg="freepygame 演示程序",
    font=None,
    size=36,
    color=TITLE_COLOR,
    dsm=1,
)

# 创建描述文本
description = FreeText(
    screen=screen,
    coordinates=[50, 100],
    msg="这是一个展示 freepygame 库功能的演示程序。",
    font=None,
    size=20,
    color=TEXT_COLOR,
)

# 创建矩形按钮
rect_button = FreeButton(
    screen=screen,
    coordinates=[100, 180],
    button_size=[200, 60],
    msg="矩形按钮",
    font=None,
    size=24,
    border_width=2,
    draw_border=True,
    draw_line=False,
    button_color=BUTTON_COLOR,
    text_color=(255, 255, 255),
    border_color=(50, 100, 150),
    dsm=1,
)

# 创建圆形按钮
circle_button = CircleButton(
    screen=screen,
    coordinates=[400, 210],
    radius=50,
    msg="圆形",
    font=None,
    size=24,
    width=0,
    rect=(0, 0),
    angle=(0, 360),
    aa=True,
    draw_border=True,
    border_width=2,
    color=CIRCLE_BUTTON_COLOR,
    border_color=(150, 50, 100),
    msg_color=(255, 255, 255),
    button_color=CIRCLE_BUTTON_COLOR,
    msg_tran=False,
    dsm=1,
)

# 创建状态文本
status_text = FreeText(
    screen=screen,
    coordinates=[100, 260],
    msg="点击按钮查看效果",
    font=None,
    size=20,
    color=TEXT_COLOR,
)

# 创建计数器文本
counter_text = FreeText(
    screen=screen,
    coordinates=[100, 300],
    msg="点击次数: 0",
    font=None,
    size=20,
    color=TEXT_COLOR,
)

# 创建圆形装饰
decoration_circle = FreeCircle(
    screen=screen,
    coordinates=[650, 150],
    radius=60,
    width=3,
    rect=(0, 0),
    angle=(0, 360),
    aa=True,
    draw_border=True,
    border_width=2,
    color=(100, 200, 100),
    border_color=(50, 150, 50),
)

# 创建弧线装饰
arc_decoration = FreeCircle(
    screen=screen,
    coordinates=[650, 300],
    radius=50,
    width=4,
    rect=(0, 0),
    angle=(45, 315),  # 不完整的圆
    aa=True,
    draw_border=False,
    color=(200, 150, 50),
)

# 创建图标（使用简单的表面作为示例）
icon_normal = pygame.Surface((40, 40))
icon_normal.fill((100, 150, 200))
pygame.draw.circle(icon_normal, (255, 255, 255), (20, 20), 15)

icon_hover = pygame.Surface((40, 40))
icon_hover.fill((200, 150, 100))
pygame.draw.rect(icon_hover, (255, 255, 255), (10, 10, 20, 20))

icon = FreeIcon(
    screen=screen,
    coordinates=[700, 400],
    image_1=icon_normal,
    image_2=icon_hover,
)

# 创建粒子引擎
particle_engine = ParticleEngine()

# 创建控制按钮
clear_button = FreeButton(
    screen=screen,
    coordinates=[100, 350],
    button_size=[150, 40],
    msg="清除粒子",
    font=None,
    size=18,
    button_color=(150, 80, 80),
    text_color=(255, 255, 255),
)

# 变量初始化
click_count = 0
icon_toggled = False
running = True

# 主循环
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # 检查矩形按钮点击
            if position_button_class(rect_button, mouse_pos):
                click_count += 1
                status_text.set_msg("矩形按钮被点击！")
                counter_text.set_msg(f"点击次数: {click_count}")

                # 生成粒子效果
                particle_engine.generate_particles(random.randint(20, 40), mouse_pos)

                # 改变按钮颜色（反馈效果）
                rect_button.set_button_color(BUTTON_HOVER_COLOR)

            # 检查圆形按钮点击
            elif position_button_class(circle_button, mouse_pos):
                click_count += 1
                status_text.set_msg("圆形按钮被点击！")
                counter_text.set_msg(f"点击次数: {click_count}")

                # 生成粒子效果
                particle_engine.generate_particles(random.randint(30, 50), mouse_pos)

                # 改变圆形按钮颜色
                new_color = (
                    random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(100, 255),
                )
                circle_button.set_button_color(new_color)

            # 检查图标点击
            elif 700 <= mouse_pos[0] <= 740 and 400 <= mouse_pos[1] <= 440:
                icon_toggled = not icon_toggled
                icon.set_index(1 if icon_toggled else 0)
                status_text.set_msg("图标被点击！")

            # 检查清除按钮点击
            elif position_button_class(clear_button, mouse_pos):
                # 清除所有粒子
                particle_engine.particles.empty()
                status_text.set_msg("粒子已清除！")

        elif event.type == pygame.MOUSEBUTTONUP:
            # 鼠标释放时恢复按钮颜色
            rect_button.set_button_color(BUTTON_COLOR)

    # 更新粒子
    particle_engine.update_particles()

    # 随机生成一些背景粒子
    if random.random() < 0.05:  # 5%的概率每帧生成
        particle_engine.generate_particles(
            random.randint(1, 3),
            (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
        )

    # 绘制背景
    screen.fill(BACKGROUND)

    # 绘制标题和描述
    title.draw()
    description.draw()

    # 绘制按钮
    rect_button.draw()
    circle_button.draw()
    clear_button.draw()

    # 绘制状态文本
    status_text.draw()
    counter_text.draw()

    # 绘制装饰图形
    decoration_circle.draw()
    arc_decoration.draw()

    # 绘制图标
    icon.draw()

    # 绘制粒子
    particle_engine.draw_particles(screen)

    # 绘制说明文本
    instructions = FreeText(
        screen=screen,
        coordinates=[50, 500],
        msg="提示: 点击按钮会产生粒子效果，点击图标会切换状态",
        font=None,
        size=16,
        color=(100, 100, 100),
    )
    instructions.draw()

    # 绘制帧率
    fps_text = FreeText(
        screen=screen,
        coordinates=[SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30],
        msg=f"FPS: {int(clock.get_fps())}",
        font=None,
        size=16,
        color=(100, 100, 100),
    )
    fps_text.draw()

    # 更新显示
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 退出程序
pygame.quit()
sys.exit()
