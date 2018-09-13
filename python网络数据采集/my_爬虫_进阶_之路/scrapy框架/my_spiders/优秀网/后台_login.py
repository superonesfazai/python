# coding:utf-8

'''
@author = super_fazai
@File    : 后台_login.py.py
@connect : superonesfazai@gmail.com
'''

from pprint import pprint
from fzutils.ocr_utils import baidu_ocr_captcha
from fzutils.common_utils import json_2_dict

with open('/Users/afa/baidu_orc.json', 'r') as f:
    bd_info = json_2_dict(f.read())

app_id = str(bd_info['app_id'])
api_key = bd_info['api_key']
secret_key = bd_info['secret_key']

res = baidu_ocr_captcha(
    app_id=app_id,
    api_key=api_key,
    secret_key=secret_key,
    img_path='./images/captcha.png',
    orc_type=2,
)
pprint(res)
