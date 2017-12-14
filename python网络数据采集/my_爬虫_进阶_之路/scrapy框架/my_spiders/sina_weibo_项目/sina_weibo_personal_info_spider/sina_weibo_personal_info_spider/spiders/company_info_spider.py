# -*- coding: utf-8 -*-
import scrapy
from MySQLdb import *
from ..items import CompanyDealInfoItem
from pprint import pprint
import re
from ..settings import COOKIES
from ..settings import HEADERS
from ..tools.cookies_to_dict import stringToDict
from ..tools.filter_emoji_str import filter_emoji_str
from time import sleep

class CompanyInfoSpiderSpider(scrapy.Spider):
    name = 'company_info_spider'
    allowed_domains = ['weibo.com']
    # start_urls = ['http://weibo.com/']

    def __init__(self):
        super().__init__()

        '''
        在这配置自己的mysql数据库信息
        '''
        self.conn = connect(
            host='localhost',       # mysql数据库地址
            port=3306,              # 端口号, 一般默认都是3306
            db='python',            # 保存的数据库
            user='root',            # 用户
            passwd='lrf654321',     # 密码
            # charset='utf-8',
        )

        self.header = HEADERS
        self.cookie = stringToDict(COOKIES)

        self.personal_deal_info_from_db = self.get_nick_name_and_personal_deal_info_url()
        # pprint(self.personal_deal_info_from_db)
        self.index = 0

    def start_requests(self):
        first_url = self.personal_deal_info_from_db[self.index][1]

        if first_url is None:
            self.index += 1
            first_url = self.personal_deal_info_from_db[self.index][1]

        yield scrapy.Request(url=first_url, headers=self.header, cookies=self.cookie, callback=self.parse)

    def parse(self, response):
        '''
        企业号私人信息爬取
        :param response:
        :return:
        '''
        company_deal_info = CompanyDealInfoItem()

        self.log('-' * 12 + '| 这是企业微博号, 企业信息页地址为: %s |' % response.url)

        the_same_info = self.get_the_same_info(response)

        # *针对第二种链接的提取模式
        # (注意: 友情链接保存的是url)
        # (注意友情链接注意判断a标签的个数, 然后都存到一个字段中)
        all_right_info = {}
        if response.css('div.WB_frame_c').extract():
            # 判断是否有简介
            if response.css('div.WB_innerwrap p.p_txt::text').extract():
                simple_desc = filter_emoji_str(response.css('div.WB_innerwrap p.p_txt::text').extract()[0])
                self.log('-' * 12 + '| 该企业号的简介内容为: %s |' % simple_desc)
            else:
                simple_desc = ''
                self.log('-' * 12 + '| 该企业号的简介内容为空 |')

            # 判断是否有基本讯息
            if response.css('div.WB_frame_c div.WB_innerwrap li').extract():    # 即存在li标签就有基本讯息
                title_list = response.css('div.WB_frame_c div.WB_innerwrap li span.pt_title::text').extract()
                tmp_info_list = response.css('div.WB_frame_c div.WB_innerwrap li span.pt_detail').extract()
                print(title_list)
                # print(tmp_info_list)

                tmp_friend_url = {}
                info_list = []
                friend_url = ''

                for item in tmp_info_list:
                    item = re.compile('<span class="pt_detail">(.*?)</span>').findall(item)[0]
                    # 判断是否有a标签
                    is_a_label = re.compile('<a href=.*?>(.*?)</a>').findall(item)
                    if is_a_label:  # 处理a标签
                        tmp_name_list = re.compile('<a href=.*?>(.*?)</a>').findall(item)
                        url_info_list = re.compile(r'<a href="(.*?)".*?>.*?</a>').findall(item)

                        # 构造友情链接
                        for index in range(0, len(tmp_name_list)):
                            tmp_friend_url[tmp_name_list[index]] = 'http:' + url_info_list[index]
                        # print(tmp_friend_url)

                        for key in tmp_friend_url:
                            tmp_str = key + ': ' + tmp_friend_url[key] + ', '
                            friend_url += tmp_str
                        item = friend_url

                    info_list.append(item)
                # print(tmp_info_list)
                # pprint(info_list)

                # 一一对应拼接信息
                for index in range(0, len(title_list)):
                    all_right_info[title_list[index]] = info_list[index]

                print('-' * 50 + '| 该企业微博的讯息如下: |')
                pprint(all_right_info)
                print('-' * 85)

            else:
                company_contact_name = ''
                company_phone = ''
                friend_url = ''
                self.log('-' * 12 + '| 该企业微博的未公开基本讯息 |')

        else:   # 在最外面加个判断用于提升程序运行速度
            simple_desc = ''
            company_contact_name = ''
            company_phone = ''
            friend_url = ''
            self.log('-' * 12 + '| 该企业未公布任何信息... |')

        company_deal_info['nick_name'] = self.personal_deal_info_from_db[self.index][0]

        company_deal_info['medal_info'] = the_same_info['medal_info']
        company_deal_info['sina_level'] = the_same_info['sina_level']
        company_deal_info['sina_level_exp'] = the_same_info['sina_level_exp']
        company_deal_info['vip_icon'] = the_same_info['vip_icon']
        company_deal_info['vip_group_speed'] = the_same_info['vip_group_speed']
        company_deal_info['vip_group_value'] = the_same_info['vip_group_value']

        company_deal_info['simple_desc'] = simple_desc

        # 先初始化赋值避免运行报错
        company_deal_info['company_contact_name'] = ''
        company_deal_info['company_phone'] = ''
        company_deal_info['friend_url'] = ''
        for key in all_right_info:
            if key == '联系人：':
                company_deal_info['company_contact_name'] = all_right_info['联系人：']

            if key == '电话：':
                company_deal_info['company_phone'] = all_right_info['电话：']

            if key == '友情链接：':
                company_deal_info['friend_url'] = all_right_info['友情链接：']

        self.log('-' * 12 + '| 该企业信息 已经爬取完成, 即将开始下一个微博号爬取 |')

        pprint(dict(company_deal_info))

        yield company_deal_info

        self.index += 1

        url = self.personal_deal_info_from_db[self.index][1]
        # print(url)
        if url is None:
            print('*' * 100 + '  给与的url为空, 跳过这个url开始下一个爬取')
            self.index += 1
            url = self.personal_deal_info_from_db[self.index][1]

        yield scrapy.Request(url=url, headers=self.header, cookies=self.cookie, callback=self.parse)

    def get_the_same_info(self, response):
        '''
        得到勋章, 等级, 会员信息相关
        :param response:
        :return:
        '''
        the_same_info = {}

        # 勋章信息
        medal_info_list = response.css('ul.bagde_list.clearfix li.bagde_item a::attr("title")').extract()
        # print(medal_info_list)
        if medal_info_list == []:
            medal_info = ''
            self.log('------------| 勋章信息为空 |')
        else:
            medal_info = ', '.join(medal_info_list)
            self.log('------------| 勋章信息为: %s |' % str(medal_info))

        # 等级信息
        tmp_sina_level = response.css('p.level_info span.S_txt1::text').extract_first()
        # print('-----------测试等级: ', tmp_sina_level)
        sina_level = int(re.compile(r'Lv.(\d+)').findall(tmp_sina_level)[0])
        self.log('-' * 12 + '| 微博level为: %d |' % sina_level)

        sina_level_exp = int(response.css('p.level_info span.S_txt1::text').extract()[1])
        self.log('-' * 12 + '| 该微博号的等级经验为: %d |' % sina_level_exp)

        # 会员信息
        vip_box = response.css('div.vip_box').extract()
        if vip_box:
            # 会员图标信息
            vip_icon_list = response.css('div.vip_box p.info_icon_box i::attr("class")').extract()
            vip_level = re.compile(r'.*?(\d+)').findall(vip_icon_list[0])[0]
            if len(vip_icon_list) > 1:  # 年费会员
                if vip_icon_list[1] == 'W_icon_year_member':
                    vip_icon = '年费会员' + '(会员等级:' + str(vip_level) + '级)'
                    self.log('-' * 12 + '| 会员图标信息为: %s |' % vip_icon)
            else:  # 普通会员
                vip_icon = '普通会员' + '(会员等级:' + str(vip_level) + '级)'
                self.log('-' * 12 + '| 会员图标信息为: %s |' % vip_icon)

            # 会员成长速度
            vip_group_speed = int(response.css('div.vip_box p.info span.point::text').extract()[0])
            # 会员经验值
            vip_group_value = int(response.css('div.vip_box p.info span.point::text').extract()[1])
            self.log('-' * 12 + '| 会员成长速度为: %d |' % vip_group_speed)
            self.log('-' * 12 + '| 会员经验值为: %d |' % vip_group_value)
        else:
            vip_icon = ''
            vip_group_speed = 0
            vip_group_value = 0
            self.log('-' * 12 + '| 该用户未开通会员信息 |')

        the_same_info['medal_info'] = medal_info
        the_same_info['sina_level'] = sina_level
        the_same_info['sina_level_exp'] = sina_level_exp
        the_same_info['vip_icon'] = vip_icon
        the_same_info['vip_group_speed'] = vip_group_speed
        the_same_info['vip_group_value'] = vip_group_value

        return the_same_info

    def get_nick_name_and_personal_deal_info_url(self):
        '''
        从数据库获取nick_name 和 personal_deal_info_url
        :return:
        '''
        try:
            cs = self.conn.cursor()

            # 只提取企业
            sql = 'select nick_name, personal_deal_info_url from bozhu_user where verify_type = \"企业蓝V认证\" and bozhu_user.nick_name not in (select nick_name from company_deal_info);'
            cs.execute(sql)

            result = cs.fetchall()  # return -> 一个 ((), (), ...)
            cs.close()

            print('=' * 12 + '| 成功获取数据库数据 |')
            return result
        except Exception as e:
            print('=' * 12 + '| 获取数据库数据失败 |')
            return None
