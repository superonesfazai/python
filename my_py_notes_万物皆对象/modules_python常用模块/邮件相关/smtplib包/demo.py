# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2018/5/18 15:11
@connect : superonesfazai@gmail.com
'''

import smtplib
from email.mime.text import MIMEText
import json

email_passwd_json_path = '/Users/afa/email_passwd.json'

def get_email_passwd():
    try:
        with open(email_passwd_json_path, 'r') as f:
            _tmp = json.loads(f.readline())
    except FileNotFoundError:
        print('严重错误, 数据库初始配置json文件未找到!请检查!')
        return ''
    except Exception as e:
        print('错误如下: ', e)
        return ''

    else:
        return _tmp['passwd']

def send_email(HOST='smtp.qq.com', FROM='2939161681@qq.com', TO='superonesfazai@gmail.com', subject='邮件主题', text='邮件正文', PASSWD=''):
    '''
    发送email(使用前提: qq邮箱设置开启smtp, 并获得授权码)
    :param HOST:
    :param FROM:
    :param TO:
    :param subject:
    :param text:
    :param PASSWD: 邮箱密码 or 邮箱smtp授权码
    :return:
    '''
    msg = MIMEText(text)    # 这个里面还可以是html eg: msg = MIMEText(r'''<html></html>''', 'html', 'utf-8')
    msg["Subject"] = subject
    msg["From"] = FROM
    msg["To"] = TO

    try:
        server = smtplib.SMTP_SSL(HOST, 465)     # 创建一个smtp主机
        if PASSWD == '':
            # print(PASSWD)
            PASSWD = get_email_passwd()

        server.login(user=FROM, password=PASSWD)
        server.sendmail(FROM, [TO], msg.as_string())
        server.quit()               # 断开smtp连接
        print('邮件发送成功!')
    except Exception as e:
        print(e)
        print('邮件发送失败!')

send_email()