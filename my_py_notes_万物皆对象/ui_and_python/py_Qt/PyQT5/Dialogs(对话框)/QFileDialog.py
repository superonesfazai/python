# coding = utf-8

'''
@author = super_fazai
@File    : QFileDialog.py
@Time    : 2017/8/15 16:53
@connect : superonesfazai@gmail.com
'''

"""
QFileDialog是一个允许使用者选择文件和文件夹的窗口类, 文件能被选择用于打开或者保存

这里我选择从QFileDialog窗口选择一个文件, 并在QTextEdit实例对象中显示其内容
"""

from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import sys


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)
        self.statusBar()

        open_file = QAction(QIcon('../images/imagespython.jpg'), 'Open', self)
        open_file.setShortcut('Ctrl+O')     # 设置一个快捷键
        open_file.setStatusTip('打开新文件')
        open_file.triggered.connect(self.showDialog)

        menu_bar = self.menuBar()
        fileMenu = menu_bar.addMenu('&File')
        fileMenu.addAction(open_file)

        menu_bar.setNativeMenuBar(False)  # 添加这句话是为了针对让mac os下显示菜单栏

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('文件对话框')
        self.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')     # 第三个参数为默认打开的位置

        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                self.text_edit.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())