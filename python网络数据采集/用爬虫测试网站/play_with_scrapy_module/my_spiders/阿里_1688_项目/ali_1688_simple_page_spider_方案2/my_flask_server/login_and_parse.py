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

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os, sys
sys.path.append(os.getcwd())
import json

# from .my_items import PageInfoItem

# chrome驱动地址
my_chrome_driver_path = '/Users/afa/myFiles/tools/chromedriver'
username = ''
pwd = ''

# 要处理并爬取信息的url的地址
# wait_to_deal_with_url = 'https://detail.1688.com/offer/526362847506.html?spm=b26110380.sw1688.mof001.13.5rHmRl'
wait_to_deal_with_url = 'https://detail.1688.com/offer/559526148757.html?spm=b26110380.sw1688.mof001.28.sBWF6s'

"""
记住不要在翻墙的情况下使用运行，要不然得不到界面的内容
"""

class LoginAndParse(object):
    def __init__(self):
        super().__init__()

        # 设置无运行界面版chrome
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')

        # 注意：测试发现还是得设置成加载图片要不然就无法得到超5张的示例图片完整地址
        # # 设置chrome不加载图片
        # prefs = {
        #     'profile.managed_default_content_settings.images': 2,
        # }
        # chrome_options.add_experimental_option('prefs', prefs)

        self.driver = webdriver.Chrome(executable_path=my_chrome_driver_path, chrome_options=chrome_options)
        # self.driver = webdriver.Chrome(executable_path=my_chrome_driver_path)
        self.start_url = 'https://login.taobao.com/member/login.jhtml?style=b2b&css_style=b2b&from=b2b&newMini2=true&full_redirect=true&redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttp%25253A%25252F%25252Fmember.1688.com%25252Fmember%25252Foperations%25252Fmember_operations_jump_engine.htm%25253Ftracelog%25253Dlogin%252526operSceneId%25253Dafter_pass_from_taobao_new%252526defaultTarget%25253Dhttp%2525253A%2525252F%2525252Fwork.1688.com%2525252F%2525253Ftracelog%2525253Dlogin_target_is_blank_1688&reg=http%3A%2F%2Fmember.1688.com%2Fmember%2Fjoin%2Fenterprise_join.htm%3Flead%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26leadUrl%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26tracelog%3Daccount_verify_s_reg'
        self.img_url = ''                   # 用来保存二维码的url
        self.wait_to_deal_with_url = ''     # 待爬取的url


    def get_qrcode_url(self):
        '''
        从官网获取二维码图片url
        :return:
        '''
        print('请稍等正在获取登录页面中...')
        # self.driver.set_page_load_timeout(5)
        self.driver.get(self.start_url)
        self.driver.implicitly_wait(10)
        # self.driver.save_screenshot('tmp_login1.png')

        locator = (By.CSS_SELECTOR, 'div.qrcode-img img')
        try:
            WebDriverWait(self.driver, 15, 0.5).until(EC.presence_of_element_located(locator))
        except Exception as e:
            print('获取验证码时错误: ', e)
        else:
            pass

        # 处理并下载二维码
        # soup = BeautifulSoup(self.driver.page_source, 'lxml')
        # img = soup.select('div.qrcode-img img')[0]
        # img_url = re.compile('<img src=\"(.*?)\"/>').findall(str(img))[0]
        img = list(Selector(text=self.driver.page_source).css('div.qrcode-img img').extract())[0]
        # print(img)
        img_url = re.compile('<img src=\"(.*?)\">').findall(str(img))[0]
        # print(img_url)
        self.img_url = 'http:' + img_url

        print('获取到的验证码的地址为: ', self.img_url)
        return self.img_url

    def login(self):
        '''
        模拟扫码登陆,并保存cookies到文件
        :return:
        '''
        """
        print('请稍等正在下载验证码到本地...即将下载完成请稍后')
        # 保存二维码图片
        buf = urlopen(self.img_url)
        with open('qrcode.jpg', 'wb') as f:
            f.write(buf.read())

        # 扫码
        qrcode_img = Image.open('./qrcode.jpg')
        qrcode_img.show()
        # print(img_src)

        before_url = self.driver.current_url

        print('正在等待扫码....')
        sleep(10)

        while self.driver.current_url != before_url:
            print('扫码登陆成功!')
            print('-' * 100)
            break
        """

        # 得到并处理保存cookies到cookies.txt
        login_cookies = self.driver.get_cookies()
        # print(login_cookies)
        cookies = self.get_qrcode_cookies(login_cookies)
        print('| 获取到的cookies为: ', cookies)
        # cookies_str = self.cookies_to_str(cookies)

        if cookies.get('isg') is not None:  # 扫码成功
            return True
        else:                               # 扫码失败
            return False

        # 将cookies写入指定文件cookies.txt
        # with open('cookies.txt', 'wb') as f:
        #     f.write(cookies_str.encode('utf-8'))

        # with open('cookies.txt', 'rb') as f:
        #     line = f.read().decode('utf-8').strip('\n')
        #     print(line)

    def deal_with_page_url(self):
        '''
        解析给与的对应地址
        :return: 返回一个解析结果的json对象
        '''
        # 遇到一个问题加载很慢，已解决
        # 解决方案直接设置给driver设置时间延迟来终止请求
        self.driver.set_page_load_timeout(5.5)
        try:
            print('待爬取的url地址为: ', self.wait_to_deal_with_url)
            self.driver.get(self.wait_to_deal_with_url)
            self.driver.implicitly_wait(10)     # 隐式等待和显式等待可以同时使用

            locator = (By.CSS_SELECTOR, 'div#mod-detail-bd')
            try:
                WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located(locator))
            except Exception as e:
                print('遇到错误: ', e)
                return 4041    # 未得到div#mod-detail-bd，返回4041
            else:
                print('div#mod-detail-bd已经加载完毕')
        except Exception as e:       # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 5.5 seconds when loading page')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作

        # 直接包含空格的CSS属性定位大法(可定位带空格的)
        try:
            if self.driver.find_element_by_css_selector('div[id="dt-tab"]>a[class="paging next"]'):
                self.driver.find_element_by_css_selector('div[id="dt-tab"]>a[class="paging next"]').click()
                print('示例图片超过5张，点击完成...')
                sleep(2)
        except Exception as e:
            print('示例图片未超过5张, 无需点击...')

        body = self.driver.page_source

        title = str(Selector(text=body).css('h1.d-title::text').extract_first())

        is_activity_price = False       # 用来判断是否为活动价格, 活动价格为True
        price = []
        # 判断是否有打折的存在，如果存在则保存的是存的是打折的价格
        try:
            if self.driver.find_element_by_css_selector('div.price-discount-sku'):
                print('这次的价格为活动价格')
                is_activity_price =True
                price = list(Selector(text=body).css('div.price-discount-sku span.value::text').extract())
        except Exception as e:
            print('正常价格非活动价格')
            price = list(Selector(text=body).css('div.d-content tr.price span.value::text').extract())
        trade_number = list(Selector(text=body).css('tr.amount span.value::text').extract())

        color = list(Selector(text=body).css('div.obj-content .box-img img::attr("alt")').extract())
        color_img_url = list(Selector(text=body).css('div.obj-content .box-img img::attr("src")').extract())

        color_img_url = self.deal_with_img_size_32_to_400(color_img_url)

        size_info = []
        detail_price = []
        rest_number = []
        '''
        通过判断div块 div.obj-content 的数量是否大于三来分类处理价格所在的不同位置
        '''
        is_div_obj_content_lt_2 = list(Selector(text=body).css('div.obj-content').extract())
        print('is_div_obj_content_lt_2的长度为 %d' % len(is_div_obj_content_lt_2))

        if len(is_div_obj_content_lt_2) == 2:   # 如果等于2说明: 只有颜色或者size之一
            if color == []:     # 如果颜色为空则说明该商品没有颜色这个属性选择, 即table.table-sku在size标签里面
                size_info = list(Selector(text=body).css('table.table-sku td.name span::text').extract())

                # 过滤size_info中的'\n'，'\t'
                size_info = self.deal_with_size_info_remove_null(size_info)

                # 偶数为价格(包含0), 奇数为库存量
                tmp_em = list(Selector(text=body).css('table.table-sku em.value::text').extract())

                detail_price = [tmp_em[index] for index in range(0, len(tmp_em)) if index % 2 == 0 or index == 0]
                rest_number = [tmp_em[index] for index in range(0, len(tmp_em)) if index % 2 != 0 and index != 0]
            else:               # 说明价格，以及库存量在color这个标签里面
                size_info = list(Selector(text=body).css('table.table-sku td.name span::text').extract())
                # print(size_info)

                # 过滤size_info中的'\n'，'\t'
                size_info = self.deal_with_size_info_remove_null(size_info)

                tmp_em = list(Selector(text=body).css('table.table-sku em.value::text').extract())

                detail_price = [tmp_em[index] for index in range(0, len(tmp_em)) if index % 2 == 0 or index == 0]
                rest_number = [tmp_em[index] for index in range(0, len(tmp_em)) if index % 2 != 0 and index != 0]

        elif len(is_div_obj_content_lt_2) > 2:    # 如果大于2, 则说明颜色，规格都有
            size_info = list(Selector(text=body).css('table.table-sku td.name span::text').extract())

            # 过滤size_info中的'\n'，'\t'
            size_info = self.deal_with_size_info_remove_null(size_info)

            tmp_em = list(Selector(text=body).css('table.table-sku em.value::text').extract())

            detail_price = [tmp_em[index] for index in range(0, len(tmp_em)) if index % 2 == 0 or index == 0]
            rest_number = [tmp_em[index] for index in range(0, len(tmp_em)) if index % 2 != 0 and index != 0]
        else:
            print('无法正确解析, 因为is_div_obj_content_lt_2值未被处理')

        tmp_img_url = list(Selector(text=body).css('div.content a.box-img img::attr("src")').extract())
        center_img_url = tmp_img_url[0]
        tmp_img_url.pop(0)
        all_img_url = tmp_img_url

        all_img_url = self.deal_with_img_size_60_to_400(all_img_url)

        """
        print('*' * 100)
        print('商品名称: ', title)
        if is_activity_price:
            print('活动价格: ', price)
        else:
            print('价格: ', price)
        print('起批量: ', trade_number)
        print('颜色: ', color)
        print('颜色图片地址: ', color_img_url)
        print('商品规格: ', size_info)
        print('商品规格对应价格: ', detail_price)
        print('商品规格对应库存量: ', rest_number)
        print('主图片地址: ', center_img_url)
        print('所有示例图片地址: ', all_img_url)
        print('*' * 100)
        """

        data = {
            'title': title,
            'price': price,
            'trade_number': trade_number,
            'color': color,
            'color_img_url': color_img_url,
            'size_info': size_info,
            'detail_price': detail_price,
            'rest_number': rest_number,
            'center_img_url': center_img_url,
            'all_img_url': all_img_url,
        }

        return data

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

    def deal_with_size_info_remove_null(self, size_info):
        '''
        过滤size_info中的'\n'，'\t'
        :param size_info:
        :return:
        '''
        c = []
        for item in size_info:
            tmp = re.compile(r'\n').sub('', item)
            tmp = re.compile(r' ').sub('', tmp)

            if tmp == '':
                pass
            else:
                c.append(tmp)
        return c

    def deal_with_img_size_60_to_400(self, all_img_url):
        tmp_all_img_url = []
        for item in all_img_url:
            tmp_img_url = re.compile(r'\.60x60\.').sub('.400x400.', item)
            tmp_all_img_url.append(tmp_img_url)
        return tmp_all_img_url

    def deal_with_img_size_32_to_400(self, color_img_url):
        tmp_color_img_url = []
        for item in color_img_url:
            tmp_img_url = re.compile(r'\.32x32\.').sub('.400x400.', item)
            tmp_color_img_url.append(tmp_img_url)
        return tmp_color_img_url

    def set_wait_to_deal_with_url(self, wait_to_deal_with_url):
        '''
        设置待爬取的url
        :param wait_to_deal_with_url:
        :return:
        '''
        self.wait_to_deal_with_url = wait_to_deal_with_url

# if __name__ == '__main__':
#     login_ali = LoginAndParse()
#     login_ali.get_qrcode_url()
#     login_ali.login()
#
#     while True:
#         # wait_to_deal_with_url = input('请输入要爬取的商品界面地址(以英文分号结束): ')
#         # wait_to_deal_with_url.strip('\n').strip(';')
#         wait_to_deal_with_url = 'https://detail.1688.com/offer/526362847506.html?spm=b26110380.sw1688.mof001.13.5rHmRl'
#         login_ali.set_wait_to_deal_with_url(wait_to_deal_with_url)
#         login_ali.deal_with_page_url()

# 马桶这个特别特殊
# https://detail.1688.com/offer/540344060909.html?spm=a260k.635.201611281602.10.JXEQXP






