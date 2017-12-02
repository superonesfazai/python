# coding = utf-8

'''
@author = super_fazai
@File    : 知乎_验证码_test.py
@Time    : 2017/9/1 10:23
@connect : superonesfazai@gmail.com
'''

"""
已失效, 知乎login页面已改版
"""

import requests
import time
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup

def captcha(data):
    with open('captcha.jpg', 'wb') as fp:
        fp.write(data)
    time.sleep(1)
    image = Image.open('captcha.jpg')
    text = pytesseract.image_to_string(image)
    print('机器识别后的验证码为: ' + text)
    command = input('请输入Y表示同意使用, 按其它键自动重新输入: ')
    if (command == 'Y' or command == 'y'):
        return text
    else:
        return input('输入验证码: ')

def zhihu_login(username, passwd):
    # 构建一个保存cookie值的session对象
    session = requests.Session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    }

    # 先获取页面信息, 找到需要post的数据(并且已记录当前页面的cookie)
    html = session.get('https://www.zhihu.com/#signin', headers=headers).content

    # 找到name属性为_xsrf的input标签, 取出value里的值
    _xsrf = BeautifulSoup(html, 'lxml').find('input', attrs={'name': '_xsrf'}).get('value')

    # 取出验证码, r后面的值是Unix时间戳, time.time()
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000)
    response = session.get(captcha_url, headers=headers)

    data = {
        '_xsrf': _xsrf,
        'email': username,
        'password': passwd,
        'remember_me': True,
        'captcha': captcha(response.content),
    }

    response = session.post('https://www.zhihu.com/login/email', data=data, headers=headers)
    print(response.text)

    response = session.get('https://www.zhihu.com/people/maozhaojun/activities', headers=headers)
    print(response.text)

if __name__ == '__main__':
    # username = raw_input("username")
    # password = raw_input("password")
    zhihu_login('xxxx@qq.com', 'ALAxxxxIME')

'''
值得注意的是，有两种异常情况会导致这个程序运行失败。
    第一种情况是，如果 Tesseract 从验证码图片中识别的结果不是四个字符(因为训练样本中验证码的所有有效答案都必须 是四个字符)，结果不会被提交，程序失败。
    第二种情况是虽然识别的结果是四个字符， 被提交到了表单，但是服务器对结果不认可，程序仍然失败。

在实际运行过程中，
第一种 情况发生的可能性大约为 50%，发生时程序不会向表单提交，程序直接结束并提示验证码 识别错误。
第二种异常情况发生的概率约为 20%，四个字符都对的概率约是 30%(每个字 母的识别正确率大约是 80%，
如果是五个字符都识别，正确的总概率是 32.8%)
'''