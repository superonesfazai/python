# coding:utf-8

'''
@author = super_fazai
@File    : remain_rest_time_total.py
@connect : superonesfazai@gmail.com
'''

"""
remain rest time total
"""

from pprint import pprint
from fzutils.common_utils import json_2_dict

def total():
    file_json_path = '/Users/afa/Desktop/remain_rest_time_total.json'

    ori_json = ''
    with open(file_json_path, 'r') as f:
        for line in f:
            ori_json += line.replace('\n', '').replace(' ', '')

    data = json_2_dict(json_str=ori_json)
    # pprint(data)

    total = 0.
    for value in data.values():
        total += value
    print('总计hours: {}h\n能调days: {}day'.format(total, total/8))

    return

total()