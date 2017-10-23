# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import re
import datetime
from pprint import pprint
import json
import gc
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

goodsLink = 'https://detail.1688.com/offer/43592024755.html'
tmp_item = re.compile(r'.*?/offer/(.*?).html').findall(goodsLink)  # 过滤筛选出唯一的阿里1688商品链接
print(tmp_item)

item = 'https://detail.1688.com/offer/559526148757.html?spm=b26110380.sw1688.mof001.28.sBWF6s'
tmp_goods_id = re.compile(r'.*?/offer/(.*?).html.*?').findall(item)[0]
print(tmp_goods_id)

a = ['a', 'b', 'c']
b = ['1', '2', '3']
c = ['100', '200', '300']
tmp = list(zip(a, b, c))
print(tmp)

a = ['a']
b = [1, 2]
tmp = list(zip(a, b))
print(tmp)

ss = {"size_info": ["L", "XL", "2XL"], "detail_price": ["119.00", "119.00", "119.00"], "rest_number": ["2000", "2000", "2000"]}
size_info = ss['size_info']
detail_price = ss['detail_price']
rest_number = ss['rest_number']
ddd = list(zip(size_info, detail_price, rest_number))
print(ddd)

print('7' * 100)
eee = {'goods_id': '559526148757', 'spider_url': 'https://detail.1688.com/offer/559526148757.html', 'username': '15661611306', 'deal_with_time': '2017-10-20 15:47:21', 'company_name': '深圳市福田区水月镜花服装批发商行', 'title': '5663实拍2017羽绒服女网红店主风面包服短款休闲夹克棉服衣女外套', 'link_name': '徐惠湘', 'link_name_personal_url': 'https://me.1688.com/*xC-i2FIyvmIyvmHLvFvT.html', 'price_info': [{'price': '119.00', 'trade_number': '3-9'}, {'price': '101.15', 'trade_number': '10-99'}, {'price': '89.25', 'trade_number': '≥100'}], 'goods_name': [{'goods_name': '颜色'}, {'goods_name': '尺码'}], 'goods_info': [{'goods_value': '白色|L|XL|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '白色|L|XL|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '白色|L|XL|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '卡其色|L|XL|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/554/084/4707480455_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '卡其色|L|XL|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/554/084/4707480455_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '卡其色|L|XL|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/554/084/4707480455_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '黑色|L|XL|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/539/381/4705183935_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '黑色|L|XL|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/539/381/4705183935_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '黑色|L|XL|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/539/381/4705183935_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}], 'center_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.400x400.jpg', 'all_img_url_info': [{'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/655/128/4704821556_608602289.400x400.jpg'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/964/038/4704830469_608602289.400x400.jpg'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/834/084/4707480438_608602289.400x400.jpg'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/125/474/4707474521_608602289.400x400.jpg'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/568/681/4705186865_608602289.400x400.jpg'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/554/084/4707480455_608602289.400x400.jpg_.webp'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/539/381/4705183935_608602289.400x400.jpg_.webp'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.400x400.jpg_.webp'}], 'p_info': [{'p_name': '货源类别', 'p_value': '现货'}, {'p_name': '产地', 'p_value': '其他'}, {'p_name': '品牌', 'p_value': '其他'}, {'p_name': '货号', 'p_value': '5663#'}, {'p_name': '填充物', 'p_value': '其他'}, {'p_name': '衣长', 'p_value': '短款(40cm＜衣长≤50cm)'}, {'p_name': '风格', 'p_value': 'OL通勤/正装'}, {'p_name': '袖长', 'p_value': '长袖'}, {'p_name': '主图来源', 'p_value': '其他来源'}, {'p_name': '颜色', 'p_value': '白色,卡其色,黑色'}, {'p_name': '尺码', 'p_value': 'L,XL,2XL'}], 'site_id': 2, 'is_delete': 0}
# rrr = {'goods_id': '540344060909', 'spider_url': 'https://detail.1688.com/offer/540344060909.html', 'username': '15661611306', 'deal_with_time': '2017-10-20 16:26:04', 'company_name': '深圳市宝安区西乡豪弈洁卫浴工厂', 'title': '2017年新款豪华家装3D雪花钻石马桶节水静音冲水坐便器 家用马桶', 'link_name': '梁凤华', 'link_name_personal_url': 'https://me.1688.com/*xC-i2FI4MC80Mmv4MFMCxDPlZNTT.html', 'price_info': [{'price': '485.46', 'trade_number': '≥1'}], 'goods_name': [{'goods_name': '规格'}], 'goods_info': [{'goods_value': '高配置+雪花智洁脲醛盖板300', 'color_img_url': '', 'detail_price': '512.43', 'rest_number': '143'}, {'goods_value': '高配置+雪花智洁脲醛盖板400', 'color_img_url': '', 'detail_price': '512.43', 'rest_number': '196'}, {'goods_value': '普通配置+雪花智洁pp盖板300', 'color_img_url': '', 'detail_price': '485.46', 'rest_number': '80'}, {'goods_value': '普通配置+雪花智洁pp盖板400', 'color_img_url': '', 'detail_price': '485.46', 'rest_number': '74'}, {'goods_value': '高配置+雪花智洁脲醛盖板350', 'color_img_url': '', 'detail_price': '537.66', 'rest_number': '77'}, {'goods_value': '普通配置+雪花智洁pp盖板350', 'color_img_url': '', 'detail_price': '502.86', 'rest_number': '80'}, {'goods_value': '高配置+雪花智洁脲醛盖板250', 'color_img_url': '', 'detail_price': '537.66', 'rest_number': '79'}, {'goods_value': '普通配置+雪花智洁pp盖板250', 'color_img_url': '', 'detail_price': '502.86', 'rest_number': '80'}, {'goods_value': '普通配置+墙排', 'color_img_url': '', 'detail_price': '521.13', 'rest_number': '80'}, {'goods_value': '高配置+墙排', 'color_img_url': '', 'detail_price': '555.06', 'rest_number': '78'}], 'center_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/750/051/4118150057_188623679.400x400.jpg', 'all_img_url_info': [{'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/750/051/4118150057_188623679.400x400.jpg'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/836/460/3790064638_188623679.400x400.jpg'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2016/495/361/3558163594_188623679.400x400.jpg'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2016/511/271/3558172115_188623679.400x400.jpg'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2016/257/420/3557024752_188623679.400x400.jpg'}], 'p_info': [{'p_name': '品牌', 'p_value': '至尊法恩纱'}, {'p_name': '材质', 'p_value': '脲醛树脂'}, {'p_name': '结构形式', 'p_value': '连体式'}, {'p_name': '冲水方式', 'p_value': '超漩式'}, {'p_name': '排水方式', 'p_value': '地排式'}, {'p_name': '冲水按键', 'p_value': '上按两端式'}, {'p_name': '最小坑距', 'p_value': '300'}, {'p_name': '承重范围', 'p_value': '300公斤'}, {'p_name': '冲水量', 'p_value': '3.6L'}, {'p_name': '型号', 'p_value': 'M-8027'}, {'p_name': '产地', 'p_value': '潮州'}, {'p_name': '加工方式', 'p_value': '贴牌'}, {'p_name': '规格', 'p_value': '高配置+雪花智洁脲醛盖板300,高配置+雪花智洁脲醛盖板400,普通配置+雪花智洁pp盖板300,普通配置+雪花智洁pp盖板400,高配置+雪花智洁脲醛盖板350,普通配置+雪花智洁pp盖板350,高配置+雪花智洁脲醛盖板250,普通配置+雪花智洁pp盖板250,普通配置+墙排,高配置+墙排'}], 'site_id': 2, 'is_delete': 0}
# pprint(eee)
# pprint(rrr)

u = '白色'
tt = ['L', 'XL', '2XL']
rr = []
yy = u
for item in tt:
    yy = ''
    yy = u
    yy += '|' + item
    rr.append(yy)

print(rr)

a = [{1:1, 'a': 1}, {2:2}, {3:3}]
for item in a:
    if item == {1:1, 'a':1}:
        a.remove(item)
print(a)

a = [{1:1, 'a': 1}, {2:2}, {3:3}]
b = [{1:1, 'a': 1}, {3:3}]
ret = [i for i in a if i not in b]
print(ret)

a = [0,1,2,3,4,5,6]
print(a[:5])

a = [{'p': 0}, {'p': 1}, {'p': 2}, {'p': 3}, {'p': 4}, {'p': 5}, {'p': 6}]
b = [0, 2, 5]
tmp_delete = []
for item in b:
    for index in range(0, len(a)):
        if item == a[index]['p']:
            tmp_delete.append(a[index])
            # print('--')
print(tmp_delete)
a = [i for i in a if i not in tmp_delete]  # 删除已被插入
print(a)

# list里面的dict的去重方法
a = [{'name':'zhang', 'age':18}, {'name':'zhang', 'age':18}, {'name':'li', 'age':18}]
list=[]
[list.append(x) for x in a if x not in list]
print(list)

a = {'goods_id': '559526148757', 'spider_url': 'https://detail.1688.com/offer/559526148757.html', 'username': '15661611306', 'deal_with_time': '2017-10-22 13:47:07', 'company_name': '深圳市福田区水月镜花服装批发商行', 'title': '5663实拍2017羽绒服女网红店主风面包服短款休闲夹克棉服衣女外套', 'link_name': '徐惠湘', 'link_name_personal_url': 'https://me.1688.com/*xC-i2FIyvmIyvmHLvFvT.html', 'price_info': [{'price': '119.00', 'trade_number': '3-9'}, {'price': '101.15', 'trade_number': '10-99'}, {'price': '89.25', 'trade_number': '≥100'}], 'goods_name': [{'goods_name': '颜色'}, {'goods_name': '尺码'}], 'goods_info': [{'goods_value': '白色|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '白色|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '白色|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '卡其色|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/554/084/4707480455_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '卡其色|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/554/084/4707480455_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '卡其色|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/554/084/4707480455_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '黑色|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/539/381/4705183935_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '黑色|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/539/381/4705183935_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}, {'goods_value': '黑色|2XL', 'color_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/539/381/4705183935_608602289.400x400.jpg', 'detail_price': '119.00', 'rest_number': '2000'}], 'center_img_url': 'https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.400x400.jpg', 'all_img_url_info': [{'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/655/128/4704821556_608602289.400x400.jpg'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/964/038/4704830469_608602289.400x400.jpg'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/834/084/4707480438_608602289.400x400.jpg'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/125/474/4707474521_608602289.400x400.jpg'}, {'img_url': 'https://cbu01.alicdn.com/img/ibank/2017/568/681/4705186865_608602289.400x400.jpg'}], 'p_info': [{'p_name': '货源类别', 'p_value': '现货'}, {'p_name': '产地', 'p_value': '其他'}, {'p_name': '品牌', 'p_value': '其他'}, {'p_name': '货号', 'p_value': '5663#'}, {'p_name': '填充物', 'p_value': '其他'}, {'p_name': '衣长', 'p_value': '短款(40cm＜衣长≤50cm)'}, {'p_name': '风格', 'p_value': 'OL通勤/正装'}, {'p_name': '袖长', 'p_value': '长袖'}, {'p_name': '主图来源', 'p_value': '其他来源'}, {'p_name': '颜色', 'p_value': '白色,卡其色,黑色'}, {'p_name': '尺码', 'p_value': 'L,XL,2XL'}], 'site_id': 2, 'is_delete': 0}
# pprint(a)

goods_info = []
tmp = {}
u = {"reason": "success", "data": {"company_name": "深圳市福田区水月镜花服装批发商行", "title": "5663实拍2017羽绒服女网红店主风面包服短款休闲夹克棉服衣女外套", "link_name": "徐惠湘", "link_name_personal_url": "https://me.1688.com/*xC-i2FIyvmIyvmHLvFvT.html", "price": ["119.00", "101.15", "89.25"], "trade_number": ["3-9", "10-99", "≥100"], "goods_name": ["颜色", "尺码"], "color": ["白色", "卡其色", "黑色"], "color_img_url": ["https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.400x400.jpg", "https://cbu01.alicdn.com/img/ibank/2017/554/084/4707480455_608602289.400x400.jpg", "https://cbu01.alicdn.com/img/ibank/2017/539/381/4705183935_608602289.400x400.jpg"], "other_size_info": [], "size_info": ["L", "XL", "2XL"], "detail_price": ["119.00", "119.00", "119.00"], "rest_number": ["2000", "2000", "2000"], "center_img_url": "https://cbu01.alicdn.com/img/ibank/2017/520/684/4707486025_608602289.400x400.jpg", "all_img_url": ["https://cbu01.alicdn.com/img/ibank/2017/655/128/4704821556_608602289.400x400.jpg", "https://cbu01.alicdn.com/img/ibank/2017/964/038/4704830469_608602289.400x400.jpg", "https://cbu01.alicdn.com/img/ibank/2017/834/084/4707480438_608602289.400x400.jpg", "https://cbu01.alicdn.com/img/ibank/2017/125/474/4707474521_608602289.400x400.jpg", "https://cbu01.alicdn.com/img/ibank/2017/568/681/4705186865_608602289.400x400.jpg"], "p_name": ["货源类别", "产地", "品牌", "货号", "填充物", "衣长", "风格", "袖长", "主图来源", "颜色", "尺码"], "p_value": ["现货", "其他", "其他", "5663#", "其他", "短款(40cm＜衣长≤50cm)", "OL通勤/正装", "长袖", "其他来源", "白色,卡其色,黑色", "L,XL,2XL"], "spider_url": "https://detail.1688.com/offer/559526148757.html", "username": "15661611306", "goods_id": "559526148757"}, "error_code": 0}
data_list = u['data']
# pprint(data_list)
tmp_goods_info = tuple(zip(data_list['size_info'], data_list['detail_price'], data_list['rest_number']))

for index in range(0, len(data_list['color'])):
    tmp_dic = {}
    # tmp_dic['goods_value'] = data_list['color'][index]
    color_img_url = data_list['color_img_url'][index]
    for item in tmp_goods_info:
        # print(item[0])
        tmp_dic['goods_value'] = ''                         # 分析后加这两句话就完美解决了在原值上进行加
        tmp_dic['goods_value'] = data_list['color'][index]
        tmp_dic['goods_value'] += '|' + item[0]
        # tmp_dic['goods_value'] = data_list['color'][index] + '|' + item[0]
        tmp_dic['color_img_url'] = color_img_url
        tmp_dic['detail_price'] = item[1]
        tmp_dic['rest_number'] = item[2]
        goods_info.append(tmp_dic)
        tmp_dic = {}
tmp['goods_info'] = goods_info
# pprint(tmp['goods_info'])

tmp = {}
tmp['title'] = '待下架款纯手工定制 魅惑大红色性感V领重工钉珠礼服裙61371'
if re.compile(r'.*?下架.*?').findall(tmp['title']) != []:  # 第一步先通过名字里有下架的来设置为已经删除
    if re.compile(r'.*?待下架.*?').findall(tmp['title']) != [] or re.compile(r'.*?即将下架.*?').findall(tmp['title']) != []:
        tmp['is_delete'] = 0
    else:
        tmp['is_delete'] = 1
print(tmp['is_delete'])

yy = '                    钱夫人家 雪梨定制                                    '
yy = re.compile(' ').sub('', yy)
print(yy)

xx = '功率: 31W(含)-40W(含)'
xx = re.compile(r':.*').sub('', xx)
print(xx)

print('*' * 100)

import requests

# offer_details版
# url = 'https://img.alicdn.com/tfscom/TB1XeNmSFXXXXXcXpXXXXXXXXXX'
# desc版
url = 'https://desc.alicdn.com/i5/551/520/559526148757/TB1GYaEn6oIL1JjSZFy8qvFBpla.desc%7Cvar%5Edesc%3Blang%5Egbk%3Bsign%5E83adeea72eb6ec904113ae971293e39e%3Bt%5E1507299424'
response = requests.get(url)
data_tfs_url_body = response.content.decode('gbk')
data_tfs_url_body = re.compile(r'\n').sub('', data_tfs_url_body)
data_tfs_url_body = re.compile(r'  ').sub('', data_tfs_url_body)
# print(body)
is_offer_details = re.compile(r'offer_details').findall(data_tfs_url_body)
if is_offer_details != []:
    data_tfs_url_body = re.compile(r'.*?{"content":"(.*?)"};').findall(data_tfs_url_body)
    # print(body)
    if data_tfs_url_body != []:
        property_info = data_tfs_url_body[0]
        property_info = re.compile(r'\\').sub('', property_info)
        print(property_info)
    else:
        property_info = ''
else:
    is_desc = re.compile(r'var desc=').findall(data_tfs_url_body)
    if is_desc != []:
        desc = re.compile(r'var desc=\'(.*)\';').findall(data_tfs_url_body)
        if desc != []:
            property_info = desc[0]
            print(property_info)
    else:
        property_info = ''

print('*' * 100)
data2 = ['{', '"', 's', 'h', 'o', 'w', 'O', 'n', '"', ':', '[', '"', 'm', 'o', 'd', '-', 'd', 'e', 't', 'a', 'i', 'l', '-', 'd', 'e', 's', 'c', 'r', 'i', 'p', 't', 'i', 'o', 'n', '"', ']', ',', '"', 't', 'i', 't', 'l', 'e', '"', ':', '"', '详', '细', '信', '息', '"', ',', '"', 't', 'a', 'b', 'C', 'o', 'n', 'f', 'i', 'g', '"', ':', '{', '"', 't', 'r', 'a', 'c', 'e', '"', ':', '"', 't', 'a', 'b', 'd', 'e', 't', 'a', 'i', 'l', '"', ',', '"', 's', 'h', 'o', 'w', 'K', 'e', 'y', '"', ':', '"', 'm', 'o', 'd', '-', 'd', 'e', 't', 'a', 'i', 'l', '-', 'd', 'e', 's', 'c', 'r', 'i', 'p', 't', 'i', 'o', 'n', '"', '}', ' ', ',', '"', 'c', 'a', 't', 'a', 'l', 'o', 'g', '"', ':', '[', '{', '"', 'i', 'd', '"', ':', '"', '0', '"', ',', '"', 't', 'i', 't', 'l', 'e', '"', ':', '"', '"', ',', '"', 'c', 'o', 'n', 't', 'e', 'n', 't', 'U', 'r', 'l', '"', ':', '"', 'h', 't', 't', 'p', 's', ':', '/', '/', 'i', 'm', 'g', '.', 'a', 'l', 'i', 'c', 'd', 'n', '.', 'c', 'o', 'm', '/', 't', 'f', 's', 'c', 'o', 'm', '/', 'T', 'B', '1', 'l', 'v', 'i', 'j', 'i', '6', 'q', 'h', 'S', 'K', 'J', 'j', 'S', 's', 'p', 'n', 'X', 'X', 'c', '7', '9', 'X', 'X', 'a', '"', '}', ']', ' ', '}']
data2 = ''.join(data2)      # str
data2 = json.loads(data2)   # json字符串反序列化dict
print(data2['catalog'][0]['contentUrl'])

