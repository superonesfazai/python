# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午6:04
# @File    : label_button_test.py

import tkinter

top = tkinter.Tk()
fuck = tkinter.Label(top, text='fuck man!')
fuck.pack()

quit = tkinter.Button(top, text='Quit',
                      command=top.quit, bg='red',
                      fg='white')

quit.pack()
tkinter.mainloop()