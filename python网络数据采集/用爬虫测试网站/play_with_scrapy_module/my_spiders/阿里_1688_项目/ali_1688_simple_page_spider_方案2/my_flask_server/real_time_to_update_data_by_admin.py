# coding:utf-8

'''
@author = super_fazai
@File    : real_time_to_update_data_by_admin.py
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
import selenium.webdriver.support.ui as ui

import os, sys
sys.path.append(os.getcwd())
import json
import datetime
import requests

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
# from .my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from settings import CHROME_DRIVER_PATH, PHANTOMJS_DRIVER_PATH
from settings import ALI_1688_COOKIES_FILE_PATH
from decimal import Decimal

# chrome驱动地址
my_chrome_driver_path = CHROME_DRIVER_PATH
username = ''
pwd = ''

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

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
        print('请稍等正在获取验证码url中...')
        self.driver.set_page_load_timeout(20)
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
            # self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
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

        print('请稍等正在下载验证码到本地...即将下载完成请稍后')
        # 保存二维码图片
        buf = urlopen(self.img_url)
        with open('qrcode.jpg', 'wb') as f:
            f.write(buf.read())

        # 扫码
        qrcode_img = Image.open('qrcode.jpg')
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

        if cookies.get('isg') is not None:  # 扫码成功
            cookies_str = self.cookies_to_str(cookies)

            # 将cookies写入指定文件cookies_ali_1688.txt
            with open(ALI_1688_COOKIES_FILE_PATH, 'wb') as f:
                f.write(cookies_str.encode('utf-8'))
            return True
        else:                               # 扫码失败
            return False

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
            sleep(.8)    # 这里睡眠的目的是为了让color_img_url先加载出来避免图片为空值
            self.driver.implicitly_wait(7)     # 隐式等待和显式等待可以同时使用

            locator = (By.CSS_SELECTOR, 'div#mod-detail-bd')
            try:
                WebDriverWait(self.driver, 7, 0.5).until(EC.presence_of_element_located(locator))
            except Exception as e:
                print('遇到错误: ', e)
                return 4041    # 未得到div#mod-detail-bd，返回4041
            else:
                print('div#mod-detail-bd已经加载完毕')
        except Exception as e:       # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 4.5 seconds when loading page')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            # pass

        # 直接包含空格的CSS属性定位大法(可定位带空格的)
        ## 不点击只取首页有的图片, 这样等不等待从而速率很快
        """
        try:
            if self.driver.find_element_by_css_selector('div[id="dt-tab"]>a[class="paging next"]'):
                self.driver.find_element_by_css_selector('div[id="dt-tab"]>a[class="paging next"]').click()
                print('示例图片超过5张，点击完成...')
                sleep(3)
        except Exception as e:
            print('示例图片未超过5张, 无需点击...')
        """

        body = self.driver.page_source      # 不能缩小范围否则抓不到size_info, detail_price
        print('页面开始解析'.center(20, '#'))
        company_name = str(Selector(text=body).css('div.base-info div.company-name::attr("title")').extract_first())    # 公司名称
        title = str(Selector(text=body).css('h1.d-title::text').extract_first())
        link_name = str(Selector(text=body).css('div.detail a.name::text').extract_first())   # 联系卖家
        link_name_personal_url = str(Selector(text=body).css('div.detail a.name::attr("href")').extract_first())    # 卖家私人主页

        is_activity_price = False       # 用来判断是否为活动价格, 活动价格为True
        price = []
        # 判断是否有打折的存在，如果存在则保存的是存的是打折的价格
        try:
            if self.driver.find_element_by_css_selector('div.price-discount-sku'):
                print('这次的价格为活动价格')
                is_activity_price =True
                price = list(Selector(text=body).css('div.price-discount-sku span.value::text').extract())
            else:
                pass
        except Exception as e:
            print('正常价格非活动价格')
            price = list(Selector(text=body).css('div.d-content tr.price span.value::text').extract())
        trade_number = list(Selector(text=body).css('tr.amount span.value::text').extract())

        color = list(Selector(text=body).css('div.obj-content .box-img img::attr("alt")').extract())
        color_img_url = list(Selector(text=body).css('div.obj-content .box-img img::attr("src")').extract())

        color_img_url = self.deal_with_img_size_32_to_400(color_img_url)

        # div.d-content div.obj-content 标签内容

        # 标签名称list
        spec_name = list(Selector(text=body).css('div.obj-header span.obj-title::text').extract())  # 标签名称list

        other_size_info = []
        size_info = []
        detail_price = []
        rest_number = []
        '''
        通过判断div块 div.obj-content 的数量是否大于三来分类处理价格所在的不同位置
        '''
        print('goods_name的长度为 %d' % len(spec_name))

        if len(spec_name) == 1:   # 如果等于2说明: 只有颜色或者size再或者其他属性之一
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

        elif len(spec_name) == 2:    # 如果大于2, 则说明颜色，规格都有(或者是非颜色是其他属性和规格)
            if color != []:     # 有颜色这个属性
                size_info = list(Selector(text=body).css('table.table-sku td.name span::text').extract())

                # 过滤size_info中的'\n'，'\t'
                size_info = self.deal_with_size_info_remove_null(size_info)

                tmp_em = list(Selector(text=body).css('table.table-sku em.value::text').extract())

                detail_price = [tmp_em[index] for index in range(0, len(tmp_em)) if index % 2 == 0 or index == 0]
                rest_number = [tmp_em[index] for index in range(0, len(tmp_em)) if index % 2 != 0 and index != 0]
            else:               # 没有颜色这个属性,而是其他属性
                # 其他属性
                other_size_info = list(Selector(text=body).css('div.d-content div.obj-content ul span::text').extract())
                size_info = list(Selector(text=body).css('table.table-sku td.name span::text').extract())

                # 过滤size_info中的'\n'，'\t'
                size_info = self.deal_with_size_info_remove_null(size_info)

                tmp_em = list(Selector(text=body).css('table.table-sku em.value::text').extract())

                detail_price = [tmp_em[index] for index in range(0, len(tmp_em)) if index % 2 == 0 or index == 0]
                rest_number = [tmp_em[index] for index in range(0, len(tmp_em)) if index % 2 != 0 and index != 0]

        elif len(spec_name) == 0:      # 没有标签名称这个属性
            pass
        else:
            print('无法正确解析, 因为is_div_obj_content_lt_2值未被处理')

        tmp_img_url = list(Selector(text=body).css('div.content a.box-img img::attr("src")').extract())
        center_img_url = tmp_img_url[0]
        tmp_img_url.pop(0)
        all_img_url = tmp_img_url

        all_img_url = self.deal_with_img_size_60_to_400(all_img_url)

        if len(all_img_url) > 5:    # 超过5张就切割出前5张
            all_img_url = all_img_url[:5]
        else:
            pass

        # 详细信息
        # div.obj-content tbody td.de-feature   名字
        # div.obj-content tbody td.de-value     value
        p_name = list(Selector(text=body).css('div.obj-content tbody td.de-feature::text').extract())   # a list
        p_value = list(Selector(text=body).css('div.obj-content tbody td.de-value::text').extract())    # a list

        # 下方所有示例
        # div.desc-lazyload-container::attr("data-tfs-url")
        data_tfs_url = str(Selector(text=body).css('div.desc-lazyload-container::attr("data-tfs-url")').extract_first())

        property_info = ''
        if data_tfs_url != 'None':
            property_info = self.get_data_tfs_url_div(data_tfs_url)
        elif data_tfs_url == 'None':
            tmp_data_tfs_url = list(Selector(text=body).css('div.mod-detail-description::attr("data-mod-config")').extract_first())
            ### 意外发现返回的是这样格式是单字母list  ['{', '"', 's', 'h', 'o', 'w', 'O', 'n', '"', ':', '[', '"', 'm', 'o', 'd', '-', 'd', 'e', 't', 'a', 'i', 'l', '-', 'd', 'e', 's', 'c', 'r', 'i', 'p', 't', 'i', 'o', 'n', '"', ']', ',', '"', 't', 'i', 't', 'l', 'e', '"', ':', '"', '详', '细', '信', '息', '"', ',', '"', 't', 'a', 'b', 'C', 'o', 'n', 'f', 'i', 'g', '"', ':', '{', '"', 't', 'r', 'a', 'c', 'e', '"', ':', '"', 't', 'a', 'b', 'd', 'e', 't', 'a', 'i', 'l', '"', ',', '"', 's', 'h', 'o', 'w', 'K', 'e', 'y', '"', ':', '"', 'm', 'o', 'd', '-', 'd', 'e', 't', 'a', 'i', 'l', '-', 'd', 'e', 's', 'c', 'r', 'i', 'p', 't', 'i', 'o', 'n', '"', '}', ' ', ',', '"', 'c', 'a', 't', 'a', 'l', 'o', 'g', '"', ':', '[', '{', '"', 'i', 'd', '"', ':', '"', '0', '"', ',', '"', 't', 'i', 't', 'l', 'e', '"', ':', '"', '"', ',', '"', 'c', 'o', 'n', 't', 'e', 'n', 't', 'U', 'r', 'l', '"', ':', '"', 'h', 't', 't', 'p', 's', ':', '/', '/', 'i', 'm', 'g', '.', 'a', 'l', 'i', 'c', 'd', 'n', '.', 'c', 'o', 'm', '/', 't', 'f', 's', 'c', 'o', 'm', '/', 'T', 'B', '1', 'l', 'v', 'i', 'j', 'i', '6', 'q', 'h', 'S', 'K', 'J', 'j', 'S', 's', 'p', 'n', 'X', 'X', 'c', '7', '9', 'X', 'X', 'a', '"', '}', ']', ' ', '}']
            # print(type(tmp_data_tfs_url))
            # print(tmp_data_tfs_url)
            tmp_data_tfs_url = ''.join(tmp_data_tfs_url)        # list -> str
            tmp_data_tfs_url = json.loads(tmp_data_tfs_url)     # json字符串反序列化dict
            try:
                data_tfs_url = tmp_data_tfs_url['catalog'][0]['contentUrl']
                property_info = self.get_data_tfs_url_div(data_tfs_url)
            except Exception as e:
                property_info = ''
        else:
            property_info = ''

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
            'company_name': company_name,                       # 公司名称
            'title': title,                                     # 商品名称
            'link_name': link_name,                             # 卖家姓名
            'link_name_personal_url': link_name_personal_url,   # 卖家个人主页地址
            'price': price,                                     # 商品价格
            'trade_number': trade_number,                       # 对应起批量
            'goods_name': spec_name,                             # 标签属性名称
            'color': color,                                     # 商品颜色
            'color_img_url': color_img_url,                     # 颜色图片地址
            'other_size_info': other_size_info,                 # 非颜色的属性值
            'size_info': size_info,                             # 商品规格
            'detail_price': detail_price,                       # 对应的价格
            'rest_number': rest_number,                         # 对应的库存量
            'center_img_url': center_img_url,                   # 主页图片地址
            'all_img_url': all_img_url,                         # 所有示例图片地址
            'p_name': p_name,                                   # 详细信息的标签名
            'p_value': p_value,                                 # 详细信息对应的值
            'property_info': property_info,                     # 下方详细div块
        }

        print('页面解析完毕'.center(20, '#'))
        # self.driver.quit()      # 每次爬取完一个数据释放一次driver资源
        return data

    def to_right_and_update_data(self, data, pipeline):
        data_list = data
        tmp = {}
        tmp['goods_id'] = data_list['goods_id']  # 官方商品id
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tmp['deal_with_time'] = now_time  # 操作时间

        tmp['company_name'] = data_list['company_name']  # 公司名称
        tmp['title'] = data_list['title']  # 商品名称
        tmp['link_name'] = data_list['link_name']  # 卖家姓名
        tmp['link_name_personal_url'] = data_list['link_name_personal_url']  # 卖家私人主页地址

        tmp_price_info = list(zip(data_list['price'], data_list['trade_number']))

        # 设置最高价price， 最低价taobao_price
        if len(data_list['price']) >= 1:
            tmp_price_list = data_list['price']
            tmp_price_list2 = []
            for ii in tmp_price_list:
                ii = float(ii)
                tmp_price_list2.append(ii)

            tmp['price'] = Decimal(sorted(tmp_price_list2)[-1]).__round__(2)  # 得到最大值并转换为精度为2的decimal类型
            tmp['taobao_price'] = Decimal(sorted(tmp_price_list2)[0]).__round__(2)
        else:
            tmp['price'] = Decimal(0).__round__(2)
            tmp['taobao_price'] = Decimal(0).__round__(2)

        price_info = []
        for item in tmp_price_info:
            tmp_dic = {}
            tmp_dic['price'] = item[0]
            tmp_dic['trade_number'] = item[1]
            price_info.append(tmp_dic)
        tmp['price_info'] = price_info  # 价格信息

        spec_name = []
        for item in data_list['goods_name']:
            tmp_dic = {}
            tmp_dic['spec_name'] = item
            spec_name.append(tmp_dic)

        tmp['spec_name'] = spec_name  # 标签属性名称

        # [{'goods_value': '红色|L', 'color_img_url': 'xxx.jpg', 'price': '99', 'stocknum': '1000'}, {…}, …]
        """
        处理得到goods_info
        """
        goods_info = []
        if data_list['color'] == []:  # 颜色为空, size必定存在
            if data_list['size_info'] != []:
                if data_list['other_size_info'] == []:  # 说明other_size_info不存在, 只有一个size_info
                    tmp_goods_info = list(
                        zip(data_list['size_info'], data_list['detail_price'], data_list['rest_number']))
                    for item in tmp_goods_info:
                        tmp_dic = {}
                        tmp_dic['spec_value'] = item[0]
                        tmp_dic['color_img_url'] = ''
                        tmp_dic['detail_price'] = item[1]
                        tmp_dic['rest_number'] = item[2]
                        goods_info.append(tmp_dic)
                    tmp['goods_info'] = goods_info
                else:  # other_size 存在
                    tmp_goods_info = list(
                        zip(data_list['size_info'], data_list['detail_price'], data_list['rest_number']))
                    for index in range(0, len(data_list['other_size_info'])):
                        tmp_dic = {}
                        tmp_dic['spec_value'] = data_list['other_size_info'][index]
                        for item in tmp_goods_info:
                            # print(item[0])
                            tmp_dic['spec_value'] = ''  # 分析后加这两句话就完美解决了在原值上进行加
                            tmp_dic['spec_value'] = data_list['other_size_info'][index]
                            tmp_dic['spec_value'] += '|' + item[0]
                            tmp_dic['color_img_url'] = ''
                            tmp_dic['detail_price'] = item[1]
                            tmp_dic['rest_number'] = item[2]
                            goods_info.append(tmp_dic)
                            # print(tmp_dic['goods_value'])
                            tmp_dic = {}  # 注意: 这里重置, 能避免一直为 如2XL
                    tmp['goods_info'] = goods_info
            else:  # 二者都为空，则goods_info = []
                tmp['goods_info'] = []

        elif data_list['color'] != [] and data_list['color_img_url'] == []:  # 颜色不为空, 但颜色图片为空
            if data_list['size_info'] == []:  # size为空
                tmp_goods_info = list(zip(data_list['color'], data_list['detail_price'], data_list['rest_number']))
                for item in tmp_goods_info:
                    tmp_dic = {}
                    tmp_dic['spec_value'] = item[0]
                    tmp_dic['color_img_url'] = ''
                    tmp_dic['detail_price'] = item[1]
                    tmp_dic['rest_number'] = item[2]
                    goods_info.append(tmp_dic)
                tmp['goods_info'] = goods_info
            else:  # size不为空
                tmp_goods_info = list(zip(data_list['size_info'], data_list['detail_price'], data_list['rest_number']))
                for color in data_list['color']:
                    tmp_dic = {}
                    tmp_dic['spec_value'] = color
                    for item in tmp_goods_info:
                        tmp_dic['spec_value'] = tmp_dic['spec_value'] + '|' + item[0]
                        tmp_dic['color_img_url'] = ''
                        tmp_dic['detail_price'] = item[1]
                        tmp_dic['rest_number'] = item[2]
                        goods_info.append(tmp_dic)
                        tmp_dic = {}  # 注意: 这里重置, 能避免一直为 如2XL
                tmp['goods_info'] = goods_info
        else:  # 颜色跟颜色图片都不为空
            if data_list['size_info'] == []:  # size为空
                tmp_goods_info = list(zip(data_list['color'], data_list['color_img_url'], data_list['detail_price'],
                                          data_list['rest_number']))
                for item in tmp_goods_info:
                    tmp_dic = {}
                    tmp_dic['spec_value'] = item[0]
                    tmp_dic['color_img_url'] = item[1]
                    tmp_dic['detail_price'] = item[2]
                    tmp_dic['rest_number'] = item[3]
                    goods_info.append(tmp_dic)
                tmp['goods_info'] = goods_info
            else:  # size不为空
                tmp_goods_info = list(zip(data_list['size_info'], data_list['detail_price'], data_list['rest_number']))
                for index in range(0, len(data_list['color'])):
                    tmp_dic = {}
                    tmp_dic['spec_value'] = data_list['color'][index]
                    color_img_url = data_list['color_img_url'][index]
                    for item in tmp_goods_info:
                        # print(item[0])
                        tmp_dic['spec_value'] = ''  # 分析后加这两句话就完美解决了在原值上进行加
                        tmp_dic['spec_value'] = data_list['color'][index]
                        tmp_dic['spec_value'] += '|' + item[0]
                        tmp_dic['color_img_url'] = color_img_url
                        tmp_dic['detail_price'] = item[1]
                        tmp_dic['rest_number'] = item[2]
                        goods_info.append(tmp_dic)
                        # print(tmp_dic['goods_value'])
                        tmp_dic = {}  # 注意: 这里重置, 能避免一直为 如2XL
                tmp['goods_info'] = goods_info
        tmp['center_img_url'] = data_list['center_img_url']  # 主图片地址

        all_img_url_info = []
        for index in range(0, len(data_list['all_img_url'])):
            tmp_dic = {}
            tmp_dic['img_url'] = data_list['all_img_url'][index]
            all_img_url_info.append(tmp_dic)
        tmp['all_img_url_info'] = all_img_url_info  # 所有示例图片地址

        p_info = []
        tmp_p_info = list(zip(data_list['p_name'], data_list['p_value']))
        for item in tmp_p_info:
            tmp_dic = {}
            tmp_dic['p_name'] = item[0]
            tmp_dic['p_value'] = item[1]
            p_info.append(tmp_dic)
        tmp['p_info'] = p_info  # 详细信息
        tmp['property_info'] = data_list['property_info']  # 下方div

        # 采集的来源地
        tmp['site_id'] = 2  # 采集来源地(阿里1688批发市场)
        tmp['is_delete'] = 0  # 逻辑删除, 未删除为0, 删除为1

        print('------>>>| 待存储的数据信息为: |', tmp)
        pipeline.update_table(tmp)

    def get_data_tfs_url_div(self, data_tfs_url):
        '''
        此处过滤得到data_tfs_url的div块
        :return:
        '''
        property_info = ''
        data_tfs_url_response = requests.get(data_tfs_url)
        data_tfs_url_body = data_tfs_url_response.content.decode('gbk')
        data_tfs_url_body = re.compile(r'\n').sub('', data_tfs_url_body)
        data_tfs_url_body = re.compile(r'  ').sub('', data_tfs_url_body)
        # print(body)
        is_offer_details = re.compile(r'offer_details').findall(data_tfs_url_body)
        if is_offer_details != []:
            data_tfs_url_body = re.compile(r'.*?{"content":"(.*?)"};').findall(data_tfs_url_body)
            # print(body)
            if data_tfs_url_body != []:
                property_info = data_tfs_url_body[0]
                property_info = re.compile(r'\\').sub('', property_info)
                # print(property_info)
            else:
                property_info = ''
        else:
            is_desc = re.compile(r'var desc=').findall(data_tfs_url_body)
            if is_desc != []:
                desc = re.compile(r'var desc=\'(.*)\';').findall(data_tfs_url_body)
                if desc != []:
                    property_info = desc[0]
                    print(property_info)
            else:
                property_info = ''
        return  property_info

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

    def get_cookies_from_cookies_txt(self):
        with open(ALI_1688_COOKIES_FILE_PATH, 'rb') as f:
            line = f.read().decode('utf-8').strip('\n')
            return line

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

if __name__ == '__main__':
    login_ali = LoginAndParse()
    login_ali.get_qrcode_url()
    login_ali.login()
    login_ali.set_self_driver_with_phantomjs()      # 不能放在循环内不然会生成很多phantomjs

    tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
    result = list(tmp_sql_server.select_all_goods_id())
    print('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
    print(result)
    print('--------------------------------------------------------')

    # while True:
    print('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
    for item in result:     # 实时更新数据
        tmp_url = 'https://detail.1688.com/offer/' + str(item[0]) + '.html'
        wait_to_deal_with_url = tmp_url
        login_ali.set_wait_to_deal_with_url(wait_to_deal_with_url)
        data = login_ali.deal_with_page_url()
        if data:
            data['goods_id'] = item[0]
            data['deal_with_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            print('------>>>| 爬取到的数据为: ', data)

            login_ali.to_right_and_update_data(data, pipeline=tmp_sql_server)
        else:   # 表示返回的data值为空值
            pass

    print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)








