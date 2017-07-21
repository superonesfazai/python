#/usr/bin/python3.5
#coding: utf-8

#一次赋 多值
v = ('a', 'b', 'e')
x, y, z = v
print(x+', '+y+', '+z)
'''
(1) v 是一个三元素的 tuple,并且 (x, y, z) 是一个三变量的 tuple。将一个 tuple
赋值给另一个 tuple,会按顺序将 v 的每个值赋值给每个变量
'''

#连续值 赋值
range(7)
print(range(7))
(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY) = range(7)
print(str(MONDAY)+' '+str(TUESDAY)+' '+str(SUNDAY))

