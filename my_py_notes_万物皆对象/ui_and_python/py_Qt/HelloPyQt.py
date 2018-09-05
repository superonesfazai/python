#!/usr/bin/python3.5
#coding:utf-8

import sys
from PyQt4 import QtCore, QtGui

class HelloPyQt(QtGui.QWidget):
    def __init__(self, parent = None):
        super(HelloPyQt, self).__init__(parent)
        self.setWindowTitle("py_Qt Test")
      
        self.textHello = QtGui.QTextEdit("This is a 避免死锁.md program written in python with py_Qt lib!")
        self.btnPress = QtGui.QPushButton("Press me!")
      
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.textHello)
        layout.addWidget(self.btnPress)   
        self.setLayout(layout)

        self.btnPress.clicked.connect(self.btnPress_Clicked)
      
    def btnPress_Clicked(self):
        self.textHello.setText("Hello py_Qt!\nThe button has been pressed.")

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = HelloPyQt()
    mainWindow.show()
    sys.exit(app.exec_())