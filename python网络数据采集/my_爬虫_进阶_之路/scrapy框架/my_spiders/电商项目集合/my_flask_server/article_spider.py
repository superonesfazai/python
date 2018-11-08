# coding:utf-8

'''
@author = super_fazai
@File    : article_spider.py
@connect : superonesfazai@gmail.com
'''

"""
文章资讯爬虫

已支持:
    1. 微信文章内容提取(https://weixin.sogou.com)
"""

from gc import collect
from my_items import WellRecommendArticle
from settings import (
    ARTICLE_ITEM_LIST,
    MY_SPIDER_LOGS_PATH,
    PHANTOMJS_DRIVER_PATH,)

from fzutils.spider.fz_driver import BaseDriver
from fzutils.spider.async_always import *

class ArticleParser(AsyncCrawler):
    def __init__(self, logger=None, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH + '/articles/_/')
        self.driver_path = PHANTOMJS_DRIVER_PATH

    async def _get_headers(self):
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    async def _get_html_by_driver(self, url, load_images=False):
        '''
        使用driver获取异步页面
        :return:
        '''
        driver = BaseDriver(
            executable_path=self.driver_path,
            ip_pool_type=self.ip_pool_type,
            load_images=load_images,
            logger=self.lg)
        body = driver.get_url_body(url=url)
        # self.lg.info(body)
        try:
            del driver
        except:
            pass
        collect()

        return body

    async def _get_wx_article_html(self, article_url) -> tuple:
        '''
        得到wx文章内容
        :return: body, video_url
        '''
        body = Requests.get_url_body(url=article_url, headers=await self._get_headers())
        # self.lg.info(body)
        assert body != '', '获取到wx的body为空值!'

        return await self._wash_wx_article_body(body=body)

    async def _get_article_html(self, article_url, article_url_type) -> tuple:
        '''
        获取文章的html
        :return:
        '''
        video_url = ''
        body = ''
        try:
            if article_url_type == 'wx':
                return await self._get_wx_article_html(article_url=article_url)
            else:
                raise AssertionError('未实现的解析!')
        except AssertionError:
            self.lg.error('遇到错误:', exc_info=True)
            return body, video_url

    async def _wash_wx_article_body(self, body) -> tuple:
        '''
        清洗wx文章
        :return: body, video_url
        '''
        # 处理微信防盗链
        body = re.compile('<head>').sub('<head><meta name=\"referrer\" content=\"never\">', body)
        body = re.compile('data-src=').sub('src=', body)

        video_url = ''
        # 单独处理含视频标签的
        try:
            # videos_url_list = re.compile('<div class=\"tvp_video\"><video.*?src=\"(.*?)\"></video><div class=\"tvp_shadow\">').findall(body)
            videos_url_list = re.compile('<iframe class=\"video_iframe\" .*? src=\"(.*?)\"></iframe>').findall(body)
            assert videos_url_list != []
            self.lg.info('视频list: {}'.format(videos_url_list))
            self.lg.info('此文章含视频! 正在重新获取文章html...')

            tmp_body = await self._get_html_by_driver(url=videos_url_list[0], load_images=True)
            # self.lg.info(tmp_body)
            assert tmp_body != '', 'tmp_body为空值!'
            try:
                video_div = '<div style=\"text-align:center; width:100%; height:100%;\">' + \
                            re.compile('(<embed.*?)</div></div>').findall(tmp_body)[0] + '</div>'
                # self.lg.info(video_div)
            except IndexError:
                raise IndexError('获取video_div时索引异常!')
            # (只处理第一个视频)
            body = re.compile('<iframe class=\"video_iframe\" .*?></iframe>').sub(video_div, body, count=1)
            video_url = videos_url_list[0]
        except AssertionError:
            pass
        except Exception:
            self.lg.error('遇到错误: ', exc_info=True)
        # self.lg.info(body)

        return body, video_url

    async def _get_parse_obj(self) -> dict:
        '''
        获取到对应解析对象
        :return:
        '''
        parse_obj = None
        for item in ARTICLE_ITEM_LIST:
            if item.get('obj_origin', '') == 'mp.weixin.qq.com':
                parse_obj = item

        return parse_obj

    async def _parse_field(self, parser: dict, target_obj: (str, dict)) -> str:
        '''
        ** 根据类型解析字段
        :param parser: 解析对象 eg: {'method': 'css', 'selector': '.sss'}
        :param target_obj: 待处理的目标对象
        :return:
        '''
        res = ''
        if parser is not None:
            parser_method = parser.get('method', '')
            parser_selector = parser.get('selector')
            if parser_method == 're':
                try:
                    res = re.compile(parser_selector).findall(target_obj)[0]
                except IndexError:
                    self.lg.error('遇到错误:', exc_info=True)

            elif parser_method == 'css':
                res = Selector(text=target_obj).css(parser_selector).extract_first() or ''

            elif parser_method == 'xpath':
                res = Selector(text=target_obj).xpath(parser_selector).extract_first() or ''

            elif parser_method == 'dict_path':
                res = parser_selector

            else:
                raise ValueError('解析该字段的method值未知!')

        return res

    async def _parse_article(self, article_url) -> dict:
        '''
        解析文章内容
        :param article_url: 待抓取文章的url
        :return:
        '''
        try:
            article_url_type = await self._judge_url_type(article_url=article_url)
        except ValueError:      # article_url未知!
            self.lg.error(exc_info=True)
            return {}

        article_html, video_url = await self._get_article_html(article_url=article_url, article_url_type=article_url_type)
        # self.lg.info(article_html)

        parse_obj = await self._get_parse_obj()
        if parse_obj is None:
            self.lg.error('未找到解析对象!')
            return {}

        try:
            title = await self._parse_field(parser=parse_obj['title'], target_obj=article_html)
            assert title != '', '获取到的title为空值!'
            author = await self._parse_field(parser=parse_obj['author'], target_obj=article_html)
            assert author != '', '获取到的author为空值!'
            head_url = await self._parse_field(parser=parse_obj['head_url'], target_obj=article_html)
            content = await self._parse_field(parser=parse_obj['content'], target_obj=article_html)
            assert content != '', '获取到的content为空值!'
            content = '<meta name=\"referrer\" content=\"never\">' + content  # hook 反盗链
            # print(content)
            create_time = await self._parse_field(parser=parse_obj['create_time'], target_obj=article_html)
            # assert create_time != '', '获取到的create_time为空值!'

            comment_num = await self._parse_field(parser=parse_obj['comment_num'], target_obj=article_html)
            fav_num = await self._parse_field(parser=parse_obj['fav_num'], target_obj=article_html)
            praise_num = await self._parse_field(parser=parse_obj['praise_num'], target_obj=article_html)
            tags_list = await self._parse_field(parser=parse_obj['tags_list'], target_obj=article_html)
            site_id = await self._get_site_id(article_url_type=article_url_type)

        except (AssertionError, Exception):
            self.lg.error('遇到错误:', exc_info=True)
            return {}

        _ = WellRecommendArticle()
        _['nick_name'] = author
        _['head_url'] = head_url
        _['profile'] = ''
        _['share_id'] = get_uuid1()
        _['title'] = title
        _['comment_content'] = ''
        _['share_img_url_list'] = []
        _['goods_id_list'] = []
        _['div_body'] = content
        _['gather_url'] = article_url       # wx 阅读原文跳出个验证
        _['create_time'] = create_time
        _['site_id'] = site_id
        _['goods_url_list'] = []
        _['tags'] = tags_list
        _['share_goods_base_info'] = []     # [{'goods_id': 'xxx', 'img_url': 'xxx'}, ...]
        _['video_url'] = video_url
        _['likes'] = praise_num
        _['collects'] = fav_num

        return dict(_)

    async def _get_site_id(self, article_url_type):
        '''
        获取文章的site_id
        :return:
        '''
        if article_url_type == 'wx':
            return 4

        raise ValueError('未知的文章url!')

    async def _judge_url_type(self, article_url):
        '''
        判断url类别
        :return:
        '''
        if 'mp.weixin.qq.com' in article_url:
            return 'wx'

        raise ValueError('未知的文章url!')

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = ArticleParser()
    loop = get_event_loop()
    # 存在链接过期的情况
    # https://mp.weixin.qq.com/s?__biz=MzA4MjQxNjQzMA==&mid=2768396229&idx=1&sn=&scene=0#wechat_redirect
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1541556001&ver=1229&signature=lj08AA2o0K2O3OkgPfQGWCVNwnImo0C--UfpaUBkWfPnGEsJoeib1oJeQ9BNqW8t41xSqeg-Pz1VQ7HFrKxCPNoYhfSN7RcalaBHBGfzXRFXgoN7xhaMh7983gSWrgPD&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1541559601&ver=1229&signature=lj08AA2o0K2O3OkgPfQGWCVNwnImo0C--UfpaUBkWfMYB*2qWsNdP0Tgbfrh7LvMIgKSts77Y9jPIKpnuNJecXu-hXhUGMc9e9yGgPwKeuwT7J3g1wcLDgT2eSAS5qL6&new=1'
    url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1541583001&ver=1230&signature=Gx4Xh*mqPnERyD1pcDJBad9mN6shC6vzh3VldnHU5a-cXE4paJA8*b3tbnt7-OyKiWCyA4LCyJWngSZK6gkn2sCADLrUt1OBY1AxggmYXCOUpyYh8E7iywNUEdTPrEVO&new=1'
    article_parse_res = loop.run_until_complete(_._parse_article(article_url=url))
    pprint(article_parse_res)