# coding = utf-8

'''
@author = super_fazai
@File    : simple_menu.py
@Time    : 2017/8/14 19:30
@connect : superonesfazai@gmail.com
'''

"""
创建一个菜单栏, 该菜单栏有一个退出操作的菜单
"""

'''
(Mac OS以不同的方式处理菜单栏)
要获得类似的结果, 我们可以添加以下行: menubar.setNativeMenuBar(False)
'''

import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QApplication)
from PyQt5.QtGui import QIcon

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        exit_act = QAction(QIcon('../images/imagespython.jpg'), '&Exit', self)
                                            # QAction是使用菜单栏, 工具栏或者自定义键盘快捷方式执行动作的抽象
                                            # 上一行创建了一个具有特定图标和'退出'标签的操作
        exit_act.setShortcut('Ctrl+Q')      # 为这个操作定义了快捷方式
        exit_act.setStatusTip('Exit application')   # 创建底部状态栏显示提示信息在状态栏中
        exit_act.triggered.connect(qApp.quit)       # 当执行这个操作, 发出触发信号, 信号连接到小部件的quit()方法QApplication, 终止了应用程序

        self.statusBar()

        menu_bar = self.menuBar()       # 创建一个菜单栏对象
        file_menu = menu_bar.addMenu('&File')   # 创建一个文件菜单
        file_menu.addAction(exit_act)   # 并添加动作addAction()

        menu_bar.setNativeMenuBar(False)    # 添加这句话是为了针对让mac os下显示菜单栏

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('simple menu')
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
