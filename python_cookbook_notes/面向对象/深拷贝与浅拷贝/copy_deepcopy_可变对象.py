# coding = utf-8

'''
@author = super_fazai
@File    : copy_deepcopy_可变对象.py
@Time    : 2017/8/3 20:32
@connect : superonesfazai@gmail.com
'''

# 对可变对象的拷贝
from copy import copy,deepcopy
a = [1,2,3]
b = a
c = copy(b)
d = deepcopy(a)
a.append(4)
print(id(a) == id(b))    # --->  True
print(id(a) == id(c))    # --->  False
print(id(a) == id(d))    # --->  False

print('')

from copy import copy,deepcopy
a = [1,2,3]
b = a
c = copy(b)
d = deepcopy(a)
a = [1,2,3,4,5]
print(id(a) == id(b))    # --->  False
print(id(a) == id(c))    # --->  False
print(id(a) == id(d))    # --->  False