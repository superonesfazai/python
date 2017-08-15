# coding = utf-8

'''
@author = super_fazai
@File    : QFontDialog.py
@Time    : 2017/8/15 16:47
@connect : superonesfazai@gmail.com
'''

"""
QFontDialog是一个选择字体的窗口对象

这里我将选择一个字体, 然后改变label的字体
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                             QSizePolicy, QLabel, QFontDialog, QApplication)
import sys


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()

        btn = QPushButton('字体选择', self)
        btn.setSizePolicy(QSizePolicy.Fixed,
                          QSizePolicy.Fixed)
        btn.move(20, 20)

        vbox.addWidget(btn)

        btn.clicked.connect(self.showDialog)

        self.lbl = QLabel('Knowledge only matters', self)
        self.lbl.move(130, 20)

        vbox.addWidget(self.lbl)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('字体对话框')
        self.show()

    def showDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.lbl.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())