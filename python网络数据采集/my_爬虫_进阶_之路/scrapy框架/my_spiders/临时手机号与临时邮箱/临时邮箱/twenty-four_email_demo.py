# coding:utf-8

'''
@author = super_fazai
@File    : twenty-four_email_demo.py
@connect : superonesfazai@gmail.com
'''

"""
can use
"""

from time import time, sleep
from fzutils.register_utils import TwentyFourEmail

_ = TwentyFourEmail()
email_address = _._get_email_address()
print('获取到的email_address: {}'.format(email_address))
# # 换个邮箱
# email_address = _._get_new_email_address()
# print(email_address)
message_count = lambda : _._get_email_message_count()
start_time = time()
index = 1
while message_count() in (0, None) and time() - start_time < 100.:
    sleep_time = 2
    print('{} try, 休眠{}s...'.format(index, sleep_time))
    sleep(sleep_time)
    index += 1

message_list = _._get_email_message_list()
print(message_list)
