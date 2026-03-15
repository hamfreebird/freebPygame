"""
测试 freepygame 中的其他组件
包括 FreeIcon, FreeParticle, FreeTransformation 等
"""

import random

import pygame
import pytest

from freepygame import (
    Fireworks,
    FreeIcon,
    Particle,
    ParticleEngine,
    array_mean_rgba,
    explode,
    image_blur_processing,
    map_to_rgba,
)


class TestFreeIcon:
    """测试 FreeIcon 类"""

    def test_icon_creation(self, test_screen):
        """测试图标创建"""
        # 创建两个测试图像表面
        image1 = pygame.Surface((50, 50))
        image1.fill((255, 0, 0))  # 红色

        image2 = pygame.Surface((50, 50))
        image2.fill((0, 255, 0))  # 绿色

        icon = FreeIcon(test_screen, [100, 100], image1, image2)

        assert icon is not None
        assert icon.screen == test_screen
        assert icon.coordinates == [100, 100]
        assert len(icon.image) == 2
        assert icon.image[0] == image1
        assert icon.image[1] == image2
        assert icon.image_index == 0
        assert icon.check_button is False
        assert icon.display_button is True

    def test_icon_set_index(self, test_screen):
        """测试设置图标索引"""
        image1 = pygame.Surface((50, 50))
        image1.fill((255, 0, 0))

        image2 = pygame.Surface((50, 50))
        image2.fill((0, 255, 0))

        icon = FreeIcon(test_screen, [100, 100], image1, image2)

        # 测试设置索引为1
        icon.set_index(1)
        assert icon.image_index == 1

        # 测试设置索引为0
        icon.set_index(0)
        assert icon.image_index == 0

    def test_icon_draw_no_error(self, test_screen):
        """测试绘制图标不抛出错误"""
        image1 = pygame.Surface((50, 50))
        image1.fill((255, 0, 0))

        image2 = pygame.Surface((50, 50))
        image2.fill((0, 255, 0))

        icon = FreeIcon(test_screen, [100, 100], image1, image2)

        # 绘制应该不抛出异常
        try:
            icon.draw()
        except Exception as e:
            pytest.fail(f"绘制图标时抛出异常: {e}")

        # 切换索引并再次绘制
        icon.set_index(1)
        try:
            icon.draw()
        except Exception as e:
            pytest.fail(f"绘制切换后的图标时抛出异常: {e}")


class TestParticleSystem:
    """测试粒子系统"""

    def test_particle_creation(self):
        """测试粒子创建"""
        particle = Particle(
            pos=(100, 100), velocity=(2, -3), acceleration=(0, 0.1), lifespan=100
        )

        assert particle is not None
        assert isinstance(particle, pygame.sprite.Sprite)
        assert particle.pos == pygame.math.Vector2(100, 100)
        assert particle.velocity == pygame.math.Vector2(2, -3)
        assert particle.acceleration == pygame.math.Vector2(0, 0.1)
        assert particle.lifespan == 100
        assert hasattr(particle, "image")
        assert hasattr(particle, "rect")

    def test_particle_update(self):
        """测试粒子更新"""
        particle = Particle(
            pos=(100, 100), velocity=(2, -3), acceleration=(0, 0.1), lifespan=100
        )

        initial_lifespan = particle.lifespan
        initial_pos = particle.pos.copy()
        initial_velocity = particle.velocity.copy()

        # 更新粒子
        particle.update()

        # 检查生命周期减少
        assert particle.lifespan == initial_lifespan - 1

        # 检查速度更新（加速度影响）
        expected_velocity = initial_velocity + particle.acceleration
        assert particle.velocity.x == pytest.approx(expected_velocity.x, abs=1e-6)
        assert particle.velocity.y == pytest.approx(expected_velocity.y, abs=1e-6)

        # 检查位置更新
        expected_pos = initial_pos + particle.velocity
        assert particle.pos.x == pytest.approx(expected_pos.x, abs=1e-6)
        assert particle.pos.y == pytest.approx(expected_pos.y, abs=1e-6)

    def test_particle_kill_when_lifespan_zero(self):
        """测试粒子生命周期结束时被移除"""
        particle = Particle(
            pos=(100, 100),
            velocity=(0, 0),
            acceleration=(0, 0),
            lifespan=1,  # 只有1帧生命周期
        )

        # 初始状态应该存活
        assert particle.lifespan == 1

        # 更新一次，生命周期应该变为0
        particle.update()
        assert particle.lifespan == 0

        # 再次更新，粒子应该被移除
        # 注意：kill()方法会将粒子从所有组中移除
        particle_group = pygame.sprite.Group()
        particle_group.add(particle)

        particle.update()  # 这会调用kill()

        # 检查粒子是否已从组中移除
        assert len(particle_group) == 0

    def test_particle_engine_creation(self):
        """测试粒子引擎创建"""
        engine = ParticleEngine()

        assert engine is not None
        assert hasattr(engine, "particles")
        assert isinstance(engine.particles, pygame.sprite.Group)

    def test_particle_engine_generate_particles(self):
        """测试粒子引擎生成粒子"""
        engine = ParticleEngine()

        # 生成前粒子组为空
        assert len(engine.particles) == 0

        # 生成10个粒子
        engine.generate_particles(10, (200, 200))

        # 检查是否生成了10个粒子
        assert len(engine.particles) == 10

        # 检查所有粒子都是Particle实例
        for particle in engine.particles:
            assert isinstance(particle, Particle)
            assert particle.pos == pygame.math.Vector2(200, 200)

    def test_particle_engine_update_particles(self):
        """测试粒子引擎更新粒子"""
        engine = ParticleEngine()
        engine.generate_particles(5, (100, 100))

        # 记录初始状态
        initial_particles = list(engine.particles)
        initial_lifespans = [p.lifespan for p in initial_particles]

        # 更新粒子
        engine.update_particles()

        # 检查所有粒子的生命周期都减少了
        for i, particle in enumerate(engine.particles):
            assert particle.lifespan == initial_lifespans[i] - 1

    def test_particle_engine_draw_particles(self, test_screen):
        """测试粒子引擎绘制粒子"""
        engine = ParticleEngine()
        engine.generate_particles(5, (100, 100))

        # 绘制应该不抛出异常
        try:
            engine.draw_particles(test_screen)
        except Exception as e:
            pytest.fail(f"绘制粒子时抛出异常: {e}")


class TestFireworks:
    """测试烟花效果"""

    def test_fireworks_creation(self):
        """测试烟花创建"""
        # 设置随机种子以确保测试可重复
        random.seed(42)

        fireworks = Fireworks(400, 300, (255, 0, 0))

        assert fireworks is not None
        assert fireworks.x == 400
        assert fireworks.y == 300
        assert fireworks.color == (255, 0, 0)
        assert fireworks.radius == 5
        assert fireworks.gravity == 0.5

        # 速度应该在预期范围内
        assert -5 <= fireworks.vx <= 5
        assert -15 <= fireworks.vy <= -5

    def test_fireworks_update(self):
        """测试烟花更新"""
        # 设置随机种子
        random.seed(42)

        fireworks = Fireworks(400, 300, (255, 0, 0))

        # 记录初始状态
        initial_x = fireworks.x
        initial_y = fireworks.y
        initial_vx = fireworks.vx
        initial_vy = fireworks.vy

        # 更新烟花
        fireworks.update()

        # 检查速度衰减（vx乘以0.98）
        expected_vx = initial_vx * 0.98
        assert fireworks.vx == pytest.approx(expected_vx, abs=1e-6)

        # 检查重力影响（vy增加重力）
        expected_vy = initial_vy + fireworks.gravity
        assert fireworks.vy == pytest.approx(expected_vy, abs=1e-6)

        # 检查位置更新
        expected_x = initial_x + fireworks.vx
        expected_y = initial_y + fireworks.vy
        assert fireworks.x == pytest.approx(expected_x, abs=1e-6)
        assert fireworks.y == pytest.approx(expected_y, abs=1e-6)

    def test_fireworks_draw_no_error(self, test_screen):
        """测试绘制烟花不抛出错误"""
        # 设置随机种子
        random.seed(42)

        fireworks = Fireworks(400, 300, (255, 0, 0))

        # 绘制应该不抛出异常
        try:
            fireworks.draw(test_screen)
        except Exception as e:
            pytest.fail(f"绘制烟花时抛出异常: {e}")

    def test_explode_function(self):
        """测试爆炸函数"""
        # 设置随机种子
        random.seed(42)

        particles = explode(400, 300)

        assert particles is not None
        assert isinstance(particles, list)
        assert len(particles) == 100

        # 检查所有粒子都是Fireworks实例
        for particle in particles:
            assert isinstance(particle, Fireworks)
            assert particle.x == 400
            assert particle.y == 300

            # 颜色应该是预定义的颜色之一
            predefined_colors = [
                (255, 0, 0),  # RED
                (255, 255, 0),  # YELLOW
                (255, 165, 0),  # ORANGE
                (0, 255, 0),  # GREEN
                (0, 0, 255),  # BLUE
                (160, 32, 240),  # PURPLE
            ]
            assert particle.color in predefined_colors


class TestTransformationFunctions:
    """测试图像处理函数"""

    def test_array_mean_basic(self):
        """测试基础数组平均值计算"""
        # 测试正常情况
        numbers = [1, 2, 3, 4, 5]
        result = array_mean_rgba._array_mean(numbers)  # 注意：需要访问内部函数
        expected = (1 + 2 + 3 + 4 + 5) / 5
        assert result == pytest.approx(expected, abs=1e-6)

        # 测试空列表
        empty_list = []
        result = array_mean_rgba._array_mean(empty_list)
        assert result == 0

        # 测试单个元素
        single = [42]
        result = array_mean_rgba._array_mean(single)
        assert result == 42

    def test_array_mean_rgba(self):
        """测试RGBA数组平均值计算"""
        # 创建测试RGBA数据
        rgba = (
            [100, 150, 200],  # R通道
            [50, 100, 150],  # G通道
            [0, 50, 100],  # B通道
            [255, 200, 150],  # A通道
        )

        result = array_mean_rgba(rgba)

        # 计算期望值
        expected_r = int((100 + 150 + 200) / 3)
        expected_g = int((50 + 100 + 150) / 3)
        expected_b = int((0 + 50 + 100) / 3)
        expected_a = int((255 + 200 + 150) / 3)

        assert result == (expected_r, expected_g, expected_b, expected_a)

        # 测试边界情况：空数组
        empty_rgba = ([], [], [], [])
        result = array_mean_rgba(empty_rgba)
        assert result == (0, 0, 0, 0)

    def test_map_to_rgba(self):
        """测试映射到RGBA函数"""
        # 创建测试像素数据
        # 2x2 像素网格，每个像素有RGBA值
        pixels = [
            [
                (100, 50, 0, 255),  # 位置 (0,0)
                (150, 100, 50, 200),  # 位置 (0,1)
            ],
            [
                (200, 150, 100, 150),  # 位置 (1,0)
                (250, 200, 150, 100),  # 位置 (1,1)
            ],
        ]

        r, g, b, a = map_to_rgba(pixels)

        # 检查R通道
        assert r == [100, 150, 200, 250]

        # 检查G通道
        assert g == [50, 100, 150, 200]

        # 检查B通道
        assert b == [0, 50, 100, 150]

        # 检查A通道
        assert a == [255, 200, 150, 100]

        # 测试没有alpha通道的情况
        pixels_no_alpha = [
            [
                (100, 50, 0),  # 位置 (0,0)
                (150, 100, 50),  # 位置 (0,1)
            ]
        ]

        r, g, b, a = map_to_rgba(pixels_no_alpha)

        # A通道应该为空列表
        assert a == []

    def test_image_blur_processing_basic(self, test_screen):
        """测试基础图像模糊处理"""
        # 创建一个简单的测试图像
        image = pygame.Surface((10, 10))

        # 填充一些颜色
        for x in range(10):
            for y in range(10):
                # 创建渐变效果
                color = (x * 25, y * 25, (x + y) * 12)
                image.set_at((x, y), color)

        # 应用模糊处理
        try:
            blurred = image_blur_processing(image, level=1)
        except Exception as e:
            pytest.fail(f"图像模糊处理时抛出异常: {e}")

        # 检查返回的是同一个图像对象
        assert blurred is image

        # 检查图像尺寸没有改变
        assert image.get_size() == (10, 10)

    def test_image_blur_processing_edge_cases(self, test_screen):
        """测试图像模糊处理的边界情况"""
        # 创建一个小图像
        small_image = pygame.Surface((3, 3))

        # 填充单一颜色
        small_image.fill((100, 100, 100))

        # 应用模糊处理（level=0应该没有效果）
        try:
            blurred = image_blur_processing(small_image, level=0)
        except Exception as e:
            pytest.fail(f"level=0的图像模糊处理时抛出异常: {e}")

        # 创建一个大图像
        large_image = pygame.Surface((100, 100))

        # 填充随机颜色
        for x in range(100):
            for y in range(100):
                color = (x % 256, y % 256, (x + y) % 256)
                large_image.set_at((x, y), color)

        # 应用较大模糊半径
        try:
            blurred = image_blur_processing(large_image, level=3)
        except Exception as e:
            pytest.fail(f"大图像模糊处理时抛出异常: {e}")

    @pytest.mark.slow
    def test_image_blur_visual_effect(self, test_screen):
        """测试图像模糊的视觉效果（慢速测试）"""
        # 创建一个有明显对比的图像
        image = pygame.Surface((20, 20))

        # 左半部分红色，右半部分蓝色
        for x in range(20):
            for y in range(20):
                if x < 10:
                    image.set_at((x, y), (255, 0, 0, 255))  # 红色
                else:
                    image.set_at((x, y), (0, 0, 255, 255))  # 蓝色

        # 应用模糊处理
        blurred = image_blur_processing(image, level=2)

        # 检查中间区域的像素（应该是红色和蓝色的混合）
        middle_pixel = blurred.get_at((10, 10))

        # 中间像素应该是紫色（红色和蓝色的混合）
        # 由于模糊，R和B值都应该大于0
        assert middle_pixel[0] > 0  # R
        assert middle_pixel[2] > 0  # B
        # G通道应该接近0
        assert middle_pixel[1] < 50
