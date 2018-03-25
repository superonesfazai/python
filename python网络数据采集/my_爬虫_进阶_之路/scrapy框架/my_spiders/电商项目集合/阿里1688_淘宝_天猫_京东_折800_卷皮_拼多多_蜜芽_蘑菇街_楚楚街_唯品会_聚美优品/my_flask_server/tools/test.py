# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

from my_logging import set_logger

my_lg = set_logger(log_file_name='test.txt')
my_lg.exception('啊')
my_lg.info('test')

