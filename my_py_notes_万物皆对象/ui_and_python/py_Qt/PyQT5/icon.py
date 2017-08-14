# coding = utf-8

'''
@author = super_fazai
@File    : icon.py
@Time    : 2017/8/14 16:52
@connect : superonesfazai@gmail.com
'''

"""
创建一个带图标的窗口
"""

# 注意mac下面会显示不出来

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 下面的三个方法都从QWidget类中继承
        self.setGeometry(300, 300, 300, 220)    # setGeometry()做2件事, 1.定位在屏幕上的窗口 2.并设置其大小 前两个参数是窗口的x和y位置. 第三个是宽度, 第四个是窗口的高度
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('images/imagespython.jpg'))    # 设置应用图标
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Example()
    sys.exit(app.exec_())