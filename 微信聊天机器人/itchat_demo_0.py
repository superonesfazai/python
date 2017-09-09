# coding = utf-8

'''
@author = super_fazai
@File    : demo_0.py
@Time    : 2017/9/8 20:42
@connect : superonesfazai@gmail.com
'''

import itchat

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    '''
    将消息原封不动的返回
    :param msg:
    :return:
    '''
    return msg['Text']

itchat.auto_login(hotReload=True)   # 避免每次都扫码登录
# itchat.auto_login(enableCmdQR=2)    # 命令行显示QR图片

# itchat.send('Msg', 'to_user_name')
# itchat.send('测试消息发送', 'filehelper')

danny_user_name = itchat.search_friends(name='LittleCoder机器人')[0]['UserName']
print(danny_user_name)

for i in range(50):
    print(i)
    itchat.send('-', toUserName=danny_user_name)

itchat.run()    # 开启监听

'''
微信有各种类型的数据，例如图片、语音、名片、分享等，也对应不同的注册参数：
    图片对应itchat.content.PICTURE
    语音对应itchat.content.RECORDING
    名片对应itchat.content.CARD
'''