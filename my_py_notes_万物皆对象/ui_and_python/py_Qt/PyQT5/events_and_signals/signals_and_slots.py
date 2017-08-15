# coding = utf-8

'''
@author = super_fazai
@File    : signals_and_slots.py
@Time    : 2017/8/15 15:06
@connect : superonesfazai@gmail.com
'''

"""
we connect a signal of a QSlider to a slot of a QLCDNumber
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
                             QVBoxLayout, QApplication)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)   # 我连接一个 valueChanged signal of the slider to the display slot of the lcd number.
                                                # 发送方是一个对象, 这个对象发送一个信号; 接收方也是一个对象, 它接收这个信号; The slot是一个方法用于响应这个信号.
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal and slot')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
