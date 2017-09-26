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
cookie = 'SINAGLOBAL=1920862274319.4636.1502628639473; httpsupgrade_ab=SSL; _s_tentry=cuiqingcai.com; Apache=7249798919057.913.1506162529527; ULV=1506162530082:6:3:3:7249798919057.913.1506162529527:1505873317470; login_sid_t=2a41e3628a877dcd52fb5a9091b93e77; TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; TC-V5-G0=f88ad6a0154aa03e3d2a393c93b76575; YF-V5-G0=02157a7d11e4c84ad719358d1520e5d4; YF-Ugrow-G0=57484c7c1ded49566c905773d5d00f82; YF-Page-G0=f27a36a453e657c2f4af998bd4de9419; cross_origin_proto=SSL; WBStorage=9fa115468b6c43a6|undefined; UOR=developer.51cto.com,widget.weibo.com,login.sina.com.cn; SSOLoginState=1506412304; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcHHeIBBuFjx2PMZUS-wHdbD5YPOfD8LUX8NcsbcXPp3rM.; SUB=_2A250zndBDeRhGeNM41sX8ybLzjmIHXVXuu-JrDV8PUNbmtBeLWXnkW8U8mBbCeUC6dQVP77W1IQLHBNsbg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFLov-n86vP3ShBTANACnLe5JpX5K2hUgL.Fo-E1h.ce0nNSK-2dJLoI7_0UPWLMLvJqPDyIBtt; SUHB=08J7I6GiMwQzNU; ALF=1537948304; un=15661611306; wvr=6'
trans = transCookie(cookie)
pprint(trans.stringToDict())