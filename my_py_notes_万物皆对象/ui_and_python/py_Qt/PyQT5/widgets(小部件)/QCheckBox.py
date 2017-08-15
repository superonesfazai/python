# coding = utf-8

'''
@author = super_fazai
@File    : QCheckBox.py
@Time    : 2017/8/15 17:07
@connect : superonesfazai@gmail.com
'''

"""
通过一个QCheckBox的实例对象改变dialog的title
"""

from PyQt5.QtWidgets import (QWidget, QCheckBox, QApplication)
from PyQt5.QtCore import Qt
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        cb = QCheckBox('Show title', self)      # 创建一个QCheckBox实例对象
        cb.move(20, 20)
        cb.toggle()                             # toggle()方法是功能是实现切换
        cb.stateChanged.connect(self.change_title)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QCheckBox')
        self.show()

    def change_title(self, state):
        """
        勾选显示窗口的title, 不勾选显示为空
        :param state:
        :return:
        """
        if state == Qt.Checked:
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle(' ')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())