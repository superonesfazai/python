# coding:utf-8

'''
@author = super_fazai
@File    : cookies_to_dict.py
@Time    : 2017/9/24 13:55
@connect : superonesfazai@gmail.com
'''

from pprint import pprint

def stringToDict(cookies):
    itemDict = {}
    items = cookies.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')  # 记得去除空格
        value = item.split('=')[1]
        itemDict[key] = value
    return itemDict


# cookies = 'SUV=1505446925567125; SMYUV=1505446925568464; UM_distinctid=15e83a1210450f-0767352fad6394-31637e01-fa000-15e83a12105261; ABTEST=0|1506166032|v1; IPLOC=CN1100; SUID=F28867D3232C940A0000000059C64510; SUID=0270820E1F13940A0000000059C64510; weixinIndexVisited=1; SNUID=82F916A3717529A8EF7CE70471D86921; JSESSIONID=aaauZkEn6Jewl6APb-y6v; sct=13'
cookies = '__cfduid=d5b4c724033c3d9a88f0dcb7ce1c8c7c61508553693; ASP.NET_SessionId=d1dshn0pmisymfpmkfvqjhxd; yjs_id=TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTJfNikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYxLjAuMzE2My4xMDAgU2FmYXJpLzUzNy4zNnx3d3cudGFvY2VjZS5jb218MTUwODU1MzY5NjA4N3xodHRwczovL3d3dy5iYWlkdS5jb20vbGluaz91cmw9dVBWem1sSUF1YTlkZnR0enp4VG9kRW9nNmRSd1l4WC1YdmhCZmhPQ3VqUm9pYW9rS3dMYmxVbEYxcGJZeWg4NyZ3ZD0mZXFpZD1kZDM0ODViNDAwMDA5YmYxMDAwMDAwMDM1OWVhYjNjMw; ctrl_time=1; Hm_lvt_dab68e029c4a0d36d12a9daef17eef11=1508553696,1508553835,1508553841; Hm_lpvt_dab68e029c4a0d36d12a9daef17eef11=1508553841'
pprint(stringToDict(cookies))