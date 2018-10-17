# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from time import sleep
from tenacity import stop_after_delay, stop_after_attempt, retry

# 下面示例用于: 只一次成功退出 or 超时停止
@retry(stop=(stop_after_delay(10) | stop_after_attempt(1)))
def stop_after_10_s_or_5_retries():
    print("Stopping after 10 seconds or 5 retries")
    sleep(11)
    raise Exception

try:
    stop_after_10_s_or_5_retries()
except Exception as e:
    print(e)

