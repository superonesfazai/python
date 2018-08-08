# coding = utf-8

'''
@author = super_fazai
@File    : toggle_button.py
@Time    : 2017/8/15 17:16
@connect : superonesfazai@gmail.com
'''

"""
toggle button是QPushButton的特殊mode, 这个button有2种状态:pressed和not pressed 
我们能够切换这两种状态通过点击它

这里我将创建3个togglet button对象, 它们能控制QFrame的背景色
"""

from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QFrame, QApplication)
from PyQt5.QtGui import QColor
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.col = QColor(0, 0, 0)      # 用于设置初始背景色

        redb = QPushButton('Red', self)
        redb.setCheckable(True)         # 设置setCheckable为True
        redb.move(10, 10)

        redb.clicked[bool].connect(self.setColor)       # 此处的bool是一个布尔值

        greenb = QPushButton('Green', self)
        greenb.setCheckable(True)
        greenb.move(10, 60)

        greenb.clicked[bool].connect(self.setColor)

        blueb = QPushButton('Blue', self)
        blueb.setCheckable(True)
        blueb.move(10, 110)

        blueb.clicked[bool].connect(self.setColor)

        self.square = QFrame(self)      # 创建一个QFrame用于展示颜色的改变
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" %
                                  self.col.name())

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Toggle button')
        self.show()

    def setColor(self, pressed):
        source = self.sender()

        if pressed:
            val = 255
        else:
            val = 0

        if source.text() == "Red":
            self.col.setRed(val)
        elif source.text() == "Green":
            self.col.setGreen(val)
        else:
            self.col.setBlue(val)

        self.square.setStyleSheet("QFrame { background-color: %s }" %
                                  self.col.name())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
