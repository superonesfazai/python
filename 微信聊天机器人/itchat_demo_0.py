# coding = utf-8

'''
@author = super_fazai
@File    : demo_0.py
@Time    : 2017/9/8 20:42
@connect : superonesfazai@gmail.com
'''

import itchat
import time

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    '''
    将消息原封不动的返回
    :param msg:
    :return:
    '''
    return msg['Text']

itchat.auto_login(hotReload=True)   # 避免每次都扫码登录

# itchat.send('Msg', 'to_user_name')
# itchat.send('测试消息发送', 'filehelper')

itchat.run()

'''
微信有各种类型的数据，例如图片、语音、名片、分享等，也对应不同的注册参数：
    图片对应itchat.content.PICTURE
    语音对应itchat.content.RECORDING
    名片对应itchat.content.CARD
'''