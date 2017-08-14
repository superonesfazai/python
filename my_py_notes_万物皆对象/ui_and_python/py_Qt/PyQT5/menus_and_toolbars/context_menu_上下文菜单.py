# coding = utf-8

'''
@author = super_fazai
@File    : context_menu_上下文菜单.py
@Time    : 2017/8/14 20:22
@connect : superonesfazai@gmail.com
'''

"""
创建一个上下文菜单(也称为弹出菜单)  (是在某些上下文下显示命令的列表)
"""

'''
例如, 在Opera Web浏览器中, 当我们右键单击网页时, 我们将获得一个上下文菜单。
这里我们可以重新加载页面, 返回或查看页面源。
如果我们右键单击工具栏, 我们将获得另一个用于管理工具栏的上下文菜单
'''

import sys
from PyQt5.QtWidgets import (QMainWindow, qApp, QMenu, QApplication)

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('context menu')
        self.show()

    # 重写contextMenuEvent()方法
    def contextMenuEvent(self, QContextMenuEvent):
        c_menu = QMenu(self)

        new_act = c_menu.addAction('New')
        opn_act = c_menu.addAction('Open')
        quit_act = c_menu.addAction('Quit')
        action = c_menu.exec_(self.mapToGlobal(QContextMenuEvent.pos()))
                        # 使用exec_()方法显示上下文菜单, 从事件对象获取鼠标指针的坐标
                        # 该mapToGlobal()方法将窗口小部件坐标转换为全局屏幕坐标

        if action == quit_act:      # 如果从上下文菜单返回的操作等于退出操作, 则终止应用程序
            qApp.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())