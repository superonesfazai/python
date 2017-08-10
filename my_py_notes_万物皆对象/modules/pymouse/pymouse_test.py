#!/usr/bin/env python
# coding=utf-8

from pymouse import PyMouse

m = PyMouse()
m.position()    # 获取当前坐标的位置
m.move(x, y)    # 鼠标移动到x,y 的位置
m.click(x, y)   # 移动并且在x,y 位置点击
m.click(x, y, 1|2)  # 移动并且在x, y 位置点击, 左右键点击
