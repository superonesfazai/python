# coding = utf-8

'''
@author = super_fazai
@File    : center_window_on_the_screen.py
@Time    : 2017/8/14 17:44
@connect : superonesfazai@gmail.com
'''

"""
在桌面中心位置创建一个窗口
"""

import sys
# QDesktopWidget类提供了有关用户的桌面信息, 包括屏幕尺寸
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QApplication)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(250, 150)
        self.center()   # 将窗口在中心显示的代码放到自定义center()方法中

        self.setWindowTitle('Center')
        self.show()

    def center(self):
        qr = self.frameGeometry()   # 得到一个指定主窗口几何的矩形, 这包括任何窗框
        cp = QDesktopWidget().availableGeometry().center()  # 得到中心点     我们弄清了我们的显示器的屏幕分辨率。从这个决议来看，我们得到了中心点。
        qr.moveCenter(cp)           # 我们的矩形已经有它的宽度和高度。现在我们将矩形的中心设置到屏幕的中心。矩形的大小不变
        self.move(qr.topLeft())     # 将应用程序窗口的左上角移到qr矩形的左上角, 从而将窗口对准在我么的屏幕上

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec_())