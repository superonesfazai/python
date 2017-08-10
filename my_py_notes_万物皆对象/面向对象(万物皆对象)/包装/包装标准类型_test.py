# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-23 下午5:25
# @File    : 包装标准类型_test.py

from time import time, ctime

class TimeWrapMe(object):
    def __init__(self, obj):
        self.__data = obj
        self.__ctime = self.__mtime = self.__atime = time()

    def get(self):
        self.__atime = time()
        return self.__data

    def get_time_val(self, t_type):
        if not isinstance(t_type, str) or \
                t_type[0] not in 'cma':
            raise(TypeError, "argument of 'c', 'm', 'a' req'd'")
        return getattr(self, '_%s__%stime' % (self.__class__.__name__, t_type[0]))

    def get_time_str(self, t_type):
        return ctime(self.get_time_val(t_type))

    def set(self, obj):
        self.__data = obj
        self.__mtime = self.__atime = time()

    def __repr__(self):     #repr()
        self.__atime = time()
        return 'self.__data'

    def __str__(self):      #str()
        self.__atime = time()
        return str(self.__data)

    def __getattr__(self, item):    #delegate
        self.__atime = time()
        return getattr(self.__data, item)

time_wrapped_obj = TimeWrapMe(932)
print(time_wrapped_obj.get_time_str('c'))
print(time_wrapped_obj.get_time_str('m'))
print(time_wrapped_obj.get_time_str('a'))
print(time_wrapped_obj)
print(time_wrapped_obj.get_time_str('c'))
print(time_wrapped_obj.get_time_str('m'))
print(time_wrapped_obj.get_time_str('a'))
# 你将注意到,一个对象在第一次被包装时,创建,修改及最后一次访问的时间是一样
# 一旦对象被访问,访问时间即被更新,但其他的没有动
# 如果用set()来置换对象,则修改和最后一次访问时间会被更新
# 下面,最后是对对象的读访问操作
print('')

time_wrapped_obj.set('time is up!')
print(time_wrapped_obj.get_time_str('m'))
print(time_wrapped_obj)
print(time_wrapped_obj.get_time_str('c'))
print(time_wrapped_obj.get_time_str('m'))
print(time_wrapped_obj.get_time_str('a'))
