# -*- coding: utf-8 -*-
import scrapy

from MySQLdb import *
from pprint import pprint
from scrapy.selector import Selector
import re
from ..items import HomeInfoItem
import time
from ..settings import COOKIES

class UserHomeInfoSpiderSpider(scrapy.Spider):
    name = 'user_home_info_spider'
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
        }

        self.cookie = self.stringToDict(COOKIES)

        self.user_name_and_url = self.get_nick_name_and_url_from_db()
        self.index = 0

    def start_requests(self):
        first_url = self.user_name_and_url[0][1]
        # first_url = 'https://weibo.com/u/5289412632?refer_flag=0000015011_&from=feed&loc=nickname&is_all=1'
        # first_url = 'https://weibo.com/weibomobile?is_all=1'
        self.log('=' * 12 + '| 待爬取的微博主页的url为 %s |' % (first_url,))
        yield scrapy.Request(first_url, headers=self.header, cookies=self.cookie, callback=self.parse)

    def parse(self, response):
        if self.index > len(self.user_name_and_url):
            self.log('=' * 12 + '| 所有微博号都已爬取完毕, 等待退出 .... |')
        # pprint(response.css('div.WB_innerwrap td.S_line1 strong').extract())

        else:
            home_info = HomeInfoItem()

            # 关注数, 粉丝数, 微博数
            tmp_strong = response.css('div.WB_innerwrap td.S_line1 strong').extract()
            tmp = re.compile(r'<strong .*?>(.*?)</strong>').findall(str(tmp_strong))
            print('*' * 100, tmp)

            '''
            特例微博地址: https://weibo.com/archicreation?refer_flag=1028035010_  链接地址为播客地址，并非主页地址
            '''
            if tmp == []:       # 观察微博号主页发现，没有公开，关注数，粉丝数，微博数
                self.log('=' * 12 + '| 该微博号的关注数, 粉丝数, 微博数返回为空, 爬虫进入短暂睡眠, 即将继续爬取...... |')
                self.log('=' * 12 + '| 原因为该用户未公开相关信息，所以无法爬取 ... |')
                # time.sleep(5)
                care_number = 0
                fans_number = 0
                weibo_number = 0

                home_info['care_number'] = care_number
                home_info['fans_number'] = fans_number
                home_info['weibo_number'] = weibo_number

            else:
                care_number = int(tmp[0])
                fans_number = int(tmp[1])
                weibo_number = int(tmp[2])

            tmp_2 = response.css('div.PCD_person_info').extract_first()
            if tmp_2 == []:
                self.log('=' * 12 + '| 该微博号的未提供 认证等级 相关信息, 爬虫进入短暂睡眠, 即将继续爬取...... |')

                home_info['nick_name'] = self.user_name_and_url[self.index][0]
                home_info['verify_type'] = '该微博未提供相关信息'
                home_info['sina_level'] = 0
                home_info['verify_desc'] = '该微博未提供相关信息'
                home_info['personal_deal_info_url'] = '该微博未提供相关信息'

            else:
                # 认证类型
                # print(response.css('p.verify.clearfix a::attr("href")').extract_first())
                verify_type_url = response.css('p.verify.clearfix a::attr("href")').extract_first()
                self.log('=' * 12 + '| 认证的url为%s |' % verify_type_url)
                if verify_type_url is None:
                    self.log('=' * 12 + '| 该微博号未被认证 |')
                    verify_type = '普通用户, 未认证'
                else:
                    # result = re.compile(r'http://(.*?).verified.weibo.com.*?').findall(verify_type_url)
                    result = re.compile(r'http://(.*?).weibo.com.*?').findall(verify_type_url)[0]
                    if len(result) == 8:
                        verify_type = '个人黄V认证'
                        self.log('=' * 12 + '| 个人黄V认证 |')
                    elif len(result) == 4:
                        verify_type = '微博达人认证'      # 微博达人自2017年5月15日停止申请，达人产品同日下线
                        self.log('=' * 12 + '| 微博达人认证 |')
                    elif len(result) == 16:
                        self.log('=' * 12 + '| 企业蓝V认证 |')
                        verify_type = '企业蓝V认证'

                # 微博等级
                try:
                    level_before = response.css('div.PCD_person_info a.W_icon_level span::text').extract_first()
                    sina_level = int(re.compile(r'Lv.(\d+)').findall(str(level_before))[0])
                except Exception as e:
                    print('-------错误如下：', e)
                    print('-' * 12 + '| 跳过此微博号, 继续下一个爬取..... |')

                    self.index += 1

                    url = self.user_name_and_url[self.index][1]

                    self.log('\n')
                    self.log('=' * 12 + '| 即将开始爬取的微博主页的url为 %s |' % (url,))

                    yield scrapy.Request(url, headers=self.header, cookies=self.cookie, callback=self.parse)


                # 微博认证文字信息
                verify_desc = response.css('div.verify_area p.info span::text').extract_first()
                if verify_desc == '':
                    verify_desc = ''

                tmp_personal_deal_info_url = response.css('div.PCD_person_info a.WB_cardmore::attr("href")').extract_first()

                tmp_url = re.compile(r'//weibo.com/').findall(tmp_personal_deal_info_url)
                if tmp_url == []:
                    personal_deal_info_url = 'https://weibo.com' + tmp_personal_deal_info_url
                else:
                    personal_deal_info_url = 'https:' + tmp_personal_deal_info_url


                self.log('=' * 12 + '| 关注数: %d, 粉丝数: %d, 微博数: %d |' % (care_number, fans_number, weibo_number))
                self.log('=' * 12 + '| 微博等级: %d |' % sina_level)
                self.log('=' * 12 + '| 微博认证文字信息为: %s' % verify_desc)
                self.log('=' * 12 + '| 私人详细信息页: %s' % personal_deal_info_url)

                home_info['nick_name'] = self.user_name_and_url[self.index][0]
                home_info['care_number'] = care_number
                home_info['fans_number'] = fans_number
                home_info['weibo_number'] = weibo_number
                home_info['verify_type'] = verify_type
                home_info['sina_level'] = sina_level
                home_info['verify_desc'] = verify_desc
                home_info['personal_deal_info_url'] = personal_deal_info_url

            self.log('============| 个人主页信息为: ' + str(list(home_info.values())))
            self.log('=' * 12 + '| 微博主页: %s 爬取完毕! |' % (response.url))

            yield home_info

            self.index += 1

            url = self.user_name_and_url[self.index][1]

            self.log('\n')
            self.log('=' * 12 + '| 即将开始爬取的微博主页的url为 %s |' % (url,))

            yield scrapy.Request(url, headers=self.header, cookies=self.cookie, callback=self.parse)

    def get_nick_name_and_url_from_db(self):
        try:
            cs = self.conn.cursor()

            sql = 'select nick_name, nick_name_url from bozhu_user where weibo_number = 0 and nick_name != \"AC建筑创作\" and nick_name != \"iWeekly周末画报\" and nick_name != \"三明中院\" and nick_name != \"中国反邪教\" and nick_name != \"交大有思\" and nick_name != \"今晚80后脱口秀\" and nick_name != \"兰州大学\" and nick_name != \"凤凰周刊\" and nick_name != \"壹读\" and nick_name != \"天气通\" and nick_name != \"太原师范学院微博协会\" and nick_name != \"央广网\" and nick_name != \"山西财经大学微博协会\" and nick_name != \"微博时评\";'
            # sql = 'select nick_name, nick_name_url from bozhu_user where weibo_number = 0;'
            # 更新所有信息
            # sql = 'select nick_name, nick_name_url from bozhu_user where nick_name != \"AC建筑创作\";'
            cs.execute(sql)

            result = cs.fetchall()  # return -> 一个 ((), (), ...)
            # pprint(result)

            cs.close()

            print('=' * 12 + '| 成功获取数据库数据 |')
            return result
        except Exception as e:
            print('=' * 12 + '| 获取数据库数据失败 |')
            return None

    def stringToDict(self, cookies):
        itemDict = {}
        items = cookies.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')  # 记得去除空格
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict



