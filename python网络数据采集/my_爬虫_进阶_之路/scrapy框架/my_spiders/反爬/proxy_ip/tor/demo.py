# coding:utf-8

import os
import socket
import socks
import requests

url = 'https://httpbin.org/get'
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket

def get_url_body(url):
    r = requests.get(url)
    body = r.text
    print(body)

    return body

get_url_body(url)
