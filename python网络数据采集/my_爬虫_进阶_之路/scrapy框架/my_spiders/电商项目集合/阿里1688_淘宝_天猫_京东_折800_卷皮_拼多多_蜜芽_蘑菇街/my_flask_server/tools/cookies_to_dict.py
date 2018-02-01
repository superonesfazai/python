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
cookies = 'UM_distinctid=16015e04f6d4ff-037c1f4e36bf3-17386d57-fa000-16015e04f6e555; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; ockeqeudmj=jJgePkU%3D; munb=2242024317; WAPFDFDTGFG=%2B4cMKKP%2B8PI%2Buj7zjGYZ%2FmcrTpFkcttXbzWPw1Gvbiu%2F; _w_app_lg=17; _m_user_unitinfo_=unit|unzbyun; _m_unitapi_v_=1508566261407; ali_apache_id=11.228.45.44.1512376392548.274581.5; uc3=sg2=WqJ5CclAaAIRL%2BjSIx%2FSzyVuMbp8JSBthJSylPIhcsc%3D&nk2=rUtEoY7x%2Bk8Rxyx1ZtN%2FAg%3D%3D&id2=UUplY9Ft9xwldQ%3D%3D&vt3=F8dBzLQKaueubXgKyDU%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; lgc=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; cookie2=218fc7ff98e02b9b3b9d2ef572476d78; t=567b173f0709a9279b1255b8cb39b2fc; _cc_=VFC%2FuZ9ajQ%3D%3D; tg=0; mt=ci=46_1; l=Anl5F-hiGIwSg0yWkdu/9YJLCf5Thm05; cna=ZyWpEl+kTywCAXHXsSxv8Ati; miid=5767446262036433919; v=0; _tb_token_=bd731a300e5e; uc1=cookie14=UoTdeYA%2B9w4Ojw%3D%3D; _m_h5_tk=5e966c55073b38cc5685058c7bc31605_1512454028549; _m_h5_tk_enc=30619b1bab9bf8bd4f6aaf76baf8a08e; isg=AqioD7RqZm2xEkrtJa7Sd03JeZB6eQ2hI1962mLZ9CO-vUgnCuHcaz67xW-y'
pprint(stringToDict(cookies))