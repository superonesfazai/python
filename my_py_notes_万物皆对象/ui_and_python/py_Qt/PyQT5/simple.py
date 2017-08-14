# coding = utf-8

'''
@author = super_fazai
@File    : simple.py
@Time    : 2017/8/14 16:42
@connect : superonesfazai@gmail.com
'''

"""
使用PyQT5创建一个简单的窗口
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)    # 每个PyQT5应用程序必须创建一个应用程序对象. 该sys.argv参数是来自命令行的参数列表

    w = QWidget()       # 创建一个用户界面实例对象
    w.resize(250, 150)  # 调整窗口的大小, 宽:250 高:150
    w.move(300, 300)    # 在屏幕上将窗口移到指定坐标处
    w.setWindowTitle('simple')
    w.show()            # 一个窗口首先在内存中创建, 然后在屏幕上显示

    sys.exit(app.exec_())   # 这个方法确保了一个干净的退出