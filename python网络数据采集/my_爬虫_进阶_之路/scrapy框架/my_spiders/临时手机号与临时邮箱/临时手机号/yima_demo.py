# coding:utf-8

'''
@author = super_fazai
@File    : yima_demo.py
@connect : superonesfazai@gmail.com
'''

from fzutils.common_utils import json_2_dict
from fzutils.register_utils import YiMaSmser

# @外部调用
# 测试批量注册微博账号: https://passport.sina.cn/signup/signup?entry=wapsso&r=https%3A%2F%2Fsina.cn%2Findex%2Fsettings%3Fvt%3D4%26pos%3D108
with open('/Users/afa/myFiles/pwd/yima_pwd.json', 'r') as f:
    yima_info = json_2_dict(f.read())
_ = YiMaSmser(username=yima_info['username'], pwd=yima_info['pwd'])

# project_id = 35
# project_id = 715
# 趣头条
project_id = 2674
while True:
    phone_num = _._get_phone_num(project_id=project_id)
    print(phone_num)
    a = input('是否可用: ')
    if a == 'y':
        break

print('\n未注册的: {}'.format(phone_num))
sms_res = _._get_sms(phone_num=phone_num, project_id=project_id)
print(sms_res)
res = _._get_account_info()
from pprint import pprint
pprint(res)