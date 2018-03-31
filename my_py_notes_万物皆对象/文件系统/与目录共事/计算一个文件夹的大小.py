# coding = utf-8

'''
@author = super_fazai
@File    : 计算一个文件夹的大小.py
@Time    : 2017/8/8 14:33
@connect : superonesfazai@gmail.com
'''

# 扫描给予对应文件夹名字的文件夹,计算一个文件夹的大小

import os
import sys      # Load the library module and the sys module for the argument vector'''

try:
    directory = sys.argv[1]   # 设置传入的参数, 即文件夹的名字, 此处只接收第一个给予的参数
except IndexError:
    sys.exit("Must provide an argument.")

dir_size = 0    # Set the size to 0
fsizedicr = {'Bytes': 1,
             'Kilobytes': float(1) / 1024,
             'Megabytes': float(1) / (1024 * 1024),
             'Gigabytes': float(1) / (1024 * 1024 * 1024)}

for (path, dirs, files) in os.walk(directory):      # Walk through all the directories. For each iteration, os.walk returns the folders, subfolders and files in the dir.
    for file in files:                              # Get all the files
        filename = os.path.join(path, file)
        dir_size += os.path.getsize(filename)       # Add the size of each file in the root dir to get the total size.

fsizeList = [str(round(fsizedicr[key] * dir_size, 2)) + " " + key for key in fsizedicr] # List of units

if dir_size == 0: print ("File Empty") # Sanity check to eliminate corner-case of empty file.

else:
    for units in sorted(fsizeList)[::-1]: # Reverse sort list of units so smallest magnitude units print first.
        print ("Folder Size: " + units)
