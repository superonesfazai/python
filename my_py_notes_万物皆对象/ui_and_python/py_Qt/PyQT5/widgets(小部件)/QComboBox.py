# coding = utf-8

'''
@author = super_fazai
@File    : QComboBox.py
@Time    : 2017/8/16 18:04
@connect : superonesfazai@gmail.com
'''

"""
QComboBox是多选框
"""

from PyQt5.QtWidgets import (QWidget, QLabel,
                             QComboBox, QApplication)
import sys


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.lbl = QLabel("Ubuntu", self)

        combo = QComboBox(self)
        combo.addItem("Ubuntu")     # 加入子选项
        combo.addItem("Mandriva")
        combo.addItem("Fedora")
        combo.addItem("Arch")
        combo.addItem("Gentoo")
        combo.addItem('mac os x')

        combo.move(50, 50)
        self.lbl.move(50, 150)

        combo.activated[str].connect(self.onActivated)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QComboBox')
        self.show()

    def onActivated(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())