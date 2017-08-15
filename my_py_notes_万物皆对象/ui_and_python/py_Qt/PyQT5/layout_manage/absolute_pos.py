# coding = utf-8

'''
@author = super_fazai
@File    : absolute_pos.py
@Time    : 2017/8/15 11:46
@connect : superonesfazai@gmail.com
'''

"""
使用绝对位置在窗口中创建3个标签
"""

import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QApplication)


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        lbl1 = QLabel('Zetcode', self)
        lbl1.move(15, 10)

        lbl2 = QLabel('tutorials', self)
        lbl2.move(35, 40)

        lbl3 = QLabel('for programmers', self)
        lbl3.move(55, 70)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Absolute')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())