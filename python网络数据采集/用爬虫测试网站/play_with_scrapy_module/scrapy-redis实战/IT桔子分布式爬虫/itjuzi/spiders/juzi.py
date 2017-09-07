# coding = utf-8

'''
@author = super_fazai
@File    : juzi.py
@Time    : 2017/9/7 21:48
@connect : superonesfazai@gmail.com
'''

"""
运行:
    Slave端：
    scrapy runspider juzi.py
    
    Master端：
    redis-cli > lpush itjuzispider:start_urls http://www.itjuzi.com/company
"""

from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_redis.spiders import RedisCrawlSpider
from ..items import CompanyItem

class ITjuziSpider(RedisCrawlSpider):
    name = 'itjuzi'
    allowed_domains = ['www.itjuzi.com']
    # start_urls = ['http://www.itjuzi.com/company']
    redis_key = 'itjuzispider:start_urls'
    rules = [
        # 获取每一页的链接
        Rule(link_extractor=LinkExtractor(allow=('/company\?page=\d+'))),
        # 获取每一个公司的详情
        Rule(link_extractor=LinkExtractor(allow=('/company/\d+')), callback='parse_item')
    ]

    def parse_item(self, response):
        soup = BeautifulSoup(response.body, 'lxml')

        # 开头部分： //div[@class="infoheadrow-v2 ugc-block-item"]
        cpy1 = soup.find('div', class_='infoheadrow-v2')
        if cpy1:
            # 公司名称：//span[@class="title"]/b/text()[1]
            company_name = cpy1.find(class_='title').b.contents[0].strip().replace('\t', '').replace('\n', '')

            # 口号： //div[@class="info-line"]/p
            slogan = cpy1.find(class_='info-line').p.get_text()

            # 分类：子分类//span[@class="scope c-gray-aset"]/a[1]
            scope_a = cpy1.find(class_='scope c-gray-aset').find_all('a')
            # 分类：//span[@class="scope c-gray-aset"]/a[1]
            scope = scope_a[0].get_text().strip() if len(scope_a) > 0 else ''
            # 子分类：# //span[@class="scope c-gray-aset"]/a[2]
            sub_scope = scope_a[1].get_text().strip() if len(scope_a) > 1 else ''

            # 城市+区域：//span[@class="loca c-gray-aset"]/a
            city_a = cpy1.find(class_='loca c-gray-aset').find_all('a')
            # 城市：//span[@class="loca c-gray-aset"]/a[1]
            city = city_a[0].get_text().strip() if len(city_a) > 0 else ''
            # 区域：//span[@class="loca c-gray-aset"]/a[2]
            area = city_a[1].get_text().strip() if len(city_a) > 1 else ''

            # 主页：//a[@class="weblink marl10"]/@href
            home_page = cpy1.find(class_='weblink marl10')['href']
            # 标签：//div[@class="tagset dbi c-gray-aset"]/a
            tags = cpy1.find(class_='tagset dbi c-gray-aset').get_text().strip().strip().replace('\n', ',')

        #基本信息：//div[@class="block-inc-info on-edit-hide"]
        cpy2 = soup.find('div', class_='block-inc-info on-edit-hide')
        if cpy2:

            # 公司简介：//div[@class="block-inc-info on-edit-hide"]//div[@class="des"]
            company_intro = cpy2.find(class_='des').get_text().strip()

            # 公司全称：成立时间：公司规模：运行状态：//div[@class="des-more"]
            cpy2_content = cpy2.find(class_='des-more').contents

            # 公司全称：//div[@class="des-more"]/div[1]
            company_full_name = cpy2_content[1].get_text().strip()[len('公司全称：'):] if cpy2_content[1] else ''

            # 成立时间：//div[@class="des-more"]/div[2]/span[1]
            found_time = cpy2_content[3].contents[1].get_text().strip()[len('成立时间：'):] if cpy2_content[3] else ''

            # 公司规模：//div[@class="des-more"]/div[2]/span[2]
            company_size = cpy2_content[3].contents[3].get_text().strip()[len('公司规模：'):] if cpy2_content[3] else ''

            #运营状态：//div[@class="des-more"]/div[3]
            company_status = cpy2_content[5].get_text().strip() if cpy2_content[5] else ''

        # 主体信息：
        main = soup.find('div', class_='main')

        # 投资情况：//table[@class="list-round-v2 need2login"]
          # 投资情况，包含获投时间、融资阶段、融资金额、投资公司
        tz = main.find('table', 'list-round-v2')
        tz_list = []
        if tz:
            all_tr = tz.find_all('tr')
            for tr in all_tr:
                tz_dict = {}
                all_td = tr.find_all('td')
                tz_dict['tz_time'] = all_td[0].span.get_text().strip()
                tz_dict['tz_round'] = all_td[1].get_text().strip()
                tz_dict['tz_finades'] = all_td[2].get_text().strip()
                tz_dict['tz_capital'] = all_td[3].get_text().strip().replace('\n', ',')
                tz_list.append(tz_dict)

        # 团队信息：成员姓名、成员职称、成员介绍
        tm = main.find('ul', class_='list-prodcase limited-itemnum')
        tm_list = []
        if tm:
            for li in tm.find_all('li'):
                tm_dict = {}
                tm_dict['tm_m_name'] = li.find('span', class_='c').get_text().strip()
                tm_dict['tm_m_title'] = li.find('span', class_='c-gray').get_text().strip()
                tm_dict['tm_m_intro'] = li.find('p', class_='mart10 person-des').get_text().strip()
                tm_list.append(tm_dict)

        # 产品信息：产品名称、产品类型、产品介绍
        pdt = main.find('ul', class_='list-prod limited-itemnum')
        pdt_list = []
        if pdt:
            for li in pdt.find_all('li'):
                pdt_dict = {}
                pdt_dict['pdt_name'] = li.find('h4').b.get_text().strip()
                pdt_dict['pdt_type'] = li.find('span', class_='tag yellow').get_text().strip()
                pdt_dict['pdt_intro'] = li.find(class_='on-edit-hide').p.get_text().strip()
                pdt_list.append(pdt_dict)

        item = CompanyItem()
        item['info_id'] = response.url.split('/')[-1:][0]
        item['company_name'] = company_name
        item['slogan'] = slogan
        item['scope'] = scope
        item['sub_scope'] = sub_scope
        item['city'] = city
        item['area'] = area
        item['home_page'] = home_page
        item['tags'] = tags
        item['company_intro'] = company_intro
        item['company_full_name'] = company_full_name
        item['found_time'] = found_time
        item['company_size'] = company_size
        item['company_status'] = company_status
        item['tz_info'] = tz_list
        item['tm_info'] = tm_list
        item['pdt_info'] = pdt_list
        return item