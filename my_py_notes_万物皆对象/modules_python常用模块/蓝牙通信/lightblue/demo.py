# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from pprint import pprint
import lightblue

blue_devices_list = lightblue.finddevices(
    getnames=True,
    length=20,)
pprint(blue_devices_list)