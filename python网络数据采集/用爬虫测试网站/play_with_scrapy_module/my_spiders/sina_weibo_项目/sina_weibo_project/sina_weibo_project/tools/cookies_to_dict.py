# coding:utf-8

'''
@author = super_fazai
@File    : cookies_to_dict.py
@Time    : 2017/9/24 13:55
@connect : superonesfazai@gmail.com
'''

from pprint import pprint

class transCookie(object):
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')  # 记得去除空格
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict


# cookie = 'SUV=1505446925567125; SMYUV=1505446925568464; UM_distinctid=15e83a1210450f-0767352fad6394-31637e01-fa000-15e83a12105261; ABTEST=0|1506166032|v1; IPLOC=CN1100; SUID=F28867D3232C940A0000000059C64510; SUID=0270820E1F13940A0000000059C64510; weixinIndexVisited=1; SNUID=82F916A3717529A8EF7CE70471D86921; JSESSIONID=aaauZkEn6Jewl6APb-y6v; sct=13'
cookie = 'SINAGLOBAL=1920862274319.4636.1502628639473; httpsupgrade_ab=SSL; wvr=6; TC-Ugrow-G0=968b70b7bcdc28ac97c8130dd353b55e; login_sid_t=6c2521139641765552eaeffdc3bc61bb; cross_origin_proto=SSL; TC-V5-G0=458f595f33516d1bf8aecf60d4acf0bf; _s_tentry=login.sina.com.cn; UOR=developer.51cto.com,widget.weibo.com,www.google.com.hk; Apache=5561465425422.705.1506498709692; ULV=1506498709703:7:4:1:5561465425422.705.1506498709692:1506162530082; SSOLoginState=1506498732; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcHYuqSfdfkuLvgn1Aleex5zsmmnegsTlkWruzgTjSBrPw.; SUB=_2A250zyj_DeRhGeNM41sX8ybLzjmIHXVXvR03rDV8PUNbmtBeLWfskW9ZsO0IUPFMAeSGgnp47TqH60IC6g..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFLov-n86vP3ShBTANACnLe5JpX5K2hUgL.Fo-E1h.ce0nNSK-2dJLoI7_0UPWLMLvJqPDyIBtt; SUHB=0RyqLwWNEb6XCS; ALF=1538034730; un=15661611306; wb_cusLike_5289638755=N; TC-Page-G0=4c4b51307dd4a2e262171871fe64f295'
trans = transCookie(cookie)
pprint(trans.stringToDict())