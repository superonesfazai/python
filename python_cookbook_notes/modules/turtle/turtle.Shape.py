# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-25 下午4:06
# @File    : turtle.Shape.py

import turtle

poly = ((0,0),(10,-5),(0,10),(-10,-5))
s = turtle.Shape('compound')
s.addcomponent(poly, 'red', 'blue')
