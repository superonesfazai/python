# coding:utf-8

'''
@author = super_fazai
@File    : taobao_login_and_parse.py
@Time    : 2017/10/22 17:51
@connect : superonesfazai@gmail.com
'''

"""
淘宝网
"""

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from scrapy import Selector
import re
from urllib.request import urlopen
from PIL import Image
from time import sleep
from pprint import pprint

from settings import CHROME_DRIVER_PATH, PHANTOMJS_DRIVER_PATH

# chrome驱动地址
my_chrome_driver_path = CHROME_DRIVER_PATH

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

class TaoBaoLoginAndParse():
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
        # self.start_url = 'https://login.taobao.com/member/login.jhtml?style=b2b&css_style=b2b&from=b2b&newMini2=true&full_redirect=true&redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttp%25253A%25252F%25252Fmember.1688.com%25252Fmember%25252Foperations%25252Fmember_operations_jump_engine.htm%25253Ftracelog%25253Dlogin%252526operSceneId%25253Dafter_pass_from_taobao_new%252526defaultTarget%25253Dhttp%2525253A%2525252F%2525252Fwork.1688.com%2525252F%2525253Ftracelog%2525253Dlogin_target_is_blank_1688&reg=http%3A%2F%2Fmember.1688.com%2Fmember%2Fjoin%2Fenterprise_join.htm%3Flead%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26leadUrl%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26tracelog%3Daccount_verify_s_reg'
        # self.start_url = 'https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do'
        self.start_url = 'https://login.taobao.com/member/login.jhtml?spm=2013.1.1997563269.1.793cab65Edp2ty&full_redirect=true&redirect_url=https://www.taobao.com'
        self.img_url = ''                   # 用来保存二维码的url
        self.wait_to_deal_with_url = ''     # 待爬取的url

    def get_qrcode_url(self):
        '''
        从官网获取二维码图片url
        :return:
        '''
        print('请稍等正在获取验证码url中...')
        self.driver.set_page_load_timeout(25)
        try:
            self.driver.get(self.start_url)
            self.driver.implicitly_wait(15)
            # self.driver.save_screenshot('tmp_login1.png')

            locator = (By.CSS_SELECTOR, 'div.qrcode-img img')
            try:
                WebDriverWait(self.driver, 15, 0.5).until(EC.presence_of_element_located(locator))
            except Exception as e:
                print('获取验证码时错误: ', e)
            else:
                pass
        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 20 seconds(当获取验证码时)')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            # pass

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
        sleep(16)

        while self.driver.current_url != before_url:
            print('扫码登陆成功!')
            print('-' * 100)
            break

        # 得到并处理保存cookies到cookies.txt
        login_cookies = self.driver.get_cookies()
        # print(login_cookies)
        cookies = self.get_qrcode_cookies(login_cookies)
        print('| 获取到的cookies为: ', cookies)

        cookies_str = self.cookies_to_str(cookies)
        '''
        这里不能用isg来判断因为前后都有
        '''
        if cookies.get('existShop') is not None:  # 扫码成功
            # 将cookies写入指定文件cookies_taobao.txt (用于高并发)
            with open('./cookies/cookies_taobao.txt', 'wb') as f:
                f.write(cookies_str.encode('utf-8'))
            # self.driver.quit()      # 释放原先的driver占用的资源
            return True
        else:                               # 扫码失败
            return False

    def deal_with_page_url(self):
        '''
        解析给与的对应地址
        :return: 返回一个解析结果的json对象
        '''
        # 遇到一个问题加载很慢，已解决
        # 解决方案直接设置给driver设置时间延迟来终止请求
        self.driver.set_page_load_timeout(4.5)
        print('待爬取的url地址为: ', self.wait_to_deal_with_url)
        try:
            self.driver.get(self.wait_to_deal_with_url)
            sleep(1)    # 这里睡眠的目的是为了让color_img_url先加载出来避免图片为空值
            self.driver.implicitly_wait(7)     # 隐式等待和显式等待可以同时使用

            locator = (By.CSS_SELECTOR, 'div#detail')
            try:
                WebDriverWait(self.driver, 7, 0.5).until(EC.presence_of_element_located(locator))
            except Exception as e:
                print('遇到错误: ', e)
                return 4041    # 未得到div#detail，返回4041
            else:
                print('div#detail已经加载完毕')
        except Exception as e:       # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 4.5 seconds when loading page')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            # pass

        body = self.driver.page_source      # 不能缩小范围否则抓不到size_info, detail_price
        print('页面开始解析'.center(20, '#'))
        # 店铺名称
        shop_name = str(Selector(text=body).css('div.pop-shop-info span.shop-name-title::attr("title")').extract_first())
        account_list = list(Selector(text=body).css('div.more-info div.shop-more-info p.info-item').extract())  # 得到对应p标签的p标签块
        account = ''
        try:
            tmp_account = re.compile(r'<span.*?>.*?</span>').sub('', account_list[1])   # 第二个就是account
            tmp_account = re.compile(r'<p.*?>').sub('', tmp_account)
            tmp_account = re.compile(r'</p>').sub('', tmp_account)
            tmp_account = re.compile(r'\s').sub('', tmp_account)
            tmp_account = re.compile(r'"').sub('', tmp_account)
            # tmp_account = re.compile(r' ').sub('', tmp_account)
            account = tmp_account
        except IndexError as e:     # 说明不是普通店铺, 这里给他跳过
            pass
        title = str(Selector(text=body).css('div#detail div.tb-title h3.tb-main-title::attr("data-title")').extract_first())
        tmp_shop_name_url = str(Selector(text=body).css('div.shop-name a.shop-name-link::attr("href")').extract_first())  # 卖家私人主页
        shop_name_url = 'https:' + tmp_shop_name_url

        if shop_name == 'None':     # 则可能是金牌卖家
            print('可能是金牌卖家...')
            shop_name = str(Selector(text=body).css('div.tb-shop-info-hd div.tb-shop-name a::attr("title")').extract_first())
            tmp_account = str(Selector(text=body).css('div.tb-shop-info-hd div.tb-shop-seller a::attr("title")').extract_first())
            account = re.compile(r'掌柜:').sub('', tmp_account)       # 过滤 '掌柜:'
            tmp_shop_name_url = str(Selector(text=body).css('div.tb-shop-info-hd div.tb-shop-name a::attr("href")').extract_first())
            shop_name_url = 'https:' + tmp_shop_name_url

        # 注意sub_title可能为空
        tmp_sub_title = str(Selector(text=body).css('div#detail div.tb-title p.tb-subtitle::text').extract_first())
        sub_title = re.compile(r'\s').sub('', tmp_sub_title)
        # link_name = str(Selector(text=body).css('div.detail a.name::text').extract_first())   # 联系卖家

        # 正常价格
        price = str(Selector(text=body).css('ul.tb-meta li strong#J_StrPrice em.tb-rmb-num::text').extract_first())
        # 淘宝价格  其值可能为空      还有就是淘宝价格是后面才加载出来的
        taobao_price = str(Selector(text=body).css('ul.tb-meta li strong.tb-promo-price em.tb-rmb-num::text').extract_first())
        # 该商品总库存量,  其值商家可能不给，所以可能为空值
        goods_stock = Selector(text=body).css('ul.tb-meta li span.tb-property-cont em.J_ItemStock::text').extract_first()   # 为空就返回None

        if goods_stock is None:
            goods_stock = ''

        """
        div#J_isku div.tb-skin      该商品所有细节属性
        """
        # 标签名list
        detail_name_list = list(Selector(text=body).css('div#J_isku div.tb-skin dl.tb-prop dt.tb-property-type::text').extract())

        '''
        # 标签值list   此处由于种类太多,就只能把里面的ul标签中所有li标签对应取出，后面想到解决方案通过re进行数据清洗即可
        '''
        # 先过滤掉'\n', '  ', '\t', 再对html进行处理
        tmp_body = body
        tmp_body = re.compile(r'\n').sub('', tmp_body)
        tmp_body = re.compile(r'\t').sub('', tmp_body)
        tmp_body = re.compile(r'  ').sub('', tmp_body)  # 此处过滤两个空格
        # body = re.compile(r'.*?<div class="tb-skin">(.*?)</div>.*?').findall(body)
        # print(body)
        tmp_detail_value_list = re.compile(r'<ul data-property=.*?>(.*?)</ul>').findall(tmp_body)
        # print(tmp_detail_value_list)
        value_list = []
        color_img_url = ''
        for item in tmp_detail_value_list:
            tmp_ss = []
            item = re.compile(r' data-value=\".*?\"').sub('', item)         # 清洗li标签
            item = re.compile(r' href=\".*?\"').sub('', item)               # 清洗a标签
            item = re.compile(r'<i>已选中</i>').sub('', item)                # 过滤'<i>已选中</i>'
            item = re.compile(r'<a><span>').sub('', item)                   # 过滤掉'<a><span>'
            item = re.compile(r'</span></a>').sub('', item)                 # 过滤掉'</span></a>'
            item = re.compile(r' class=".*?"').sub('', item)                # 过滤掉' class=".*?"'
            item = re.compile(r'</li><li>').sub('|', item)                  # 通过</li><li>, 来进行分割多个li的
            item = re.compile(r'<li>').sub('', item)                        # 过滤'<li>'
            item = re.compile(r'</li>').sub('', item)                       # 过滤'</li>'
            item = re.compile(r'<a id="J_TbMultitermsLogin".*?>.*</a>').sub('', item)  # 过滤分期购(此处用贪婪匹配使匹配到的值为最大值)
            tmp_color_img_url_list = re.compile(r'url\((.*?)\)').findall(item)          # 查看是否有颜色示例图片
            color_img_url_list = []
            is_color_url = False
            if tmp_color_img_url_list != []:
                is_color_url = True
                for url in tmp_color_img_url_list:
                    url = 'https:' + url
                    color_img_url_list.append(url)
            color_img_url_list = self.deal_with_img_size_30_to_400(color_img_url_list)
            item = re.compile(r'<a style="background:url.*?>').sub('', item)  # 过滤掉a标签(这个a标签里面通常是颜色示例图片)
            item = re.compile(r'<span>').sub('', item)  # 过滤掉span标签
            if item == '':
                pass
            if re.compile(r'\|').findall(item):
                item = item.split('|')
            if isinstance(item, str):
                item = [item,]
            if item == ['']:
                pass
            if is_color_url:
                item = list(zip(item, color_img_url_list))
            value_list.append(item)
        value_list = [i for i in value_list if i != ['']]       # 过滤掉里面为空的值, ['']这个值
        detail_value_list = value_list
        # pprint(detail_value_list)

        # ul#J_UlThumb li div a img    示例图片地址
        tmp_all_img_url = list(Selector(text=body).css('ul#J_UlThumb li div a img::attr("src")').extract())
        tmp_all_img_url = ['https:'+item for item in tmp_all_img_url]
        all_img_url = self.deal_with_img_size_50_to_400(tmp_all_img_url)

        # 详细信息
        # div.attributes ul li::text   里面包含标签名和标签值  只需筛选出':'前面的就是标签名
        # div.attributes ul li::attr("title")     value
        tmp_p_name = list(Selector(text=body).css('div.attributes ul li::text').extract())   # a list
        p_name = [re.compile(r':.*').sub('', item) for item in tmp_p_name]      # 此处让其为贪婪匹配就能去掉冒号后面的值
        p_value = list(Selector(text=body).css('div.attributes ul li::attr("title")').extract())    # a list

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
            'shop_name': shop_name,                             # 店铺名称
            'account': account,                                 # 掌柜
            'title': title,                                     # 商品名称
            'sub_title': sub_title,                             # 子标题
            'shop_name_url': shop_name_url,                     # 店铺主页地址
            'price': price,                                     # 商品价格
            'taobao_price': taobao_price,                       # 淘宝价
            'goods_stock': goods_stock,                         # 商品库存
            'detail_name_list': detail_name_list,               # 商品标签属性名称
            'detail_value_list': detail_value_list,             # 商品标签属性对应的值
            'all_img_url': all_img_url,                         # 所有示例图片地址
            'p_name': p_name,                                   # 详细信息的标签名
            'p_value': p_value,                                 # 详细信息对应的值
        }

        print('页面解析完毕'.center(20, '#'))
        self.driver.quit()      # 每次爬取完一个数据释放一次driver资源
        return data

    def set_self_driver_with_phantomjs(self):
        """
        初始化带cookie的驱动，之所以用phantomjs是因为其加载速度很快(快过chrome驱动太多)
        """
        cookies_str = self.get_cookies_from_cookies_txt()
        cookies = self.str_to_dict(cookies_str)
        # print('从文件中获取到的cookies: ', cookies)
        print('--->>>初始化phantomjs驱动中<<<---')
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000  # 1秒
        cap['phantomjs.page.settings.loadImages'] = False
        cap['phantomjs.page.settings.disk-cache'] = True
        cap['phantomjs.page.customHeaders.Cookie'] = cookies
        # print('============| phantomjs即将执行 |')
        tmp_execute_path = EXECUTABLE_PATH
        self.driver = webdriver.PhantomJS(executable_path=tmp_execute_path, desired_capabilities=cap)
        # print('============| phantomjs执行成功 |')
        # self.driver.set_window_size(1200, 2000)      # 设置默认大小，避免默认大小显示
        wait = ui.WebDriverWait(self.driver, 10)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        print('------->>>初始化完毕<<<-------')

    def get_cookies_from_cookies_txt(self):
        with open('./cookies/cookies_taobao.txt', 'rb') as f:
            line = f.read().decode('utf-8').strip('\n')
            return line

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

    def str_to_dict(self, cookies):
        itemDict = {}
        items = cookies.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')  # 记得去除空格
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

    def deal_with_img_size_30_to_400(self, all_img_url):
        tmp_all_img_url = []
        for item in all_img_url:
            tmp_img_url = re.compile(r'\_30x30\.').sub('_400x400.', item)
            tmp_all_img_url.append(tmp_img_url)
        return tmp_all_img_url

    def deal_with_img_size_50_to_400(self, all_img_url):
        tmp_all_img_url = []
        for item in all_img_url:
            tmp_img_url = re.compile(r'\_50x50\.').sub('_400x400.', item)
            tmp_all_img_url.append(tmp_img_url)
        return tmp_all_img_url

    def set_wait_to_deal_with_url(self, wait_to_deal_with_url):
        '''
        设置待爬取的url
        :param wait_to_deal_with_url:
        :return:
        '''
        self.wait_to_deal_with_url = wait_to_deal_with_url

if __name__ == '__main__':
    login_taobao = TaoBaoLoginAndParse()
    login_taobao.get_qrcode_url()
    login_taobao.login()

    while True:
        wait_to_deal_with_url = input('请输入要爬取的商品界面地址(以英文分号结束): ')
        wait_to_deal_with_url.strip('\n').strip(';')
        # wait_to_deal_with_url = 'https://detail.1688.com/offer/526362847506.html?spm=b26110380.sw1688.mof001.13.5rHmRl'
        login_taobao.set_wait_to_deal_with_url(wait_to_deal_with_url)
        login_taobao.set_self_driver_with_phantomjs()
        data = login_taobao.deal_with_page_url()
        pprint(data)
