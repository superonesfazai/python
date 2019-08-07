# coding:utf-8

'''
@author = super_fazai
@File    : demo2.py
@connect : superonesfazai@gmail.com
'''

import requests
from time import sleep
import stem
import stem.connection
from stem import Signal
from stem.control import Controller

from fzutils.internet_utils import get_random_headers

# with Controller.from_port(port=9051) as controller:
#     """连接tor前必须先认证"""
#     controller.authenticate(password='haguagaugugxa')  # provide the password here if you set one
#
#     bytes_read = controller.get_info("traffic/read")
#     bytes_written = controller.get_info("traffic/written")
#
#     print("My Tor relay has read %s bytes and written %s." % (bytes_read, bytes_written))

def renew_tor():
    '''
    让Tor重建连接，获得新的线路
    :return:
    '''
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='haguagaugugxa')
        controller.signal(Signal.NEWNYM)
        controller.close()

def get_public_ip():
    renew_tor()
    proxies = {
        'http': '127.0.0.1:8118'
    }
    headers = get_random_headers(
        connection_status_keep_alive=False,
        upgrade_insecure_requests=False,
        cache_control='', )
    body = requests.get(
        url="https://httpbin.org/get",
        headers=headers,
        proxies=proxies)\
        .text
    print(body)

# 47.91.21.176
for i in range(10):
    get_public_ip()
    print('sleep 20s...')
    sleep(20)