# coding = utf-8

'''
@author = super_fazai
@File    : set_test.py
@Time    : 2017/8/7 16:09
@connect : superonesfazai@gmail.com
'''

x = set('abcd')
print('x = ', x)
print(type(x))

print('-' * 30)

y = set(['h','e','l','l','o'])
print('y = ', y)
z = set('spam')
print('z = ', z)

print('-' * 30)

print('y & z = ', y & z)        # 交集
print('x & z = ', x & z)        # 交集
print('x | y = ', x | y)        # 并集
print('x - y = ', x - y)        # 差集

print('(x-z) | (z-x) = ', (x-z) | (z-x))    # 两个效果一样
print('x ^ z = ', x ^ z)                    # 对称差集(在x或z中， 但不会同时出现在⼆者中)

'''
测试结果:
x =  {'b', 'd', 'c', 'a'}
<class 'set'>
------------------------------
y =  {'l', 'o', 'h', 'e'}
z =  {'m', 'a', 's', 'p'}
------------------------------
y & z =  set()
x & z =  {'a'}
x | y =  {'c', 'h', 'e', 'l', 'a', 'b', 'o', 'd'}
x - y =  {'b', 'a', 'c', 'd'}
(x-z) | (z-x) =  {'s', 'b', 'm', 'c', 'd', 'p'}
x ^ z =  {'m', 'c', 'p', 's', 'b', 'd'}
'''