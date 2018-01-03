# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-25 下午3:41
# @File    : turtle.setworldcoordinates.py

import turtle

turtle.reset()
turtle.setworldcoordinates(-50, -7.5, 50, 7.5)
for _ in range(72):
    turtle.left(10)

for _ in range(8):
    turtle.left(45)
    turtle.fd(2)