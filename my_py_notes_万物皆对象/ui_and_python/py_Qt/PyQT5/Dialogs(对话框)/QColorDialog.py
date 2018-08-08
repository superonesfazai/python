# coding = utf-8

'''
@author = super_fazai
@File    : QColorDialog.py
@Time    : 2017/8/15 16:36
@connect : superonesfazai@gmail.com
'''

"""
QColorDialog 提供一个窗口小部件用于选择颜色的值

我从QColorDialog 选择一个颜色用于改变QFrame的背景色
"""

from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame,
                             QColorDialog, QApplication)
from PyQt5.QtGui import QColor
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        col = QColor(0, 0, 0)       # 用于设置QFrame的初始背景色

        self.btn = QPushButton('颜色选择', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }"
                               % col.name())
        self.frm.setGeometry(130, 22, 100, 100)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Color dialog')
        self.show()

    def showDialog(self):
        col = QColorDialog.getColor()
        if col.isValid():   # 如果颜色可利用
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                                   % col.name())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())