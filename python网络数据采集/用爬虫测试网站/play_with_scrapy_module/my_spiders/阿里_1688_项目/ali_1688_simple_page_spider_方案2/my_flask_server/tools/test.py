# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import re
import datetime

a = [1.6, 23, 1.8, 34]

price = [a[index] for index in range(0, len(a)) if index % 2 == 0 or index == 0]
rest = [a[index] for index in range(0, len(a)) if index % 2 != 0 and index != 0]
print(price)
print(rest)

print('-' * 100)

b = ['\n                                        ', '\n                                    ', '\n                                        ', '\n                                    ']
c = []
for item in b:
    tmp = re.compile(r'\n').sub('', item)
    tmp = re.compile(r' ').sub('', tmp)

    if tmp == '':
        pass
    else:
        c.append(tmp)
print(b)
print(c)

print('-' * 100)

d = 'https://cbu01.alicdn.com/img/ibank/2017/655/128/4704821556_608602289.60x60.jpg'

d = re.compile(r'\.60x60\.').sub('.400x400.', d)
print(d)

print('-' * 100)

goodLinks = {
    'goodLinks': ['aa', 'bbb'],
}

def get_item_from_goodsLinks(goodLinks):
    for item in goodLinks.get('goodLinks'):
        tmp = yield item

        # return tmp

a = get_item_from_goodsLinks(goodLinks)

while True:
    try:
         print(a.__next__())
    except StopIteration as e:
        # print(e, 'this is StopIteration')
        # print('')
        break

print()
print('*' * 100)

item_list = [
    'https://detail.1688.com/offer/548722137629.html?spm=a262n.9599402.j32cvor0.4.gw6bl7',
    'https://detail.1688.com/offer/540344060909.html?spm=a260k.635.201611281602.10.JXEQXP',
    'https://detail.1688.com/offer/43592024755.html?spm=0.0.0.0.JyGZCI&tracelog=samplelist0801_offer_detail#activity-yangpin-scroll',
    'https://detail.1688.com/offer/559526148757.html?spm=b26110380.sw1688.mof001.28.sBWF6s',
]
for item in item_list:
    tmp_item = re.compile(r'(.*?)&.*?').findall(item)  # 过滤筛选出唯一的阿里1688商品链接
    if tmp_item == []:
        wait_to_deal_with_url = item
    else:
        wait_to_deal_with_url = tmp_item[0]
    print(wait_to_deal_with_url)

print('8' * 100)
import base64
# username = 'db56245c1e4f2edce5e131567f2e85f83759af005671be4ae612b1c2bffc762c'

username = '15661611306'

def encrypt(key, s):
    '''
    加密算法
    :param key:
    :param s:
    :return:
    '''
    b = bytearray(str(s).encode("gbk"))
    n = len(b) # 求出 b 的字节数
    c = bytearray(n*2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key # b1 = b2^ key
        c1 = b2 % 16
        c2 = b2 // 16 # b2 = c2*16 + c1
        c1 = c1 + 65
        c2 = c2 + 65 # c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码
        c[j] = c1
        c[j+1] = c2
        j = j+2
    return c.decode("gbk")
def decrypt(key, s):
    '''
    解密算法
    :param key:
    :param s:
    :return:
    '''
    c = bytearray(str(s).encode("gbk"))
    n = len(c) # 计算 b 的字节数
    if n % 2 != 0 :
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j+1]
        j = j+2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2*16 + c1
        b1 = b2^ key
        b[i]= b1
    try:
        return b.decode("gbk")
    except:
        return "failed"
key = 15
s1 = encrypt(key, '15661611306')
s2 = decrypt(key, s1)
print(s1)
print(s2)

print('9' * 100)

class a():
    def __init__(self):
        self.b = 1
        self.c = 2

d = []

ee = a()
rr = a()

d.append(ee)
d.append(rr)

print(d[0].b)

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(time)

erf = ['3.2', '32.4', '5.6']

d = ';'.join(erf)
print(d)

goodsLink = 'https://detail.1688.com/offer/43592024755.html?spm=0.0.0.0.JyGZCI&tracelog=samplelist0801_offer_detail#activity-yangpin-scroll'
tmp_item = re.compile(r'(.*?)\?.*?').findall(goodsLink)  # 过滤筛选出唯一的阿里1688商品链接
print(tmp_item)
