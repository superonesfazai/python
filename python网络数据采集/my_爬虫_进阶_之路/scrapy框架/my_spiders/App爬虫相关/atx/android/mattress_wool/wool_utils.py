# coding:utf-8

'''
@author = super_fazai
@File    : wool_utils.py
@connect : superonesfazai@gmail.com
'''

from time import sleep
from random import uniform

def device_id_in_red_rice_1s(device_id:str) -> bool:
    """
    设备id 是否是红米1s
    :return:
    """
    res = False
    # 红米1s
    red_rice_1s_device_id_list = [
        '0123456789ABCDEF',
        'de295374',
    ]
    if device_id in red_rice_1s_device_id_list:
        res = True

    return res

def device_id_in_oppo_r7s(device_id:str) -> bool:
    """
    设备id 是否为oppo r7s
    :param device_id:
    :return:
    """
    res = False
    # oppo r7s
    oppo_r7s_device_id_list = [
        'JNPJJREEY5NBS88D',
        'KFWORWGQJNIBZPOV',
        'USOFUK7SFUJBAQ6P',
    ]
    if device_id in oppo_r7s_device_id_list:
        res = True

    return res

def sleep_random_time(min_time:float, max_time:float) -> None:
    """
    随机休眠某段时间
    :param min_time:
    :param max_time:
    :return:
    """
    sleep(uniform(min_time, max_time))

    return