# coding = utf-8

'''
@author = super_fazai
@File    : box_layout.py
@Time    : 2017/8/15 11:55
@connect : superonesfazai@gmail.com
'''

"""
QHBoxLayout and QVBoxLayout are basic layout classes that line up widgets horizontally and vertically.
"""

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication)


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")

        hbox = QHBoxLayout()        # 创建一个水平布局 and add a stretch factor and both buttons.
        hbox.addStretch(1)          # 增加一个Stretch()
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        vbox = QVBoxLayout()        # 创建一个垂直布局
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
