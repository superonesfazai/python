# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午6:01
# @File    : button_test.py

import tkinter

top = tkinter.Tk()
quit = tkinter.Button(top, text='fuck man!', command=top.quit)
quit.pack()
tkinter.mainloop()