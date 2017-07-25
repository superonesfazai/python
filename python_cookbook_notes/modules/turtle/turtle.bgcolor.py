# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-25 下午3:19
# @File    : turtle.bgcolor.py

import turtle
import time

turtle.Screen().screensize(400, 300)
turtle.Screen().bgcolor('orange')
time.sleep(2)
# turtle._Screen.delay(5)
print(turtle.Screen().bgcolor())

turtle.Screen().screensize(400, 300)
turtle.Screen().bgcolor('#800080')
time.sleep(2)
print(turtle.Screen().bgcolor())

