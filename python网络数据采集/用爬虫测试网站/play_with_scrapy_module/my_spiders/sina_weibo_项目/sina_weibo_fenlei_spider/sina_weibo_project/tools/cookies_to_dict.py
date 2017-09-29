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
cookie = 'SINAGLOBAL=1920862274319.4636.1502628639473; httpsupgrade_ab=SSL; __utma=15428400.1070391683.1506563351.1506563351.1506563351.1; __utmz=15428400.1506563351.1.1.utmcsr=verified.weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/verify; TC-Ugrow-G0=968b70b7bcdc28ac97c8130dd353b55e; TC-V5-G0=52dad2141fc02c292fc30606953e43ef; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; _s_tentry=login.sina.com.cn; Apache=9131340312967.717.1506609903037; ULV=1506609903208:8:5:2:9131340312967.717.1506609903037:1506498709703; YF-Page-G0=ab26db581320127b3a3450a0429cde69; YF-V5-G0=694581d81c495bd4b6d62b3ba4f9f1c8; login_sid_t=9b45845aa1847e9045ed0dab201cdca2; cross_origin_proto=SSL; UOR=developer.51cto.com,widget.weibo.com,login.sina.com.cn; SSOLoginState=1506674650; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcHEOOhEj6-APWydXz03IBKyK-HBIiQ4RwY7O4Udv_ZZSo.; SUB=_2A250yneKDeRhGeNM41sX8ybLzjmIHXVXvu5CrDV8PUNbmtAKLVfWkW8tBcGBwIOOdOrHd25ayHS5IiZK1g..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFLov-n86vP3ShBTANACnLe5JpX5K2hUgL.Fo-E1h.ce0nNSK-2dJLoI7_0UPWLMLvJqPDyIBtt; SUHB=03oFyrPxCsfWs7; ALF=1538210649; un=15661611306; wvr=6; wb_cusLike_5289638755=N'
trans = transCookie(cookie)
pprint(trans.stringToDict())