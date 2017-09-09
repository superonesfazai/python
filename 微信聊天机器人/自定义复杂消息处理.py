# coding = utf-8

'''
@author = super_fazai
@File    : 自定义复杂消息处理.py
@Time    : 2017/9/9 14:17
@connect : superonesfazai@gmail.com
'''

import itchat
from itchat.content import *

# 如果收到[TEXT, MAP, CARD, NOTE, SHARING]类的消息, 会自动回复
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])  # 文字, 位置, 名片, 通知, 分享
def text_reply(msg):
    reply = '{}: {}'.format(msg['Type'], msg['Text'])
    itchat.send(reply, msg['FromUserName'])

# 如果收到[PICTURE, RECORDING, ATTACHMENT, VIDEO]类的信息，会自动存档
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])   # 图片, 语音, 文件, 视频
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' \
           % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

# 如果收到新朋友的请求，会自动通过验证添加加好友，并主动打个招呼：幸会幸会！Nice to meet you!
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg(u'幸会幸会！Nice to meet you!', msg['RecommendInfo']['UserName'])

# 在群里，如果收到@自己的文字信息，会自动回复：
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])

itchat.auto_login(hotReload=True)

itchat.run()

# itchat.logout()     # 安全退出