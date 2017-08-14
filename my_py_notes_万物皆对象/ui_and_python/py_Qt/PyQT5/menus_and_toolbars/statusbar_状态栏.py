# coding = utf-8

'''
@author = super_fazai
@File    : statusbar_状态栏.py
@Time    : 2017/8/14 19:23
@connect : superonesfazai@gmail.com
'''

"""
创建一个(底部)状态栏
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication)

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.statusBar().showMessage('Ready')   # 调用QMainWindow类中的statusBar()方法创建一个状态栏对象, 返回一个状态栏对象
                                                # 在showMessage()显示状态栏信息

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Statusbar')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())