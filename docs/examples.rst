示例
====

基础示例
--------

``examples/basic_demo.py`` 演示了按钮、文本、圆形与图标的基础用法：

.. literalinclude:: ../examples/basic_demo.py
   :language: python
   :caption: examples/basic_demo.py
   :linenos:

表单与控件
----------

下面的示例展示输入框、下拉框、开关与单选组如何接入 ``FreeFrame``，
由框架自动完成焦点与键盘事件的分发：

.. code-block:: python

   import pygame
   from freepygame import (
       FreeFrame, InputBox, Dropdown, Switch,
       RadioGroup, RadioButton,
   )

   app = FreeFrame(title="表单示例", size=(400, 320))

   name = InputBox(app.screen, [20, 20], width=240, placeholder="请输入姓名")
   name.on_submit = lambda v: print("提交:", v)

   dd = Dropdown(app.screen, [20, 70], width=240,
                 options=["红", "绿", "蓝"])
   dd.on_select = lambda i, v: print("选中:", i, v)

   sw = Switch(app.screen, [20, 120], checked=False)
   sw.on_change = lambda on: print("开关:", on)

   group = RadioGroup()
   group.add(RadioButton(app.screen, [20, 170], label="选项A", value="A"))
   group.add(RadioButton(app.screen, [140, 170], label="选项B", value="B"))

   for w in (name, dd, sw, *group.buttons):
       app.add_widget(w)

   app.run()
