#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import math

#自定义球绝对值函数
def my_abs(x):
    if not isinstabce(x, (int, float)):
        raise TypeError('bad operand type')
    if x>= 0:
        return x
    elif x == -1:
        pass
    else:
        return -x

#空函数
def nop():
    pass

#返回多个值
#但其实这只是一种假象，Python函数返回的仍然是单一值
#原来返回值是一个tuple！但是，在语法上，返回一个tuple可以省略括号，而多个变量可以同时接收一个tuple，按位置赋给对应的值，所以，Python的函数返回多值其实就是返回一个tuple，但写起来更方便
def move(x, y, step, angle=0):
        nx = x + step * math.cos(angle)
        ny = y - step * math.sin(angle)
        return nx, ny
