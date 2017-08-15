# coding = utf-8

'''
@author = super_fazai
@File    : emit_custom_signals.py
@Time    : 2017/8/15 16:03
@connect : superonesfazai@gmail.com
'''

"""
发出一个习惯的信号

创建一个信号被叫做callApp, 这个信号在鼠标点击事件时传递, 这个信号连接QMainWindow的close()信号口
"""

import sys
from PyQt5.QtCore import (pyqtSignal, QObject)
from PyQt5.QtWidgets import (QMainWindow, QApplication)

class Communicate(QObject):
    closeApp = pyqtSignal()     # 创建一个pyqtSignal信号的实例对象作为Communicate类的一个属性

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.c = Communicate()
        self.c.closeApp.connect(self.close)     # closeApp就相当于一个pyqtSignal的实例对象, 其能够通过connect()连接self.close的方法

        self.setGeometry(300, 300, 250,150)
        self.setWindowTitle('emit signal')
        self.show()

    def mousePressEvent(self, QMouseEvent):
        self.c.closeApp.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())