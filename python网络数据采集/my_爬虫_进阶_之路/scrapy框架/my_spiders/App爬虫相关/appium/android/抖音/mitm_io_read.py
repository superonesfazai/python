# coding:utf-8

'''
@author = super_fazai
@File    : mitm_io_read.py
@Time    : 2017/8/7 16:37
@connect : superonesfazai@gmail.com
'''

"""
从log文件中读取需求信息并处理
"""

from pprint import pprint

from fzutils.common_utils import json_2_dict

result = []
path = '/Users/afa/myFiles/tmp/douyin_ops.txt'
with open(path, "r") as log_file:
    for line in log_file:
        line = line.replace('\n', '').replace(' ', '')
        # print(line)
        _ = json_2_dict(json_str=line)
        if _ == {}:
            print('出错行:{0}'.format(line))

        print(_)
        # pprint(_)
