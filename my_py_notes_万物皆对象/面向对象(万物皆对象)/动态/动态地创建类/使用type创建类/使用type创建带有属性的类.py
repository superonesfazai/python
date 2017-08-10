# coding = utf-8

'''
@author = super_fazai
@File    : 使用type创建带有属性的类.py
@Time    : 2017/8/6 16:05
@connect : superonesfazai@gmail.com
'''

A = type('A', (), {'bar': True})

print(A)
print(A.bar)

f = A()
print(f)
print(f.bar)

A_child = type('A_child', (A,), {})
print(A_child)
print(A_child.bar)      #  bar属性继承自A

'''
测试结果:
<class '__main__.A'>
True
<__main__.A object at 0x10915a710>
True
<class '__main__.A_child'>
True
'''