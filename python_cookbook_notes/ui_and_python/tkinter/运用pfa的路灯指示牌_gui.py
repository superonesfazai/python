# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 下午6:26
# @File    : 运用pfa的路灯指示牌_gui.py

from functools import partial as pto
from tkinter import Tk, Button, X
from tkMessageBox import showinfo, showwarning, showerror

warn = 'warn'
crit = 'crit'
regu = 'regu'

signs = {
    'do not enter': crit,
    'railroad': warn,
    '55\nspeed limit':regu,
    'wrong way': crit,
    'merging traffic': warn,
    'one way': regu,
}

crit_cb = lambda: showerror('Error', 'Error button pressed!')
warn_cb = lambda: showwarning('Waring', 'Warning button pressed!')
info_cb = lambda: showinfo('Info', 'Info button pressed!')

top = Tk()
top.title('Roads Sings')
Button(top, text='Quit', command=top.quit, bg='red', fg='white').pack()

my_button = pto(Button, top)
crit_button = pto(my_button, command=crit_cb, bg='white', fg='red')
warn_button = pto(my_button, command=warn_cb, bg='goldenrod1')
regu_button = pto(my_button, command=info_cb, bg='white')

for each_sign in signs:
    sign_type = signs[each_sign]
    cmd = '%sButton(text=%r%s).pack(fill=X, expand=True)' % (sign_type.title(), each_sign,
                                                                '.upper()' if sign_type == crit else '.title()')
    eval(cmd)

top.mainloop()