# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
#from urllib import parse  #python3
import urlparse  #python2

from AtricleSpider.items import JobBoleArticleItem
from AtricleSpider.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        1. 获取文章列表页中文章的url并交给scrapy下载后并进行解析
        2. 获取下一页的url并交给scrapy进行下载,下载完成后交给parse
        '''

        #获取文章列表页中文章的url并交给scrapy下载后并进行解析
        #a::attr(href)表示获取到a标签的href属性的值
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            image_url = post_node.css('img::attr(src)').extract_first('').encode('utf-8')
            post_url = post_node.css('::attr(href)').extract_first('').encode('utf-8')
            #前面加yield即自动交给url进行下载
            #urlparse.urljoin(response.url, post_url)  的作用如果post_url没有域名,就加上response.url的父域名,从而避免出错
            yield Request(url=urlparse.urljoin(response.url, post_url), meta={'front_image_url':image_url}, callback=self.parse_detail)

        #提取下一页并交给scrapy进行下载
        #css选择器中选择筛选一个class有多个名字,只需要写成eg: .css('.next.page-numbers')
        next_urls = response.css('.next.page-numbers::attr(href)').extract_first('')
        if next_urls:
            yield Request(url=urlparse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem() #实例化一个对象
        #提取文章的具体字段

        #re_selector = response.xpath('/html/body/div[3]/div[3]/div[1]/div[1]')
        #re_selector = response.xpath('//*[@id="post-111541"]/div[1]/h1/text()')
        #front_image_url = response.mate['front_image_url']
        #为了保险起见不用上面的方法,而改用get方法获取不会抛异常
        front_image_url = response.meta.get('front_image_url', '')  #文章封面图
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('').encode('utf-8')
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().encode(
            'utf-8').replace(' \xc2\xb7', '')  #strip()去空格和去换行 extract()为转换成数组,然后可以通过索引值访问
        #当一个class有多个名字的时候找唯一的那个,然后用contains(@class, 'str')来筛选
        praise_nums = int(response.xpath("//span[contains(@class,'vote-post-up')]/h10[1]/text()").extract()[0].encode('utf-8'))

        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0].encode('utf-8')
        match_re = re.match('.*?(\d+).*', fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0].encode('utf-8')
        match_re = re.match('.*?(\d+).*', comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0

        content = response.xpath('//div[@class="entry"]').extract()[0]
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().encode(
            'utf-8').replace(' \xc2\xb7', '')

        tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        #去重,去评论
        tag_list = [element for element in tag_list if not element.strip().encode('utf-8').endswith('评论')]
        tags = ','.join(tag_list).encode('utf-8')

        article_item['url_object_id'] = get_md5(response.url)  #用md5编码使其变为固定长度
        article_item['title'] = title
        try:
            create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()
        except Exception as e:
            create_date = datetime.datetime.now()
        article_item['create_date'] = create_date
        article_item['url'] = response.url
        article_item['front_image_url'] = [front_image_url]  #因为setting.py中的IMAGES_URLS_FIELD默认把传入的数值当成数组处理,为了避免错误,要把传入的front_image_url以数组的形式传入
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['tags'] = tags
        article_item['content'] = content

        yield article_item

        '''
        #通过css选择器提取字段
        title = response.css('.entry-header h1::text').extract()
        create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().encode('utf-8').replace(' \xc2\xb7', '')
        praise_nums = response.css('.vote-post-up h10::text').extract()

        fav_nums = response.css('.bookmark-btn::text').extract()[0].strip()
        match_re = re.match('.*?(\d+).*', fav_nums)
        if match_re:
            fav_nums = match_re.group(1)

        comment_nums = response.css('a[href="#article-comment"] span::text').extract()[0].strip()
        match_re = re.match('.*?(\d+).*', comment_nums)
        if match_re:
            comment_nums = match_re.group(1)

        content = response.xpath('div.entry').extract()[0]
        create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().encode('utf-8').replace(
            ' \xc2\xb7', '')

        tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        # 去重,去评论
        tag_list = [element for element in tag_list if not element.strip().encode('utf-8').endswith('评论')]
        tags = ','.join(tag_list)
        '''
