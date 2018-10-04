# coding:utf-8

'''
@author = super_fazai
@File    : sms_utils.py
@connect : superonesfazai@gmail.com
'''

"""
sms utils
"""

from twilio.rest import Client

__all__ = [
    'sms_2_somebody_by_twilio',         # 通过twilio发送短信
]

def sms_2_somebody_by_twilio(account_sid,
                             auth_token,
                             to='8618698570079',
                             _from='16083058199',
                             body='Hello from Python!') -> bool:
    '''
    通过twilio发送短信
        官网: https://www.twilio.com
        添加手机号: https://www.twilio.com/console/phone-numbers/verified
    :param account_sid: sid
    :param auth_token:
    :return:
    '''
    res = False
    try:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="+{}".format(to),
            from_="+{}".format(_from),
            body=body)

        # print(message.sid)
        if message.sid != '':
            res = True
    except Exception as e:
        print(e)
        pass

    return res
