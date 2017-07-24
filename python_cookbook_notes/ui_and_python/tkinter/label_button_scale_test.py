# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午6:14
# @File    : label_button_scale_test.py

from tkinter import *

def resize(ev = None):
    label.config(font='Helvetica -%d bold' % scale.get())

top = Tk()
top.geometry('250x150')

label = Label(top, text='fuck man!',
              font='Helvetica -12 bold')
label.pack(fill=Y, expand=1)

scale = Scale(top, from_=10, to=40, orient=HORIZONTAL, command=resize)

scale.set(12)
scale.pack(fill=X, expand=1)

quit = Button(top, text='Quit', command=top.quit,
                activeforeground='white',
                activebackground='red')

quit.pack()

mainloop()