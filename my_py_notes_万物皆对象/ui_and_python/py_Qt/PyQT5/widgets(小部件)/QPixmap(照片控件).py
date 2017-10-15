# coding = utf-8

'''
@author = super_fazai
@File    : QPixmap(照片控件).py
@Time    : 2017/8/16 17:49
@connect : superonesfazai@gmail.com
'''

"""
QPixmap是一个照片控件

这里我显示一张照片
"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication)
from PyQt5.QtGui import QPixmap
import sys


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout(self)
        pixmap = QPixmap("../images/imagespython.jpg")

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.move(300, 200)
        self.setWindowTitle('Red Rock')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())