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
from fzutils.spider.async_always import *

class WXArticleParser(object):
    def __init__(self):
        self.loop = get_event_loop()
        self.article_url = None
        self.article_html = None

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

    async def _get_article_html(self) -> str:
        '''
        获取文章的html
        :return:
        '''
        body = Requests.get_url_body(url=self.article_url, headers=await self._get_headers())
        # print(body)
        if body == '':
            print('获取到的body为空值!')
            return ''

        # 处理微信防盗链
        body = re.compile('<head>').sub('<head><meta name=\"referrer\" content=\"never\">', body)
        body = re.compile('data-src=').sub('src=', body)
        # print(body)

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
                except IndexError as e:
                    print(e)

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
        # print(self.article_html)

        parse_obj = await self._get_parse_obj()
        if parse_obj is None:
            print('未找到解析对象!')
            return {}

        try:
            title = await self._parse_field(parser=parse_obj['title'], target_obj=self.article_html)
            assert title != '', '获取到的title为空值!'
            author = await self._parse_field(parser=parse_obj['author'], target_obj=self.article_html)
            assert author != '', '获取到的author为空值!'
            content = await self._parse_field(parser=parse_obj['content'], target_obj=self.article_html)
            assert content != '', '获取到的content为空值!'
            content = '<meta name=\"referrer\" content=\"never\">' + content        # hook 反盗链
            # print(content)
            create_time = await self._parse_field(parser=parse_obj['create_time'], target_obj=self.article_html)
            # assert create_time != '', '获取到的create_time为空值!'

            comment_num = await self._parse_field(parser=parse_obj['comment_num'], target_obj=self.article_html)
            fav_num = await self._parse_field(parser=parse_obj['fav_num'], target_obj=self.article_html)
            praise_num = await self._parse_field(parser=parse_obj['praise_num'], target_obj=self.article_html)
            tags_list = await self._parse_field(parser=parse_obj['tags_list'], target_obj=self.article_html)

        except (AssertionError, ) as e:
            print(e)
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
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1540268075&ver=1199&signature=9s8yg0BRca0W4Yjs00UP6xnlpMkGPBfHLPfZutCt5I1WRKFlCOMOKtc07DsES8UOpq27IlISj954*t1eZn7ZlBSFoGfkG7qhC0fiwNr-z6EdvEGhQXGuH3Y3JXS9JkJJ&new=1'
    url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1540276201&ver=1199&signature=I1lirGPjYRleuigNrRYSNP8BhHeFTjO3Zex9QQzXKeEj3eCsAUSoRVMwKWfpLtshxt984X02pLIdO0tBs01bOmzP2WdFRMH0YAvrZngLMBZ4SxpE9NbjW8wliafXdz9E&new=1'
    article_parse_res = loop.run_until_complete(_._parse_article(article_url=url))
    pprint(article_parse_res)