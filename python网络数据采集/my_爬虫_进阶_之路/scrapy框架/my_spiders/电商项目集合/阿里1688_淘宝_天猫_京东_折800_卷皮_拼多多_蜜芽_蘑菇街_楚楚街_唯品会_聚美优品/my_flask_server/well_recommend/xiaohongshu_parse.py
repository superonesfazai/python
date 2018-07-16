# coding:utf-8

'''
@author = super_fazai
@File    : xiaohongshu_parse.py
@Time    : 2018/7/9 13:24
@connect : superonesfazai@gmail.com
'''

"""
小红书parse
    NOTICE: 
        视频播放地址为: 
            原先为: https://sa.xiaohongshu.com/ljEITehG-zL_GFn_5Q4x-AYkFj69_compress_L2
            能直接播放的地址为: https://v.xiaohongshu.com/ljEITehG-zL_GFn_5Q4x-AYkFj69_compress_L2   (将sa替换成v即可)
"""

import sys
sys.path.append('..')

from settings import (
    MY_SPIDER_LOGS_PATH,
)

from logging import INFO, ERROR
import gc
from time import sleep
from pprint import pprint
import time
import re

from my_items import WellRecommendArticle

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,
    string_to_datetime,)
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests
from fzutils.common_utils import json_2_dict
from fzutils.common_utils import delete_list_null_str

class XiaoHongShuParse():
    def __init__(self, logger=None):
        self._set_logger(logger)
        self._set_headers()
        self.CRAWL_ARTICLE_SLEEP_TIME = 2.5     # 抓每天文章的sleep_time

    def _set_headers(self):
        self.headers = {
            'authority': 'www.xiaohongshu.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_pc_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'cookie': 'Hm_lvt_9df7d19786b04345ae62033bd17f6278=1530954715,1530954763,1530954908,1531113520; Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1530954716,1530954763,1530954907,1531113520; Hm_lpvt_d0ae755ac51e3c5ff9b1596b0c09c826=1531119425; Hm_lpvt_9df7d19786b04345ae62033bd17f6278=1531119425; beaker.session.id=b8a1a4ca0c2293ec3d447c7edbdc9dc2c528b5f2gAJ9cQEoVQhfZXhwaXJlc3ECY2RhdGV0aW1lCmRhdGV0aW1lCnEDVQoH4gcOCQIMAD2ghVJxBFUDX2lkcQVVIDNmMmM5NmE1YjQzNDQyMjA5MDM5OTIyNjU4ZjE3NjIxcQZVDl9hY2Nlc3NlZF90aW1lcQdHQdbQwdBhhRtVDl9jcmVhdGlvbl90aW1lcQhHQdbQIEMRyBF1Lg==; xhs_spses.5dde=*; xhs_spid.5dde=af753270e27cdd3c.1530953997.5.1531119433.1531115989.18f4b29f-8212-42a2-8ad6-002c47ebdb65',
        }

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/小红书/_/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    def _get_xiaohongshu_home_aritles_info(self):
        '''
        小红书主页json模拟获取
        :return: eg: ['小红书地址', ...]
        '''
        # cookies = {
        #     'beaker.session.id': '2ce91a013076367573e263a34e3691a510bb0479gAJ9cQEoVQhfZXhwaXJlc3ECY2RhdGV0aW1lCmRhdGV0aW1lCnEDVQoH4gcNDQoiDh9FhVJxBFULc2Vzc2lvbmlkLjFxBVgbAAAAc2Vzc2lvbi4xMjEwNDI3NjA2NTM0NjEzMjgycQZVCHVzZXJpZC4xcQdYGAAAADU4ZWRlZjc0NWU4N2U3NjBjOWMyNzAyNHEIVQNfaWRxCVUgMjMyNTRkOWU1MDUyNDY3NDkzZTMzZGM0YjE1MzUzZmZxClUOX2FjY2Vzc2VkX3RpbWVxC0dB1s/aksJmZlUOX2NyZWF0aW9uX3RpbWVxDEdB1s/akrUrE3Uu',
        #     'xhsTrackerId': '96359c99-a7b3-4725-c75d-2ee052cf2cc1',
        #     'xhs_spid.5dde': '9f350c095b58c416.1529844024.1.1529844045.1529844024.dfa500dd-18b6-4cf1-a094-3bc87addd183',
        # }

        headers = {
            'Accept-Encoding': 'br, gzip, deflate',
            'Connection': 'keep-alive',
            # 'device_id': '2AEEF650-2CAE-480F-B30C-CA5CABC26193',
            'Accept': 'application/json',
            'Host': 'www.xiaohongshu.com',
            'User-Agent': 'discover/5.19.1 (iPhone; iOS 11.0; Scale/3.00) Resolution/1242*2208 Version/5.19.1 Build/5191001 Device/(Apple Inc.;iPhone7,1)',
            # 'Authorization': 'session.1210427606534613282',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'X-Tingyun-Id': 'LbxHzUNcfig;c=2;r=551911068',
        }

        # 下面参数每个都是必须的, 且不变
        params = (
            ('deviceId', '2AEEF650-2CAE-480F-B30C-CA5CABC26193'),
            ('device_fingerprint', '201805101352429dd715d37f422fe3e64dd3923c0b0bc8017d90c099539039'),
            ('device_fingerprint1', '201805101352429dd715d37f422fe3e64dd3923c0b0bc8017d90c099539039'),
            ('lang', 'zh'),
            ('num', '10'),
            ('oid', 'homefeed_recommend'),
            ('platform', 'iOS'),
            ('sid', 'session.1210427606534613282'),
            ('sign', 'c9a9eadc6c46823ae3075d7b28fe97fa'),
            ('t', '1531010946'),    # 用原来的避免sign错误
            # ('t', int(time.time())),
        )

        url = 'https://www.xiaohongshu.com/api/sns/v6/homefeed'
        body = MyRequests.get_url_body(url=url, headers=headers, params=params, cookies=None)
        # self.my_lg.info(body)
        if body == '':
            self.my_lg.error('获取到的body为空值!请检查!')
            return {}

        _ = json_2_dict(body, logger=self.my_lg).get('data', [])
        # pprint(_)
        if _ == []:
            self.my_lg.error('获取到的data为空值!请检查!')
            return {}

        _ = [item.get('share_link', '') for item in _]

        return _

    def _deal_with_home_article(self):
        home_articles_link_list = self._get_xiaohongshu_home_aritles_info()
        # pprint(home_articles_link_list)
        self.my_lg.info(str(home_articles_link_list))
        print()

        data = self._deal_with_articles(articles_list=home_articles_link_list)
        pprint(data)

        return None

    def _deal_with_articles(self, articles_list):
        '''
        处理给与小红书地址(articles_list)
        :param articles_list: 待抓取的文章地址list  eg: ['小红书地址', ...]
        :return: data a list
        '''
        data = []
        for article_link in articles_list:  # eg: [{'id': '5b311bfc910cf67e693d273e','share_link': 'https://www.xiaohongshu.com/discovery/item/5b311bfc910cf67e693d273e'},...]
            self.my_lg.info('正在crawl小红书地址为: {0}'.format(article_link))

            if article_link != '':
                body = MyRequests.get_url_body(url=article_link, headers=self.headers)
                try:
                    article_info = re.compile('window.__INITIAL_SSR_STATE__=(.*?)</script>').findall(body)[0]
                    # self.my_lg.info(str(article_info))
                except IndexError:
                    self.my_lg.error('获取article_info时IndexError!请检查!')
                    sleep(self.CRAWL_ARTICLE_SLEEP_TIME)
                    continue

                article_info = self._wash_article_info(json_2_dict(json_str=article_info, logger=self.my_lg))
                # pprint(article_info)
                article_info = self._parse_page(article_link=article_link, article_info=article_info)
                # pprint(article_info)
                data.append(article_info)
                sleep(self.CRAWL_ARTICLE_SLEEP_TIME)
            else:
                pass

        self.my_lg.info('@@@ 抓取完毕!')
        # pprint(data)

        return data

    def _parse_page(self, **kwargs):
        '''
        解析单个article的info
        :return: a dict
        '''
        article_link = kwargs.get('article_link', '')
        article_info = kwargs.get('article_info', {}).get('NoteView', {})

        error_msg = '出错article_url: {0}'.format(article_link)
        try:
            nick_name = article_info.get('noteInfo', {}).get('user', {}).get('nickname', '')
            assert nick_name != '', '获取到的nick_name为空值!请检查!' + error_msg

            head_url = article_info.get('noteInfo', {}).get('user', {}).get('image', '')
            assert head_url != '', '获取到的head_url为空值!请检查!' + error_msg

            profile = ''          # 个人简介或者个性签名(留空)

            share_id = article_info.get('noteInfo', {}).get('id', '')
            assert share_id != '', '获取到的share_id为空值!请检查!' + error_msg

            title = ''            # title默认留空
            comment_content = self.wash_sensitive_info(article_info.get('noteInfo', {}).get('desc', ''))
            assert comment_content != '', '获取到的comment_content为空!请检查!' + error_msg

            share_img_url_list = [{   # 如果是视频的话, 则里面第一章图片就是视频第一帧
                'img_url': item.get('original', ''),
                'height': item.get('height'),           # 图片高宽
                'width': item.get('width'),
            } for item in article_info.get('noteInfo', {}).get('images', [])]
            assert share_img_url_list != [], '获取到的share_img_url_list为空list!请检查!' + error_msg

            div_body = ''         # 默认留空

            gather_url = article_link

            # 原文章原始的创建日期
            tmp_create_time = article_info.get('noteInfo', {}).get('time', '')
            assert tmp_create_time != '', '获取到的create_time为空值!请检查!'
            create_time = string_to_datetime(tmp_create_time + ':00')

            site_id = 3           # 小红书
            goods_url_list = []   # 该文章待抓取的商品地址

            tmp_tags = [str(item.get('name', '')) for item in article_info.get('noteInfo', {}).get('relatedTags', [])]
            # list先转str, 去掉敏感字眼, 再转list, 并去除''元素, 得到最后list
            tmp_tags = delete_list_null_str(self.wash_sensitive_info('|'.join(tmp_tags)).split('|'))
            tags = [{   # tags可以为空list!
                'keyword': item,
            } for item in tmp_tags]

            share_goods_base_info = []

            # 视频播放地址
            tmp_video_url = article_info.get('noteInfo', {}).get('video', '')
            tmp_video_url = 'https:' + tmp_video_url if tmp_video_url != '' else ''
            video_url = re.compile(r'//sa.').sub(r'//v.', tmp_video_url)

        except Exception:
            self.my_lg.error('遇到错误: ', exc_info=True)
            return {}

        _ = WellRecommendArticle()
        _['nick_name'] = nick_name
        _['head_url'] = head_url
        _['profile'] = profile
        _['share_id'] = share_id
        _['title'] = title
        _['comment_content'] = comment_content
        _['share_img_url_list'] = share_img_url_list
        _['div_body'] = div_body
        _['gather_url'] = gather_url
        _['create_time'] = create_time
        _['site_id'] = site_id
        _['goods_url_list'] = goods_url_list
        _['tags'] = tags
        _['share_goods_base_info'] = share_goods_base_info
        _['video_url'] = video_url

        return _

    def _wash_article_info(self, _dict):
        '''
        清洗无用字段
        :param _dict:
        :return:
        '''
        try:
            _dict['NoteView']['commentInfo'] = {}   # 评论信息
            _dict['NoteView']['panelData'] = []     # 相关笔记
        except:
            pass

        return _dict

    def wash_sensitive_info(self, data):
        '''
        清洗敏感信息
        :param data:
        :return:
        '''
        data = re.compile(r'小红书|xiaohongshu|XIAOHONGSHU|某宝').sub('优秀网', data)

        tmp_str = r'''
        淘宝|taobao|TAOBAO|天猫|tmall|TMALL|
        京东|JD|jd|红书爸爸|共产党|邪教|操|艹|
        杀人|胡锦涛|江泽民|习近平|小红薯
        '''.replace(' ', '').replace('\n', '')
        data = re.compile(tmp_str).sub('', data)

        return data

    def __del__(self):
        try:
            del self.my_lg
        except:
            pass
        gc.collect()

if __name__ == '__main__':
    while True:
        _ = XiaoHongShuParse()
        # 处理主页推荐地址
        _._deal_with_home_article()
        sleep(60)

        # 处理单个地址
        # article_url = 'https://www.xiaohongshu.com/discovery/item/5b46ca07910cf60eb7031af7'
        # data = _._deal_with_articles(articles_list=[article_url])
        # pprint(data)
