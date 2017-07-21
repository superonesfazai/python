#coding: utf-8

'''
下面的示例中使用的 MIMEText 对象,为底层的 MIME(Multipurpose Internet Mail
Extensions,多用途互联网邮件扩展类型)协议传输创建了一封空邮件,最后通过高层的
SMTP 协议发送出去。
'''

'''
MIMEText 对象 msg 包括收发邮箱地址、邮件正文和主题,Python 通
过它就可以创建一封格式正确的邮件
'''

'''
这个程序每小时检查一次 https://isitchristmas.com/ 网站(根据日期判断当天是不是圣诞
节)。如果页面上的信息不是“NO”(中国用户在网站页面上看到的“NO”在源代码里是<noscript> 不是 </noscript> )
,就会给你发一封邮件,告诉你圣诞节到了
'''

'''
虽然这个程序看起来并没有墙上的挂历有用,但是稍作修改就可以做很多有用的事情。它
可以发送网站访问失败、应用测试失败的异常情况,也可以在 Amazon 网站上出现了一款
卖到断货的畅销品时通知你——这些都是挂历做不到的事情
'''

import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

def send_mail(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "christmas_alerts@pythonscraping.com"
    msg['To'] = "ryan@pythonscraping.com"

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()

bs_obj = BeautifulSoup(urlopen("https://isitchristmas.com/"))
while (bs_obj.find("a", {"id": "answer"}).attrs['title'] == "NO"):
    print("It is not Christmas yet.")
    time.sleep(3600)
bs_obj = BeautifulSoup(urlopen("https://isitchristmas.com/"))
send_mail("It's Christmas!",
        "According to http://itischristmas.com, it is Christmas!")