# coding:utf-8

'''
@author = super_fazai
@File    : spider_items.py
@connect : superonesfazai@gmail.com
'''

from scrapy.item import Item
from scrapy import Field

class CompanyItem(Item):
    """企业 or 商铺对象"""
    province_id = Field()           # 省份id
    city_id = Field()               # city id
    unique_id = Field()             # 企业唯一的id
    company_url = Field()           # 企业信息的url
    company_link = Field()          # 企业的官网网址
    company_status = Field()        # 企业状态
    company_name = Field()          # 企业名称
    legal_person = Field()          # 法人
    phone = Field()                 # 电话
    email_address = Field()         # 企业邮箱
    address = Field()               # 企业地址
    brief_introduction = Field()    # company简介
    business_range = Field()        # 经营范围
    founding_time = Field()         # 成立时间
    create_time = Field()           # 记录创建时间点
    site_id = Field()               # 采集源
    employees_num = Field()         # 员工人数
    type_code = Field()             # 公司 or 商品分类的code
    lng = Field()                   # 经度
    lat = Field()                   # 纬度