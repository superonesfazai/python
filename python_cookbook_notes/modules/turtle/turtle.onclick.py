# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-25 下午3:56
# @File    : turtle.onclick.py

import turtle
import time

def goto_pos(x, y):
    turtle.up()
    turtle.goto(x, y)
    print('goto (%d, %d)' % (x, y))
    turtle.dot(10, 'red')

turtle.Screen().onclick(goto_pos)
turtle.Screen().mainloop()
