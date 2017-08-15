# coding = utf-8

'''
@author = super_fazai
@File    : QGridLayout_calculator_test.py
@Time    : 2017/8/15 12:17
@connect : superonesfazai@gmail.com
'''

"""
QGridLayout是一个普遍的布局类, 它能将空间划分为行和列

创建一个简单的计算器
"""

import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton, QApplication)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()    # 创建一个QGridLayout布局
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']

        positions = [(i, j) for i in range(5) for j in range(4)]    # 创建一个 list of positions in the grid
        # print(positions)
        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)   # 增加到grid布局中

        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())