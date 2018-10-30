# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@connect : superonesfazai@gmail.com
'''

"""
因为 PhantomJS 有网络通信的检查功能，它也很适合用来做网络行为的分析

当接受到请求时，可以通过改写onResourceRequested和onResourceReceived回调函数来实现接收到资源请求和资源接受完毕的监听
"""