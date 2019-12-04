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
from collections import OrderedDict
from fzutils.common_utils import json_2_dict
from fzutils.time_utils import (
    date_parse,
    datetime_to_timestamp,)

def total():
    def get_ordered_dict(data):
        """
        获取有序字典
        :param data:
        :return:
        """
        # 获取有序字典
        ordered_dict = OrderedDict()
        tmp_ordered_day_list = [{
            datetime_to_timestamp(date_parse(key)): key,
        } for key in data.keys()]
        # 已被正确排序的日期
        ordered_day_list = sorted(
            tmp_ordered_day_list,
            key=lambda item: item.keys())
        # pprint(ordered_day_list)

        for item_dict in ordered_day_list:
            item_dict_value = list(item_dict.values())[0]
            # print(item_dict_value)
            for key, value in data.items():
                if key == item_dict_value:
                    ordered_dict[key] = value
                else:
                    continue

        return ordered_dict

    file_json_path = '/Users/afa/Desktop/remain_rest_time_total.json'
    ori_json = ''
    with open(file_json_path, 'r') as f:
        for line in f:
            ori_json += line.replace('\n', '').replace(' ', '')

    # 默认字典无序
    data = json_2_dict(json_str=ori_json)
    # pprint(data)
    # 获取有序字典
    ordered_dict = get_ordered_dict(data)
    pprint(ordered_dict)

    total = 0.
    # 是否进入if total >= xxx and sign_value 的信号值
    sign_value = True
    rest_hours = 0.
    for key, value in ordered_dict.items():
        # print(key, value)
        if value == .5:
            # 不满一小时不算
            continue

        total += value
        if total >= 280 and sign_value:
            # 160h是2018.12->2019.5月total调休时长, 2019.5 用到2019.4.30号
            # 184h是2018.12->2019.6月total调休时长, 2019.6 用到2019.5.24号
            # 200h是2018.12->2019.7月total调休时长, 2019.7 用到2019.6.13号
            # 208h是2018.12->2019.8月total调休时长, 2019.8 用到2019.6.18号
            # 216h是2018.12->2019.9月total调休时长, 2019.9 用到2019.6.21号
            # 240h是2018.12->2019.10月total调休时长, 2019.10 用到2019.7.26号
            # 280h是2018.12->2019.11月total调休时长, 2019.11 用到2019.9.24号
            print('当前total: {}, 当前调休到day: {}'.format(total, key))
            # break
            sign_value = False
        else:
            if not sign_value:
                # print(key, value)
                rest_hours += value
            else:
                pass

    print('rest_time: {}h, can used days: {}'.format(rest_hours, rest_hours/8))
    print('\n总计hours: {}h, 能调days: {}'.format(total, total/8))

    return

total()