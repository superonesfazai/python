# coding = utf-8

'''
@author = super_fazai
@File    : draw_text.py
@Time    : 2017/8/16 18:14
@connect : superonesfazai@gmail.com
'''

"""
QPainter 提供了简单到复杂的绘画功能

In this example, we draw text in Russian Cylliric.
"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.text = "Лев Николаевич Толстой\nАнна Каренина"

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Drawing text')
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    # 重写drawText方法
    def drawText(self, event, qp):
        qp.setPen(QColor(168, 34, 3))       # 设置画笔颜色
        qp.setFont(QFont('Decorative', 10))     # 设置字体
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)    # 在窗口上绘制


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())