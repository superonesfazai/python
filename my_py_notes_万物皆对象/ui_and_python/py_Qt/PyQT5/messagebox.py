# coding = utf-8

'''
@author = super_fazai
@File    : messagebox.py
@Time    : 2017/8/14 17:31
@connect : superonesfazai@gmail.com
'''

"""
按钮的消息框展示
"""

import sys
from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Message box')
        self.show()

    # 重新实现closeEvent()方法来处理关闭程序
    def closeEvent(self, QCloseEvent):
        # 返回值存储在reply变量中
        reply = QMessageBox.question(self, 'Message',   # 标题栏
                                     'Are you sure to quit?',   # 对话框显示的文本
                                     QMessageBox.Yes | QMessageBox.No,  # 指定出现在对话框中按钮的组合
                                     QMessageBox.No)    # 默认按钮
        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())