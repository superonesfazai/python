# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from fzutils.spider.fz_requests import MyRequests

# img_url 在e里
# var e = this.props.el;
# arguments里面

import requests

cookies = {
    '_ntes_nuid': 'b9e56f8d2caea9349ceebc00eb1318fc',
    '__f_': '1533265025165',
    '_ntes_nnid': '1db094c118e9cd0c25d33de09f7b391d,1533265025337',
    'yx_from': 'web_search_google',
    'yx_aui': 'e0c1b456-39ef-4ff8-824c-d5526c719f4c',
    'mail_psc_fingerprint': '26a7cc93b2b579f7a8a1851a10404970',
    'yx_delete_cookie_flag': 'true',
    'yx_new_user_modal_show': '1',
    'yx_show_new_user_entrance': 'true',
    'yx_page_key_list': 'http%3A//you.163.com/item/detail%3Fid%3D1487016%26_stat_area%3Dmod_6_item_2%26_stat_id%3D1013001%26_stat_referer%3DitemList%2Chttp%3A//you.163.com/item/list%3FcategoryId%3D1013001%26subCategoryId%3D1013002%2Chttp%3A//you.163.com/item/detail%3Fid%3D1130056%26_stat_area%3Dmod_1_item_1%26_stat_id%3D1005000%26_stat_referer%3DitemList',
    'yx_stat_seesionId': 'e0c1b456-39ef-4ff8-824c-d5526c719f4c1533808473418',
    'yx_stat_lastSendTime': '1533808673258',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = (
    ('id', '1130056'),
)

# response = requests.get('http://m.you.163.com/item/detail', headers=headers, params=params, cookies=None)
# print(response.text)

url = 'http://m.you.163.com/item/detail'
body = MyRequests.get_url_body(url=url, params=params, headers=headers)
print(body)