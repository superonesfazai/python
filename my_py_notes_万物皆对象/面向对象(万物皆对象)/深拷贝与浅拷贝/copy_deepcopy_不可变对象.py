# coding = utf-8

'''
@author = super_fazai
@File    : copy_deepcopy_test1.py
@Time    : 2017/8/3 20:28
@connect : superonesfazai@gmail.com
'''
# 对不可变对象的拷贝
from copy import copy,deepcopy
a = (1,2,3)
b = a
c = copy(b)
d = deepcopy(a)
print(id(a) == id(b))    # --->  True
print(id(a) == id(c))    # --->  True
print(id(a) == id(d))    # --->  True

print('')

from copy import copy, deepcopy
a = (1, 2, 3, [])
b = a
c = copy(b)
d = deepcopy(a)
print(id(a) == id(b))    # --->  True
print(id(a) == id(c))    # --->  True
print(id(a) == id(d))    # --->  False