# coding = utf-8

'''
@author = super_fazai
@File    : QInputDialog_test.py
@Time    : 2017/8/15 16:23
@connect : superonesfazai@gmail.com
'''

"""
创建一个QInputDialog对话框用于接收输入的数据

输入的值可以是 a string, a number, or an item from a list
"""

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.show_dialog)      # 连接事件处理的函数

        self.le = QLineEdit(self)
        self.move(130, 22)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()

    def show_dialog(self):
        text, ok = QInputDialog.getText(self, '输入的对话框', 'Enter your name:')
        if ok:
            self.le.setText(str(text))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


