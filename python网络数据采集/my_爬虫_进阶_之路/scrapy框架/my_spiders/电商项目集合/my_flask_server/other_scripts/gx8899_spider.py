# coding:utf-8

'''
@author = super_fazai
@File    : gx8899_spider.py
@Time    : 2018/8/23 10:40
@connect : superonesfazai@gmail.com
'''

"""
个性8899头像网
    gx8899.com

旨在: 替换掉原先db中的卡通头像
"""

import sys
sys.path.append('..')

import gc
from scrapy.selector import Selector
from asyncio import get_event_loop
import re
from pprint import pprint
from time import sleep
from random import randint

from settings import (
    MY_SPIDER_LOGS_PATH,
    PHANTOMJS_DRIVER_PATH,
    IP_POOL_TYPE,)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from fzutils.spider.fz_aiohttp import AioHttp
from fzutils.spider.fz_phantomjs import BaseDriver
from fzutils.internet_utils import get_random_pc_ua
from fzutils.time_utils import (
    get_shanghai_time,
    fz_set_timeout,)
from fzutils.spider.crawler import Crawler

class GX8899Spider(Crawler):
    def __init__(self, logger=None):
        super(GX8899Spider, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/gx8899/_/',
            
            is_use_driver=True,
            driver_executable_path=PHANTOMJS_DRIVER_PATH
        )
        self._set_sort_type_name()
        self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
        self.update_sql = 'update dbo.sina_weibo set head_img_url=%s, modify_time=%s where id=%s'
        self.id_list = []
        self.update_index = 0

    def _set_sort_type_name(self):
        '''
        设置抓取的分类名
        :return:
        '''
        self.sort_type_name_list = [
            # 'weixin',
            # 'nansheng',
            # 'nvsheng',
            'fengjing',
            'jingxuan',
            'wupin',
            'oumei',
            'weimei',
            'heibai',
            'baqi',
            'xiaoqingxin',
            'yijing',
            'beiying',
            'chouyan',
            'sumiao',
            'gexing',
            'xiaohai',
            'qiche',
            'zhiwu',
            'shouhui',
            'weshen',
            'mingxing',
            'jianzhu',
            'renwu',
        ]

    def _get_gx8899_all_img_url(self):
        self.lg.info('即将开始采集gx8899...')
        fz = []
        for sort_type_name in self.sort_type_name_list:
            tmp = self._get_one_sort_type_name_page_info(sort_type_name)
            if tmp != []:
                fz += tmp

        self.lg.info('@@@ 全部头像抓取完毕!')
        self.fz = fz

        return fz

    def _get_new_wait_2_handle_id_list(self):
        '''
        获取新的带处理的
        :return:
        '''
        sql_str = '''
        select top 1000 id 
        from dbo.sina_weibo
        where sina_type = 'bilibili' and modify_time is null
        '''
        if self.id_list == []:
            self.lg.info('@@@ 重新获取id_list...')
            self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
            try:
                wait = self.my_pipeline._select_table(sql_str=sql_str)
                self.id_list = [i[0] for i in wait]
            except TypeError or IndexError:
                sleep(8)
                return []
        else:
            pass

        return self.id_list

    @fz_set_timeout(6)
    def oo(self, id, img_url):
        try:
            self.my_pipeline._update_table_2(
                sql_str=self.update_sql,
                params=(img_url, get_shanghai_time(), id),
                logger=self.lg
            )
        except Exception:
            return False
        return True

    def _get_one_sort_type_name_page_info(self, sort_type_name):
        '''
        得到一个分类的某页信息
        :return:
        '''
        base_url = 'http://m.gx8899.com/{0}/'.format(sort_type_name)
        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Referer': 'http://m.gx8899.com/weixin/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        index = 0
        res = []
        while True:
            if index == 0:
                url = base_url
                index += 1  # 第二页index_2开始
            else:
                url = base_url + 'index_{0}.html'.format(index)

            self.lg.info('正在抓取{0}'.format(url))
            # 太慢, 改用phantomjs
            # body = self._get_loop_run_result(url=url, headers=headers)

            if index % 15 == 0:
                try:
                    del self.driver
                except:
                    pass
                gc.collect()
                self.driver = BaseDriver(executable_path=PHANTOMJS_DRIVER_PATH, logger=self.lg, ip_pool_type=self.ip_pool_type)
                self.lg.info('[+] phantomjs已重置!')

            body = self.driver.use_phantomjs_to_get_url_body(url=url)
            # self.lg.info(str(body))
            if re.compile(r'<title>404 - 找不到文件或目录。</title>').findall(body) != []:
                break

            need = Selector(text=body).css('div#con_tabone_1 li.last a:last-child ::attr(href)').extract()
            pprint(need)
            if need == []:
                self.lg.error('获取到的need为空list!出错地址:{0}'.format(url))
                continue

            for article_url in need:
                _ = self._get_one_article_page_info(article_url)
                if _ != []:
                    res += _

                self.lg.info('#### 已更新{0}个id !'.format(self.update_index))

            index += 1

        return res

    def _get_one_article_page_info(self, url):
        '''
        得到一个推荐地址里面所有图片list
        :param url:
        :return:
        '''
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        # body = self._get_loop_run_result(url=url, headers=headers)
        body = self.driver.use_phantomjs_to_get_url_body(url=url)
        if body == '':
            self.lg.info('获取到img list为空list!出错地址:{}'.format(url))
            return []

        need = Selector(text=body).css('div.content p img ::attr(src)').extract()
        # pprint(need)
        # self.lg.info(str(need))
        if need != []:
            self.lg.info('[+] crawl子地址success')
        else:
            self.lg.info('[-] crawl子地址fail')

        # 数据更新操作
        for img_url in need:
            try:
                random_id_index = randint(0, len(self._get_new_wait_2_handle_id_list())-1)
            except:
                sleep(5)
                continue
            res = self.oo(
                id=self.id_list[random_id_index],
                img_url=img_url,
            )
            if res:
                self.id_list.pop(random_id_index)
                self.update_index += 1

        return need

    async def _get_one_page_body(self, url, headers):
        '''
        异步获取body
        :param url:
        :param headers:
        :return:
        '''
        body = await AioHttp.aio_get_url_body(url=url, headers=headers, ip_pool_type=self.ip_pool_type)

        return body

    def _get_loop_run_result(self, **kwargs):
        loop = get_event_loop()
        result = loop.run_until_complete(self._get_one_page_body(
            url=kwargs.get('url', ''),
            headers=kwargs.get('headers', {})
        ))

        return result

    def __del__(self):
        try:
            del self.driver
            del self.lg
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    gx = GX8899Spider()
    # gx._get_one_sort_type_name_page_info('weixin')

    # url = 'http://m.gx8899.com/touxiang/151502.html'
    # gx._get_one_article_page_info(url)

    gx._get_gx8899_all_img_url()