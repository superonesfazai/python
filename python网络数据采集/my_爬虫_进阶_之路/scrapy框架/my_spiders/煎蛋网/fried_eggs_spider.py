# coding:utf-8

'''
@author = super_fazai
@File    : fried_eggs_spider.py
@connect : superonesfazai@gmail.com
'''

import re
from scrapy.selector import Selector
from pprint import pprint
from fzutils.spider.fz_requests import Requests
from fzutils.internet_utils import get_random_pc_ua

class FriedEggsSpider(object):
    """煎蛋网spider"""
    def __init__(self):
        pass

    def _get_one_page_articles(self, page_num) -> list:
        '''
        得到一个页面的所有文章
        :return:
        '''
        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://jandan.net/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        url = 'http://jandan.net/page/{}'.format(page_num)
        body = Requests.get_url_body(url=url, headers=headers)
        # print(body)
        if body == '':
            return []

        part = list(Selector(text=body).css('div.post.f.list-post').extract())
        # pprint(part)
        _ = []
        for item in part:
            try:
                title = Selector(text=item).css('div.indexs h2 a ::text').extract_first() or ''
                assert title != '', '获取到的title为空值!'
                author = Selector(text=item).css('div.time_s a ::text').extract_first() or ''
                assert author != '', '获取到的author为空值!'
                tag = Selector(text=item).css('div.time_s strong a ::text').extract_first() or ''
                assert tag != '', '获取到的tag为空值!'
                img = Selector(text=item).css('div.thumbs_b a img ::attr("src")').extract_first() or ''
                img = 'http:' + img if img != '' else ''
                try:
                    comment_num = int(Selector(text=item).css('div.indexs span ::text').extract_first())
                except TypeError:
                    comment_num = 0
                # print(comment_num)
                sub_title = re.compile('<div class=\"indexs\">.*?</div>.*?</div>').findall(item)[0].replace('\n', '').replace(' ', '')
            except (AssertionError, IndexError, Exception) as e:
                print(e)
                continue

            _.append({
                'title': title,
                'author': author,
                'tag': tag,
                'img': img,
                'comment_num': comment_num,
                'sub_title': sub_title,
            })

        return _

    def _crawl_all_latest_articles(self):
        '''
        抓取所有最新的新鲜事
        :return:
        '''
        all = []
        for page_num in range(1, 2500):
            one_res = self._get_one_page_articles(page_num)
            # pprint(one_res)
            all += one_res
            label = '+' if one_res != [] else '-'
            print('[{}] 第{}页...'.format(label, page_num))

        return all

if __name__ == '__main__':
    _ = FriedEggsSpider()
    _._crawl_all_latest_articles()