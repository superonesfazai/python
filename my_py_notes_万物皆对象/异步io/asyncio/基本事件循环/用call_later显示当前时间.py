# coding:utf-8

'''
@author = super_fazai
@File    : 用call_later显示当前时间.py
@connect : superonesfazai@gmail.com
'''

from asyncio import get_event_loop
import datetime

def show_date(end_time, loop):
    print(datetime.datetime.now())
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, show_date, end_time, loop)
    else:
        loop.stop()

loop = get_event_loop()

# Schedule the first call to show_date()
end_time = loop.time() + 5.0
loop.call_soon(show_date, end_time, loop)

# Blocking call interrupted by loop.stop()
loop.run_forever()
loop.close()