# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-25 下午3:51
# @File    : turtle.onkey.py

import turtle
import time

def f():
    turtle.fd(50)
    turtle.lt(60)

turtle.onkey(f, 'a')
turtle.listen()

time.sleep(3)
