# coding:utf-8

'''
@author = super_fazai
@File    : boss_login.py
@connect : superonesfazai@gmail.com
'''

"""
成功!
"""

import requests
from pprint import pprint
from scrapy.selector import Selector

from fzutils.internet_utils import get_random_pc_ua
from fzutils.img_utils import save_img_through_url
from fzutils.common_utils import json_2_dict
from fzutils.ocr_utils import baidu_ocr_captcha

def login(phone_num):
    '''
    boss直聘 login
    :param phone_num:
    :param phone_code:
    :return:
    '''
    def orc_captcha(captcha_url):
        '''识别验证码'''
        baidu_orc_info_path = '/Users/afa/baidu_orc.json'
        with open(baidu_orc_info_path, 'r') as f:
            baidu_orc_info = json_2_dict(f.read())

        img_path = './images/captcha.jpg'
        app_id = str(baidu_orc_info['app_id'])
        api_key = baidu_orc_info['api_key']
        secret_key = baidu_orc_info['secret_key']

        save_img_through_url(img_url=captcha_url, save_path=img_path)
        orc_res = baidu_ocr_captcha(
            app_id=app_id,
            api_key=api_key,
            secret_key=secret_key,
            img_path=img_path,
            orc_type=2)
        # print(orc_res)
        captcha = ''
        try:
            captcha = orc_res.get('words_result', [])[0].get('words', '')
        except IndexError:
            pass

        return captcha

    def send_sms(captcha, random_key):
        '''给手机发送验证码'''
        print('模拟给手机发送验证码中...')
        headers = {
            'origin': 'https://login.zhipin.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'referer': 'https://login.zhipin.com/?ka=header-login',
            'authority': 'login.zhipin.com',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = [
            ('pk', 'cpc_user_sign_up'),
            ('regionCode', '+86'),
            ('phone', str(phone_num)),
            ('captcha', captcha),
            ('randomKey', random_key),
            ('phoneCode', ''),
            ('smsType', '1'),
        ]

        response = requests.post('https://login.zhipin.com/registe/sendSms.json', headers=headers, data=data)
        body = response.text
        print(body)
        resmsg = json_2_dict(body)
        res = False
        if resmsg.get('rescode') != 1:
            print('{}'.format(resmsg.get('resmsg', '')))
        else:
            print('发送成功!!')
            res = True

        return res

    headers = {
        'authority': 'login.zhipin.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': get_random_pc_ua(),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    body = requests.get('https://login.zhipin.com/', headers=headers).text
    # print(body)

    random_key = Selector(text=body).css('input.randomkey ::attr("value")').extract_first() or ''
    captcha_url = Selector(text=body).css('img.verifyimg ::attr("src")').extract_first() or ''
    if captcha_url == '':
        return False

    captcha_url = 'https://login.zhipin.com' + captcha_url
    print(random_key)
    # print(captcha_url)
    captcha = orc_captcha(captcha_url=captcha_url)
    print('识别结果: {}'.format(captcha))

    if captcha == '':
        return False

    send_res = send_sms(captcha=captcha, random_key=random_key)
    if not send_res:
        return False

    phone_code = input('亲, 请输入来自boss直聘的短信captcha:')
    headers = {
        'origin': 'https://login.zhipin.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': get_random_pc_ua(),
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': 'https://login.zhipin.com/?ka=header-login',
        'authority': 'login.zhipin.com',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = [
      ('pk', 'cpc_user_sign_up'),
      ('regionCode', '+86'),
      ('phone', str(phone_num)),
      ('captcha', captcha),
      ('randomKey', random_key),
      ('phoneCode', str(phone_code)),
      ('smsType', '1'),
    ]

    response = requests.post('https://login.zhipin.com/login/phone.json', headers=headers, data=data)
    print(response.text)
    pprint(response.cookies)

    print('[+] 登陆boss直聘成功!!')

    return True

phone_num = '18698570079'
index = 1
while True:
    print('attempt {} 次...'.format(index))
    res = login(phone_num)
    if res:
        break
    index += 1