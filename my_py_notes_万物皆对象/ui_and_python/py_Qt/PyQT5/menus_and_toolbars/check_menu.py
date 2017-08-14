# coding = utf-8

'''
@author = super_fazai
@File    : check_menu.py
@Time    : 2017/8/14 20:05
@connect : superonesfazai@gmail.com
'''

"""
创建一个可选菜单    (可以被检查和取消选中的菜单)
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication)

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.statusBar = self.statusBar()
        self.statusBar.showMessage('Ready')

        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu('View')    # 创建一个'视图'菜单, 菜单中的操作用于显示或隐藏状态栏
                                                # 当菜单栏可见时, 菜单栏被选中

        menu_bar.setNativeMenuBar(False)  # 添加这句话是为了针对让mac os下显示菜单栏

        view_stat_act = QAction('View status_bar', self, checkable=True)    # 通过checkable选项我们创建了一个可检查的菜单
        view_stat_act.setStatusTip('View status_bar')       # 状态栏
        view_stat_act.setChecked(True)          # 由于状态栏从一开始是可见的, 所以使用setChecked()方法检查操作
        view_stat_act.triggered.connect(self.toggle_menu)

        view_menu.addAction(view_stat_act)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('check menu')
        self.show()

    def toggle_menu(self, state):   # 根据操作的状态, 显示或隐藏状态栏
        if state:
            self.statusBar.show()
        else:
            self.statusBar.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

