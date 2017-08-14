# coding = utf-8

'''
@author = super_fazai
@File    : close_a_window.py
@Time    : 2017/8/14 17:23
@connect : superonesfazai@gmail.com
'''

"""
创建一个quit按钮用于关闭窗口
"""

'''
PyQt5中的事件处理系统采用信号和插槽机制构建。
如果我们点击按钮，信号clicked就会发出。
插槽可以是Qt插槽或任何Python可调用。
它QCoreApplication包含主事件循环，它处理和调度所有事件。
该instance()方法给我们当前的实例。
注意QCoreApplication是用QApplication创建的。
点击的信号连接到quit() 终止应用程序的方法。
通信在两个对象之间完成：发送方和接收方。
发件人是按钮，接收者是应用对象
'''

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication)
from PyQt5.QtCore import QCoreApplication

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        qbtn = QPushButton('Quit', self)    # 创建一个按钮实例对象
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())