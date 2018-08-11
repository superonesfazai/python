# coding:utf-8

'''
@author = super_fazai
@File    : taobao_weitao_share_parse.py
@Time    : 2018/5/26 12:18
@connect : superonesfazai@gmail.com
'''

"""
可采集对象: 淘宝微淘, ifashion, 必买清单, 
"""

import sys
sys.path.append('..')

from json import loads, dumps
import re
import asyncio
from logging import INFO, ERROR
import gc
from pprint import pprint
from urllib.parse import unquote

from settings import (
    MY_SPIDER_LOGS_PATH,
    TAOBAO_REAL_TIMES_SLEEP_TIME,
)
from my_items import WellRecommendArticle
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from taobao_parse import TaoBaoLoginAndParse

from fzutils.log_utils import set_logger
from fzutils.time_utils import get_shanghai_time
from fzutils.linux_utils import restart_program
from fzutils.cp_utils import get_taobao_sign_and_body
from fzutils.common_utils import list_duplicate_remove
from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests

class TaoBaoWeiTaoShareParse():
    def __init__(self, logger=None):
        self._set_headers()
        self._set_logger(logger)
        self.msg = ''
        self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()

    def _set_headers(self):
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': '*/*',
            'referer': 'https://market.m.taobao.com/apps/market/content/index.html?ut_sk=1.VmYadv9DXkkDAFZm0VV4JBNq_21380790_1527298517854.Copy.33&params=%7B%22csid%22%3A%2254a52aea54b7c29d289a0e36b2bf2f51%22%7D&wh_weex=true&contentId=200668154273&source=weitao_2017_nocover&data_prefetch=true&suid=3D763077-A7BF-43BC-9092-C17B35E896F9&wx_navbar_transparent=false&wx_navbar_hidden=false&sourceType=other&un=bc80c9f324602d31384c4a342af87869&share_crt_v=1&sp_tk=o6R2Q0ZDMHZvaDBlS6Ok&cpp=1&shareurl=true&spm=a313p.22.68.948703884987&short_name=h.WAjz5RP&app=chrome',
            'authority': 'h5api.m.taobao.com',
            # cookie得注释掉, 否则为非法请求
            # 'cookie': 't=70c4fb481898a67a66d437321f7b5cdf; cna=nbRZExTgqWsCAXPCa6QA5B86; l=AkFBuFEM2rj4GbU8Mjl3KsFo0YZa/7Vg; thw=cn; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; _cc_=UIHiLt3xSw%3D%3D; tg=0; enc=OFbfiyN19GGi1GicxsjVmrZoFzlt9plbuviK5OuthXYfocqTD%2BL079G%2BIt4OMg6ZrbV4veSg5SQEpzuMUgLe0w%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; miid=763730917900964122; mt=ci%3D-1_1; cookie2=16c0da3976ab60d7c87ef7cea1e83cb2; v=0; _tb_token_=dd9fe0edb4b3; tk_trace=oTRxOWSBNwn9dPy4KVJVbutfzK5InlkjwbWpxHegXyGxPdWTLVRjn23RuZzZtB1ZgD6Khe0jl%2BAoo68rryovRBE2Yp933GccTPwH%2FTbWVnqEfudSt0ozZPG%2BkA1iKeVv2L5C1tkul3c1pEAfoOzBoBsNsJyRfZ0FH5AEyz0CWtQgYlWnUAkbLeBYDpeNMwsdmBZ5GYwOAPdU1B2IUBU8G0MXGQCqFCjZt1pjb2TJN2uXIiZePpK9SWkwA%2FlD1sTTfYGTmnCo0YJ7IAG%2BnJtbITMYZ3mzYjFZtYlGojOqye861%2FNFDJbTR41FruF%2BHJRnt%2BHJNgFj3F7IDGXJCs8K; linezing_session=4ic7MPhjlPi65fN5BzW36xB7_1527299424026Fe7K_1; isg=BDo6U2SENb2uULiLxiJ4XA6ri2ZWbZPa3G9M1kQz602YN9pxLHsO1QBGg8PrpzZd; _m_h5_tk=53d85a4f43d72bc623586c142f0c5293_1527305714711; _m_h5_tk_enc=cc75764d122f72920ae715c9102701a8'
        }

    def _set_logger(self, logger):
        if logger is None:
            self.my_lg = set_logger(
                log_file_name=MY_SPIDER_LOGS_PATH + '/淘宝/微淘/' + str(get_shanghai_time())[0:10] + '.txt',
                console_log_level=INFO,
                file_log_level=ERROR
            )
        else:
            self.my_lg = logger

    async def _get_target_url_and_content_id_and_csid(self, taobao_short_url):
        '''
        根据给与的淘宝分享短链接, 得到target_url, content_id, csid
        :param taobao_short_url:
        :return:
        '''
        if re.compile(r'contentId').findall(taobao_short_url) != []:
            # 先检查是否已为目标地址
            target_url = taobao_short_url

        else:
            body = MyRequests.get_url_body(url=taobao_short_url, headers=self.headers)
            # self.my_lg.info(str(body))
            if body == '':
                self.my_lg.error('获取到的body为空值, 出错短链接地址: {0}'.format(str(taobao_short_url)))
                return '', '', ''

            try:
                # 获取短连接的目标地址
                target_url = re.compile('var url = \'(.*?)\';').findall(body)[0]
                # self.my_lg.info(str(target_url))
            except IndexError:
                self.my_lg.error('获取target_url的时候IndexError! 出错短链接地址: {0}'.format(str(taobao_short_url)))
                target_url = ''

        try:
            # 得到contentId
            content_id = re.compile('contentId=(\d+)').findall(target_url)[0]
            # self.my_lg.info(content_id)
        except IndexError:
            self.my_lg.error('获取content_id时IndexError! 出错短链接地址: {0}'.format(str(taobao_short_url)))
            content_id = ''

        try:
            # 得到csid
            csid = re.compile('csid%22%3A%22(.*?)%22%7D').findall(target_url)[0]
            # self.my_lg.info(csid)
        except IndexError:
            self.my_lg.info('此链接为无csid情况的链接...')
            # self.my_lg.error('获取csid时IndexError! 出错短链接地址: {0}'.format(str(taobao_short_url)))
            csid = ''

        try:
            tag_name = re.compile('tagName=(.*?)&').findall(target_url)[0]
        except IndexError:
            tag_name = ''

        try:
            tag = re.compile('tag=(.*?)&').findall(target_url)[0]
        except IndexError:
            tag = ''

        return target_url, content_id, csid, tag_name, tag

    async def _get_api_body(self, taobao_short_url):
        '''
        获取该页面api返回的文件
        :param taobao_short_url:
        :return: body 类型 str
        '''
        base_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.beehive.detail.contentservicenewv2/1.0/'

        try:
            target_url, content_id, csid, tag_name, tag = await self._get_target_url_and_content_id_and_csid(taobao_short_url)
        except ValueError:
            self.my_lg.error('遇到ValueError!', exc_info=True)
            return ''

        if content_id == '' and csid == '':      # 异常退出
            return ''

        data = dumps({
            'businessSpm': '',
            'business_spm': '',
            'contentId': content_id,
            'params': dumps({
                "csid": csid,
            }) if csid != '' else '',   # 没有csid时，就不传这个参数
            'source': 'weitao_2017_nocover',
            'tagName': tag_name,        # 这个是我自己额外加的用于获取tags的api接口
            'track_params': '',
            'type': 'h5',
        })

        params = {
            'AntiCreep': 'true',
            'AntiFlood': 'true',
            'api': 'mtop.taobao.beehive.detail.contentservicenewv2',
            'appKey': '12574478',
            'callback': 'mtopjsonp1',
            # 'data': '{"contentId":"200668154273","source":"weitao_2017_nocover","type":"h5","params":"{\\"csid\\":\\"54a52aea54b7c29d289a0e36b2bf2f51\\"}","businessSpm":"","business_spm":"","track_params":""}',
            'data': data,
            'dataType': 'jsonp',
            'data_2': '',
            'jsv': '2.4.11',
            # 'sign': 'e8cb623e58bab0ceb10e9edffdacd5b2',
            # 't': '1527300457911',
            'type': 'jsonp',
            'v': '1.0'
        }

        result_1 = await get_taobao_sign_and_body(
            base_url=base_url,
            headers=self.headers,
            params=params,
            data=data,
            logger=self.my_lg
        )
        _m_h5_tk = result_1[0]

        if _m_h5_tk == '':
            self.my_lg.error('获取到的_m_h5_tk为空str! 出错短链接地址: {0}'.format(taobao_short_url))

        # 带上_m_h5_tk, 和之前请求返回的session再次请求得到需求的api数据
        result_2 = await get_taobao_sign_and_body(
            base_url=base_url,
            headers=self.headers,
            params=params,
            data=data,
            _m_h5_tk=_m_h5_tk,
            session=result_1[1],
            logger=self.my_lg
        )
        body = result_2[2]

        return body

    async def _deal_with_api_info(self, taobao_short_url):
        '''
        处理api返回的信息, 并结构化存储
        :param taobao_short_url:
        :return:
        '''
        data = await self._get_api_body(taobao_short_url)
        if data == '':
            self.my_lg.error('获取到的api数据为空值!')
            return {}

        try:
            data = re.compile('mtopjsonp1\((.*)\)').findall(data)[0]
        except IndexError:
            self.my_lg.error('re获取主信息失败, IndexError, 出错短链接地址:{0}'.format(taobao_short_url))
            data = {}

        try:
            data = await self._wash_api_info(loads(data))
            # pprint(data)
        except Exception as e:
            self.my_lg.error('出错短链接地址:{0}'.format(taobao_short_url))
            self.my_lg.exception(e)
            return {}

        article = await self._get_article(data=data, taobao_short_url=taobao_short_url)
        pprint(article)

        if article != {} and article.get('share_id', '') != '':
            '''采集该文章推荐的商品'''
            await self._crawl_and_save_these_goods(goods_url_list=article.get('goods_url_list', []))

            '''存储该文章info'''
            await self._save_this_article(article=article)

            return True
        else:
            self.my_lg.info('获取到的文章失败! article为空dict!')
            return False

    async def _crawl_and_save_these_goods(self, goods_url_list):
        '''
        采集该文章推荐的商品
        :param goods_url_list:
        :return:
        '''
        sql_str = r'select GoodsID from dbo.GoodsInfoAutoGet where SiteID=1 or SiteID=3 or SiteID=4 or SiteID=6'

        try:
            result = self.my_pipeline._select_table(sql_str=sql_str)
        except TypeError:
            result = []

        self.my_lg.info('即将开始抓取该文章的goods, 请耐心等待...')
        index = 1

        db_all_goods_id_list = [item[0] for item in result]
        for item in goods_url_list:
            try:
                goods_id = re.compile(r'id=(\d+)').findall(item.get('goods_url', ''))[0]
            except IndexError:
                self.my_lg.error('re获取goods_id时出错, 请检查!')
                continue

            if goods_id in db_all_goods_id_list:
                self.my_lg.info('该goods_id[{0}]已存在于db中!'.format(goods_id))
                continue

            else:
                taobao = TaoBaoLoginAndParse(logger=self.my_lg)
                if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                    self.my_lg.info('正在重置，并与数据库建立新连接中...')
                    self.my_pipeline = SqlServerMyPageInfoSaveItemPipeline()
                    self.my_lg.info('与数据库的新连接成功建立...')

                if self.my_pipeline.is_connect_success:
                    goods_id = taobao.get_goods_id_from_url(item.get('goods_url', ''))
                    if goods_id == '':
                        self.my_lg.info('@@@ 原商品的地址为: {0}'.format(item.get('goods_url', '')))
                        continue

                    else:
                        self.my_lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id, str(index)))
                        tt = taobao.get_goods_data(goods_id)
                        data = taobao.deal_with_data(goods_id=goods_id)
                        if data != {}:
                            data['goods_id'] = goods_id
                            data['goods_url'] = 'https://item.taobao.com/item.htm?id=' + str(goods_id)
                            data['username'] = '18698570079'
                            data['main_goods_id'] = None

                            # print('------>>>| 爬取到的数据为: ', data)
                            taobao.old_taobao_goods_insert_into_new_table(data, pipeline=self.my_pipeline)

                        else:
                            pass

                else:  # 表示返回的data值为空值
                    self.my_lg.info('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                index += 1
                gc.collect()
                await asyncio.sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)

        self.my_lg.info('该文章的商品已经抓取完毕!')

        return True

    async def _save_this_article(self, article):
        '''
        存储该文章info
        :param article:
        :return:
        '''
        sql_str = r'select share_id from dbo.daren_recommend'
        db_share_id = [j[0] for j in list(self.my_pipeline._select_table(sql_str=sql_str))]

        if article.get('share_id') in db_share_id:
            self.my_lg.info('该share_id({})已存在于数据库中, 此处跳过!'.format(article.get('share_id', '')))

            return True

        else:
            self.my_lg.info('即将开始存储该文章...')
            if self.my_pipeline.is_connect_success:
                params = await self._get_db_insert_params(item=article)
                # pprint(params)
                sql_str = r'insert into dbo.daren_recommend(nick_name, head_url, profile, share_id, gather_url, title, comment_content, share_goods_base_info, div_body, create_time, site_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                self.my_pipeline._insert_into_table_2(sql_str=sql_str, params=params, logger=self.my_lg)

                return True
            else:
                self.my_lg.error('db连接失败!存储失败! 出错article地址:{0}'.format(article.get('gather_url', '')))
                return False

    async def _get_db_insert_params(self, item):
        params = (
            item['nick_name'],
            item['head_url'],
            item['profile'],
            item['share_id'],
            item['gather_url'],
            item['title'],
            item['comment_content'],
            # dumps(item['share_img_url_list'], ensure_ascii=False),
            # dumps(item['goods_id_list'], ensure_ascii=False),
            dumps(item['share_goods_base_info'], ensure_ascii=False),
            item['div_body'],
            item['create_time'],
            item['site_id'],
        )

        return params

    async def _get_article(self, data, taobao_short_url):
        '''
        得到该文章的需求信息
        :param data:
        :return:
        '''
        try:
            nick_name = data.get('data', {}).get('models', {}).get('account', {}).get('name', '')
            assert nick_name != '', '获取到的nick_name为空值!'

            head_url = await self._get_head_url(data=data)

            # 推荐人的简介或者个性签名
            tmp_profile = data.get('data', {}).get('models', {}).get('account', {}).get('accountDesc', '')
            profile = tmp_profile if tmp_profile is not None else ''

            title = self._wash_sensitive_info(data.get('data', {}).get('models', {}).get('content', {}).get('title', ''))
            # self.my_lg.info(title)
            assert title != '', '获取到的title为空值!请检查!'

            # 达人的评论，可用于荐好首页的文字信息
            comment_content = self._wash_sensitive_info(data.get('data', {}).get('models', {}).get('content', {}).get('summary', ''))

            '''微淘抓包的接口: 图片，商品依次对应'''
            tmp_goods_list = data.get('data', {}).get('models', {}).get('content', {}).get('drawerList', [])
            assert tmp_goods_list != [], '获取到的goods_id_list为空list! 请检查! 可能该文章推荐商品为空[]!'

            share_img_url_list = [{'img_url': 'https:' + item.get('itemImages', [])[0].get('picUrl', '')} for item in tmp_goods_list]
            goods_id_list = [{'goods_id': item.get('itemId', '')} for item in tmp_goods_list]

            # 由于微淘的图片跟商品信息一一对应，so直接存一个字段, 清除重复的推荐商品(list去重，并保持原来的顺序)
            share_goods_base_info = list_duplicate_remove([{
                'img_url': 'https:' + item.get('itemImages', [])[0].get('picUrl', ''),
                'goods_id': item.get('itemId', ''),
            } for item in tmp_goods_list])

            # div_body
            div_body = self._wash_sensitive_info(await self._get_div_body(rich_text=data.get('data', {}).get('models', {}).get('content', {}).get('richText', [])))
            # print(div_body)

            # 待抓取的商品地址, 统一格式为淘宝的，如果是tmall地址, 浏览器会重定向到天猫
            goods_url_list = [{'goods_url': 'https://item.taobao.com/item.htm?id=' + item.get('goods_id', '')} for item in goods_id_list]

            _ = (await self._get_target_url_and_content_id_and_csid(taobao_short_url))
            gather_url = _[0]
            share_id = _[1]  # 即content_id

            create_time = get_shanghai_time()

            site_id = 2  # 淘宝微淘

            # tags 额外的文章地址
            tags = await self._get_tags(data=data)
            # pprint(tags)

        except Exception as e:
            self.my_lg.error('出错短链接地址:{0}'.format(taobao_short_url))
            self.my_lg.exception(e)
            return {}

        article = WellRecommendArticle()
        article['nick_name'] = nick_name
        article['head_url'] = head_url
        article['profile'] = profile
        article['share_id'] = share_id
        article['title'] = title
        article['comment_content'] = comment_content
        article['share_img_url_list'] = share_img_url_list
        article['goods_id_list'] = goods_id_list
        article['div_body'] = div_body
        article['gather_url'] = gather_url
        article['create_time'] = create_time
        article['site_id'] = site_id
        article['goods_url_list'] = goods_url_list
        article['tags'] = tags
        article['share_goods_base_info'] = share_goods_base_info

        return article

    async def _get_head_url(self, data):
        '''
        获取头像地址
        :param data:
        :return:
        '''
        tmp_head_url = data.get('data', {}).get('models', {}).get('account', {}).get('accountPic', {}).get('picUrl', '')
        if tmp_head_url != '':
            if re.compile('http').findall(tmp_head_url) == []:
                head_url = 'https:' + tmp_head_url
            else:
                head_url = tmp_head_url
        else:
            head_url = ''

        return head_url

    def _wash_sensitive_info(self, data):
        '''
        清洗敏感信息
        :param data:
        :return:
        '''
        data = re.compile('淘宝|天猫|taobao|tmall|TAOBAO|TMALL').sub('', data)

        return data

    async def _get_tags(self, data):
        '''
        获得额外文章的信息
        :param data:
        :return:
        '''
        tags = data.get('data', {}).get('models', {}).get('tags', [])
        tags = [{
            'url': unquote(item.get('url', '')),
            'name': item.get('name', ''),
        } for item in tags]

        return tags

    async def _get_div_body(self, rich_text):
        '''
        处理得到目标文章
        :param rich_text: 待处理的原文章
        :return:
        '''
        div_body = ''
        for item in rich_text:
            if item.get('resource') is None:
                continue

            for resource_item in item.get('resource', []):   # 可能是多个
                # resource = item.get('resource', [])[0]
                text = resource_item.get('text', '')         # 介绍的文字
                picture = resource_item.get('picture', {})   # 介绍的图片
                _goods = resource_item.get('item', {})       # 一个商品

                if text != '':
                    text = '<p style="height:auto;width:100%">' + text + '</p>' + '<br>'
                    div_body += text
                    continue

                if picture != {}:
                    # 得到该图片的宽高，并得到图片的<img>标签
                    _ = r'<img src="{0}" style="height:{1}px;width:{2}px;"/>'.format(
                        'https:' + picture.get('picUrl', ''),
                        picture.get('picHeight', ''),
                        picture.get('picWidth', '')
                    )
                    _ = _ + '<br>'
                    div_body += _
                    continue

                if _goods != {}:
                    _hiden_goods_id = r'<p style="display:none;">此处有个商品[goods_id]: {0}</p>'.format(_goods.get('itemId', '')) + '<br>'
                    div_body += _hiden_goods_id
                    continue

        return '<div>' + div_body + '</div>' if div_body != '' else ''

    async def _wash_api_info(self, data):
        '''
        清洗接口
        :param data:
        :return:
        '''
        try:
            data['data']['assets'] = []
            data['data']['models']['config'] = {}
            data['data']['modules'] = []
        except Exception:
            pass

        return data

    def __del__(self):
        try:
            del self.my_lg
            del self.msg
            del self.my_pipeline
        except: pass
        gc.collect()

# _short_url = 'http://m.tb.cn/h.WAjz5RP'
# _short_url = 'http://m.tb.cn/h.WA6JGoC'
_short_url = 'http://m.tb.cn/h.WA6Hp6H'

if __name__ == '__main__':
    while True:
        taobao_short_url = input('请输入淘宝短链接:').replace(';', '')
        weitao = TaoBaoWeiTaoShareParse()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(weitao._deal_with_api_info(taobao_short_url))
        try:
            del weitao
            loop.close()
        except:
            pass
        gc.collect()
        restart_program()  # 通过这个重启环境, 避免log重复打印
