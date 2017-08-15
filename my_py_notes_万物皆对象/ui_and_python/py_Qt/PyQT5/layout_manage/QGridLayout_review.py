# coding = utf-8

'''
@author = super_fazai
@File    : QGridLayout_review.py
@Time    : 2017/8/15 12:32
@connect : superonesfazai@gmail.com
'''

"""
使用QGridLayout创建一个更复杂的布局
"""

import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        title_edit = QLineEdit()        # 创建一个行编辑框对象
        author_edit = QLineEdit()
        review_edit = QTextEdit()       # 创建一个多行编辑文本框

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(title_edit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(author_edit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(review_edit, 3, 1, 5, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())