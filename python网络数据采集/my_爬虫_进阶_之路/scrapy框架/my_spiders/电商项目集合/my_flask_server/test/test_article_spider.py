# coding:utf-8

'''
@author = super_fazai
@File    : test_article_spider.py
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from article_spider import ArticleParser
from multiprocessing import Pool
from fzutils.spider.async_always import *

def worker(target_url,):
    loop = get_event_loop()
    article_parser = ArticleParser()
    res = loop.run_until_complete(article_parser._parse_article(
        article_url=target_url,
    ))

    return res

def main():
    process_num = 4
    pool = Pool(process_num)
    # target_url = 'https://haokan.baidu.com/v?vid=17448170737812377575&tab=shishang'
    target_url = 'https://www.meipai.com/media/1131644923'
    target_url_list = [target_url for i in range(0, process_num)]

    for item in target_url_list:
        pool.apply_async(
            func=worker,
            args=[
                item,
            ],)
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()