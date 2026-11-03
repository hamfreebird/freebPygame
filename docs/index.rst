欢迎使用 freepygame
===================

**freepygame** 是一个为 `Pygame <https://www.pygame.org/>`_ 游戏开发提供
UI 控件与工具函数的 Python 库。它内置按钮、文本、圆形、图标、进度条、滑块、
复选框、输入框、下拉框、开关、单选组等组件，并提供主题系统、自动布局与
窗口框架，让 Pygame 的界面开发更简洁。

.. code-block:: python

   import pygame
   from freepygame import FreeButton, FreeText

   pygame.init()
   screen = pygame.display.set_mode((800, 600))
   button = FreeButton(screen, [100, 100], [200, 50], msg="点击我")

   running = True
   while running:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           elif event.type == pygame.MOUSEBUTTONDOWN:
               if button.handle_click(event.pos):
                   print("按钮被点击")
       screen.fill((240, 240, 245))
       button.draw()
       pygame.display.flip()
   pygame.quit()

.. toctree::
   :maxdepth: 2
   :caption: 内容

   api
   examples

特性
----

- 🎨 丰富的 UI 组件（按钮、文本、圆形、图标、进度条、滑块、复选框等）
- 📝 表单控件（输入框、下拉选择、开关、单选组）
- 🎭 主题系统（内置 light / dark 调色板）
- 📐 自动布局（VBox / HBox / 锚点布局）
- 🔧 点击回调与 FreeFrame 事件分发
- ✨ 粒子系统、图像处理等高级功能

索引
----

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
