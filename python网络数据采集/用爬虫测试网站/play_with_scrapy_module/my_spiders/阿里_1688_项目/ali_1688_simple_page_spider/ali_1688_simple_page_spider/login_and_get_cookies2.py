# coding:utf-8

'''
@author = super_fazai
@File    : login_and_get_cookies2.py
@Time    : 2017/10/10 15:31
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from PIL import Image
from pprint import pprint
from scrapy.selector import Selector

# chrome驱动地址
my_chrome_driver_path = '/Users/afa/myFiles/tools/chromedriver'
username = ''
pwd = ''

# 要处理并爬取信息的url的地址
wait_to_deal_with_url = 'https://detail.1688.com/offer/526362847506.html?spm=b26110380.sw1688.mof001.13.5rHmRl'

class Login(object):
    def __init__(self):
        super().__init__()
        self.driver = webdriver.Chrome(my_chrome_driver_path)
        self.start_url = 'https://login.taobao.com/member/login.jhtml?style=b2b&css_style=b2b&from=b2b&newMini2=true&full_redirect=true&redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttp%25253A%25252F%25252Fmember.1688.com%25252Fmember%25252Foperations%25252Fmember_operations_jump_engine.htm%25253Ftracelog%25253Dlogin%252526operSceneId%25253Dafter_pass_from_taobao_new%252526defaultTarget%25253Dhttp%2525253A%2525252F%2525252Fwork.1688.com%2525252F%2525253Ftracelog%2525253Dlogin_target_is_blank_1688&reg=http%3A%2F%2Fmember.1688.com%2Fmember%2Fjoin%2Fenterprise_join.htm%3Flead%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26leadUrl%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26tracelog%3Daccount_verify_s_reg'


    def login(self):
        # tmp_url = 'https://detail.1688.com/offer/526362847506.html?spm=b26110380.sw1688.mof001.13.5rHmRl'
        # self.start_url = self.bash_url + tmp_url
        self.driver.get(self.start_url)
        self.driver.implicitly_wait(10)
        # self.driver.save_screenshot('tmp_login1.png')

        # 处理并下载二维码
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        img = soup.select('div.qrcode-img img')[0]
        img_url = re.compile('<img src=\"(.*?)\"/>').findall(str(img))[0]
        # print(img_url)
        img_url = 'http:' + img_url

        # 保存二维码图片
        buf = urlopen(img_url)
        with open('qrcode.jpg', 'wb') as f:
            f.write(buf.read())

        # 扫码
        qrcode_img = Image.open('./qrcode.jpg')
        qrcode_img.show()
        # print(img_src)

        before_url = self.driver.current_url

        print('正在等待扫码....')
        sleep(15)

        while self.driver.current_url != before_url:
            print('扫码登陆成功!')
            break

        # 得到并处理保存cookies到cookies.txt
        login_cookies = self.driver.get_cookies()
        # print(login_cookies)
        cookies = self.get_qrcode_cookies(login_cookies)
        cookies_str = self.cookies_to_str(cookies)

        # 将cookies写入指定文件cookies.txt
        with open('./../cookies.txt', 'wb') as f:
            f.write(cookies_str.encode('utf-8'))

        # with open('cookies.txt', 'rb') as f:
        #     line = f.read().decode('utf-8').strip('\n')
        #     print(line)

    def deal_with_page_url(self):
        self.driver.get(wait_to_deal_with_url)
        self.driver.implicitly_wait(10)

        body = self.driver.page_source

        title = Selector(text=body).css('h1.d-title::text').extract_first().encode().decode()
        price = Selector(text=body).css('span.value.price-length-6::text').extract()
        trade_number = Selector(text=body).css('tr.amount span.value::text').extract()

        color = Selector(text=body).css('div.obj-content div.box-img img::attr("alt")').extract()
        color_img_url = Selector(text=body).css('div.obj-content div.box-img img::attr("src")').extract()

        print(title)
        print(price)
        print(trade_number)
        print(color)
        print(color_img_url)



    def get_qrcode_cookies(self, login_cookies):
        '''
        处理传入的cookies,从而得到自己需求的cookies
        :param login_cookies:
        :return:
        '''
        cookies = {}
        tmp_key = ''
        tmp_value = ''
        for item in login_cookies:
            for key in item.keys():
                if 'name' == key:
                    # print(item[key])
                    tmp_key = item[key]
                if 'value' == key:
                    tmp_value = item[key]

                if tmp_key != '' and tmp_value != '':
                    cookies[tmp_key] = tmp_value
        return cookies

    def cookies_to_str(self, cookies):
        '''
        将字典类型的cookies转换为str类型的cookies
        :param cookies:
        :return:
        '''
        cookie = [str(key) + "=" + str(value) for key, value in cookies.items()]
        # print cookie

        cookiestr = ';'.join(item for item in cookie)
        return cookiestr

if __name__ == '__main__':
    login_ali = Login()
    login_ali.login()
    login_ali.deal_with_page_url()


