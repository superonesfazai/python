# coding = utf-8

'''
@author = super_fazai
@File    : main_window.py
@Time    : 2017/8/14 22:14
@connect : superonesfazai@gmail.com
'''

"""
将创建一个菜单栏，工具栏和状态栏。我们还将创建一个中心的小部件
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QApplication)
from PyQt5.QtGui import QIcon

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        text_edit = QTextEdit()
        self.setCentralWidget(text_edit)

        exit_act = QAction(QIcon('../iamges/imagespython.jpg'), 'Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(self.close)

        self.statusBar()

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(exit_act)

        menu_bar.setNativeMenuBar(False)  # 添加这句话是为了针对让mac os下显示菜单栏

        tool_bar = self.addToolBar('Exit')
        tool_bar.addAction(exit_act)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('main window')
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())