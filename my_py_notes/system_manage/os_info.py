# coding = utf-8

'''
@author = super_fazai
@File    : os_info.py
@Time    : 2017/8/8 14:51
@connect : superonesfazai@gmail.com
'''

# Modification 1	: Changed the profile to list again. Order is important. Everytime we run script we don't want to see different ordering.
# Modification 2        : Fixed the AttributeError checking for all properties. Using hasttr().
# Modification 3        : Removed ': ' from properties inside profile.

# 通过运行此脚本得到自己机器的os信息

import platform as pl

profile = [
        'architecture',
        'linux_distribution',
        'mac_ver',
        'machine',
        'node',
        'platform',
        'processor',
        'python_build',
        'python_compiler',
        'python_version',
        'release',
        'system',
        'uname',
        'version',
    ]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


for key in profile:
    if hasattr(pl, key):
        print(key + bcolors.BOLD + ": " + str(getattr(pl, key)()) + bcolors.ENDC)

