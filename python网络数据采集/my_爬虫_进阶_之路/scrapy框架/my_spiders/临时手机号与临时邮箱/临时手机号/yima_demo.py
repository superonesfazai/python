# coding:utf-8

'''
@author = super_fazai
@File    : yima_demo.py
@connect : superonesfazai@gmail.com
'''

from pprint import pprint
from fzutils.common_utils import json_2_dict
from fzutils.register_utils import YiMaSmser

# @外部调用
# 测试批量注册微博账号: https://passport.sina.cn/signup/signup?entry=wapsso&r=https%3A%2F%2Fsina.cn%2Findex%2Fsettings%3Fvt%3D4%26pos%3D108
with open('/Users/afa/myFiles/pwd/yima_pwd.json', 'r') as f:
    yima_info = json_2_dict(f.read())

ym_cli = YiMaSmser(username=yima_info['username'], pwd=yima_info['pwd'])
# project_id = 35
# project_id = 715
# 趣头条
# project_id = 2674
# 惠头条
# project_id = 8080
# 淘新闻
# project_id = 11065
# Testin 云测
project_id = 17993

def get_phone_num_and_sms_res():
    """
    获取手机号和短信
    :return:
    """
    while True:
        while True:
            phone_num = ym_cli._get_phone_num(project_id=project_id)
            print(phone_num)
            a = input('是否可用: ')
            if a == 'y':
                break

        print('\n未注册的: {}'.format(phone_num))
        sms_res = ym_cli._get_sms(phone_num=phone_num, project_id=project_id)
        print(sms_res)
        res = ym_cli._get_account_info()
        pprint(res)

def get_sms_res_by_phone_num():
    """
    根据手机号获取短信(不可长期使用)
    :return:
    """
    while True:
        phone_num = input('请输入目标phone_num:').replace('\n', '')
        try:
            assert phone_num != '' or len(phone_num) == 11, 'phone_num异常!'
        except AssertionError:
            continue
        sms_res = ym_cli._get_sms(
            phone_num=phone_num,
            project_id=project_id,)
        print(sms_res)

get_phone_num_and_sms_res()
# get_sms_res_by_phone_num()