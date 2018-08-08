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
import re

from fzutils.common_utils import json_2_dict

result = []
path = '/Users/afa/myFiles/tmp/douyin_ops.txt'
right_data_num = 0
with open(path, "r") as log_file:
    for line in log_file:
        line = line.replace('\n', '').replace(' ', '')
        # print(line)
        if re.compile('data').findall(line) == []:
            continue

        # print(line)
        _ = json_2_dict(json_str=line)
        if _ == {}:
            print('出错行:{0}'.format(line))
            continue

        right_data_num += 1
        print(_)
        # pprint(_)

print(right_data_num)
