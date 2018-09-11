# coding = utf-8

'''
@author = super_fazai
@File    : 短信提醒_test.py
@Time    : 2017/9/22 20:04
@connect : superonesfazai@gmail.com
'''

from twilio.rest import Client

# 下面认证信息的值在你得twilio账户里可以找到
account_sid = ''
auth_token = ''

client = Client(account_sid, auth_token)

message = client.messages.create(
    # to = '+8615661611306',
    to = '+8615010957485',
    from_ = '+16506812561',
    body = '别来无恙哦!'
)