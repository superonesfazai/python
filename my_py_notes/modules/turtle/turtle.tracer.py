# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-25 下午3:46
# @File    : turtle.tracer.py

import turtle
import time

turtle.tracer(8, 25)
dist = 2
for i in range(200):
    turtle.fd(dist)
    turtle.rt(90)
    dist += 2

time.sleep(2)
