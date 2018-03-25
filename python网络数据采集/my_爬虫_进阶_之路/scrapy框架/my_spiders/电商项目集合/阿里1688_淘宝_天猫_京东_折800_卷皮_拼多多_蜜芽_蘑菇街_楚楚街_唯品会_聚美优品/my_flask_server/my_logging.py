# coding:utf-8

'''
@author = super_fazai
@File    : my_logging.py
@Time    : 2018/2/7 10:56
@connect : superonesfazai@gmail.com
'''

import logging
from logging import handlers
import os

__all__ = ['set_logger']

def set_logger(log_file_name, console_log_level=logging.DEBUG, file_log_level=logging.ERROR):
    # 创建一个logger,可以考虑如何将它封装
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件
    # fh = logging.FileHandler(os.path.join(os.getcwd(), './my_log.txt'))
    # 通过下面这句话就可以输出中文, encoding='utf-8'
    file_handler = handlers.RotatingFileHandler(filename=log_file_name, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')
    file_handler.setLevel(file_log_level)

    # 再创建一个handler，用于输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_log_level)

    # 定义handler的输出格式
    console_formatter = logging.Formatter('%(asctime)s [%(levelname)-6s] ➞ %(message)s')
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)-6s] at %(filename)s 出错函数%(funcName)s.%(lineno)d ↴\n %(message)s\n')
    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)

    # 给logger添加handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 记录一条日志
    # logger.info('hello world, i\'m log helper in python, may i help you')
    return logger

# log_file_name = './logs/my_log.txt'
# lg = set_logger(log_file_name=log_file_name)
#
# try:
#     1/0
# except Exception as e:
#     # lg.error(e, exc_info=False)
#     lg.exception(e)