# coding = utf-8

'''
@author = super_fazai
@File    : event_object.py
@Time    : 2017/8/15 15:30
@connect : superonesfazai@gmail.com
'''

"""
事件对象也是一个python对象, 它包含一个数字属性用于描述这个事件, 事件对象是明确的产生事件类型

这个例子, 我在一个标签部件里, 绘制鼠标的坐标
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QApplication, QGridLayout, QLabel)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        x, y = 0, 0

        self.text = 'x:{0}, y:{1}'.format(x, y)
        self.label  = QLabel(self.text, self)
        grid.addWidget(self.label, 0, 0, Qt.AlignTop)

        self.setMouseTracking(True)     # 鼠标跟踪默认是关闭的(false), 设置为开启状态, 即True

        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 200)
        self.setWindowTitle('event object')
        self.show()

    def mouseMoveEvent(self, QMouseEvent):
        x, y = QMouseEvent.x(), QMouseEvent.y()

        tmp_text = 'x:{0}, y:{1}'.format(x, y)
        self.label.setText(tmp_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
