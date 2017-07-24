# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 上午8:53
# @File    : 批量修改文件名称.py

import os

print('')

file_path_now = os.getcwd()     # 获取当前目录
print(file_path_now)
file_path_now = os.chdir(file_path_now)     # 改变路径
directory_name = input('请输入要修改名称的文件夹:')
# 获取文件所在目录
file_list = os.listdir(directory_name)
# print(file_list)
if os.path.isdir(directory_name):
    for file in file_list:
        # if os.path.isfile(file):
        os.rename(file, '[北京热]'+file)       # 每个文件逐一修改名称
