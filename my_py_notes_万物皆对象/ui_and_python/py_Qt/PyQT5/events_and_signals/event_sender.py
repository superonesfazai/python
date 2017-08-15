# coding = utf-8

'''
@author = super_fazai
@File    : event_sender.py
@Time    : 2017/8/15 15:52
@connect : superonesfazai@gmail.com
'''

"""
PyQt5可以通过sender()方法, 方便的知道哪一个widget是信号的发送者

在这个例子中, 我来查出事件的发送者是谁
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QApplication)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        btn1 = QPushButton("Button 1", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Button 2", self)
        btn2.move(150, 50)

        btn1.clicked.connect(self.button_clicked)    # 通过buttonClicked()方法我查明了哪个按钮被点击回调了sender()方法
        btn2.clicked.connect(self.button_clicked)

        self.statusBar()    # 创建一个底部状态栏

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Event sender')
        self.show()

    def button_clicked(self):        # 两个button连接相同的信号口
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())