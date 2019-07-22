# coding:utf-8

'''
@author = super_fazai
@File    : xiaohongshu_parse.py
@Time    : 2018/7/9 13:24
@connect : superonesfazai@gmail.com
'''

"""
小红书parse
    NOTICE: (此爬虫偶尔会被403禁掉, 可以在服务器上跑)
        视频播放地址为: 
            原先为: https://sa.xiaohongshu.com/ljEITehG-zL_GFn_5Q4x-AYkFj69_compress_L2
            能直接播放的地址为: https://v.xiaohongshu.com/ljEITehG-zL_GFn_5Q4x-AYkFj69_compress_L2   (将sa替换成v即可)
            html下可直接实现播放<body>
            <embed src="https://v.xiaohongshu.com/lmgn7xFw_6eowrZEmNF-3kqNr1Kc_compress_L2"/>
            </body>
"""

import sys
sys.path.append('..')

from settings import (
    MY_SPIDER_LOGS_PATH,
    IS_BACKGROUND_RUNNING,
    IP_POOL_TYPE,
)

import gc
from time import sleep
from pprint import pprint
import re
from json import dumps

from my_items import WellRecommendArticle
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from fzutils.time_utils import (
    string_to_datetime,)
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import Requests
from fzutils.linux_utils import daemon_init
from fzutils.common_utils import (
    json_2_dict,
    delete_list_null_str,
    get_random_int_number,
    list_duplicate_remove,
    wash_sensitive_info,)
from fzutils.spider.crawler import Crawler

class XiaoHongShuParse(Crawler):
    def __init__(self, logger=None, by_wx=False):
        '''
        :param logger:
        :param by_wx: 抓取wx小程序(弊端: 没有tags值 优点: 可长期采集, 不容易被封) √
                      vs 抓取app(弊端: 测试发现就算用高匿proxy每跑20个, 就被封3-5分钟, 效率低)
        '''
        super(XiaoHongShuParse, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/小红书/_/',
        )
        self._set_headers()
        self.by_wx = by_wx
        self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
        self.index = 0
        self.success_insert_db_num = 0
        self.CRAWL_ARTICLE_SLEEP_TIME = 1       # 抓每天文章的sleep_time(wx=1/app=2)
        self.LONG_SLEEP_TIME = 0                # 每抓10条休眠时间
        self.db_share_id = []                   # db原先存在的
        self.ip_pool_type = IP_POOL_TYPE

    def _set_headers(self):
        self.headers = {
            'authority': 'www.xiaohongshu.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_pc_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

    def _get_xiaohongshu_home_aritles_info(self):
        '''
        小红书主页json模拟获取(模拟app端主页请求)
        :return:
        '''
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
        body = Requests.get_url_body(url=url, headers=headers, params=params, cookies=None, high_conceal=True, ip_pool_type=self.ip_pool_type)
        # self.lg.info(body)
        if body == '':
            self.lg.error('获取到的body为空值!请检查!')
            return []

        if re.compile(r'<title>403 Forbidden</title>').findall(body) != []:
            self.lg.info('此次抓取被403禁止!')
            sleep(self.CRAWL_ARTICLE_SLEEP_TIME)
            return []

        _ = json_2_dict(body, logger=self.lg).get('data', [])
        # pprint(_)
        if _ == []:
            self.lg.error('获取到的data为空值!请检查!')
            return []

        _ = [{
            'share_link': item.get('share_link', ''),
            'likes': item.get('likes', 0),
        } for item in _]

        return _

    def _deal_with_home_article(self):
        home_articles_link_list = self._get_xiaohongshu_home_aritles_info()
        # pprint(home_articles_link_list)
        self.lg.info(home_articles_link_list)

        # self.lg.info(str(home_articles_link_list) + '\n')
        data = self._deal_with_articles(articles_list=home_articles_link_list)
        # pprint(data)

        self._save_articles(data=data)

        self.lg.info('一次采集完毕, 进入{0}s休眠...'.format(self.LONG_SLEEP_TIME))
        sleep(self.LONG_SLEEP_TIME)   # 设置休眠, 实现周期抓取, 避免频繁抓取被封禁(测试发现抓20个就会封一会)

        return True

    def _deal_with_articles(self, articles_list):
        '''
        处理给与小红书地址(articles_list)
        :param articles_list: 待抓取的文章地址list  eg: [{'share_link':'小红书地址', 'likes': 111}, ...]   # likes可以为空
        :return: data a list
        '''
        data = []
        _db = self.my_pipeline._select_table(sql_str='select share_id from dbo.daren_recommend')
        if _db is not None and _db != [] and _db != [()]:
            self.db_share_id = [item[0] for item in _db]
            # self.lg.info(self.db_share_id)

        for item in articles_list:
            self.index += 1
            article_link = item.get('share_link', '')
            article_likes = item.get('likes', 0)
            article_id = re.compile(r'/item/(\w+)').findall(article_link)[0]

            if article_id in self.db_share_id:
                self.lg.info('该{0}已存在于db中...跳过!'.format(article_id))

            self.lg.info('[+] {0}'.format(article_link))
            if article_link != '':
                if not self.by_wx:  # 通过pc端
                    params = (
                        ('_at', '499a292d16aed3d80a068fc60e0c1e3ee3410'),
                    )
                    body = Requests.get_url_body(url=article_link, headers=self.headers, params=params, high_conceal=True, ip_pool_type=self.ip_pool_type)
                    # self.lg.info(str(body))
                    try:
                        article_info = re.compile('window.__INITIAL_SSR_STATE__=(.*?)</script>').findall(body)[0]
                        # self.lg.info(str(article_info))
                    except IndexError:
                        self.lg.error('获取article_info时IndexError!请检查!')
                        sleep(self.CRAWL_ARTICLE_SLEEP_TIME)
                        continue

                    article_info = self._wash_article_info(json_2_dict(json_str=article_info, logger=self.lg))
                    # pprint(article_info)
                    article_info = self._parse_page(
                        article_link=article_link,
                        article_info=article_info,
                        article_likes=article_likes)
                    # pprint(article_info)

                else:               # 通过wx小程序
                    # url = "https://www.xiaohongshu.com/wx_mp_api/sns/v1/note/" + article_id
                    # wx接口改版, 需要一个参数Auth认证, 暂时没处理
                    url = 'https://www.xiaohongshu.com/sapi/wx_mp_api/sns/v1/note/' + article_id
                    params = {
                        "sid": "session.1210427606534613282",  # 对方服务器用来判断登录是否过期(过期则替换这个即可再次采集)
                    }
                    body = Requests.get_url_body(url=url, headers=self.headers, params=params, ip_pool_type=self.ip_pool_type)
                    # self.lg.info(str(body))
                    if body == '':
                        self.lg.error('获取到的article的body为空值!跳过!')
                        sleep(self.CRAWL_ARTICLE_SLEEP_TIME)
                        continue
                    article_info = self._wash_article_info_from_wx(json_2_dict(json_str=body, logger=self.lg))
                    article_info = self._parse_page_from_wx(
                        article_link=article_link,
                        article_info=article_info,
                        article_likes=article_likes)
                    # pprint(article_info)

                data.append(article_info)
                sleep(self.CRAWL_ARTICLE_SLEEP_TIME)
            else:
                pass

        self.lg.info('@@@ 抓取完毕!')
        # pprint(data)

        return data

    def _parse_page(self, **kwargs):
        '''
        解析单个article的info
        :return: a dict
        '''
        article_link = kwargs.get('article_link', '')
        article_info = kwargs.get('article_info', {}).get('NoteView', {})
        article_likes = kwargs.get('article_likes', get_random_int_number())

        error_msg = '出错article_url: {0}'.format(article_link)
        try:
            nick_name = article_info.get('noteInfo', {}).get('user', {}).get('nickname', '')
            assert nick_name != '', '获取到的nick_name为空值!请检查!' + error_msg

            head_url = article_info.get('noteInfo', {}).get('user', {}).get('image', '')
            assert head_url != '', '获取到的head_url为空值!请检查!' + error_msg

            profile = ''          # 个人简介或者个性签名(留空)

            share_id = article_info.get('noteInfo', {}).get('id', '')
            assert share_id != '', '获取到的share_id为空值!请检查!' + error_msg

            title = article_info.get('noteInfo', {}).get('title', '')            # title默认留空
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
            share_goods_base_info = []

            tags = self._get_tags(article_info=article_info)

            # 视频播放地址
            tmp_video_url = article_info.get('noteInfo', {}).get('video', '')
            tmp_video_url = 'https:' + tmp_video_url if tmp_video_url != '' else ''
            video_url = re.compile(r'//sa.').sub(r'//v.', tmp_video_url)

            likes = article_likes
            collects = article_info.get('noteInfo', {}).get('collects', None)
            assert collects is not None, '获取到的collects为None!请检查!' + error_msg

        except Exception:
            sleep(self.CRAWL_ARTICLE_SLEEP_TIME)
            self.lg.error('遇到错误: ', exc_info=True)
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
        _['likes'] = likes
        _['collects'] = collects

        return _

    def _parse_page_from_wx(self, **kwargs):
        '''
        解析wx单个article的info
        :param kwargs:
        :return: a WellRecommendArticle object
        '''
        article_link = kwargs.get('article_link', '')
        article_info = kwargs.get('article_info', {}).get('data', {})
        article_likes = kwargs.get('article_likes', get_random_int_number())

        error_msg = '出错article_url: {0}'.format(article_link)
        try:
            nick_name = article_info.get('user', {}).get('nickname', '')
            assert nick_name != '', '获取到的nick_name为空值!请检查!' + error_msg

            head_url = article_info.get('user', {}).get('images', '')
            assert head_url != '', '获取到的head_url为空值!请检查!' + error_msg

            profile = ''        # 个人简介或者个性签名(留空)

            share_id = article_info.get('id', '')
            assert share_id != '', '获取到的share_id为空值!请检查!' + error_msg

            title = self.wash_sensitive_info(article_info.get('title', ''))          # title默认留空
            comment_content = self.wash_sensitive_info(article_info.get('desc', ''))
            assert comment_content != '', '获取到的comment_content为空!请检查!' + error_msg

            share_img_url_list = [{  # 如果是视频的话, 则里面第一章图片就是视频第一帧
                'img_url': item.get('original', ''),
                'height': item.get('height'),  # 图片高宽
                'width': item.get('width'),
            } for item in article_info.get('images_list', [])]
            assert share_img_url_list != [], '获取到的share_img_url_list为空list!请检查!' + error_msg

            div_body = ''  # 默认留空
            gather_url = article_link

            # 原文章原始的创建日期
            tmp_create_time = article_info.get('time', '')
            assert tmp_create_time != '', '获取到的create_time为空值!请检查!'
            create_time = string_to_datetime(tmp_create_time + ':00')

            site_id = 3  # 小红书
            goods_url_list = []  # 该文章待抓取的商品地址
            share_goods_base_info = []

            # wx端tags没有返回值
            tags = self._get_tags_from_wx(article_info=article_info)

            # 视频播放地址
            tmp_video_url = article_info.get('video', '')
            tmp_video_url = re.compile('\?.*').sub('', tmp_video_url)
            video_url = re.compile(r'//sa.').sub(r'//v.', tmp_video_url)

            likes = article_likes
            collects = article_info.get('fav_count', None)
            assert collects is not None, '获取到的collects为None!请检查!' + error_msg

        except Exception:
            sleep(self.CRAWL_ARTICLE_SLEEP_TIME)
            self.lg.error('遇到错误:', exc_info=True)
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
        _['likes'] = likes
        _['collects'] = collects

        return _

    def _save_articles(self, data):
        '''
        存储数据
        :param data:
        :return:
        '''
        self.lg.info('即将开始存储该文章...')
        sql_str = 'insert into dbo.daren_recommend(share_id, nick_name, head_url, profile, gather_url, title, comment_content, share_img_url_list, div_body, create_time, site_id, tags, video_url, likes, collects) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for item in data:
            if self.index % 20 == 0:
                self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

            if self.my_pipeline.is_connect_success:
                share_id = item.get('share_id', '')
                if share_id == '':
                    continue

                self.lg.info('------>>>| 正在存储share_id: {0}...'.format(share_id))
                try:
                    params = self._get_db_insert_into_params(item=item)
                except Exception:
                    continue
                result = self.my_pipeline._insert_into_table_2(sql_str=sql_str, params=params, logger=self.lg)
                if result:
                    self.success_insert_db_num += 1

            else:
                self.lg.error('db连接失败!存储失败! 出错article地址:{0}'.format(item.get('gather_url', '')))

        self.lg.info('@' * 9 + ' 目前成功存储{0}个!'.format(self.success_insert_db_num))

        return True

    def _get_db_insert_into_params(self, item):
        '''
        得到待存储的数据
        :param item:
        :return:
        '''
        params = [
            item['share_id'],
            item['nick_name'],
            item['head_url'],
            item['profile'],
            item['gather_url'],
            item['title'],
            item['comment_content'],
            dumps(item['share_img_url_list'], ensure_ascii=False),
            # dumps(item['goods_id_list'], ensure_ascii=False),
            # dumps(item['share_goods_base_info'], ensure_ascii=False),
            item['div_body'],
            item['create_time'],
            item['site_id'],
            dumps(item['tags'], ensure_ascii=False),
            item['video_url'],
            item['likes'],
            item['collects'],
        ]

        return tuple(params)

    def _get_tags(self, article_info):
        '''
        获取tags
        :return:
        '''
        tmp_tags = list_duplicate_remove(
            [str(item.get('name', '')) for item in article_info.get('noteInfo', {}).get('relatedTags', [])])
        # self.lg.info(str(tmp_tags))
        # list先转str, 去掉敏感字眼, 再转list, 并去除''元素, 得到最后list
        tmp_tags = delete_list_null_str(self.wash_sensitive_info('|'.join(tmp_tags)).split('|'))
        tags = [{  # tags可以为空list!
            'keyword': item,
        } for item in tmp_tags]

        return tags

    def _get_tags_from_wx(self, article_info):
        '''
        从wx获取tags
        :param article_info:
        :return:
        '''

        return []

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

    def _wash_article_info_from_wx(self, _dict):
        '''
        清洗wx无用字段
        :param _dict:
        :return:
        '''
        try:
            _dict['data']['mini_program_info'] = {}     # 推荐首页的缩略信息
            _dict['data']['share_info'] = {}            # 分享的信息
        except:
            pass

        return _dict

    def wash_sensitive_info(self, data):
        '''
        清洗敏感信息
        :param data:
        :return:
        '''
        replace_str_list = [
            ('小红书', '优秀网'),
            ('xiaohongshu', '优秀网'),
            ('XIAOHONGSHU', '优秀网'),
            ('某宝', '优秀网'),
            ('薯队长', '秀队长'),
            ('薯宝宝', '秀客'),
            ('红薯们', '秀客们'),
            ('小红薯', '小秀客'),
        ]

        add_sensitive_str_list = [
            '#.*#',
            '@.*?薯',
        ]

        return wash_sensitive_info(
            data=data,
            replace_str_list=replace_str_list,
            add_sensitive_str_list=add_sensitive_str_list,
            is_default_filter=True,
            is_lower=False,)

    def __del__(self):
        try:
            del self.lg
            del self.my_pipeline
        except:
            pass
        gc.collect()

def just_fuck_run():
    # _ = XiaoHongShuParse()
    _ = XiaoHongShuParse(by_wx=False)   # wx headers加了个Auth, pc老死

    while True:
        # 处理主页推荐地址
        _._deal_with_home_article()

        # 处理单个地址
        # article_url_list = [
        #     {'share_link': 'https://www.xiaohongshu.com/discovery/item/5b46ca07910cf60eb7031af7',},
        #     {'share_link': 'https://www.xiaohongshu.com/discovery/item/5b498680672e140532a7ce49',},
        #     {'share_link': 'https://www.xiaohongshu.com/discovery/item/5b48e0cb910cf646d2a6c056',},
        #     {'share_link': 'https://www.xiaohongshu.com/discovery/item/5b4b0d7207ef1c50ac3cd94a',},
        # ]
        # data = _._deal_with_articles(articles_list=article_url_list)
        # pprint(data)

        sleep(3)

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()