# coding = utf-8

'''
@author = super_fazai
@File    : 用户搜索.py
@Time    : 2017/9/8 22:47
@connect : superonesfazai@gmail.com
'''

import itchat
from pprint import pprint

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    '''
    将消息原封不动的返回
    :param msg:
    :return:
    '''
    print(msg['Text'])

itchat.auto_login(hotReload=True)

'''
使用search_friends方法可以搜索用户，有四种搜索方式：
    1. 仅获取自己的用户信息
    2. 获取特定UserName的用户信息
    3. 获取备注、微信号、昵称中的任何一项等于name键值的用户
    4. 获取备注、微信号、昵称分别等于相应键值的用户
    其中三、四项可以一同使用
'''

# 获取自己的用户信息, 返回自己的属性字典
my = itchat.search_friends()
print(my)

# 获取特定UserName的用户信息
tmp_user_name = itchat.search_friends(name='LittleCoder机器人')[0]['UserName']
tmp_user_name2 = itchat.search_friends(userName=tmp_user_name)
print(tmp_user_name2)

# 获取任何一项等于name键值的用户
# 'NickName' 昵称, set by that friend, changeable
danny = itchat.search_friends(name='danny')
# danny = itchat.search_friends(remarkName='李大傻👹')  # remarkName 昵称
pprint(danny)

# 获取分别对应相应键值的用户
# 'Alias' ID微信号 = wechatAccount, one time set by that friend， cannot change
tmp = itchat.search_friends(wechatAccount='littlecodersh')
print(tmp)

# 三、四项功能可以一同使用
tmp2 = itchat.search_friends(name='LittleCoder机器人', wechatAccount='littlecodersh')
print(tmp2)

print('查找群组'.center(100, '-'))
# 查找群组
group = itchat.search_chatrooms(name='阿发自嗨群')
pprint(group)

itchat.run()