#!/usr/bin/python3.5
#coding:utf-8

import os

#注意用listdir()时得用具体目录位置具体
print(os.listdir('/home/afa/myFiles'))

dirname = '/home/afa/myFiles/'

#在这里,我们使用 os.path.join 来确保得到一个全路径名
print([f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))])

print([f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))])

# 通过os.getcwd()来获取当前目录
print(os.getcwd())

'''
我们使用 os.path.normcase(f) 根据操作系统的缺省
值对大小写进行标准化处理。 normcase 是一个有用的函数,用于对大小写
不敏感操作系统的一个补充。这种操作系统认为 mahadeva.mp3 和
mahadeva.MP3
normcase
是同一个文件名。例如,在 Windows 和 Mac OS 下,
将把整个文件名转换为小写字母;而在 UNIX 兼容的系统下,它
将返回未作修改的文件名
'''

#使用glob列出目录

print(os.listdir('/home/afa/myFiles/'))

import glob
'''
glob 模块,另一方面,接受一个通配符并且返回文件的或目录的完整路径
与之匹配。这个通配符是一个目录路径加上“*.csv”,它将匹配所有的.csv
文件系统。注意返回列表的每一个元素已经包含了文件的完整路径
'''
print(glob.glob('/home/afa/myFiles/tmp/aircrack-ng_/go/*.csv'))
print(glob.glob('/home/afa/myFiles/tmp/aircrack-ng_/go/-02*'))

'''
现在考查这种情况:你有一个 music 目录,它包含几个子目录,子目录中
包含一些 .mp3 文件系统。使用两个通配符,仅仅调用 glob 一次就可以立刻获
得所有这些文件的一个 list。一个通配符是 "*.mp3" (用于匹配 .mp3 文件系统),
另一个通配符是 子目录名本身 ,用于匹配 c:\music 中的所有子目录。这看
上去很简单,但它蕴含了强大的功能
'''