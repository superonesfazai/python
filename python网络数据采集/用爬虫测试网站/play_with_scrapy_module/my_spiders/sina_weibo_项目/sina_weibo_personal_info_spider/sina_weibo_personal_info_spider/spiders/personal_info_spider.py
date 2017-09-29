# -*- coding: utf-8 -*-
import scrapy
from MySQLdb import *
from ..items import PersonalDealInfoItem, CompanyDealInfoItem
from pprint import pprint
import re
from ..settings import COOKIES
from ..tools.cookies_to_dict import stringToDict

class PersonalInfoSpiderSpider(scrapy.Spider):
    name = 'personal_info_spider'
    allowed_domains = ['weibo.com']
    # start_urls = ['http://weibo.com/']

    def __init__(self):
        super().__init__()
        self.conn = connect(
            host='localhost',
            port=3306,
            db='python',
            user='root',
            passwd='lrf654321',
            # charset='utf-8',
        )

        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding:': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'd.weibo.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }

        self.cookie = stringToDict(COOKIES)

        self.personal_deal_info_from_db = self.get_nick_name_and_personal_deal_info_url()
        self.index = 0

    def start_requests(self):
        # first_url = self.personal_deal_info_from_db[self.index][1]
        # first_url = 'https://weibo.com/p/1005051881871034/info?mod=pedit_more'
        first_url = 'https://weibo.com/p/1003065542109985/info?mod=pedit_more'
        # first_url = 'https://weibo.com/2286596480/about'
        yield scrapy.Request(url=first_url, headers=self.header, cookies=self.cookie, callback=self.parse)

    def parse(self, response):
        is_had = re.compile(r'.*?(about)').findall(response.url)
        if is_had == []:      # 个人微博号
            self.log('-' * 12 + '| 这是个人微博号, 个人信息页地址为: %s |' % response.url)

            # 个人微博与企业微博共有相似信息, 下面是其中的关键字
            # (medal_info, sina_level, sina_level_exp,
            # vip_icon, vip_group_speed, vip_group_value)
            the_same_info = self.get_the_same_info(response)

            # 阳光信用
            credit_box = response.css('div.credit_wrap_box').extract()
            if credit_box:
                credit_value = response.css('div.credit_wrap_box div.radius_min_box.radiusDifferent p::text').extract()[1]
                self.log('-' * 12 + '| 阳光信用度：%s |' % credit_value)

            '''
            右侧详细信息页
            '''
            all_right_info = self.get_all_right_info(response)

        else:           # 企业号
            self.log('-' * 12 + '| 这是企业微博号, 企业信息页地址为: %s |' % response.url)

            the_same_info = self.get_the_same_info(response)

            # *针对第二种链接的提取模式
            # (注意: 友情链接保存的是url)
            # (注意友情链接注意判断a标签的个数, 然后都存到一个字段中)
            if response.css('div.WB_frame_c').extract():

            else:
                simple_desc = ''
                company_contact_name = ''
                company_phone = ''
                friend_url = ''



    def get_the_same_info(self, response):
        the_same_info = {}

        # 勋章信息
        medal_info_list = response.css('ul.bagde_list.clearfix li.bagde_item a::attr("title")').extract()
        if medal_info_list == []:
            medal_info = ''
            self.log('------------| 勋章信息为空 |')
        else:
            medal_info = ', '.join(medal_info_list)
            self.log('------------| 勋章信息为: %s |' % str(medal_info))

        # 等级信息
        tmp_sina_level = response.css('p.level_info span.S_txt1::text').extract_first()
        # print(tmp_sina_level)
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

    def get_all_right_info(self, response):
        all_right_info = {}

        # 标题名字
        title_list = response.css('div.m_wrap.clearfix ul.clearfix li span.pt_title::text').extract()
        pprint(title_list)
        # 标题对应信息
        tmp_info_list = response.css('div.m_wrap.clearfix ul.clearfix li span.pt_detail').extract()
        # print(tmp_info_list)

        info_list = []
        # 数据清洗
        for item in tmp_info_list:
            item = item.replace(' ', '|')  # 先把空格替换成'|', 然后待替换完，再替换回去
            item = re.compile('\s+').sub('', item)
            item = item.replace('|', ' ')
            # print(item)
            item = re.compile(r'<span class="pt_detail">(.*?)</span>').findall(item)[0]

            # 用于判断提取个性域名
            is_a_label = re.compile('<a .*?>.*?</a>').findall(item)
            if is_a_label:
                item = re.compile(r'<a href=.*?>(.*?)</a>').findall(item)[0]
            info_list.append(item)

        # print(info_list)

        # 一一对应赋值
        for index in range(0, len(title_list)):
            all_right_info[title_list[index]] = info_list[index]
            # print(all_right_info[title_list[index]])


        # 然后单独处理重新赋值一些定位出错的元素
        if all_right_info['标签：']:
            all_right_info['标签：'] = response.css('div.m_wrap.clearfix ul.clearfix li span.pt_detail a.W_btn_tag::text').extract()
            tmp_label_list = []
            for item in all_right_info['标签：']:
                item = re.compile(r'\s+').sub('', item)
                tmp_label_list.append(item)

            for item in tmp_label_list:     # 去除空值
                if item == '':
                    tmp_label_list.remove(item)
            all_right_info['标签：'] = ', '.join(tmp_label_list)

        print('-' * 50)
        pprint(all_right_info)
        print('-' * 50)
        return all_right_info


    def get_nick_name_and_personal_deal_info_url(self):
        try:
            cs = self.conn.cursor()

            sql = 'select nick_name, personal_deal_info_url from bozhu_user;'
            cs.execute(sql)

            result = cs.fetchall()  # return -> 一个 ((), (), ...)
            cs.close()

            print('=' * 12 + '| 成功获取数据库数据 |')
            return result
        except Exception as e:
            print('=' * 12 + '| 获取数据库数据失败 |')
            return None