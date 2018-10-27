# coding:utf-8

'''
@author = super_fazai
@File    : 10minutemail_demo.py
@connect : superonesfazai@gmail.com
'''

from time import time, sleep
from fzutils.register_utils import TenMinuteEmail

_ = TenMinuteEmail()
email_address = _._get_email_address()
print('email_address: {}'.format(email_address))
print('time_left: {}s'.format(_._get_email_seconds_left()))
email_message_count = lambda : _._get_email_message_count()
index = 1
start_time = time()
while email_message_count() == 0 and time() - start_time < 80.:
    sleep_time = 2
    print('{} try, 休眠 {} s...'.format(index, sleep_time))
    index += 1
    sleep(sleep_time)

print('email_message_list: {}'.format(_._get_email_message_list()))