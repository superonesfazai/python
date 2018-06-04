# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import requests

headers = {
    # 'cookie': 't=70c4fb481898a67a66d437321f7b5cdf; cna=nbRZExTgqWsCAXPCa6QA5B86; l=AkFBuFEM2rj4GbU8Mjl3KsFo0YZa/7Vg; thw=cn; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; _cc_=UIHiLt3xSw%3D%3D; tg=0; enc=OFbfiyN19GGi1GicxsjVmrZoFzlt9plbuviK5OuthXYfocqTD%2BL079G%2BIt4OMg6ZrbV4veSg5SQEpzuMUgLe0w%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; miid=763730917900964122; mt=ci%3D-1_1; linezing_session=i72FGC0gr3GTls7K7lswxen2_1527664168714VAPN_1; cookie2=1cf9585e0c6d98c72c64beac41a68107; v=0; _tb_token_=5ee03e566b165; uc1=cookie14=UoTeOZOVOtrsVw%3D%3D; _m_h5_tk=f8666ba7a6533330715e41474f8bf209_1527747490977; _m_h5_tk_enc=4e94e9488ab4af3ec438845664822838; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=C707A346EC1DFACF112FE06EB592281D; isg=BPDwLkNAX_wr-gIlKLACWgiZwbhIvk5nGh1WOOpBvMsepZBPkkmkE0aT-a3FLoxb',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'referer': 'https://s.taobao.com/search?q=a&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180531&ie=utf8',
    'authority': 's.taobao.com',
    'x-requested-with': 'XMLHttpRequest',
}

params = (
    # ('_ksTS', '1527746039367_226'),
    ('callback', 'jsonp227'),
    ('ajax', 'true'),
    ('m', 'customized'),
    ('stats_click', 'search_radio_all:1'),
    ('q', 'a'),
    ('s', '36'),
    ('imgfile', ''),
    # ('initiative_id', 'staobaoz_20180531'),
    ('bcoffset', '-1'),
    ('js', '1'),
    ('ie', 'utf8'),
    # ('rn', 'b2ea8a3d982387813f32e92187392202'),
)

response = requests.get('https://s.taobao.com/api', headers=headers, params=params)
print(response.text)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://s.taobao.com/api?_ksTS=1527746039367_226&callback=jsonp227&ajax=true&m=customized&stats_click=search_radio_all:1&q=a&s=36&imgfile=&initiative_id=staobaoz_20180531&bcoffset=-1&js=1&ie=utf8&rn=b2ea8a3d982387813f32e92187392202', headers=headers)

