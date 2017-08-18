# coding = utf-8

'''
@author = super_fazai
@File    : re_complie_编译re对象提高re匹配速度.py
@Time    : 2017/8/18 17:19
@connect : superonesfazai@gmail.com
'''

"""
re.compile函数根据一个模式字符串和可选的标志参数生成一个正则表达式对象。
该对象拥有一系列方法用于正则表达式匹配和替换。

这么用的原因就是为了提高正则匹配的速度, 重复利用re表达式
"""