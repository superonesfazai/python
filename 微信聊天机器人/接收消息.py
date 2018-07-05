# coding = utf-8

'''
@author = super_fazai
@File    : 接收消息.py
@Time    : 2017/9/9 13:51
@connect : superonesfazai@gmail.com
'''

import itchat
from pprint import pprint

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    '''
    回复发送给自己的信息
    :param msg:
    :return:
    '''
    from_user_name = msg['FromUserName']
    tmp_sender = itchat.search_friends(userName=from_user_name)['NickName']
    # pprint(tmp_sender)

    # 显示发送给自己的信息
    print('收到来自 ' + tmp_sender + ' 的信息: ' + msg['Text'])

    # 回复发送诶自己的信息
    reply = '谢谢亲[嘴唇]\n我收到您的信息如下:\n' \
            + '-'*30 + '\n' \
            + ' ' + msg['Text']
    return reply

itchat.auto_login(hotReload=True)

itchat.run()
