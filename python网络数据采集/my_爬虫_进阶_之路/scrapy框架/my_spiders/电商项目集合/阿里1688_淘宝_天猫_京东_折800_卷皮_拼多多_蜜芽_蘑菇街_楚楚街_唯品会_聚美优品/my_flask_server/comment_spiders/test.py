# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2018/4/9 17:04
@connect : superonesfazai@gmail.com
'''
import sys
sys.path.append('..')
import requests

from my_requests import MyRequests
from my_phantomjs import MyPhantomjs

headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    # 'referer': 'https://detail.1688.com/offer/558138661205.html',
    # 'cookie': 't=5de7bdbe0c944c70edf42507df48b7d4; cna=nGIlE3QL1ksCAX145epTBk9n; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; lgc=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; tg=0; enc=XbQN9%2FZ5BOjIMJ3%2BNpNGywfaXkDB2IiEdebYnFvLS2XEPMDl4crrCuln1oh3edcjZ4wsm9o%2FHZLwUPUfPALCKQ%3D%3D; uc3=nk2=rUtEoY7x%2Bk8Rxyx1ZtN%2FAg%3D%3D&id2=UUplY9Ft9xwldQ%3D%3D&vt3=F8dBz4WxXQovmTd8Kcs%3D&lg2=UIHiLt3xD8xYTw%3D%3D; _cc_=URm48syIZQ%3D%3D; UM_distinctid=1623368af544cc-0c911cd96f128e-33627805-fa000-1623368af56536; cookie2=11e6242be5a55e1354af072798df1d35; _tb_token_=5bcb9ee73eb58; v=0; isg=BAQE82gLAj19brakTXGnZSjl1YQ2tSj7Xb6Kwx6lkE_OSaQTRi34FzqgjeeR0WDf',
}

params = (
    ('_input_charset', 'GBK'),
    ('offerId', '558138661205'),
    ('page', '1'),
    ('pageSize', '15'),
    ('starLevel', '7'),
    ('orderBy', 'date'),
    # ('semanticId', ''),
    ('showStat', '0'),
    ('content', '1'),
    # ('t', '1523270824794'),
    # ('memberId', 'b2b-2456626674'),
    ('memberId', 'zhangchenghao2009'),
    # ('callback', 'jQuery17205412475448980596_1523270772503'),
)

# response = requests.get('https://rate.1688.com/remark/offerDetail/rates.json', headers=headers, params=params)
# print(response.content.decode('gbk'))

m = MyPhantomjs()
body = m.use_phantomjs_to_get_url_body(url='https://rate.1688.com/remark/offerDetail/rates.json?_input_charset=GBK&offerId=558138661205&page=1&pageSize=15&starLevel=7&orderBy=date&semanticId=&showStat=0&content=1&t=1523270824794&memberId=b2b-2456626674&callback=jQuery17205412475448980596_1523270772503')
print('https://rate.1688.com/remark/offerDetail/rates.json?_input_charset=GBK&offerId=558138661205&page=1&pageSize=15&starLevel=7&orderBy=date&semanticId=&showStat=0&content=1&memberId=b2b-2456626674')
print(body)

del m

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://rate.1688.com/remark/offerDetail/rates.json?_input_charset=GBK&offerId=558138661205&page=1&pageSize=15&starLevel=7&orderBy=date&semanticId=&showStat=0&content=1&t=1523270824794&memberId=b2b-2456626674&callback=jQuery17205412475448980596_1523270772503', headers=headers)
