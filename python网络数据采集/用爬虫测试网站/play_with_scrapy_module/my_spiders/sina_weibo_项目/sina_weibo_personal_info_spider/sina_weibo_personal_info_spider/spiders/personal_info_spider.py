# -*- coding: utf-8 -*-
import scrapy
from MySQLdb import *
from ..items import PersonalDealInfoItem, CompanyDealInfoItem
from pprint import pprint
import re
from ..settings import COOKIES
from ..settings import HEADERS
from ..tools.cookies_to_dict import stringToDict
from ..tools.filter_emoji_str import filter_emoji_str
from time import sleep

class PersonalInfoSpiderSpider(scrapy.Spider):
    name = 'personal_info_spider'
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

        # 测试通过
        # first_url = 'https://weibo.com/p/1005051756788837/info?mod=pedit_more'      # 特殊, 一个a标签直接属于li标签, 所以报索引异常

        # first_url = 'https://weibo.com/p/1005055774988006/info?mod=pedit_more'      # 用于筛选教育年份和工作年份
        # first_url = 'https://weibo.com/p/1035051926515457/info?mod=pedit_more'      # 测试工作信息

        # 这个有多个工作信息
        # first_url = 'http://weibo.com/p/1005051663765234/info?mod=pedit_more'         # 测试多层嵌套的信息, 如工作信息里的三层：就业公司, 地区, 岗位(后两个位置可以交换)

        # first_url = 'https://weibo.com/p/1005052689645383/info?mod=pedit_more'     # 测试大学第一个br前包含<a></a>, 试着过滤他
        # first_url = 'https://weibo.com/1752825395/about'

        ## 如果报错 ：IndexError: tuple index out of range ，说明数据库取出的nick_name都已经爬取完毕
        yield scrapy.Request(url=first_url, headers=self.header, cookies=self.cookie, callback=self.parse)

    def parse(self, response):
        '''
        个人微博号私人信息抓取
        :param response:
        :return:
        '''
        personal_deal_info = PersonalDealInfoItem()
        self.log('-' * 12 + '| 这是个人微博号, 个人信息页地址为: %s |' % response.url)

        # 个人微博与企业微博共有相似信息, 下面是其中的关键字
        # (medal_info, sina_level, sina_level_exp,
        # vip_icon, vip_group_speed, vip_group_value)
        the_same_info = self.get_the_same_info(response)

        # 阳光信用
        credit_value = ''
        credit_box = response.css('div.credit_wrap_box').extract()
        if credit_box:
            tmp_credit_value = response.css('div.credit_wrap_box div.radius_min_box.radiusDifferent p::text').extract()
            if tmp_credit_value:
                credit_value = response.css('div.credit_wrap_box div.radius_min_box.radiusDifferent p::text').extract()[1]
                self.log('-' * 12 + '| 阳光信用度：%s |' % credit_value)
            else:
                credit_value = response.css('div.credit_wrap_box div.radius_min_box p::text').extract()[0]
                self.log('-' * 12 + '| 阳光信用度：%s |' % credit_value)

        '''
        右侧详细信息页
        '''
        all_right_info = self.get_all_right_info(response)

        personal_deal_info['nick_name'] = self.personal_deal_info_from_db[self.index][0]

        personal_deal_info['medal_info'] = the_same_info['medal_info']
        personal_deal_info['sina_level'] = the_same_info['sina_level']
        personal_deal_info['sina_level_exp'] = the_same_info['sina_level_exp']
        personal_deal_info['vip_icon'] = the_same_info['vip_icon']
        personal_deal_info['vip_group_speed'] = the_same_info['vip_group_speed']
        personal_deal_info['vip_group_value'] = the_same_info['vip_group_value']
        personal_deal_info['credit_value'] = credit_value

        # 先赋初始值, 下面再进行筛选
        personal_deal_info['true_name'] = ''
        personal_deal_info['live_place'] = ''
        personal_deal_info['sex'] = ''
        personal_deal_info['love_man_or_woman'] = ''
        personal_deal_info['feeling'] = ''
        personal_deal_info['birthday'] = ''
        personal_deal_info['blood_type'] = ''
        personal_deal_info['blog_url'] = ''
        personal_deal_info['simple_desc'] = ''
        personal_deal_info['individuality_url'] = ''
        personal_deal_info['register_time'] = ''
        personal_deal_info['_email'] = ''
        personal_deal_info['qq'] = ''
        personal_deal_info['msn'] = ''
        personal_deal_info['company'] = ''
        personal_deal_info['edu'] = ''  # 避免在里面报错
        personal_deal_info['_label'] = ''

        for key in all_right_info.keys():
            if key == '真实姓名：':
                personal_deal_info['true_name'] = all_right_info['真实姓名：']

            if key == '所在地：':
                # print(all_right_info['所在地：'])
                personal_deal_info['live_place'] = all_right_info['所在地：']
                # print(personal_deal_info['live_place'])

            if key == '性别：':
                personal_deal_info['sex'] = all_right_info['性别：']

            if key == '性取向：':
                personal_deal_info['love_man_or_woman'] = all_right_info['性取向：']

            if key == '感情状况：':
                personal_deal_info['feeling'] = all_right_info['感情状况：']

            if key == '生日：':
                personal_deal_info['birthday'] =  all_right_info['生日：']

            if key == '血型：':
                personal_deal_info['blood_type'] = all_right_info['血型：']

            if key == '博客：':
                personal_deal_info['blog_url'] = all_right_info['博客：']

            if key == '简介：':
                personal_deal_info['simple_desc'] = filter_emoji_str(all_right_info['简介：'])

            if key == '个性域名：':
                personal_deal_info['individuality_url'] = all_right_info['个性域名：']

            if key == '注册时间：':
                personal_deal_info['register_time'] = all_right_info['注册时间：']

            if key == '邮箱：':
                personal_deal_info['_email'] = all_right_info['邮箱：']

            if key == 'QQ：':
                personal_deal_info['qq'] = all_right_info['QQ：']

            if key == 'MSN：':
                personal_deal_info['msn'] = all_right_info['MSN：']

            if key == '公司：':
                personal_deal_info['company'] = all_right_info['公司：']

            if key == '大学：':
                personal_deal_info['edu'] += '大学: ' + all_right_info['大学：'] + ', '

            if key == '高中：':
                personal_deal_info['edu'] += '高中:' + all_right_info['高中：'] + ', '

            if key == '初中：':
                personal_deal_info['edu'] += '初中：' + all_right_info['初中：'] + ', '

            if key == '小学：':
                personal_deal_info['edu'] += '小学: ' + all_right_info['小学：'] + ', '

            if key == '：':      # 大学的特殊情况
                personal_deal_info['edu'] += '：' + all_right_info['：'] + ', '

            if key == '标签：':
                personal_deal_info['_label'] = all_right_info['标签：']

        self.log('-' * 12 + '| 该个人微博信息爬取完成, 即将开始下一个微博号爬取 |')

        # pprint(dict(personal_deal_info))
        print('*' * 60 + '| 爬取到的该微博号的信息如下: |')
        pprint(personal_deal_info)
        print('*' * 60)

        yield personal_deal_info
        self.index += 1

        url = self.personal_deal_info_from_db[self.index][1]
        # print(url)
        if url is None:
            print('*' * 100 + '  给与的url为空, 跳过这个url开始下一个爬取')
            self.index += 1
            url = self.personal_deal_info_from_db[self.index][1]

        yield scrapy.Request(url=url, headers=self.header, cookies=self.cookie, callback=self.parse)

    def get_the_same_info(self, response):
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

    def get_all_right_info(self, response):
        '''
        个人微博右边主要信息处理
        :param response:
        :return:
        '''
        all_right_info = {}

        # 标题名字
        title_list = response.css('div.m_wrap.clearfix ul.clearfix li span.pt_title::text').extract()
        pprint(title_list)
        # 标题对应信息
        tmp_info_list = response.css('div.m_wrap.clearfix ul.clearfix li span.pt_detail').extract()
        # print(tmp_info_list)

        # # 判断是否博客key标签下，有a标签只属于li标签，作为特殊处理
        # if response.css('div.m_wrap.clearfix ul.clearfix li > a').extract():
        #     blog_url = response.css('div.m_wrap.clearfix ul.clearfix li > a::text').extract()[0]

        info_list = []
        # 数据清洗
        for item in tmp_info_list:
            item = item.replace(' ', '|')  # 先把空格替换成'|', 然后待替换完，再替换回去
            item = re.compile('\s+').sub('', item)
            item = item.replace('|', ' ')
            # print(item)
            item = re.compile(r'<span class="pt_detail">(.*?)</span>').findall(item)[0]

            # 用于判断提取个性域名, 以及处理多成的工作信息和学校信息
            is_a_label = re.compile('<a .*?>.*?</a>').findall(item)
            if is_a_label:
                item1 = re.compile(r'<a href=.*?>(.*?)</a>').findall(item)[0]
                # 筛选读书年份
                # 提取第一个br标签内容   -- 年份
                item4 = ''  # 避免报错
                is_br_label = re.compile(r'<a href="http://s.weibo.com/.*?>.*?</a>(.*?)<br>').findall(item)
                if is_br_label != []:
                    item2 = re.compile(r'<a .*?>.*?</a>(.*?)<br>').findall(item)[0]
                    # print(item2)
                    item2 = re.compile(r'<a .*?>.*?</a>').sub('', item2)
                    # 提取第二个br标签内容   -- 就业职位, 也可能是地区,  也可能是学院信息, 如法学院
                    is_br_label2 = re.compile(r'<a href="http://s.weibo.com/.*?>.*?</a>.*?<br>(.*?)<br>').findall(item)
                    if is_br_label2 != []:
                        item3 = re.compile(r'<a .*?>.*?</a>.*?<br>(.*?)<br>').findall(item)[0]
                        item3 = re.compile(r'<a .*?>.*?</a>').sub('', item3)    # 此处过滤a标签的链接
                        # 提取第三个br标签内容   -- 可能是 就业职位, 也可能是 地区
                        is_br_label3 = re.compile(r'<a href="http://s.weibo.com/.*?>.*?</a>.*?<br>.*?<br>(.*?)<br>').findall(item)
                        if is_br_label3 != []:
                            item4 = re.compile(r'<a .*?>.*?</a>.*?<br>.*?<br>(.*?)<br>').findall(item)[0]
                            item4 = re.compile(r'<a .*?>.*?</a>').sub('', item3)    # 过滤a 标签
                        else:
                            item4 = ''
                    else:
                        item3 = ''
                    # item3 = ''
                else:
                    item2 = ''
                    item3 = ''
                    item4 = ''
                item = item1 + item2 + item3 + item4
            info_list.append(item)

        # print(info_list)

        is_company_span = response.css('div.WB_frame_c div.WB_innerwrap li span.pt_title::text').extract()
        # print(is_company_span)
        if is_company_span:  # 先判断是否有右侧栏信息
            if is_company_span[0] == '公司：':
                print('进入公司test')
                #   还未写处理多个公司的代码

            else:
                pass

        # 判断是否博客key标签下，有a标签只属于li标签，作为特殊处理
        if response.css('div.m_wrap.clearfix ul.clearfix li > a').extract():
            blog_url = response.css('div.m_wrap.clearfix ul.clearfix li > a::text').extract()[0]
            # print('--------------测试博客: ', blog_url)
        else:
            blog_url = ''

        # 针对处理由于博客存在：导致title_list和info_list长度不同的正确合并
        for index in range(0, len(title_list)):     # 在与title_list对应位置, 插入博客信息
            if title_list[index] == '博客：':
                info_list.insert(index, blog_url)
        # print(info_list)

        for index in range(0, len(title_list)):
            all_right_info[title_list[index]] = info_list[index]
        # pprint(all_right_info)

        # 单独处理易错元素
        for key in all_right_info.keys():
            if key == '标签：':        # 标签
                all_right_info['标签：'] = response.css('div.m_wrap.clearfix ul.clearfix li span.pt_detail a.W_btn_tag::text').extract()
                tmp_label_list = []
                for item in all_right_info['标签：']:
                    item = re.compile(r'\s+').sub('', item)
                    tmp_label_list.append(item)

                for item in tmp_label_list:     # 去除空值
                    if item == '':
                        tmp_label_list.remove(item)
                all_right_info['标签：'] = ', '.join(tmp_label_list)

            if key == '：' or key == '大学：':
                had_text_in = response.css('div.m_wrap.clearfix ul.clearfix li span.pt_detail')

        # print('-' * 50)
        # pprint(all_right_info)
        # print('-' * 50)
        return all_right_info


    def get_nick_name_and_personal_deal_info_url(self):
        try:
            cs = self.conn.cursor()

            # 只提取个人
            sql = 'select nick_name, personal_deal_info_url from bozhu_user where bozhu_user.nick_name not in (select nick_name from personal_deal_info) and bozhu_user.nick_name not in (select nick_name from company_deal_info) and bozhu_user.verify_type != \"企业蓝V认证\" and bozhu_user.nick_name != \"_可口可心\" and bozhu_user.nick_name != \"-_KEI_-\" and bozhu_user.nick_name != \"0511天蝎\" and bozhu_user.personal_deal_info_url != \"https://weibo.comjavascript:;\";'
            cs.execute(sql)

            result = cs.fetchall()  # return -> 一个 ((), (), ...)
            cs.close()

            print('=' * 12 + '| 成功获取数据库数据 |')
            return result
        except Exception as e:
            print('=' * 12 + '| 获取数据库数据失败 |')
            return None
