#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
__author__ = 'afa'

import os

def check(file_name = None):
    #性能检测
    if file_name is None:
        print('请指定文件名称')
    else:
        cmd = "python -m cProfile %s" % file_name
        print(cmd)
        os.system(cmd)

if __name__ == '__main__':
    check('performance.py')
