# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaWeiboPersonalInfoSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PersonalDealInfoItem(scrapy.Item):
    # 昵称
    nick_name = scrapy.Field()
    # 真实姓名
    true_name = scrapy.Field()
    # 所在地
    live_place = scrapy.Field()
    # 性别
    sex = scrapy.Field()
    # 性取向
    love_man_or_woman = scrapy.Field()
    # 感情状况
    feeling = scrapy.Field()
    # 生日
    birthday = scrapy.Field()
    # 血型
    blood_type = scrapy.Field()
    # 博客地址
    blog_url = scrapy.Field()
    # 简介
    simple_desc = scrapy.Field()
    # 个性域名
    individuality_url = scrapy.Field()
    # 注册时间
    register_time = scrapy.Field()
    # 邮箱
    _email = scrapy.Field()
    # QQ
    qq = scrapy.Field()
    # MSN
    msn = scrapy.Field()
    # 公司
    company = scrapy.Field()
    # 大学
    edu = scrapy.Field()
    # 标签
    _label = scrapy.Field()

    # 勋章信息
    medal_info = scrapy.Field()
    # 等级信息
    # 微博等级
    sina_level = scrapy.Field()
    # 当前微博经验值
    sina_level_exp = scrapy.Field()

    # 会员信息
    # 会员图标
    vip_icon = scrapy.Field()
    # 会员成长速度
    vip_group_speed = scrapy.Field()
    # 会员成长值
    vip_group_value = scrapy.Field()

    # 阳光信用
    credit_value = scrapy.Field()

class CompanyDealInfoItem(scrapy.Item):
    # 昵称
    nick_name = scrapy.Field()
    # 简介
    simple_desc = scrapy.Field()
    # 联系人
    company_contact_name = scrapy.Field()
    # 电话
    company_phone = scrapy.Field()
    # 友情链接
    friend_url = scrapy.Field()

    # 勋章信息
    medal_info = scrapy.Field()

    # 等级信息
    # 微博等级
    sina_level = scrapy.Field()
    # 当前微博经验值
    sina_level_exp = scrapy.Field()

    # 会员信息
    # 会员图标
    vip_icon = scrapy.Field()
    # 会员成长速度
    vip_group_speed = scrapy.Field()
    # 会员成长值
    vip_group_value = scrapy.Field()