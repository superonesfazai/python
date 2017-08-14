# coding = utf-8

'''
@author = super_fazai
@File    : sub_menu_子菜单.py
@Time    : 2017/8/14 19:54
@connect : superonesfazai@gmail.com
'''

"""
创建一个子菜单(另一个菜单中的菜单)
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QMenu, QApplication)

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        menu_bar.setNativeMenuBar(False)  # 添加这句话是为了针对让mac os下显示菜单栏

        imp_Menu = QMenu('Import', self)        # 创建新菜单QMenu
        imp_act = QAction('Import mail', self)
        imp_Menu.addAction(imp_act)             # 在子菜单中添加一个动作addAction()

        new_act = QAction('New', self)

        file_menu.addAction(new_act)
        file_menu.addMenu(imp_Menu)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('sub_menu')
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
