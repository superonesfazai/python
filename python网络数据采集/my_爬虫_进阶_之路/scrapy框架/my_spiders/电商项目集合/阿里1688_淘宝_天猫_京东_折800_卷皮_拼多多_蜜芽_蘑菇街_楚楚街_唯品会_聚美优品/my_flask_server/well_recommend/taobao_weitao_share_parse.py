# coding:utf-8

'''
@author = super_fazai
@File    : taobao_weitao_share_parse.py
@Time    : 2018/5/26 12:18
@connect : superonesfazai@gmail.com
'''
import sys
sys.path.append('..')

from json import loads, dumps
import re
import asyncio
from logging import INFO, ERROR
from random import randint
import gc
from pprint import pprint

from my_logging import set_logger
from my_utils import (
    get_shanghai_time,
    get_taobao_sign_and_body,
    restart_program,
)
from settings import (
    MY_SPIDER_LOGS_PATH,
    HEADERS,
)
from my_requests import MyRequests
from my_items import WellRecommendArticle

class TaoBaoWeiTaoShareParse():
    def __init__(self, logger=None):
        self._set_headers()
        self._set_logger(logger)
        self.msg = ''

    def _set_headers(self):
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': HEADERS[randint(0, len(HEADERS)-1)],
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

        return target_url, content_id, csid

    async def _get_api_body(self, taobao_short_url):
        '''
        获取该页面api返回的文件
        :param taobao_short_url:
        :return: body 类型 str
        '''
        base_url = 'https://h5api.m.taobao.com/h5/mtop.taobao.beehive.detail.contentservicenewv2/1.0/'

        target_url, content_id, csid = await self._get_target_url_and_content_id_and_csid(taobao_short_url)
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
            pprint(data)
        except Exception as e:
            self.my_lg.error('出错短链接地址:{0}'.format(taobao_short_url))
            self.my_lg.exception(e)
            return {}

        try:
            nick_name = data.get('data', {}).get('models', {}).get('account', {}).get('name', '')
            assert nick_name != '', '获取到的nick_name为空值!'

            tmp_goods_list = data.get('data', {}).get('models', {}).get('content', {}).get('drawerList', [])
            assert tmp_goods_list != [], '获取到的goods_id_list为空list! 请检查! 可能该文章推荐商品为空[]!'

            share_img_url_list = [{'img_url': 'https:' + item.get('itemImages', [])[0].get('picUrl', '')} for item in tmp_goods_list]
            goods_id_list = [{'goods_id': item.get('itemId', '')} for item in tmp_goods_list]

            # div_body
            div_body = await self._get_div_body(rich_text=data.get('data', {}).get('models', {}).get('content', {}).get('richText', []))
            print(div_body)

            # 待抓取的商品地址
            goods_url_list = [{'goods_url': item.get('itemUrl', '')} for item in tmp_goods_list]

            gather_url = (await self._get_target_url_and_content_id_and_csid(taobao_short_url))[0]

            create_time = get_shanghai_time()

            site_id = 2     # 淘宝微淘

        except Exception as e:
            self.my_lg.error('出错短链接地址:{0}'.format(taobao_short_url))
            self.my_lg.exception(e)
            return {}

        article = WellRecommendArticle()
        article['nick_name'] = data

    async def _get_div_body(self, rich_text):
        '''
        处理得到目标文章
        :param rich_text: 待处理的原文章
        :return:
        '''
        div_body = ''
        for item in rich_text:
            resource = item.get('resource', [])[0]
            text = resource.get('text', '')         # 介绍的文字
            picture = resource.get('picture', {})   # 介绍的图片
            _goods = resource.get('item', {})       # 一个商品

            if text != '':
                text = text + '<br>'
                div_body += text
                continue

            if picture != {}:
                # 得到该图片的宽高，并得到图片的<img>标签
                _ = r'<img src="{0}" style="height:{1}px;width:{2}px;"/>'.format(
                    picture.get('picUrl', ''),
                    picture.get('picHeight', ''),
                    picture.get('picWidth', '')
                )
                _ = _ + '<br>'
                div_body += _

            if _goods != {}:
                _hiden_goods_id = r'<p style="display:none;">此处有个商品[goods_id]: {0}</p>'.format(_goods.get('itemId', '')) + '<br>'
                div_body += _hiden_goods_id

        return '<div>' + div_body + '</div>'

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
