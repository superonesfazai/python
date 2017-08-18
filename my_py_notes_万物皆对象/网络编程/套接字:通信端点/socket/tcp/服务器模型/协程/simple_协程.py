# coding = utf-8

'''
@author = super_fazai
@File    : simple_协程.py
@Time    : 2017/8/18 10:01
@connect : superonesfazai@gmail.com
'''

import time

def A():
    while True:
        print("----A---")
        yield
        time.sleep(0.5)

def B(c):
    while True:
        print("----B---")
        c.__next__()
        time.sleep(0.5)

if __name__=='__main__':
    a = A()
    B(a)

'''
----B---
----A---
----B---
----A---
----B---
----A---
----B---
----A---
----B---
----A---
----B---
----A---
----B---
----A---
'''