# coding = utf-8

'''
@author = super_fazai
@File    : zhihu_cookies.py
@Time    : 2017/9/5 20:32
@connect : superonesfazai@gmail.com
'''

import scrapy

class ZhiHuCookieSpider(scrapy.Spider):
    name = 'zhihu_cookies'
    allowed_domains = 'zhihu.com'
    start_urls = [
        'https://www.zhihu.com',
    ]

    cookies = {
        'q_c1': '1fd88b88af4441bb93a78375fe22e6fd|1504614925000|1501937701000',
         '_zap': 'b999064c-19a3-41e9-ac52-56666138f030', 'd_c0': '"AXBCWuToTgyPThCDA_hgX84Qo9ZJBzky6YU',
         'aliyungf_tc': 'AQAAAJYUOSgcXQsAAnCCDi46uAy4lWtV', 'r_cap_id': '"ZGM5MTAxZDlmNDlmNDQ1ODgzOTY4ZjgxYzRlMWQ4Yzc',
         'cap_id': '"ZmQzZTUyZGRiNGU4NDM4NDhhZDU3ZTE5YTczMjZkZDA',
         '__utma': '51854390.121838955.1504614940.1504614940.1504614940.1', '__utmb': '51854390.0.10.1504614940',
         '__utmc': '51854390', '__utmz': '51854390.1504614940.1.1.utmcsr', '__utmv': '51854390.000--|3',
         'z_c0': 'Mi4xdTRfRUF3QUFBQUFCY0VKYTVPaE9EQmNBQUFCaEFsVk51U2ZXV1FBZ1ZNY2pENnlMSkJXUkstY1diMVl0WVVxcU93|1504615097|c3abb993ce4fb4dc809510844b87fd3d7e966d09',
         '_xsrf': 'bec8863b-3438-4b3b-a4a1-4fceb656cb27'
    }

    headers = {
        'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    }

    def start_requests(self):
        yield scrapy.FormRequest(url=self.start_urls[0], headers=self.headers, cookies=self.cookies, callback=self.parse_page)

    def parse_page(self, response):
        print('-' * 30, response.url)
        with open('zhihu.html', 'w', encoding='utf-8') as file:
            file.write(response.body.decode('utf-8'))

