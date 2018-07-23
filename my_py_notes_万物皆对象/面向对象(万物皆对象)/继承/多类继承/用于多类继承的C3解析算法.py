# coding = utf-8

'''
@author = super_fazai
@File    : 用于多类继承的C3解析算法.py
@Time    : 2017/8/18 19:55
@connect : superonesfazai@gmail.com
'''

"""
如果我们处理多继承, 则会使用较新的[C3解析算法]
"""

# 例1:
class A(object):
    def foo(self):
        print("class A")

class B(object):
    def foo(self):
        print("class B")

class C(A, B):
    pass

C().foo()   # 输出结果为:class A 搜索顺序: C->A->B

# 例2:
class A(object):
   def foo(self):
      print("class A")

class B(A):
   pass

class C(A):
   def foo(self):
      print("class C")

class D(B,C):
   pass

D().foo()   # 输出结果为:class C 搜索顺序: D->B->C->A