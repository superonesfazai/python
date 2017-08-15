# coding = utf-8

'''
@author = super_fazai
@File    : QProgressBar(进度条).py
@Time    : 2017/8/15 17:43
@connect : superonesfazai@gmail.com
'''

"""
QProgressBar(进度条):PyQt5提供水平和垂直的进度条, 这个进度条的默认最小值为0, 最大值为99, 我们可以改变其值
"""

from PyQt5.QtWidgets import (QWidget, QProgressBar,
                             QPushButton, QApplication)
from PyQt5.QtCore import QBasicTimer
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.pbar = QProgressBar(self)          # 创建一个QProcessBar实例对象
        self.pbar.setGeometry(30, 40, 200, 25)

        self.btn = QPushButton('开始', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.do_action)

        self.timer = QBasicTimer()              # 通过QBasicTimer的实例对象self.timer来用于激活进度条
        self.step = 0

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('进度条')
        self.show()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('结束')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def do_action(self):                # 通过do_action()方法我能开始或停止进度条
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('开始')
        else:
            self.timer.start(100, self)         # 调用start()方法来激活进度条, 这个方法有2个参数:the timeout and the object which will receive the events.
            self.btn.setText('结束')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())