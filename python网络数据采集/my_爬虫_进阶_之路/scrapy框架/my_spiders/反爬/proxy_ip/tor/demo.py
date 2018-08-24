# coding:utf-8

import os
import socket
import socks
import requests

url = 'http://api.ipify.org?format=json'

def get_url_body(url):
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket

    r = requests.get(url)
    body = r.text
    print(body)
    print("[+] IP is: " + body.replace("\n", ""))

    return body

get_url_body(url)
