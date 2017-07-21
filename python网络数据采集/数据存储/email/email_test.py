#coding:utf-8

import smtplib
from email.mime.text import MIMEText

# python 有两个包可以发送邮件: smtplib 和 email
msg = MIMEText("The body of the email is here")
msg['Subject'] = "An Email Alert"
msg['From'] = "ryan@pythonscraping.com"
msg['To'] = "webmaster@pythonscraping.com"
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()

# Python 的 email 模块里包含了许多实用的邮件格式设置函数,可以用来创建邮件"包裹"
