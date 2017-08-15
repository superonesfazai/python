# coding = utf-8

'''
@author = super_fazai
@File    : 重写_event_handler.py
@Time    : 2017/8/15 15:22
@connect : superonesfazai@gmail.com
'''

"""
重新实现一个事件处理
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('event handler')
        self.show()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:    # 按键为esc
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())