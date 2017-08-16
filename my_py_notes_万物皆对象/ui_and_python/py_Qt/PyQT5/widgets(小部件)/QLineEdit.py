# coding = utf-8

'''
@author = super_fazai
@File    : QLineEdit.py
@Time    : 2017/8/16 17:52
@connect : superonesfazai@gmail.com
'''

"""
QLineEdit 行编辑器

这里我用一个label来显示行编辑框的改变
"""

import sys
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QLineEdit, QApplication)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.lbl = QLabel(self)
        qle = QLineEdit(self)

        qle.move(60, 100)
        self.lbl.move(60, 40)

        qle.textChanged[str].connect(self.on_changed)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QLineEdit')
        self.show()

    def on_changed(self, text):
        self.lbl.setText(text)      # 改变显示
        self.lbl.adjustSize()       # 调整标签大小


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
