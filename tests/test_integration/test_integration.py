"""
集成测试：测试 freepygame 组件之间的交互和完整工作流程
"""

import pygame
import pytest

from freepygame import (
    CircleButton,
    FreeButton,
    FreeCircle,
    FreeIcon,
    FreeText,
    ParticleEngine,
    SuperCircle,
    SuperText,
    array_mean_rgba,
    image_blur_processing,
    position_button_class,
)


class TestComponentIntegration:
    """组件集成测试"""

    def test_button_and_text_integration(self, test_screen):
        """测试按钮和文本组件的集成"""
        # 创建按钮
        button = FreeButton(
            screen=test_screen,
            coordinates=[100, 100],
            button_size=[200, 50],
            msg="点击我",
            button_color=(0, 100, 200),
            text_color=(255, 255, 255),
        )

        # 创建文本标签
        label = FreeText(
            screen=test_screen,
            coordinates=[100, 170],
            msg="按钮状态: 未点击",
            color=(0, 0, 0),
        )

        # 绘制两个组件
        try:
            button.draw()
            label.draw()
        except Exception as e:
            pytest.fail(f"按钮和文本集成绘制时抛出异常: {e}")

        # 测试按钮点击检测
        click_pos = (200, 125)  # 按钮中心附近
        is_clicked = position_button_class(button, click_pos)

        # 根据点击状态更新文本
        if is_clicked:
            label.set_msg("按钮状态: 已点击")
        else:
            label.set_msg("按钮状态: 未点击")

        # 再次绘制更新后的文本
        try:
            label.draw()
        except Exception as e:
            pytest.fail(f"更新文本后绘制时抛出异常: {e}")

    def test_circle_button_and_circle_integration(self, test_screen):
        """测试圆形按钮和圆形组件的集成"""
        # 创建圆形按钮
        circle_button = CircleButton(
            screen=test_screen,
            coordinates=[400, 300],
            radius=60,
            msg="圆形按钮",
            button_color=(200, 0, 0),
            msg_color=(255, 255, 255),
        )

        # 创建一个装饰性的圆环
        decoration_circle = FreeCircle(
            screen=test_screen,
            coordinates=[400, 300],
            radius=70,
            width=3,
            color=(100, 100, 100),
            draw_border=True,
            border_width=2,
            border_color=(50, 50, 50),
        )

        # 绘制两个组件
        try:
            decoration_circle.draw()
            circle_button.draw()
        except Exception as e:
            pytest.fail(f"圆形按钮和装饰圆环集成绘制时抛出异常: {e}")

        # 测试圆形按钮的继承关系
        assert isinstance(circle_button, CircleButton)
        # CircleButton 应该继承自 FreeCircle
        assert isinstance(circle_button, FreeCircle)

        # 测试可以调用父类的方法
        center = circle_button.get_center_coordinates()
        assert center == [400, 300]

    def test_particle_system_with_ui_components(self, test_screen):
        """测试粒子系统与UI组件的集成"""
        # 创建粒子引擎
        particle_engine = ParticleEngine()

        # 创建触发按钮
        particle_button = FreeButton(
            screen=test_screen,
            coordinates=[50, 500],
            button_size=[150, 40],
            msg="生成粒子",
            button_color=(0, 150, 0),
            text_color=(255, 255, 255),
        )

        # 创建粒子计数器文本
        particle_counter = FreeText(
            screen=test_screen,
            coordinates=[220, 510],
            msg="粒子数: 0",
            color=(0, 0, 0),
        )

        # 绘制UI组件
        try:
            particle_button.draw()
            particle_counter.draw()
        except Exception as e:
            pytest.fail(f"粒子系统UI绘制时抛出异常: {e}")

        # 模拟按钮点击生成粒子
        button_click_pos = (125, 520)  # 按钮中心
        if position_button_class(particle_button, button_click_pos):
            # 生成粒子
            particle_engine.generate_particles(50, button_click_pos)

            # 更新粒子计数器
            particle_count = len(particle_engine.particles)
            particle_counter.set_msg(f"粒子数: {particle_count}")

        # 更新和绘制粒子
        try:
            particle_engine.update_particles()
            particle_engine.draw_particles(test_screen)
            # 重新绘制更新后的计数器
            particle_counter.draw()
        except Exception as e:
            pytest.fail(f"粒子系统更新和绘制时抛出异常: {e}")

    def test_icon_and_button_integration(self, test_screen):
        """测试图标和按钮的集成"""
        # 创建两个图标状态
        normal_icon = pygame.Surface((40, 40))
        normal_icon.fill((0, 100, 200))  # 蓝色

        hover_icon = pygame.Surface((40, 40))
        hover_icon.fill((200, 100, 0))  # 橙色

        # 创建图标
        icon = FreeIcon(
            screen=test_screen,
            coordinates=[600, 100],
            image_1=normal_icon,
            image_2=hover_icon,
        )

        # 创建控制按钮
        toggle_button = FreeButton(
            screen=test_screen,
            coordinates=[550, 150],
            button_size=[140, 30],
            msg="切换图标",
            button_color=(100, 100, 100),
            text_color=(255, 255, 255),
        )

        # 创建状态显示文本
        status_text = FreeText(
            screen=test_screen,
            coordinates=[550, 190],
            msg="图标状态: 正常",
            color=(0, 0, 0),
        )

        # 绘制所有组件
        try:
            icon.draw()
            toggle_button.draw()
            status_text.draw()
        except Exception as e:
            pytest.fail(f"图标和按钮集成绘制时抛出异常: {e}")

        # 模拟按钮点击切换图标
        button_pos = (620, 165)  # 切换按钮中心
        if position_button_class(toggle_button, button_pos):
            # 切换图标状态
            if icon.image_index == 0:
                icon.set_index(1)
                status_text.set_msg("图标状态: 悬停")
            else:
                icon.set_index(0)
                status_text.set_msg("图标状态: 正常")

            # 重新绘制
            icon.draw()
            status_text.draw()

    def test_super_components_integration(self, test_screen):
        """测试超级组件（SuperText, SuperCircle）的集成"""
        # 创建超级文本
        super_text = SuperText(
            screen=test_screen,
            coordinates=[100, 400],
            msg="超级文本示例",
            font=None,
            size=20,
            color=(0, 0, 150),
            dsm=1.5,  # 1.5倍缩放
        )

        # 创建超级圆形
        super_circle = SuperCircle(
            screen=test_screen,
            coordinates=[300, 400],
            radius=40,
            width=2,
            color=(150, 0, 0),
            aa=True,
        )

        # 创建控制按钮
        control_button = FreeButton(
            screen=test_screen,
            coordinates=[200, 470],
            button_size=[120, 30],
            msg="改变属性",
            button_color=(150, 0, 150),
            text_color=(255, 255, 255),
        )

        # 绘制所有组件
        try:
            super_text.draw()
            super_circle.draw()
            control_button.draw()
        except Exception as e:
            pytest.fail(f"超级组件集成绘制时抛出异常: {e}")

        # 模拟按钮点击改变属性
        button_pos = (260, 485)
        if position_button_class(control_button, button_pos):
            # 使用操作符快捷改变属性
            super_text << (24,)  # 改变字体大小
            super_circle << (60,)  # 改变半径
            super_circle << ((255, 0, 0),)  # 改变颜色

            # 重新绘制
            super_text.draw()
            super_circle.draw()

    def test_image_processing_integration(self, test_screen):
        """测试图像处理功能的集成"""
        # 创建一个测试图像
        test_image = pygame.Surface((100, 100))

        # 填充渐变颜色
        for x in range(100):
            for y in range(100):
                # 创建从红色到蓝色的渐变
                r = int(255 * (x / 100))
                g = 0
                b = int(255 * (y / 100))
                test_image.set_at((x, y), (r, g, b, 255))

        # 创建原始图像显示区域
        original_surface = pygame.Surface((100, 100))
        original_surface.blit(test_image, (0, 0))

        # 应用模糊处理
        try:
            blurred_image = image_blur_processing(test_image.copy(), level=2)
        except Exception as e:
            pytest.fail(f"图像模糊处理时抛出异常: {e}")

        # 创建模糊后图像显示区域
        blurred_surface = pygame.Surface((100, 100))
        blurred_surface.blit(blurred_image, (0, 0))

        # 创建标签
        original_label = FreeText(
            screen=test_screen,
            coordinates=[50, 50],
            msg="原始图像",
            color=(0, 0, 0),
        )

        blurred_label = FreeText(
            screen=test_screen,
            coordinates=[200, 50],
            msg="模糊后图像",
            color=(0, 0, 0),
        )

        # 绘制到测试屏幕
        try:
            # 绘制原始图像
            test_screen.blit(original_surface, (50, 70))
            original_label.draw()

            # 绘制模糊后图像
            test_screen.blit(blurred_surface, (200, 70))
            blurred_label.draw()
        except Exception as e:
            pytest.fail(f"图像处理结果显示时抛出异常: {e}")

        # 测试RGBA处理功能
        # 从模糊图像中提取一个区域进行RGBA分析
        sample_rect = pygame.Rect(40, 40, 20, 20)
        sample_area = []
        for x in range(sample_rect.left, sample_rect.right):
            column = []
            for y in range(sample_rect.top, sample_rect.bottom):
                column.append(blurred_image.get_at((x, y)))
            sample_area.append(column)

        # 计算平均RGBA值
        try:
            avg_color = array_mean_rgba(map_to_rgba(sample_area))
            # 创建平均颜色显示
            color_display = pygame.Surface((50, 50))
            color_display.fill(avg_color[:3])  # 只使用RGB部分

            # 绘制平均颜色
            test_screen.blit(color_display, (350, 70))

            # 添加标签
            color_label = FreeText(
                screen=test_screen,
                coordinates=[350, 50],
                msg="平均颜色",
                color=(0, 0, 0),
            )
            color_label.draw()
        except Exception as e:
            pytest.fail(f"RGBA处理时抛出异常: {e}")

    @pytest.mark.slow
    def test_complete_ui_scenario(self, test_screen):
        """测试完整的UI场景（慢速测试）"""
        # 创建多个UI组件
        title = SuperText(
            screen=test_screen,
            coordinates=[300, 30],
            msg="freepygame 演示",
            size=32,
            color=(0, 0, 150),
            dsm=1,
        )

        button1 = FreeButton(
            screen=test_screen,
            coordinates=[100, 100],
            button_size=[180, 50],
            msg="按钮 1",
            button_color=(70, 130, 180),
            text_color=(255, 255, 255),
            draw_border=True,
            border_width=2,
        )

        button2 = CircleButton(
            screen=test_screen,
            coordinates=[400, 125],
            radius=40,
            msg="圆形",
            button_color=(180, 70, 130),
            msg_color=(255, 255, 255),
        )

        status_text = FreeText(
            screen=test_screen,
            coordinates=[100, 170],
            msg="状态: 等待交互",
            color=(0, 0, 0),
            size=18,
        )

        # 创建粒子引擎（用于特效）
        particle_engine = ParticleEngine()

        # 绘制所有静态组件
        try:
            title.draw()
            button1.draw()
            button2.draw()
            status_text.draw()
        except Exception as e:
            pytest.fail(f"完整UI场景绘制时抛出异常: {e}")

        # 模拟交互
        interactions = [
            ((190, 125), button1, "按钮1被点击"),
            ((400, 125), button2, "圆形按钮被点击"),
        ]

        for pos, component, message in interactions:
            if position_button_class(component, pos):
                # 更新状态
                status_text.set_msg(message)

                # 生成粒子特效
                particle_engine.generate_particles(30, pos)

                # 重新绘制
                status_text.draw()

        # 更新和绘制粒子
        particle_engine.update_particles()
        particle_engine.draw_particles(test_screen)

        # 验证所有组件正常工作
        assert title.msg == "freepygame 演示"
        assert button1.msg == "按钮 1"
        assert button2.msg == "圆形"
        assert len(particle_engine.particles) <= 60  # 最多60个粒子

    def test_error_handling_integration(self, test_screen):
        """测试集成环境中的错误处理"""
        # 测试无效参数的处理
        try:
            # 创建带有无效颜色的按钮（应该能处理）
            button = FreeButton(
                screen=test_screen,
                coordinates=[100, 100],
                button_size=[100, 50],
                msg="测试按钮",
                button_color=(-1, 300, 0),  # 无效的RGB值
            )
            button.draw()  # 应该不崩溃
        except Exception as e:
            # 某些Pygame版本可能会抛出异常，这是可以接受的
            pass

        # 测试空文本
        try:
            empty_text = FreeText(
                screen=test_screen,
                coordinates=[100, 200],
                msg="",  # 空文本
                color=(0, 0, 0),
            )
            empty_text.draw()
        except Exception as e:
            pytest.fail(f"空文本处理时抛出异常: {e}")

        # 测试零尺寸组件
        try:
            zero_button = FreeButton(
                screen=test_screen,
                coordinates=[100, 300],
                button_size=[0, 0],  # 零尺寸
                msg="零尺寸",
            )
            zero_button.draw()
        except Exception as e:
            # 零尺寸按钮可能会在渲染时出现问题，这是可以接受的
            pass

    def test_performance_integration(self, test_screen):
        """测试集成环境中的性能"""
        import time

        # 创建多个组件
        components = []
        start_time = time.time()

        # 创建100个文本组件
        for i in range(10):
            for j in range(10):
                text = FreeText(
                    screen=test_screen,
                    coordinates=[50 + i * 70, 50 + j * 30],
                    msg=f"文本{i * 10 + j}",
                    color=(i * 25, j * 25, (i + j) * 12),
                    size=12,
                )
                components.append(text)

        creation_time = time.time() - start_time
        print(f"创建100个文本组件耗时: {creation_time:.3f}秒")

        # 批量绘制
        start_time = time.time()
        for component in components:
            component.draw()
        draw_time = time.time() - start_time
        print(f"绘制100个文本组件耗时: {draw_time:.3f}秒")

        # 批量更新
        start_time = time.time()
        for i, component in enumerate(components):
            component.set_msg(f"更新{i}")
        update_time = time.time() - start_time
        print(f"更新100个文本组件耗时: {update_time:.3f}秒")

        # 性能要求：创建、绘制、更新都应该在合理时间内完成
        assert creation_time < 1.0, "组件创建时间过长"
        assert draw_time < 2.0, "组件绘制时间过长"
        assert update_time < 1.0, "组件更新时间过长"
