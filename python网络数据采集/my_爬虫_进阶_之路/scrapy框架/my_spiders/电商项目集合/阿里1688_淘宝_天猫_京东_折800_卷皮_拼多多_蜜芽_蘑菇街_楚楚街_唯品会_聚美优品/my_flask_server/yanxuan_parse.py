# coding:utf-8

'''
@author = super_fazai
@File    : yanxuan_parse.py
@Time    : 2018/8/6 09:40
@connect : superonesfazai@gmail.com
'''

import requests

cookies = {
    '_ntes_nuid': 'b9e56f8d2caea9349ceebc00eb1318fc',
    '__f_': '1533265025165',
    '_ntes_nnid': '1db094c118e9cd0c25d33de09f7b391d,1533265025337',
    'yx_from': 'web_search_google',
    'yx_delete_cookie_flag': 'true',
    'yx_aui': 'e0c1b456-39ef-4ff8-824c-d5526c719f4c',
    'mail_psc_fingerprint': '26a7cc93b2b579f7a8a1851a10404970',
    'yx_page_key_list': 'http%3A//you.163.com/%2Chttp%3A//you.163.com/item/list%3FcategoryId%3D1005000%26subCategoryId%3D1036000',
    'yx_new_user_modal_show': '1',
    'yx_stat_seesionId': 'e0c1b456-39ef-4ff8-824c-d5526c719f4c1533519630302',
    'yx_stat_lastSendTime': '1533519670398',
}

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = (
    ('id', '1130056'),
)

url = 'http://m.you.163.com/item/detail'
response = requests.get(url=url, headers=headers, params=params, cookies=cookies)
print(response.text)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('http://m.you.163.com/item/detail?id=1130056', headers=headers, cookies=cookies)
