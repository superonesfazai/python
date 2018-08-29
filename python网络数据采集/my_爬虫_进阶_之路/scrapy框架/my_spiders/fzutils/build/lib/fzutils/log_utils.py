# coding:utf-8

# log utils

"""
切记: 不要重复创造日志对象，否则会重复打印
"""

import logging
from logging import handlers
# import os
# from colorama import init, Back, Fore

__all__ = [
    'set_logger'
]

CONSOLE_FORMATTER = '%(asctime)s [%(levelname)-6s] ➞ %(message)s'
FILE_FORMATTER = '%(asctime)s [%(levelname)-6s] at %(filename)s 出错函数%(funcName)s.%(lineno)d ↴\n %(message)s\n'

def set_logger(log_file_name,
               console_log_level=logging.DEBUG,
               file_log_level=logging.ERROR,
               console_formatter=CONSOLE_FORMATTER,
               file_formatter=FILE_FORMATTER,
               logger_name='my_logger'):
    # 创建一个logger,可以考虑如何将它封装
    logger = logging.getLogger(logger_name)     # 建议: 在有多个相互关联的文件都需要用到python的日志系统时，不要用默认的root logger。因为所有的名称都会继承root导致重复打印。用logger时一定要起名字！！
    logger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件
    # fh = logging.FileHandler(os.path.join(os.getcwd(), './my_log.txt'))
    file_handler = handlers.RotatingFileHandler(filename=log_file_name, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')  # 通过下面这句话就可以输出中文, encoding='utf-8'

    file_handler.setLevel(file_log_level)

    # 再创建一个handler，用于输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_log_level)

    # 定义handler的输出格式
    _console_formatter = logging.Formatter(console_formatter)
    _file_formatter = logging.Formatter(file_formatter)
    console_handler.setFormatter(_console_formatter)
    file_handler.setFormatter(_file_formatter)

    # 给logger添加handler
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # 记录一条日志
    # logger.info('hello world, i\'m log helper in python, may i help you')

    return logger
