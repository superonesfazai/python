# coding = utf-8

'''
@author = super_fazai
@File    : toolbar_工具栏.py
@Time    : 2017/8/14 20:39
@connect : superonesfazai@gmail.com
'''

"""
创建一个工具栏(工具栏可以快速访问最常用的命令)    (该程序有一个动作, 如果触发, 其中终止应用程序)
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QApplication)
from PyQt5.QtGui import QIcon

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        exit_act = QAction(QIcon('../images/imagespython.jpg'), 'Exit', self)   # 创建一个动作对象. 对象有一个标签, 图标和一个shorcut
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(qApp.quit)

        self.tool_bar = self.addToolBar('Exit')     # 使用addToolBar()方法创建工具栏
        self.tool_bar.addAction(exit_act)           # 我们用工具栏添加一个动作对象addAction()

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('tool_bar')
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())