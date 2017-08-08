#!/usr/bin/python3.5
#coding: utf-8

import os

print(os.path.join(r'~/myFile/', 'test.txt'))
print(os.path.join(r'~/myFile', 'test.txt'))

# expander将对使用~来表示当前用户根目录进行扩展
# 在任何平台上,只要用户拥有一个根目录,它就会有效,像 Windows、UNIX 和Mac OS X,
# 但在 Mac OS 上无效
print(os.path.expanduser('~'))

#将这些技术组合在一起,你可以容易地为在用户根目录下的目录和文件构造出路径名
print(os.path.join(os.path.expanduser('~'), 'python'))