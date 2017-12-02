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
cookies = 'TY_SESSION_ID=252160ce-3248-4fc7-a3a3-6afcd2c65016; session_id=327130943.1510496021; firstTime=2017-11-12; UM_distinctid=15fb0942ca921a-07d35b19088781-31657c00-fa000-15fb0942caafc; qd_user=51374722.1510496149911; gr_user_id=382743ae-6446-401a-8fad-27ca315f94b9; user_role=1; student=0; utm_csr_first=direct; wris_session_id=162592065.1510496683; user_type=0; downloadGuide_config=%257B%25220direct%2522%253A%257B%2522open%2522%253A7%257D%252C%25221015direct%2522%253A%257B%2522open%2522%253A1%257D%257D; has_webp=1; utm_ccn=notset_c0; utm_cmd=; utm_ctr=; utm_cct=; utm_etr=tao.home; str=q3f8; new_old_user=1; ju_rv=1000TD; frequency=1%2C1%2C1%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0; lastTime=2017-11-15; unix_time=1510725125; ju_version=0; screenversion=1%2C0; bullet_token=VER5SXhHYVY2NExDRUg3VFVDcy80KzRvRVpmblg3Y0NrQ1BPeHV6WHFJbS9EYXAyUEc4T053PT0tWnoyWTA; __utma=148564220.1187264585.1510496022.1510724850.1510731676.14; __utmc=148564220; __utmz=148564220.1510731676.14.9.utmcsr=brand.zhe800.com|utmccn=(referral)|utmcmd=referral|utmcct=/huaei11; jk=1459991510734941129TfActXWw; user_id=; source=; platform=; version=; channelId=; deviceId=; userId=; cType=; cId=; dealId=; visit=130; utm_csr=direct'
pprint(stringToDict(cookies))