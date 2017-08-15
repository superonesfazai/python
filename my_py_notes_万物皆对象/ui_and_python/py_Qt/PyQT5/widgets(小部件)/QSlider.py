# coding = utf-8

'''
@author = super_fazai
@File    : QSlider.py
@Time    : 2017/8/15 17:34
@connect : superonesfazai@gmail.com
'''

"""
创建一个QSlider widget

这里我假装了一个类似调音量的slider, 通过拖动slider的把手, 来改变图片的显示
"""

from PyQt5.QtWidgets import (QWidget, QSlider,
                             QLabel, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        sld = QSlider(Qt.Horizontal, self)      # 创建一个水平的QSlider
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(30, 40, 100, 30)
        sld.valueChanged[int].connect(self.changeValue)

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('../images/imagespython.jpg'))     # 给创建的label初始化显示一张图片
        self.label.setGeometry(160, 40, 80, 30)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QSlider')
        self.show()

    def changeValue(self, value):

        if value == 0:   # 没有图片
            self.label.setPixmap(QPixmap('mute.png'))
        elif value > 0 and value <= 30:
            self.label.setPixmap(QPixmap('min.png'))
        elif value > 30 and value < 80:
            self.label.setPixmap(QPixmap('med.png'))
        else:
            self.label.setPixmap(QPixmap('max.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())