# coding:utf-8

'''
@author = super_fazai
@File    : wy_kaola_parse.py
@Time    : 2018/7/27 14:18
@connect : superonesfazai@gmail.com
'''

"""
网易考拉m站抓取
"""

import requests
from pprint import pprint
from fzutils.spider.fz_requests import MyRequests
from fzutils.spider.fz_phantomjs import MyPhantomjs
from fzutils.common_utils import json_2_dict
from fzutils.internet_utils import get_random_phone_ua

# 下面是sku_info相关
headers = {
    # 'cookie': 'davisit=2; usertrack=O2+g2Ftatitk7YwIAwY2Ag==; _ntes_nnid=7732365205c88dc47486ad1208406e7e,1532671534874; _ga=GA1.2.960357080.1532671535; _gid=GA1.2.1543960295.1532671535; JSESSIONID-WKL-8IO=JpPe0U2ISOSX%2B7b86uwx%2FDCCROKOxwv%2B9vh7Yj%2BBTVVOOIQXHVnSAe19xxMrURx2OK5Q6PV1E%2FSR5UOnm%5C0U2i1RDD3ur5uh%2F7lHemHDcbf90BrkXSqTqZySf%2F%5CWgGSu81cjbESgntQrE%2FYJU89hyhg%5CtPZ6jYgVrxw3yil6BxlEonas%3A1532757935029; _klhtxd_=31; kaola_user_key=47cca4d0-57c9-41ca-ae67-2172c4a81500; KAOLA_NEW_USER_COOKIE=yes; __da_ntes_utma=2525167.1705273738.1532671535.1532671535.1532671535.1; davisit=1; __da_ntes_utmb=2525167.1.10.1532671535; __da_ntes_utmz=2525167.1532671535.1.1.utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none); __da_ntes_utmfc=utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none); _jzqa=1.658432386831847000.1532671536.1532671536.1532671536.1; _jzqc=1; _jzqx=1.1532671536.1532671536.1.jzqsr=google%2Ecom|jzqct=/.-; _jzqckmp=1; WM_TID=BuJzWuW25WT9h9YnJbNPwKuHb0%2FJdiEw; __kaola_usertrack=20180727140634933960; _da_ntes_uid=20180727140634933960; NTES_KAOLA_ADDRESS_CONTROL=330000|330100|330102|1; _jzqb=1.8.10.1532671536.1; NTES_KAOLA_RV=1472242_1532671698324_0|27979_1532671614705_0; _gat=1',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': '*/*',
    # 'referer': 'https://m-goods.kaola.com/product/27979.html?ri=navigation&from=page1&zn=result&zp=page1-5&position=5&istext=0&srId=7891cc6632688f65bdcb4f04e150950c&isMarketPriceShow=true&hcAntiCheatSwitch=0&anstipamActiCheatSwitch=1&anstipamActiCheatToken=de3223456456fa2e3324354u4567lt&anstipamActiCheatValidate=anstipam_acti_default_validate',
    'authority': 'm-goods.kaola.com',
    'x-requested-with': 'XMLHttpRequest',
}

params = (
    ('t', '1532672522828'),
    ('goodsId', '27979'),
    ('provinceCode', '330000'),
    ('cityCode', '330100'),
    ('districtCode', '330102'),
)

url = 'https://m-goods.kaola.com/product/getWapGoodsDetailDynamic.json'
# body = MyRequests.get_url_body(url=url, headers=headers, params=params)
# pprint(json_2_dict(body))

# phone_body(requests设置代理一直302, 于是phantomjs)
headers = {
    'authority': 'goods.kaola.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': get_random_phone_ua(),
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'referer': 'https://www.kaola.com/category/2620/2622.html?zn=top&zp=category-1-1-1-1',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': 'davisit=19; usertrack=O2+g2Ftatitk7YwIAwY2Ag==; _ntes_nnid=7732365205c88dc47486ad1208406e7e,1532671534874; _ga=GA1.2.960357080.1532671535; _gid=GA1.2.1543960295.1532671535; JSESSIONID-WKL-8IO=JpPe0U2ISOSX%2B7b86uwx%2FDCCROKOxwv%2B9vh7Yj%2BBTVVOOIQXHVnSAe19xxMrURx2OK5Q6PV1E%2FSR5UOnm%5C0U2i1RDD3ur5uh%2F7lHemHDcbf90BrkXSqTqZySf%2F%5CWgGSu81cjbESgntQrE%2FYJU89hyhg%5CtPZ6jYgVrxw3yil6BxlEonas%3A1532757935029; _klhtxd_=31; kaola_user_key=47cca4d0-57c9-41ca-ae67-2172c4a81500; KAOLA_NEW_USER_COOKIE=yes; __da_ntes_utma=2525167.1705273738.1532671535.1532671535.1532671535.1; davisit=1; __da_ntes_utmb=2525167.1.10.1532671535; __da_ntes_utmz=2525167.1532671535.1.1.utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none); __da_ntes_utmfc=utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none); _jzqa=1.658432386831847000.1532671536.1532671536.1532671536.1; _jzqc=1; _jzqx=1.1532671536.1532671536.1.jzqsr=google%2Ecom|jzqct=/.-; _jzqckmp=1; WM_TID=BuJzWuW25WT9h9YnJbNPwKuHb0%2FJdiEw; __kaola_usertrack=20180727140634933960; _da_ntes_uid=20180727140634933960; NTES_KAOLA_ADDRESS_CONTROL=330000|330100|330102|1; _qzjc=1; _ga=GA1.3.960357080.1532671535; _gid=GA1.3.1543960295.1532671535; _qzja=1.171255260.1532671601817.1532671601817.1532671601817.1532671615270.1532671697604..0.0.3.1; _qzjb=1.1532671601817.3.0.0.0; _qzjto=3.1.0; _jzqb=1.8.10.1532671536.1; NTES_KAOLA_RV=1472242_1532671698324_0|27979_1532671614705_0',
}

params = (
    ('ri', 'navigation'),
    ('from', 'page1'),
    ('zn', 'result'),
    ('zp', 'page1-5'),
    ('position', '5'),
    ('istext', '0'),
    # ('srId', '7891cc6632688f65bdcb4f04e150950c'),
    ('isMarketPriceShow', 'true'),
    ('hcAntiCheatSwitch', '0'),
    # ('anstipamActiCheatSwitch', '1'),
    # ('anstipamActiCheatToken', 'de3223456456fa2e3324354u4567lt'),
    # ('anstipamActiCheatValidate', 'anstipam_acti_default_validate'),
)

phone_url = 'https://goods.kaola.com/product/27979.html'
# body = MyRequests.get_url_body(url=phone_url, headers=headers, params=params)
# print(body)

_ = MyPhantomjs()
body = _.use_phantomjs_to_get_url_body(url=phone_url)
print(body)
del _

# response = requests.get(url=phone_url, headers=headers, params=params)
# print(response.text)
