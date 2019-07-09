# coding:utf-8

'''
@author = super_fazai
@File    : huobi_spider.py
@connect : superonesfazai@gmail.com
'''

import zlib
from websocket import create_connection

def crawl_huobi_demo():
    """ 抓取火币的数据 """
    url = 'wss://www.huobi.pro/-/s/pro/ws'
    ws = create_connection(
        url=url,
        timeout=10)
    ws.send('{"sub":"market.btcusdt.trade.detail"}')

    for i in range(5):
        content_compress = ws.recv()
        content = zlib.decompress(content_compress, 16+zlib.MAX_WBITS)
        print(content)

    ws.close()

def crawl_okcoin_demo():
    """ 抓取okcoin的数据 """
    url = 'wss://real.okcoin.com:10440/websocket'
    ws = create_connection(
        url=url,
        timeout=10,)
    ws.send("""{event:'addChannel',parameters:{"base":"btc","binary":"1","product":"spot","quote":"usd","type":"depth"}}""")

    for i in range(5):
        content_compress = ws.recv()
        content = zlib.decompress(content_compress, -zlib.MAX_WBITS)
        print(content)

    ws.close()

if __name__ == '__main__':
    crawl_huobi_demo()
    crawl_okcoin_demo()