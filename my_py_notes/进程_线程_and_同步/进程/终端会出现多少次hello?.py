# coding = utf-8

'''
@author = super_fazai
@File    : 终端会出现多少次hello?.py
@Time    : 2017/8/9 15:23
@connect : superonesfazai@gmail.com
'''

from os import fork

fork()      # 调用fork()创建一个子进程
fork()

print("hello")


'''
测试结果:
hello
hello
hello
hello
'''
