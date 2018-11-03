# coding:utf-8

'''
@author = super_fazai
@File    : wx_article_parse.py
@connect : superonesfazai@gmail.com
'''

"""
微信文章内容提取
    基于 https://weixin.sogou.com
"""

from gc import collect
from items import ArticleItem
from settings import ARTICLE_ITEM_LIST
from fzutils.spider.fz_driver import BaseDriver
from fzutils.spider.async_always import *

MY_SPIDER_LOGS_PATH = '/Users/afa/myFiles/my_spider_logs/电商项目'
PHANTOMJS_DRIVER_PATH = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'

class WXArticleParser(AsyncCrawler):
    def __init__(self, logger=None, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            logger=logger,
            log_save_path=MY_SPIDER_LOGS_PATH+'/articles/_/')
        self.article_url = None
        self.article_html = None
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
            load_images=load_images)
        body = driver.get_url_body(url=url)
        # self.lg.info(body)
        try:
            del driver
        except:
            pass
        collect()

        return body

    async def _get_article_html(self) -> str:
        '''
        获取文章的html
        :param first_time: 是否为第一次使用
        :return:
        '''
        body = Requests.get_url_body(url=self.article_url, headers=await self._get_headers())
        # self.lg.info(body)
        if body == '':
            self.lg.info('获取到的body为空值!')
            return ''

        body = await self._wash_wx_article_body(body=body)

        return body

    async def _wash_wx_article_body(self, body) -> str:
        '''
        清洗wx文章
        :return:
        '''
        # 处理微信防盗链
        body = re.compile('<head>').sub('<head><meta name=\"referrer\" content=\"never\">', body)
        body = re.compile('data-src=').sub('src=', body)

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
                video_div = '<div style=\"text-align:center; width:100%; height:100%;\">' + re.compile('(<embed.*?)</div></div>').findall(tmp_body)[0] + '</div>'
                # self.lg.info(video_div)
            except IndexError:
                raise IndexError('获取video_div时索引异常!')
            # (只处理第一个视频)
            body = re.compile('<iframe class=\"video_iframe\" .*?></iframe>').sub(video_div, body, count=1)
        except AssertionError:
            pass
        except Exception:
            self.lg.error('遇到错误: ', exc_info=True)
        # self.lg.info(body)

        return body
    
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
        
    async def _parse_field(self, parser:dict, target_obj:(str, dict)) -> str:
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
        self.article_url = article_url
        self.article_html = await self._get_article_html()
        # self.lg.info(self.article_html)

        parse_obj = await self._get_parse_obj()
        if parse_obj is None:
            self.lg.info('未找到解析对象!')
            return {}

        try:
            title = await self._parse_field(parser=parse_obj['title'], target_obj=self.article_html)
            assert title != '', '获取到的title为空值!'
            author = await self._parse_field(parser=parse_obj['author'], target_obj=self.article_html)
            assert author != '', '获取到的author为空值!'
            content = await self._parse_field(parser=parse_obj['content'], target_obj=self.article_html)
            assert content != '', '获取到的content为空值!'
            content = '<meta name=\"referrer\" content=\"never\">' + content        # hook 反盗链
            self.lg.info(content)
            create_time = await self._parse_field(parser=parse_obj['create_time'], target_obj=self.article_html)
            # assert create_time != '', '获取到的create_time为空值!'

            comment_num = await self._parse_field(parser=parse_obj['comment_num'], target_obj=self.article_html)
            fav_num = await self._parse_field(parser=parse_obj['fav_num'], target_obj=self.article_html)
            praise_num = await self._parse_field(parser=parse_obj['praise_num'], target_obj=self.article_html)
            tags_list = await self._parse_field(parser=parse_obj['tags_list'], target_obj=self.article_html)

        except (AssertionError, Exception):
            self.lg.error('遇到错误:', exc_info=True)
            return {}
        
        _ = ArticleItem()
        _['title'] = title
        _['author'] = author
        _['content'] = content
        _['create_time'] = create_time
        _['comment_num'] = comment_num
        _['fav_num'] = fav_num
        _['praise_num'] = praise_num
        _['tags_list'] = tags_list

        return _

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = WXArticleParser()
    loop = get_event_loop()
    # 存在链接过期的情况
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1541219424&ver=1220&signature=G-L9gXPuIzywRFOsDZK-21JxkcVmmhK*Xb0VhZUU9xywrmNCy2nSdHBy6qOUXGce2jcXNE8hMO0yWAkR-GiDWGDz3Q5ZVvPD6cDAdyghdByamVSuiIJh9Ltwr8uiBKtQ&new=1'
    url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1541219424&ver=1220&signature=2DSKqD9M-85xFzskcvdnO5LZuIe421tGzKyqVn2UqpJd57IkEgnCzhPwOOi1EHTNdNy0n5uElKPvDud524r-xJ2XNddxjy2ZMuy-PbvvACVJFYlwyViV3-BkxNfrnOeC&new=1'
    article_parse_res = loop.run_until_complete(_._parse_article(article_url=url))
    pprint(article_parse_res)