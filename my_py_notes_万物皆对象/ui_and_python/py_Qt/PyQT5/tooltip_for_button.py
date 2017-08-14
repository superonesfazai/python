# coding = utf-8

'''
@author = super_fazai
@File    : tooltip_for_button.py
@Time    : 2017/8/14 17:07
@connect : superonesfazai@gmail.com
'''

"""
显示一个按钮提示 tooltip
"""

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        QToolTip.setFont(QFont('SansSerif', 10))    # 设置用于呈现工具提示的字体

        self.setToolTip('this a <b>QWidget</b> widget')     # 创建一个工具提示, 我们可以使用富文本格式

        btn = QPushButton('Button', self)   # 创建一个按钮, 并为其设置工具提示
        btn.setToolTip('this is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())          # 该sizeHint()方法给出了按钮的推荐大小
        btn.move(50, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')
        self.show()

if __name__ == "__main__":1
    app = QApplication(sys.argv)

    ex = Example()
    sys.exit(app.exec_())

