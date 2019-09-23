# coding:utf-8

"""
@author = super_fazai
@File    : article_spider.py
@connect : superonesfazai@gmail.com
"""

"""
文章资讯爬虫obj

supported:
    1.  微信文章内容爬取(https://weixin.sogou.com)
    2.  简书文章内容爬取(https://www.jianshu.com)
    3.  今日头条文章内容爬取(https://www.toutiao.com)
    4.  搜狗头条(https://wap.sogou.com)
    5.  百度m站(https://m.baidu.com/)
    6.  qq看点文章内容爬取(根据QQ看点中分享出的地址)
    7.  天天快报(根据天天快报分享出的地址)
    8.  东方头条文章内容爬取(https://toutiao.eastday.com)
    9.  中青看点(https://focus.youth.cn/html/articleTop/mobile.html)
    10. 阳光宽频网(短视频)(https://www.365yg.com/)
    11. 凤凰网(https://news.ifeng.com/ | https://i.ifeng.com article m站都跳转到pc站, 故直接做pc)
    12. 51健康养生网(http://www.51jkst.com/)
    13. 彩牛养生网(权威医生: 对养生的见解, 短视频为主, 包含部分文章)(http://m.cnys.com/)
    14. 爱范儿(pc: https://www.ifanr.com/)
    15. 科学松鼠会(https://songshuhui.net/)
    16. 界面新闻(https://www.jiemian.com/)
    17. 澎湃网(https://m.thepaper.cn/)
    18. 虎嗅网(https://m.huxiu.com)
    19. 南方周末(http://www.infzm.com/wap/#/)
    20. 好奇心日报(http://m.qdaily.com/mobile/homes.html)
    21. 西瓜视频(短视频)(https://www.ixigua.com)
    22. 场库网(短视频)(https://www.vmovier.com/)
    23. 梨视频(短视频)(https://www.pearvideo.com/)
    24. 艾墨镇(短视频)(https://aimozhen.com/)
    25. 美拍(短视频)(https://www.meipai.com/)
    26. 百度好看视频(短视频)(https://haokan.baidu.com/)
    27. 七丽女性网(https://i.7y7.com/)
    28. 亲亲宝贝网(https://m.qbaobei.com/)
    29. 发条网(https://m.fatiao.pro/)
    30. 觅糖网(短视频or图文)(https://www.91mitang.com/)
    31. 雪球网(https://xueqiu.com)
    32. 5号女性网(http://m.5h.com/)
    33. 百思不得姐(http://www.budejie.com/)
    
not supported:
    1. 男人窝(https://m.nanrenwo.net/)
    2. 爱秀美(https://m.ixiumei.com/)
    3. yoka时尚网(http://www.yoka.com/dna/m/)
    4. 美妆网(http://www.chinabeauty.cn/)
    5. 新华网(http://m.xinhuanet.com)
    6. 36氪(https://36kr.com)
    7. 太平洋时尚网(https://www.pclady.com.cn/)
    8. 网易新闻
    9. cnbeta(https://m.cnbeta.com/)
    10. 少数派(https://sspai.com/)
    11. 经济日报(https://www.jingjiribao.cn)
    12. 中国青年网(http://m.youth.cn/)
    
news_media_ranking_url(https://top.chinaz.com/hangye/index_news.html)
"""

from os import getcwd
from os.path import abspath
from ftfy import fix_text
from requests import session
from my_items import WellRecommendArticle
from settings import (
    ARTICLE_ITEM_LIST,
    MY_SPIDER_LOGS_PATH,
    PHANTOMJS_DRIVER_PATH,
    FIREFOX_DRIVER_PATH,
    CHROME_DRIVER_PATH,
    IP_POOL_TYPE,)

from fzutils.spider.fz_driver import (
    PHANTOMJS,
    FIREFOX,
    CHROME,
    PC,
    PHONE,
    BaseDriver,)
from fzutils.internet_utils import _get_url_contain_params
from fzutils.data.list_utils import list_remove_repeat_dict_plus
from fzutils.spider.selector import (
    async_parse_field,
    parse_field,)
from fzutils.spider.async_always import *

class ArticleParser(AsyncCrawler):
    """article spider"""
    def __init__(self, logger=None, loop=None, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            logger=logger,
            is_new_loop=False,
            loop=loop,
            log_save_path=MY_SPIDER_LOGS_PATH + '/articles/_/',
            ip_pool_type=IP_POOL_TYPE)
        self.request_num_retries = 6
        # api data
        self.hook_target_api_data = None

    async def _parse_article(self, article_url) -> dict:
        """
        解析文章内容
        :param article_url: 待抓取文章的url
        :return:
        """
        # 设置obj_origin_dict
        self.obj_origin_dict = await self._get_obj_origin()
        child_debug = await self.is_child_can_debug(article_url)
        if not child_debug:
            self.lg.error('article_url未匹配到对象 or debug未开启!')
            return {}

        try:
            article_url_type = await self._judge_url_type(article_url=article_url)
            parse_obj = await self._get_parse_obj(article_url_type=article_url_type)
            # self.lg.info(article_url_type)
            # pprint(parse_obj)
        except (ValueError, NotImplementedError):
            # NotImplementedError: article_url未知!
            self.lg.error('遇到错误: ', exc_info=True)
            return {}

        article_html, video_url = await self._get_article_html(
            article_url=article_url,
            article_url_type=article_url_type)
        # self.lg.info(article_html)
        try:
            title = await self._get_article_title(
                parse_obj=parse_obj,
                target_obj=article_html,
                video_url=video_url)
            author = await self._get_author(
                parse_obj=parse_obj,
                target_obj=article_html,
                video_url=video_url)
            head_url = await self._get_head_url(
                parse_obj=parse_obj,
                target_obj=article_html,
                video_url=video_url,)
            content = await self._get_article_content(
                parse_obj=parse_obj,
                target_obj=article_html,
                article_url=article_url,
                video_url=video_url,)
            # print(content)
            create_time = await self._get_article_create_time(
                parse_obj=parse_obj,
                target_obj=article_html,
                video_url=video_url,
                article_url=article_url,)
            comment_num = await self._get_comment_num(parse_obj=parse_obj, target_obj=article_html)
            fav_num = await self._get_fav_num(parse_obj=parse_obj, target_obj=article_html)
            praise_num = await self._get_praise_num(parse_obj=parse_obj, target_obj=article_html)
            tags_list = await self._get_tags_list(
                parse_obj=parse_obj,
                video_url=video_url,
                target_obj=article_html)
            profile = await self._get_profile(parse_obj=parse_obj, target_obj=article_html)
            site_id = await self._get_site_id(article_url_type=article_url_type)
        except (AssertionError, Exception):
            self.lg.error('遇到错误:', exc_info=True, stack_info=False)
            return {}

        _ = WellRecommendArticle()
        _['nick_name'] = author
        _['head_url'] = head_url
        _['profile'] = profile
        _['share_id'] = await self._get_share_id(
            article_url_type=article_url_type,
            article_url=article_url,
            video_url=video_url,
            parse_obj=parse_obj,)
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
        _['comment_num'] = comment_num

        return dict(_)

    async def get_article_list_by_article_type(self, article_type: str) -> list:
        """
        根据文章类型获取article list
        :param article_type:
        :return:
        """
        if article_type == 'zq':
            return await self.get_zq_article_list()

        else:
            raise NotImplemented

    async def get_zq_article_list(self) -> list:
        """
        获取zq的article_list
        :return:
        """
        def get_tasks_params_list() -> list:
            tasks_params_list = []
            for page_num in range(1, 5):
                # 蹿红页, 默认只有4页
                tasks_params_list.append({
                    'type': '1',
                    'page_num': page_num,
                })

            for page_num in range(1, 2):
                # 七天页, 默认只有1页
                tasks_params_list.append({
                    'type': '2',
                    'page_num': page_num,
                })

            for page_num in range(1, 3):
                # 总榜页, 默认只有2页
                tasks_params_list.append({
                    'type': '3',
                    'page_num': page_num,
                })

            return tasks_params_list

        def get_create_task_msg(k) -> str:
            return 'create task[where zq: type: {}, page_num: {}]...'.format(
                k['type'],
                k['page_num'],
            )

        def get_now_args(k) -> list:
            return [
                k['page_num'],
                k['type'],
            ]

        all_res = await get_or_handle_target_data_by_task_params_list(
            loop=self.loop,
            tasks_params_list=get_tasks_params_list(),
            func_name_where_get_create_task_msg=get_create_task_msg,
            func_name=self.get_zq_shoot_to_fame_article_list_by_page_num,
            func_name_where_get_now_args=get_now_args,
            func_name_where_handle_one_res=None,
            func_name_where_add_one_res_2_all_res=default_add_one_res_2_all_res,
            one_default_res=[],
            step=self.concurrency,
            logger=self.lg,
            get_all_res=True,
            concurrent_type=0,
        )
        all_res = list_remove_repeat_dict_plus(
            target=all_res,
            repeat_key='article_id',
        )
        # pprint(all_res)
        self.lg.info('all_res_len: {}'.format(len(all_res)))

        return all_res

    @catch_exceptions_with_class_logger(default_res=[])
    def get_zq_shoot_to_fame_article_list_by_page_num(self, page_num: int, _type: str) -> list:
        """
        根据page_num 获取zq蹿红页的article_list
        :param page_num: 1开始
        :return:
        """
        headers = get_random_headers(
            user_agent_type=1,
            upgrade_insecure_requests=False,
            cache_control='',)
        headers.update({
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Origin': 'https://focus.youth.cn',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://focus.youth.cn/html/articleTop/mobile.html',
            'X-Requested-With': 'XMLHttpRequest',
        })
        data = dumps({
            'type': _type,
            'page': str(page_num),
            'catid': '0',
        })
        body = Requests.get_url_body(
            method='post',
            url='https://focus.youth.cn/WebApi/Article/top',
            headers=headers,
            data=data,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            num_retries=self.request_num_retries,)
        assert body != ''
        # self.lg.info(body)

        data = json_2_dict(
            json_str=body,
            logger=self.lg,
            default_res={},).get('data', {}).get('items', [])
        assert data != []
        # pprint(data)

        res = []
        for item in data:
            try:
                title = item.get('title', '')
                assert title != ''
                # 标题必须小于等于30
                assert len(title) <= 30
                article_id = item.get('id', '')
                video_play_url = item.get('video_play_url', '')
                assert article_id != ''
                # 跳过视频文章
                assert video_play_url == ''
                # 跳过无图的
                _extra = item.get('extra', [])
                assert _extra != []
                article_url = 'https://focus.youth.cn/mobile/detail/id/{}#'.format(article_id)
            except (AssertionError, Exception):
                continue

            res.append({
                # db中存储的uid eg: get_uuid3('zq::123')
                'uid': get_uuid3(target_str='{}::{}'.format('zq', article_id)),
                'article_type': 'zq',
                'title': title,
                'article_id': str(article_id),
                'article_url': article_url,
            })

        self.lg.info('[{}] zq::type:{}::page_num:{}'.format(
            '+' if res != [] else '-',
            _type,
            page_num,
        ))

        return res

    @staticmethod
    async def _get_obj_origin() -> dict:
        """
        设置obj_origin_dict
        :return:
        """
        return {
            'wx': {
                'debug': True,
                'name': '搜狗微信公众号(部分图片无法跨域下载)',
                'url': 'https://weixin.sogou.com',
                'obj_origin': 'mp.weixin.qq.com',
                'site_id': 4,
            },
            'tt': {
                'debug': True,
                'name': '今日头条',
                'url': 'https://www.toutiao.com',
                'obj_origin': 'www.toutiao.com',
                'site_id': 5,
            },
            'js': {
                'debug': True,
                'name': '简书',
                'url': 'https://www.jianshu.com',
                'obj_origin': 'www.jianshu.com',
                'site_id': 6,
            },
            'kd': {
                'debug': True,
                'name': 'qq看点',
                'url': '根据QQ看点中分享出的地址',
                'obj_origin': 'post.mp.qq.com',
                'site_id': 7,
            },
            'kb': {
                'debug': True,
                'name': '天天快报',
                'url': '根据天天快报分享出的地址',
                'obj_origin': 'kuaibao.qq.com',
                'site_id': 8,
            },
            'df': {
                'debug': True,
                'name': '东方头条',
                'url': 'https://toutiao.eastday.com',
                'obj_origin': 'toutiao.eastday.com',
                'site_id': 9,
            },
            'sg': {
                'debug': True,
                'name': '搜狗头条',
                'url': 'https://wap.sogou.com',
                'obj_origin': 'sa.sogou.com',
                'site_id': 10,
            },
            'bd': {
                'debug': True,
                'name': '百度m站',
                'url': 'https://m.baidu.com/',
                'obj_origin': 'm.baidu.com',
                'site_id': 11,
            },
            'zq': {
                'debug': True,
                'name': '中青看点',
                'url': 'https://focus.youth.cn/html/articleTop/mobile.html',
                'obj_origin': 'focus.youth.cn',
                'site_id': 12,
            },
            'fh': {
                'debug': True,
                'name': '凤凰网',
                'url': 'https://news.ifeng.com/',
                'obj_origin': 'news.ifeng.com',
                'site_id': 13,
            },
            'ys': {
                'debug': True,
                'name': '51健康养生网',
                'url': 'http://www.51jkst.com/',
                'obj_origin': 'www.51jkst.com',
                'site_id': 14,
            },
            'cn': {
                'debug': True,
                'name': '彩牛养生网(短视频)',
                'url': 'http://m.cnys.com/',
                'obj_origin': 'm.cnys.com',
                'site_id': 15,
            },
            'if': {
                'debug': True,
                'name': '爱范儿',
                'url': 'https://www.ifanr.com/',
                'obj_origin': 'www.ifanr.com',
                'site_id': 16,
            },
            'ss': {
                'debug': True,
                'name': '科学松鼠会',
                'url': 'https://songshuhui.net/',
                'obj_origin': 'songshuhui.net',
                'site_id': 17,
            },
            'jm': {
                'debug': True,
                'name': '界面新闻',
                'url': 'https://www.jiemian.com/',
                'obj_origin': 'www.jiemian.com',
                'site_id': 18,
            },
            'pp': {
                'debug': True,
                'name': '澎湃网',
                'url': 'https://m.thepaper.cn/',
                'obj_origin': 'm.thepaper.cn',
                'site_id': 19,
            },
            'hx': {
                'debug': True,
                'name': '虎嗅网',
                'url': 'https://m.huxiu.com',
                'obj_origin': 'm.huxiu.com',
                'site_id': 20,
            },
            'nfzm': {
                'debug': True,
                'name': '南方周末',
                'url': 'http://www.infzm.com/wap/#/',
                'obj_origin': 'www.infzm.com',
                'site_id': 21,
            },
            'hqx': {
                'debug': True,
                'name': '好奇心日报',
                'url': 'http://m.qdaily.com/mobile/homes.html',
                'obj_origin': 'm.qdaily.com',
                'site_id': 22,
            },
            'hk': {
                'debug': True,
                'name': '百度好看视频(短视频)',
                'url': 'https://haokan.baidu.com/',
                'obj_origin': 'haokan.baidu.com',
                'site_id': 23,
            },
            'xg': {
                'debug': True,
                'name': '西瓜视频(短视频)',
                'url': 'https://www.ixigua.com',
                'obj_origin': 'www.ixigua.com',
                'site_id': 24,
            },
            'yg': {
                'debug': True,
                'name': '阳光宽频网(短视频)',
                'url': 'https://www.365yg.com/',
                'obj_origin': 'www.365yg.com',
                'site_id': 25,
            },
            'ck': {
                'debug': True,
                'name': '场库网(短视频)',
                'url': 'https://www.vmovier.com/',
                'obj_origin': 'www.vmovier.com',
                'site_id': 26,
            },
            'lsp': {
                'debug': True,
                'name': '梨视频(短视频)',
                'url': 'https://www.pearvideo.com/',
                'obj_origin': 'www.pearvideo.com',
                'site_id': 27,
            },
            '91mt': {
                'debug': True,
                'name': '觅糖网',
                'url': 'https://www.91mitang.com',
                'obj_origin': 'www.91mitang.com',
                'site_id': 28,
            },
            'amz': {
                'debug': False,
                'name': '艾墨镇(短视频)',
                'url': 'https://aimozhen.com/',
                'obj_origin': 'aimozhen.com',
                'site_id': 29,
            },
            'mp': {
                'debug': True,
                'name': '美拍(短视频)',
                'url': 'https://www.meipai.com/',
                'obj_origin': 'www.meipai.com',
                'site_id': 30,
            },
            '7y7': {
                'debug': True,
                'name': '七丽女性网(部分图片无法跨域下载)',
                'url': 'https://i.7y7.com/',
                'obj_origin': 'i.7y7.com',
                'site_id': 31,
            },
            'qqbb': {
                'debug': True,
                'name': '亲亲宝贝网',
                'url': 'https://m.qbaobei.com/',
                'obj_origin': 'm.qbaobei.com',
                'site_id': 32,
            },
            'ft': {
                'debug': False,
                'name': '发条网',
                'url': 'https://m.fatiao.pro/',
                'obj_origin': 'fatiao.pro',
                'site_id': 33,
            },
            'xq': {
                'debug': False,
                'name': '雪球网',
                'url': 'https://xueqiu.com',
                'obj_origin': 'xueqiu.com',
                'site_id': 34,
            },
            '5h': {
                'debug': False,
                'name': '5号女性网',
                'url': 'http://m.5h.com/',
                'obj_origin': 'm.5h.com',
                'site_id': 35,
            },
            'bdj': {
                'debug': False,
                'name': '百思不得姐',
                'url': 'http://www.budejie.com',
                'obj_origin': 'www.budejie.com',
                'site_id': 36,
            },
        }

    async def get_article_spiders_intro(self) -> str:
        """
        获取可用文章爬虫介绍
        :return:
        """
        _ = await self._get_obj_origin()
        intro_str = '<tr><th>index</th><th>name</th><th>url</th></tr>'
        order_list = [value for value in _.values()]
        order_list.sort(key=lambda k: (k.get('site_id', 0)))

        index = 1
        for item in order_list:
            try:
                debug = item.get('debug', False)
                name = item.get('name', '')
                assert name != ''
                url = item.get('url', '')
            except AssertionError:
                self.lg.error('遇到错误:', exc_info=True)
                continue

            if debug:
                a, b = index, name
                if re.compile('^http').findall(url) != []:
                    c = '<a href=\"{}\" target=\"_blank\">{}</a>'.format(url, url)
                else:
                    c = url
                intro_str += '<tr><th>{}</th><th>{}</th><th>{}</th></tr>'.format(
                    a,
                    b,
                    c,)
                index += 1

            else:
                continue

        res = '<style type=\"text/css\">table{border-collapse: collapse;margin: 0 auto;text-align: center;}table td, table th{border: 1px solid #cad9ea;color: #666;height: 30px;}table thead th{background-color: #CCE8EB;width: 100px;}table tr:nth-child(odd){background: #fff;}table tr:nth-child(even){background: #F5FAFA;}</style>' \
            + '<table border=\"1\">' + intro_str + '</table>'

        return res

    async def _get_html_by_driver(self,
                                  url,
                                  _type=PHANTOMJS,
                                  load_images=False,
                                  headless=False,
                                  user_agent_type=PC,
                                  exec_code='',
                                  css_selector='',
                                  timeout=20,):
        """
        使用driver获取异步页面
        :return:
        """
        if _type == PHANTOMJS:
            executable_path = PHANTOMJS_DRIVER_PATH
        elif _type == FIREFOX:
            executable_path = FIREFOX_DRIVER_PATH
        else:
            raise ValueError('_type value 异常!')

        body = await unblock_request_by_driver(
            url=url,
            type=_type,
            executable_path=executable_path,
            ip_pool_type=self.ip_pool_type,
            load_images=load_images,
            headless=headless,
            user_agent_type=user_agent_type,
            exec_code=exec_code,
            css_selector=css_selector,
            timeout=timeout,
            logger=self.lg,)

        return body

    def unblock_get_wx_article_html(self, article_url) -> tuple:
        """
        得到wx文章内容
        :return: body, video_url
        """
        body = Requests.get_url_body(
            url=article_url,
            headers=get_random_headers(),
            ip_pool_type=self.ip_pool_type,)
        # self.lg.info(body)
        assert body != '', '获取到wx的body为空值!'

        return self._wash_wx_article_body(
            article_url=article_url,
            body=body)

    async def _get_tt_article_html(self, article_url) -> tuple:
        """
        得到头条文章内容
        :param article_url:
        :return: body, video_url
        """
        headers = await async_get_random_headers()
        headers.update({
            'authority': 'www.toutiao.com',
            'referer': 'https://www.toutiao.com/',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg,)
        # self.lg.info(str(body))
        assert body != '', '获取到wx的body为空值!'

        return body, ''

    async def _get_js_article_html(self, article_url) -> tuple:
        """
        得到简书文章html
        :param article_url:
        :return:
        """
        headers = await async_get_random_headers()
        headers.update({
            'authority': 'www.jianshu.com',
            'referer': 'https://www.jianshu.com/',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            # https代理太慢, 直接http
            # proxy_type=PROXY_TYPE_HTTPS,
            num_retries=self.request_num_retries,
            logger=self.lg,)
        assert body != '', '获取到的js的body为空值!'
        # self.lg.info(str(body))

        return body, ''

    @staticmethod
    async def _wash_tt_article_content(content) -> str:
        """
        清洗头条文章的content内容
        :return: body, video_url
        """
        content = content[6:-6]
        # print(content)
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('\\\\u003C', '<'),
                ('\\\\u003E', '>'),
                ('\\\\u002F', '/'),
                # 下面2个过滤顺序不能调换
                ('&quot;', '"'),
                ('\\\\"', '"'),

                ('&#x3D;', '='),
                ('&nbsp;', ' '),
                ('&#160;', ' '),
                ('&lt;', '<'),
                ('&#60;', '<'),
                ('&gt;', '>'),
                ('&#62;', '>'),
                ('&amp;', '&'),
                ('&#38;', '&'),
                ('&#34;', '"'),
            ],
            add_sensitive_str_list=None,
            is_default_filter=False,
            is_lower=False,)

        # print(content)
        # 最初有效, 后面无效
        # content = fix_text(text=content[6:-6])
        # print(content)
        # 图片设置居中
        content = re.compile(' inline=\"0\">').sub(' style=\"height:auto;width:100%;\">', content)

        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_js_article_content(content) -> str:
        """
        清洗简书文章的content内容
        :param content:
        :return:
        """
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                (' data-original-src=', ' src='),
                (' data-original-filesize=\".*?\"', ' style=\"height:auto;width:100%;\"'),
                ('<img src=\"\/\/', '<img src=\"http://'),
            ],
            add_sensitive_str_list=[
                '<div class=\"image-caption\">图片发自简书App</div>',
            ],
            is_default_filter=False,
            is_lower=False,)

        # 直接处理到原js
        _ = '<style type="text/css">.ant-back-top{-webkit-box-sizing:border-box;box-sizing:border-box;margin:0;padding:0;color:rgba(0,0,0,.65);font-size:14px;font-variant:tabular-nums;line-height:1.5;list-style:none;-webkit-font-feature-settings:"tnum","tnum";font-feature-settings:"tnum","tnum";position:fixed;right:100px;bottom:50px;z-index:10;width:40px;height:40px;cursor:pointer}.ant-back-top-content{width:40px;height:40px;overflow:hidden;color:#fff;text-align:center;background-color:rgba(0,0,0,.45);border-radius:20px}.ant-back-top-content,.ant-back-top-content:hover{-webkit-transition:all .3s cubic-bezier(.645,.045,.355,1);transition:all .3s cubic-bezier(.645,.045,.355,1)}.ant-back-top-content:hover{background-color:rgba(0,0,0,.65)}.ant-back-top-icon{width:14px;height:16px;margin:12px auto;background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACQAAAAoCAYAAACWwljjAAAABGdBTUEAALGPC/xhBQAAAbtJREFUWAntmMtKw0AUhhMvS5cuxILgQlRUpIggIoKIIoigG1eC+AA+jo+i6FIXBfeuXIgoeKVeitVWJX5HWhhDksnUpp3FDPyZk3Nm5nycmZKkXhAEOXSA3lG7muTeRzmfy6HneUvIhnYkQK+Q9NhAA0Opg0vBEhjBKHiyb8iGMyQMOYuK41BcBSypAL+MYXSKjtFAW7EAGEO3qN4uMQbbAkXiSfRQJ1H6a+yhlkKRcAoVFYiweYNjtCVQJJpBz2GCiPt7fBOZQpFgDpUikse5HgnkM4Fi4QX0Fpc5wf9EbLqpUCy4jMoJSXWhFwbMNgWKhVbRhy5jirhs9fy/oFhgHVVTJEs7RLZ8sSEoJm6iz7SZDMbJ+/OKERQTttCXQRLToRUmrKWCYuA2+jbN0MB4OQobYShfdTCgn/sL1K36M7TLrN3n+758aPy2rrpR6+/od5E8tf/A1uLS9aId5T7J3CNYihkQ4D9PiMdMC7mp4rjB9kjFjZp8BlnVHJBuO1yFXIV0FdDF3RlyFdJVQBdv5AxVdIsq8apiZ2PyYO1EVykesGfZEESsCkweyR8MUW+V8uJ1gkYipmpdP1pm2aJVPEGzAAAAAElFTkSuQmCC) 100%/100% no-repeat}@media screen and (max-width:768px){.ant-back-top{right:60px}}@media screen and (max-width:480px){.ant-back-top{right:20px}}.ant-affix{position:fixed;z-index:10}._3VRLsv{-webkit-box-sizing:content-box;box-sizing:content-box;width:1000px;padding-left:16px;padding-right:16px;margin-left:auto;margin-right:auto}._3Z3nHf,.ouvJEz{background-color:#fff;border-radius:4px;margin-bottom:10px;-webkit-box-shadow:0 1px 3px rgba(26,26,26,.1);box-shadow:0 1px 3px rgba(26,26,26,.1)}body.reader-night-mode ._3Z3nHf,body.reader-night-mode .ouvJEz{background-color:#3d3d3d;-webkit-box-shadow:0 1px 3px rgba(0,0,0,.3);box-shadow:0 1px 3px rgba(0,0,0,.3)}._3kbg6I{background-color:#f9f9f9}body.reader-night-mode ._3kbg6I{background-color:#2d2d2d}._3VRLsv{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;-webkit-box-align:start;-ms-flex-align:start;align-items:flex-start;min-height:calc(100vh - 66px);padding-top:10px;font-size:16px}._gp-ck{-ms-flex-negative:0;flex-shrink:0;width:730px;margin-bottom:24px;margin-right:10px}.ouvJEz{padding:24px}._2OwGUo{-ms-flex-negative:0;flex-shrink:0;width:260px}._3Z3nHf{padding:16px}.QxT4hD{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-pack:justify;-ms-flex-pack:justify;justify-content:space-between;-webkit-box-align:center;-ms-flex-align:center;align-items:center;margin-bottom:16px;padding-left:12px;border-left:4px solid #ec7259;font-size:18px;font-weight:500;height:20px;line-height:20px}._3yfjDE{-webkit-box-orient:vertical;-webkit-box-direction:normal;-ms-flex-direction:column;flex-direction:column;height:calc(100vh - 56px)}._3yfjDE,.l3_euy{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center}.l3_euy{margin-bottom:32px;padding-bottom:48px;border-bottom:1px solid #eee}body.reader-night-mode .l3_euy{border-color:#2f2f2f}._23lAnl{width:280px;height:280px;margin-right:48px}._2msktx{font-size:24px;font-weight:500;margin-bottom:8px}._1gKcub{font-size:14px;width:400px;line-height:1.7}._2QxXJ4{display:-webkit-box;display:-ms-flexbox;display:flex}._2QxXJ4,._3Fatyw{-webkit-box-align:center;-ms-flex-align:center;align-items:center}._3Fatyw{display:-webkit-inline-box;display:-ms-inline-flexbox;display:inline-flex;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;font-size:14px}._3Fatyw>i{font-size:18px;margin-right:4px}._3Fatyw+._3Fatyw{margin-left:120px}._16zCst,._26qd_C{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;height:56px}.FTZkZo{-webkit-box-sizing:content-box;box-sizing:content-box;width:1000px;padding-left:16px;padding-right:16px;margin-left:auto;margin-right:auto;display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-pack:justify;-ms-flex-pack:justify;justify-content:space-between;height:56px}._16zCst{max-width:730px;overflow:hidden;padding:0 24px}._2zeTMs{margin:0;font-size:24px;font-weight:700;overflow:hidden;-o-text-overflow:ellipsis;text-overflow:ellipsis;white-space:nowrap}._26qd_C{-ms-flex-negative:0;flex-shrink:0}.qzhJKO{display:-webkit-inline-box;display:-ms-inline-flexbox;display:inline-flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}._2JlnTn{width:40px;height:40px;border-radius:50%}._22gUMi{color:#7d7d7d;margin:0 10px}._1bCFo7{width:320px;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}._3PUMf1{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;height:32px}._2W7JCU{width:8px;height:8px;background-color:#8c8c8c;margin:0 5px;border-radius:50%;cursor:pointer;-webkit-transition:background-color .1s;-o-transition:background-color .1s;transition:background-color .1s}._2W7JCU:hover{background-color:#737373}._2W7JCU._1je2YA{background-color:#595959;pointer-events:none}body.reader-night-mode ._2W7JCU:hover{background-color:#a6a6a6}body.reader-night-mode ._2W7JCU._1je2YA{background-color:#bfbfbf}._3F7sjs{width:100%;display:-webkit-box;display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}._3F7sjs,._3kPlPc{-ms-flex-negative:0;flex-shrink:0}._3kPlPc{display:-webkit-inline-box;display:-ms-inline-flexbox;display:inline-flex;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;font-size:24px;color:#404040;width:32px;height:32px;padding:4px;border-radius:4px;cursor:pointer;overflow:hidden}._3kPlPc:hover{background-color:rgba(51,51,51,.1)}body.reader-night-mode ._3kPlPc:hover{background-color:#4d4d4d}body.reader-night-mode ._2SihW7,body.reader-night-mode ._5g0jij .ant-dropdown-menu-sub{background-color:#3d3d3d}._5g0jij .ant-dropdown-menu-submenu-title{padding:8px 20px 8px 12px;color:#666}._5g0jij .ant-dropdown-menu-submenu-title:hover{background-color:rgba(236,114,89,.1)}body.reader-night-mode ._5g0jij .ant-dropdown-menu-submenu-title{color:#a6a6a6}body.reader-night-mode ._5g0jij .ant-dropdown-menu-submenu-title:hover{background-color:#303030}._5g0jij .ant-dropdown-menu-submenu-arrow{top:7px;right:8px}._5g0jij .ant-dropdown-menu-submenu-arrow-icon{color:#666}body.reader-night-mode ._5g0jij .ant-dropdown-menu-submenu-arrow-icon{color:#a6a6a6}._1SgxkY{padding:8px 12px;color:#666}._1SgxkY:hover{background-color:rgba(236,114,89,.1)}body.reader-night-mode ._1SgxkY{color:#a6a6a6}body.reader-night-mode ._1SgxkY:hover{background-color:#303030}._1Jdfvb{-webkit-box-sizing:content-box;box-sizing:content-box;width:1000px;padding-left:16px;padding-right:16px;margin-left:auto;margin-right:auto}.W2TSX_{background-color:#f2f2f2}.W2TSX_::-webkit-input-placeholder{color:#999}.W2TSX_::-moz-placeholder{color:#999}.W2TSX_:-ms-input-placeholder{color:#999}.W2TSX_::-ms-input-placeholder{color:#999}.W2TSX_::placeholder{color:#999}body.reader-night-mode .W2TSX_{background-color:#333}._1LI0En{position:relative;display:block}._2xr8G8{position:fixed;left:0;right:0;bottom:0;background-color:#fff;-webkit-box-shadow:0 -1px 3px rgba(26,26,26,.1);box-shadow:0 -1px 3px rgba(26,26,26,.1);z-index:100}body.reader-night-mode ._2xr8G8{background-color:#3d3d3d;-webkit-box-shadow:0 -1px 3px rgba(0,0,0,.3);box-shadow:0 -1px 3px rgba(0,0,0,.3)}._1Jdfvb{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;padding-top:10px;padding-bottom:10px}._1Jdfvb.ufcbR-{-webkit-box-align:end;-ms-flex-align:end;align-items:flex-end}._1Jdfvb.ufcbR- .W2TSX_{width:560px;height:56px;padding-right:80px;border-radius:4px}.TDvCqd{display:-webkit-box;display:-ms-flexbox;display:flex;position:relative}.TDvCqd[focus-within] .W2TSX_{will-change:width,height,padding-right,border-radius}.TDvCqd:focus-within .W2TSX_{will-change:width,height,padding-right,border-radius}.W2TSX_{display:-webkit-inline-box;display:-ms-inline-flexbox;display:inline-flex;width:200px;height:36px;resize:none;margin-right:16px;padding:8px 18px;border-radius:18px;border:none;-webkit-transition:all .2s cubic-bezier(.19,.4,.17,.85);-o-transition:all .2s cubic-bezier(.19,.4,.17,.85);transition:all .2s cubic-bezier(.19,.4,.17,.85)}._2qhU6p{position:absolute;right:16px;bottom:8px;font-size:20px;margin-right:12px;color:#969696}._2qhU6p:hover{color:#7d7d7d}.-pXE92{color:#969696;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}.-pXE92,._3nj4GN{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}._3nj4GN{font-size:14px;cursor:pointer}._3nj4GN>span{margin-left:8px;line-height:20px}._3nj4GN .anticon{font-size:22px}._3nj4GN:not(:last-child){margin-right:12px}._3nj4GN._3oieia{color:#ec7259}.rEsl9f{-webkit-box-pack:justify;-ms-flex-pack:justify;justify-content:space-between;-webkit-box-align:center;-ms-flex-align:center;align-items:center;margin-bottom:32px;color:#969696;font-size:13px}.rEsl9f,.s-dsoj{display:-webkit-box;display:-ms-flexbox;display:flex}.s-dsoj>:not(:last-child){margin-right:8px}._3tCVn5{display:-webkit-inline-box;display:-ms-inline-flexbox;display:inline-flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;color:#ec7259}._3tCVn5 i{margin-right:.5em}._3_y8t4{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;width:100%;margin:20px 0;padding:8px 16px;border-radius:4px;background-color:#f2f2f2}body.reader-night-mode ._3_y8t4{background-color:#4d4d4d}._3_y8t4._1cBl4m,body.reader-night-mode ._3_y8t4._1cBl4m{background-color:rgba(218,158,85,.1)}._3_y8t4._1cBl4m ._1NiROM{background-image:url(data:image/png;base64,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);-webkit-animation:none;animation:none}._1NiROM{-ms-flex-negative:0;flex-shrink:0;width:32px;height:32px;cursor:pointer;background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHAAAABwCAMAAADxPgR5AAAAgVBMVEUAAADrcFrqb1vqb1rrb1rrcFrrcFvvc1/rcFrucVzrb1rrb1ruc1z4dGXxdWDrb1rrcVzrcVzscVv/lGvrcFvtcVvscVvscFvscF3velv/gHzrb1rrcFvscVzrcFvtcVzrcFvqcFvrcFztcVzzeV/rb1vqb1rqb1rrcFzrcFvqb1ocs5f0AAAAKnRSTlMA+8fo7c5wH98k5JYsCxinTEp5BLJSgms2DwbawELyOtKfZGATjPi4i4l1OaSPAAAD10lEQVRo3rTY2ZaqMBAF0BOMzGCDIoPtrG2b///A+5AS0fZqCsJ+d9WiKqeSJXiCzI0uzs6XQkh/51wiNwswkiQ7T3/UCz/Tc5bAsnjpCPWGcJYxrEndqTIwdVPYsF4IZUgs1hjqy1EszheGKJ57KZ19Xmxj79Q0Jy/eFvnekc+dLdBX/K26wtnRwwvecRaqru+4Xwyu3dmt8uBtPvNVd5bXBGxZ2GlkVOGjKpKdbmTgmf92flwmhj0pQ9X6nYPBc+69PDQw1hzunXU8RhakIht3zmyNu1FEGiekFIrMUrClM0VECSNLRfx1z93kK7KEgUiRRY2e6oUiET66NUS4GMAVt6GYft+kwiDVRGmR2fz8AAMFvskcy9sCTjFYelv85Zv8Cdq+NSyoafeL/+bRk/R9Nayo6Rulh5fmDs0vhSUpzdF5va5oX08CWBNMaJPjhYw6XsGiik5Fhj8SulpcWOXSFZfg2ZX2GSyjLXfFk1joA1PDstrXk4rxiDKzhnVryjYeFO2qtY+ugwJdOqKbFCNIN3qdPOw0/gnln9TuhtM7ZjXHKOYrvW/+zPWAkRzoRD5lJWwwkiZ8zHgq6N4aTamzmD4MVSYYTSIfDuXU9IFVRLMyQR9RNxmxHmllthbDAj1UukbceTitDAahLTzw6WQsOyHM8cm3IpucH9j8HsVEn9EAn4SqtduCKdDnNGnXWoiPJqpjfwJP2K63M90TvIJKHvrcGec2FEdGQeLEYDi2wdD/n3n8gkqcGaH09P9yt2lKsAtyQynpbGa6PeyC3FBS+jJapHt2QXYo97ROI4o9tyA7lDlt7Au9cLgFuaGkd9qFWrtlF2SHckuHZUdrnFuQHcpY9x8+xXBgQSVyoyD6FI/TsIImB+9Egdd3RTOsoMkbpdGN+Fe9tawwDMMwSumaso21DMYeZTvslv//wF10C4PIdlxXPxAIUSJLiuGCeapZ0HBL81izpRaHBljrDo2eFkAaq2ihJn610wnia682IC21V5vu8ga627P68lY9T8A6Ec+T4gEG+i/1AIslBtAdH5zEkIooYLiTIkouExEysDJRLoRBPV4I81IfeC0Cqb8ww0xfUo8fZphxrS+ox49r1ECaCurxAyk1cl8K6vEjN2UqnN6gntxUIG2Tz5BzOlwVtgltDI2Tzhjytr7czT1v+9LdoPW2oN1Ndu8YwT0o8Y6Ctg+7Gsd5EQLLppFsjNC5XawepzjQphoRq/xhX2+JV+CxrSjFLGHZ1cziFulsqoKxy5DquuceCq3yyu6eSsl87XqPxXL/6jxwnv9/DpgJGnh/f/gBFVizjSPxtMoAAAAASUVORK5CYII=);background-position:50%;background-repeat:no-repeat;background-size:cover}._30e-qR{background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHAAAABwCAMAAADxPgR5AAAAjVBMVEUAAADsblrqcFrqblrrblrpbVnrb1rrb1r7hXPvdF/rcFvqb1vrcFvrcFvrb1rtclzucl/5dWTrcFrrcFvvclzqcVzte17rcFvscVvscFvscVvrcVvscF3vdV7rb1rrb1vscFztcVzscVvrb1rwd17rcFvscVvqb1rrcFvrcFvqb1rqb1rrcFvsb1vqb1rZDUZoAAAALnRSTlMAZZnaMk2z+gUYz8eMcO0sHwrheSJJDaGCbFJLNhPkxEE5KKgQsEOU2PLpuL9arCjQDwAABLlJREFUaN681wl2qjAUBuAfqBBmkMGxdcSh9mX/y3s95IK0B2JQ6LcAQ+6UK/pJM1+/bZxpYFnB1NncdD9LMZI88xyLt7AcL8sxsHDuWlzCcuchBmP7Dlfg+DaGsDUtrsgyt3jVyuW9uCu8Yvk7loE7S5a7MHpn7D0Kd8tk5ga/I7vEs8Iv3vQx0yK0iLTZB2/6CvGM2Gvm7pLsIbFPLs1cejF6y6aNQJ7XeGh9bgR3mqEf5jVCuYihJF40Qusx9BDda9PQGJQxzbjXawRlk4CTq8/QC/OvnAQTKFrwysFGb/aBVxZQMq8zf8JTTlNO5lCgc1Ic8aRjwYmOh6qAWD5e4FtVUlTv97nGS9afXNDV8mekeFFq1HlUqE/Hxsts53GtTriwyTGAfMOFCTpEAd0vxyByumMQoRVzKX82BmJTHl2GNh7VZ4rBpFSrHlpk1H9rDGhN/Zi1vC00j3wMyqcpGXcFtMDAio6ghpb4kiMGdhSRs0L8RPvSCYM70WaFH5b1qB0ePQdLNIkWvdoYgX0V4wQNK0mFDlapK9y5YsQwKLK9zcazoYiJgeOituUlTfk81/jmKp+o8dIWFVPsnwyKPKPkQRET+6oJYlv0bqnaGKUN+u2Blv0jqUEMVQaBqjigomz2xBnjHYhzszNCXlqPeeCal8LG4nTBmAfiQgvVvQkTdDv6B/0kL5q3RTKJ0S25t2IuanSPTlH5eUXe3RZxYn7TbXTaizrN67H28fhJu6RdjW+fzZIsSqIVV/XLO5MElJNg2z7awoNJJEGd1e+w82ispbxyDdEiOpgVSUy1ujFECiN0o9WrKw6+WZmhWySSWH1/oPYH1UAL3axMICGGTYqM6lXG48RBC88kGmRc2hd9ipXUP0vyQi/NUrGF1Ix+Qae2l3srd69bjBZsXuYvBZG2vo4bbTgPxElRaAytWJYkyxhytKfdKLQ7jG5HxeLQGB9dSGU3pTYcGzXilNrjHaN7p4YXBc8wOkaj5q8P/POQKhRN/J84M2hxGASiMMoIEQomNA3dzUqjlPaU///3tlTroz044yHpd6sUwuiM8+ZpR0fRM0l/PJzV0vNJw5aFdZSwVfNfJw4ntiwu9cLvqVA55+tdv1jrhX9hrraOgK+oQA18/WpjLm8v+2DQINQvb6Y9eZJtqQZ/THtCA2a2lEuazH1gGjAkRjVEx5aFTiyMxGBF1DS62F87gT9Cv8fzT+REFGTipkAmQghvCoQwpP6GQOqf3ocZHkshdvg50LzI3E4MMxjXBJB5cJtKnqzqAfKSH9caB9LePAml+tSTKB9IG0fum0nkTe1UYpWP3G2mQm8yQy5RlYlNpgJsE2mApeetCFFum8iNIW8ysWyUylihMdRmfUWTmMv/BpUhmfXVaO6NJuGwFFTCycy9RvtymNMJlrNGiJPUvpQbtAjRvi0hQN6gbbegPQWaPpYWs1iZBb27yb73M8LuDyV7PwV9/7Hrv3o7NAIABoEgGI/H0H+fUUhECD9zfBu3L855hGApTbKM6KzL6hw4oKERLPwxz1t4gGeWKDER1hwz40K6GSrIxpDf3HMDaO2T3U0o+Z1db4TlYjpfz6M+B4QfxfL+YHl/sMb94QKtd3ujrQOdfAAAAABJRU5ErkJggg==);-webkit-animation:spinning 1s linear infinite;animation:spinning 1s linear infinite}._2qk-7T{background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHAAAABwCAMAAADxPgR5AAAAgVBMVEUAAADrb1rrcFvqb1vscFvrcVzrb1rscFvwdF//in7rb1rrcFvqcFrrb1vrcFvuc1zvc17rb1rrcFvrcFrrcFvrb1vrcVvwc1zyeVzse17/c2bscF3rcFvrb1rrcFvrcFvscVvrcVvtcVztcFvscVvsclvscF3tcV3rb1zsc1vqb1qqgzfAAAAAKnRSTlMA+s/HcEvtZhgF8+LelosrH+fIvbaheSISDQo2wKjVsIOBYVRRQ0I5JzXOPizQAAADRklEQVRo3ryX23qrIBCFB0ED1lMOxlPbpDlv3v8B98UQMW00GoH/rh/1mzBr1gJgGoXP4g31ooCQIPLoJmZ+AZao/MQj8gnES/wKDJPuKZEDELpPwRiceXIEHuNggsuGyJGQzQXm4lM5CerDHI6/exnQfHu6plkpRJml19M2p8Hvzh7fn5RP2WWZHzJ4QnbIl7LL53vzUydd7b63Nxjgtv3uapnUb4j30Wlk3MBLmrjT3I+pUoqk8zGrR/aEdX5kImACmZ7NaDHhS7GI9LxmE9rZNidkYmJrWNgKMbqtC3nni8Nk+Je8s4BR/LTineEtzq2UPzCCWCp2JbxJuZOKGF5ybwhhMANG7qKM3d+ygVk0S73HMfpFBcykiLSOr+fT4zAb7r2eVf+evhUYoLpnf68fs0DtrwIjVGqPQU/mCKr042AIrnSkAp6RqPkswBiFmtVkQEDSgEEa0itjrfKIgVGYSsm6r6E7MMyup6kpwV9SgmFK7BxJ4RHlmTMY56y8DQ8cddSaRR8HR+iCFg05WICHGCdPLMHACuyvNShGjAArCAwcCi0XHevm0YeQfuls0BICLCHQGptWVWJTQa0i4Q9/BvVgV1ZhuFpMX0Pq4GFL3svLB1+jCms+aU0Td52R4gf/oJ+1VKwnrWka/BfMtz2+x15NGbIYXOsHX3P7jgm30M9KtqwG1/rZaitWOKM36CeULeHgWj83nNOqjbUlDCA7DK4NsMR4a0/e3HbBHM/h1hQH2wUPrTFQwsx2wQxFBCgwZsB2QcCwKdTMUPsFqZoahjNjv2Cu4jRG29sviNaP1Vl4sl/whGeiau3VfsErDouyYWq/YKqMGKEN7RdEI0bKHqX9giUaXgWNsF9QYNQ4L+i8pc6HxrktnBvfebQ5D2/nx5PzA9j5FcP1Jcr5NdH5Rdj5Vd/5Y8b5c839g1Q/uf9XbwdVAIQwEEOFrAL8G9wzJx7QCakABDD5/YgvNz0q4LMJPgzR0xc+7tHzJT7Q0hM0PrLTGQEPJXQKeh+7wjnPECyjSdYRnXNZ3QMHMjTChT/qeYsP8NQSJSfCqmNmXkgHUMEVhhzrB2PGkH7ueQVau5DdM5TcjV3vwfKudD5wHACeP/zOAcLuAXk0BwAAAABJRU5ErkJggg==)}._35-1od{-webkit-box-flex:1;-ms-flex-positive:1;flex-grow:1;margin:0 16px;overflow:hidden}._2aoc2_{font-size:14px;font-weight:500;margin-bottom:2px;overflow:hidden;-o-text-overflow:ellipsis;text-overflow:ellipsis;white-space:nowrap}.iWiJE9{font-size:12px}._2z_B4K{color:#da9e55;margin-right:8px}._1jirLm,._3u_PHG{color:#969696}._1jirLm{-ms-flex-negative:0;flex-shrink:0;font-size:13px}@-webkit-keyframes _2cozGY{0%{-webkit-transform:rotate(0deg);transform:rotate(0deg)}to{-webkit-transform:rotate(1turn);transform:rotate(1turn)}}@keyframes _2cozGY{0%{-webkit-transform:rotate(0deg);transform:rotate(0deg)}to{-webkit-transform:rotate(1turn);transform:rotate(1turn)}}.video-package{display:block;width:100%;margin-bottom:20px;border:1px solid #eee;background-color:hsla(0,0%,60%,.15);-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}body.reader-night-mode .video-package{border-color:#2f2f2f}.video-package:after{content:"";display:block;width:110px;height:110px;background-color:rgba(0,0,0,.4);background-image:url(data:image/png;base64,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);background-position:50%;background-size:50%;background-repeat:no-repeat;-webkit-transition:all .1s linear;-o-transition:all .1s linear;transition:all .1s linear}.video-package br{display:none}.video-package .video-description{padding:10px;line-height:32px;max-height:110px;overflow:hidden;-o-text-overflow:ellipsis;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;float:left;margin-left:110px}.H8iPN2{display:-webkit-box;display:-ms-flexbox;display:flex;width:100%;margin-bottom:20px;border:1px solid #eee;background-color:hsla(0,0%,60%,.15);-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}body.reader-night-mode .H8iPN2{border-color:#2f2f2f}._1paJhJ{position:relative;cursor:pointer}._1paJhJ,._1paJhJ>img{width:110px;height:110px}._1paJhJ>img{min-width:110px;min-height:110px}._1paJhJ:hover:after{background-color:rgba(0,0,0,.2)}._1paJhJ:after{position:absolute;top:0;left:0;content:"";display:block;width:110px;height:110px;background-color:rgba(0,0,0,.4);background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFgAAABYCAYAAABxlTA0AAANJUlEQVR4Ae2dCVCU5xnHYUEEb8QTtYqjqEGJOtY7mpkotRKtZByJR62tJDFV422mdmpba00VdJogE5PYycSoDY4H1QHjwTROvGujolCDjrfgfYVLQez/v/HZeRf4ll3Yb/fbZXcGnve73vd9fvt+7/m8z/r7GeTz/Plz0/Hjx/vWr18/OiQk5CX8RTZo0KBTvXr1GgUGBjZ48RfC7JaVlRXjr4h/paWlBUVFRZeLi4tz8Zfz5MmTrP79+3/n7+9fbgTV/N2ZiSNHjgxo2rRpbLNmzV5t0aJFH8J0Rn4I/e7duycfPnz4zaNHj9IHDRp0zBnxekQchw8f7nX+/PmUgoKCfJRal3yYFtNk2q6G5JISDIoBWVlZs9u3b5/QvHnzKC0l8ao/uHPnztXbt2/nXblyJT87O5vyBxwX37hxowThYj7bsWPHkHbt2gW3atUqBOHGUVFR4ZBtcRzesmXLn6BqCdVK4/79+9nXr19fHx0dnYxq5JnWfc46rytglJr6JSUlCyMiImY1bNiwTcVM81W+fPny2VOnTmVv3bo1e8uWLTcr3lOT4wkTJrQZP358VO/evaM6derUs6qqp7Cw8OalS5fWBgcHJ3Xt2vVJTdKx5xndAKPEzu/SpcsSNFZhakZQmsug2KmMjIxvly5d+t2DBw90LUWhoaEBy5Yt6zt69OhX8EX3RqkNVPODhvHehQsXVqBEr1HPOyvsdMBHjx4dCLCfhoWFWdV3T58+fXzgwIGvFy9evB8ltsBZCjgSD0p0o1WrVo0YPnz4qKCgoCbqs/fu3TsD0G8PHDjwqHq+tmGnAUbJDLp48eI6lJKpKCUBkjGUkAf79+9PnzlzZua1a9d0exUlPXtkhw4d6qekpLw2YsSIWLxhlvoaOjzD27Whc+fO70CHUnviqu4epwBGqX0pMjJyO17HbpIgqwK02unx8fE70EA9lfNGkmgog1JTU+MGDx4cq1YdqLa+xycO3bv/1Ta/tQZ88uTJBLTif0dD0lAyk5eXl42q4PNNmzblyTkjy8mTJ4ej6vh1eHi4pYeDBrgQvZi5ffr0WV+bvNcKML7lj1ByZ0sGysvLy3bt2rV53LhxX8s5T5JpaWmjxowZM8lkMlkawtzc3ORu3bq9V1M9TDV5EK+/CXXVVypcdOZvz50794+eCpccmHfqQF2EC3WkrtRZzjkiHS7B7NuiI5+O1+k1SQiN1+mRI0d+hBJtHgjIeU+VKLEh+/btm4PGMFp0QLWXiYFQrKN9ZocA81tEQntVuOfOnTs0YMCAdY8fP9a1PyuKuko2adIk4NixYzO6d+8+RNIkZOgegwbR7okkh4o9Rl2bVbjIwO6ePXumeBtcAqVO1I06CmDqTgZybI+0GzAbNAw74yVSJoxO+ZfPnnlVwRX1zJK6UUcVMhmQhdWNNg7sqiLYFcMo6DOJh9UCv11vhiu6UgYEBPidPXt2plpdYDT6lj1duGpLMAcR7OdKgmjQsljn1hW41Ju6UmfqLhzIhGzkWEvaBIxGrR5HaDKIYPcFvYUPvbHO1QIk56kzdZcuHJmQDRnJPVVJm4Axt/CJDH85iFiyZMmH3tIVqwpGdeeoOxmQBe8lGzKy9ZxmHcxZMaxtHZSJG4xyvoiLi9tjK7K6cm3Hjh0/w6DkV9QXJfgZ1hKHas3CaQLGmlaWTDlybgETI3+tKwDt0RMTWL9Ht808d8GpTqwpWgYl6vNVVhGcLBe4+IbKFi5c+Ln6kC/s58fJLLIhC7Iis6q4VCrBHAqjtN6QlYhDhw79a+jQoalVPVzXzx08eDB+yJAhvyAHroygVLerOJSuVIK5hiZwOVnO+dy6DlJLf7IhI14nM7KreK8VYBT5AC5Qyk1ciTDqZLnk0Z2SbMhI8kB2ZCjHlFaAubQuq79cQ+Myj3qzL1yZABmRFa+QHRmqd1kBpt2CXOQCpVHW0CRPRpRkRFaSN5Uhz1kAo98bLUYhbB25+isPuUKuXLnyZdgqJMPUKSk9Pf11Lre7Il1npEFW0qMgQ9WCyAIYXY0ZkhjtFly9tD5r1qwETOSHYR42HDYMk2DFk5iUlNRH8mRkSVZkJnmEdZGFpQVw27Zt4+QGGoVI2FWScNW0Gjdu3GbBggWLMP/6Plrrtuo1I4ZVZmD5huTR3A/msBizRUd4kuZMrVu3fldvixvJgEi8YpoT2Xz9kMc9U6dO3Q7jEEMuS7FKu3Xr1sdipoU55EEcPptLMF7L0aIobcVcDVfS1pK0WYCNQuyZM2fWbNy4cTjnZ432ITOyk3wJUzNg2ufKBdQn2RI2moShXlPYMLyTn5+/HNVHV6PlT2UnTE14/Uw0fpbM0spRwkaVaEQ6owH8EwxD3oWdWTOj5FNlR6Zk64+6oh+mJf/DTNI+F53lme7IsK062FZ+sI2gBKOptEmTJqUboWpDVzNF7JMxjflTE/dEiAI0fpawp0js3QgeNWrUm+jWJa1evbqvu/OtMiRbEyYpLOtKtCx3dwZrmj66da3nz5+/8OrVq+9PnDgxvKbx1PY5lSHZEnCkRIpSkC9hT5WwxnkZRod/Q7duCi10XK2HypBsTagvOkkmuCdCwp4s2a1Dv3706dOn1wD2qzC2rjTvrZd+KkOyNUnHmAmC/g96JeyOeFEHNkXj9zamFf+yaNEil3TrVIZka+IGP1Geu3kk7E0SXabOsP/9c05Ozm/17tapDMnWCjC+6RJvAltRlx49egzNzMxcs2LFCkvPqeI9tT1WGQpgS0OA4u2VJViFhmF28OzZs3+jnnNmWGUIwCHmobIzE/CQuFzW6Jm4sVqgcAelhL1VYrawKDk5+R966acyJFsCLpLEuD1Vwl4oy7Fe9m8ss8+D+VOWXvqpDMk2UAXMvb96JezOeG/evJm7fPnyL7A37pLe+VAZmgFzgl0S5cZqCXuD5OQV9j9vTkhIOOQqc1uVIdkGIhOXxUyKu9YBNsfT4cL6sRS+KDKmTJmShklwl+4ufcHQjJBsA2GZkitAQd/wa1+SVy0JoP+dN2/el7AGva11j57nVYZkS8CWEkt/C3omrmfcMJDOQx27Qc8GzJ78qwzJNpA+buRBOrOQsKdINiS7d+/ejupgjxEs71WGZGuiAyFp6DgTT2cWHgL3OTamfDNs2LD5Y8eOzTACXLKT1QwyJVsTN9XRgZBApacQCRtVYkLl/Jw5c/7Qq1evT9GYPTZKPlV2ZEq25k3P9M4EY4lXmFG6YYEwpNEf6jR2u76aPn36t67qdjny5b1gZ36ETBkwz0Xg9cown8U/+rgxml0YN53AEHwX9uYtmDZtmiHhkhnZCUe6E2PYDJgWKHQSxBOcJKaPG4aN8EG36yTqtsWwsv8ndvQYdjqVzGTxgizFV5tlNg3GHNsFKB0ISdhVEp3ye2paeKvyExMTV8GoOXHbtm3mL1+9brSwykxlaQGMnTKfSKahFKqT3k7xwidxVifXrl27npABNg/mqxvxusEqdLHFYrG65915nazITPKApft1EraaFwXks2IjDH8JW2JiYtLkRp/UJrB3795x2AU6gXfQ8R2mHix1saUE8yI94lHyQ9dX9M7045HvvxYBMiIrua4y5DkrwHQ3KI0d/YrR9ZU86JNVEyAj8cFGdmSo3mkFGB1j+g1bKzfQrxgmkIPk2CetCZANGclZsiNDOaa0AswT9OWIDr25RYdlSij9ivG871OZANmQEa+QGdlVvKsSYO5UpC9HuZFO29xp6yX5MJqkrzWykXyRWcVdnrxm1YuQmyl9m8FVGpXDsH+o+WZwRkdHmbDZNdcn3FVOp22Vk6mbZ8hCdtqTEVlpkahURciNHD6j0t4gx/SIB4ONCDmuq5IMyEL0JyMtXxG8R7OK4EV8O/VgNX4GExlmp590p9KvX7/f1VWvJzSHPXHixAeNGjVqRT5g8z3Y9ELPQdNTq2YJZgR8EL4b38DkcSGPGTE94tFpG4/r0oc6U3eBSyYoaHG24JKPTcC8AcU/h15IGeaH7gaxr2OGEbdS/ZhD5/+nrtSZukvsZGKP+9tqATNC+gejF1KJnP7DMD/7Szn2dkldVZ9pZGGPzzRysVkHVwSHCj0Vs1zmSQ1ew7e6G6ZIXuv9jyWXcGEt/3Nhgfnp1IiIiDfluDrpEGA0ej7noHo6B0WFXo4521h6IZVvjq8OVncXuWPDieTB2ZK6UCe1WqDO1J0MHEnPrjpYjZDDQXSyY/iqyHlW/uy+eEM/mTpQF7VBo67UuaqhsDDQkg5VERUjQTelkovxnTt3bvJUB3Z0OAcbi8ludzEuoPEqvYcN0G9JP5kZo0c8jtM9aYKIeWWemXeBS52oG3UUfWsia1WCJUFs+vO6n3ngAItjANGxptIpgJk4Hdrh2/8YXRjfD5Uo34bTAEucKM2+n9oRGJBOByxx05ej78eidARM0L6fO9MZsJRmjADr7A/2CQOXSd9PTroMtZ8fG0R6Z9LzR1NpOWprxUFvdXVr5BzNOCeSvPFnf/8PDtJFz61AWfoAAAAASUVORK5CYII=);background-position:50%;background-size:50%;background-repeat:no-repeat;-webkit-transition:all .1s linear;-o-transition:all .1s linear;transition:all .1s linear}._3_y-pA{padding:10px;line-height:32px;max-height:110px;overflow:hidden;-o-text-overflow:ellipsis;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-flex:1;-ms-flex-positive:1;flex-grow:1}._3_y-pA,._3nROLh{-webkit-box-orient:vertical}._3nROLh{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-direction:normal;-ms-flex-direction:column;flex-direction:column;-webkit-box-align:start;-ms-flex-align:start;align-items:flex-start;margin-bottom:20px}._10T2go{border:none}.ISr9-J{cursor:pointer;font-size:14px;margin-top:4px}._2rhmJa code,._2rhmJa pre,._2rhmJa pre[class*=language-]{font-family:Consolas,Monaco,"Andale Mono","Ubuntu Mono",monospace;font-size:12px}._2rhmJa{font-weight:400;line-height:1.8;margin-bottom:20px}._2rhmJa h1,._2rhmJa h2,._2rhmJa h3,._2rhmJa h4,._2rhmJa h5,._2rhmJa h6{font-weight:700;margin:0 0 16px}._2rhmJa h1{font-size:26px}._2rhmJa h2{font-size:24px}._2rhmJa h3{font-size:22px}._2rhmJa h4{font-size:20px}._2rhmJa h5{font-size:18px}._2rhmJa h6{font-size:16px}._2rhmJa p{margin-bottom:20px;word-break:break-word}._2rhmJa hr{margin:0 0 20px;border:0;border-top:1px solid #eee!important}body.reader-night-mode ._2rhmJa hr{border-color:#2f2f2f!important}._2rhmJa blockquote{padding:20px;background-color:#fafafa;border-left:6px solid #e6e6e6;word-break:break-word;font-size:16px;font-weight:normal;line-height:30px;margin:0 0 20px}body.reader-night-mode ._2rhmJa blockquote{background-color:#595959;border-color:#262626}._2rhmJa blockquote h1:last-child,._2rhmJa blockquote h2:last-child,._2rhmJa blockquote h3:last-child,._2rhmJa blockquote h4:last-child,._2rhmJa blockquote h5:last-child,._2rhmJa blockquote h6:last-child,._2rhmJa blockquote li:last-child,._2rhmJa blockquote ol:last-child,._2rhmJa blockquote p:last-child,._2rhmJa blockquote ul:last-child{margin-bottom:0}._2rhmJa blockquote .image-package{width:100%;margin-left:0}._2rhmJa ol,._2rhmJa ul{word-break:break-word;margin:0 0 20px 20px}._2rhmJa ol li,._2rhmJa ul li{line-height:30px}._2rhmJa ol li ol,._2rhmJa ol li ul,._2rhmJa ul li ol,._2rhmJa ul li ul{margin-top:16px}._2rhmJa ol{list-style-type:decimal}._2rhmJa ul{list-style-type:disc}._2rhmJa code{padding:2px 4px;border:none;vertical-align:middle;white-space:pre-wrap}._2rhmJa :not(pre) code{color:#c7254e;background-color:#f2f2f2}body.reader-night-mode ._2rhmJa :not(pre) code{background-color:#262626}._2rhmJa pre,._2rhmJa pre[class*=language-]{word-wrap:normal;word-break:break-all;white-space:pre;overflow:auto;margin-bottom:20px;border-radius:4px;padding:1em;line-height:1.5;color:#ccc;background:#2d2d2d}._2rhmJa pre[class*=language-] code,._2rhmJa pre code{padding:0;background-color:rgba(0,0,0,0);white-space:pre}._2rhmJa table{width:100%;margin-bottom:20px;border-collapse:collapse;border:1px solid #eee;border-left:none;word-break:normal}body.reader-night-mode ._2rhmJa table,body.reader-night-mode ._2rhmJa table td,body.reader-night-mode ._2rhmJa table th{border-color:#2f2f2f}._2rhmJa table td,._2rhmJa table th{padding:8px;border:1px solid #eee;line-height:20px;vertical-align:middle}._2rhmJa table th{font-weight:bold}._2rhmJa table thead th{vertical-align:middle;text-align:inherit}._2rhmJa table tr:nth-of-type(2n){background-color:hsla(0,0%,70.2%,.15)}._2rhmJa table .image-package{width:100%;margin-left:0}._2rhmJa img{max-width:100%}._2rhmJa .image-package{width:100%;margin:0;padding-bottom:25px;text-align:center;font-size:0}._2rhmJa .image-package img{max-width:100%;width:auto;height:auto;vertical-align:middle;border:0}body.reader-night-mode ._2rhmJa .image-package img{opacity:.85}._2rhmJa .image-package .image-container{position:relative;z-index:95;background-color:#e6e6e6;-webkit-transition:background-color .1s linear;-o-transition:background-color .1s linear;transition:background-color .1s linear;margin:0 auto}body.reader-night-mode ._2rhmJa .image-package .image-container{background-color:#595959}._2rhmJa .image-package .image-container-fill{z-index:90}._2rhmJa .image-package .image-container .image-view{position:absolute;top:0;left:0;width:100%;height:100%;overflow:hidden}._2rhmJa .image-package .image-container .image-view-error{cursor:pointer;color:grey}body.reader-night-mode ._2rhmJa .image-package .image-container .image-view-error{color:#b3b3b3}._2rhmJa .image-package .image-container .image-view-error:after{content:"\56FE\7247\83B7\53D6\5931\8D25\FF0C\8BF7\70B9\51FB\91CD\8BD5";position:absolute;top:50%;left:50%;width:100%;-webkit-transform:translate(-50%,-50%);-ms-transform:translate(-50%,-50%);transform:translate(-50%,-50%);color:inherit;font-size:14px}._2rhmJa .image-package .image-container .image-view img.image-loading{opacity:.3}._2rhmJa .image-package .image-container .image-view img{-webkit-transition:all .15s linear;-o-transition:all .15s linear;transition:all .15s linear;z-index:95;opacity:1}._2rhmJa .image-package .image-caption{min-width:20%;max-width:80%;min-height:43px;display:inline-block;padding:10px;margin:0 auto;border-bottom:1px solid #eee;font-size:13px;color:#999}._2rhmJa .image-package .image-caption:empty{display:none}body.reader-night-mode ._2rhmJa .image-package .image-caption{border-color:#2f2f2f}._2rhmJa .math-block[mathimg="1"]{display:block;margin:1em auto}._2rhmJa .math-inline[mathimg="1"]{display:inline;margin:0 3px;vertical-align:middle}._2rhmJa .math-block[mathimg="1"],._2rhmJa .math-inline[mathimg="1"]{max-width:100%}body.reader-night-mode ._2rhmJa .math-block[mathimg="1"],body.reader-night-mode ._2rhmJa .math-inline[mathimg="1"]{-webkit-filter:invert(.8);filter:invert(.8)}._3GbnS5{padding:0;line-height:1.5;position:relative;width:100%;height:1px;margin:20px 0;border:none;border-top:#b3b3b3;display:table;white-space:nowrap;text-align:center}._3GbnS5:after,._3GbnS5:before{content:"";display:table-cell;position:relative;top:50%;left:0;width:50%;border-top:1px solid;border-top-color:inherit;-webkit-transform:scaleY(.5) translateY(50%);-ms-transform:scaleY(.5) translateY(50%);transform:scaleY(.5) translateY(50%);-webkit-transform-origin:50% 50% 0;-ms-transform-origin:50% 50% 0;transform-origin:50% 50% 0;-webkit-transform-origin:initial;-ms-transform-origin:initial;transform-origin:initial}._2Lt-af{display:inline-block;padding:0 12px;font-size:14px;font-weight:normal;text-align:center;white-space:nowrap;color:#b3b3b3;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}._2Lt-af>a{margin-left:.5em}._19DgIp{width:100%;height:1px;margin:16px 0;background-color:#eee}body.reader-night-mode ._19DgIp{background-color:#2f2f2f}._23ISFX{position:relative;display:block;margin:0 auto}._23ISFX-mask{position:fixed;top:0;right:0;left:0;bottom:0;background-color:rgba(0,0,0,.5);height:100vh;filter:alpha(opacity=50);z-index:1000}._23ISFX-mask-hidden{display:none}._23ISFX-wrap{position:fixed;top:0;right:0;bottom:0;left:0;z-index:1050;overflow:auto;outline:0;-webkit-overflow-scrolling:touch}._23ISFX-wrap-middle{text-align:center}._23ISFX-wrap-middle:before{content:"";display:inline-block;width:0;height:100%;vertical-align:middle}._23ISFX-wrap-middle ._23ISFX{position:static;display:inline-block;text-align:left;vertical-align:middle}._23ISFX-content{position:relative;background-color:#fff;border-radius:4px;-webkit-box-shadow:0 2px 8px rgba(26,26,26,.1);box-shadow:0 2px 8px rgba(26,26,26,.1)}body.reader-night-mode ._23ISFX-content{background-color:#3d3d3d}._23ISFX-close{position:absolute;top:0;right:0;margin:0;padding:0;border:0;outline:0;color:grey;background-color:rgba(0,0,0,0);cursor:pointer;text-decoration:none}._23ISFX-close-x{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;width:48px;height:48px;font-size:16px}._23ISFX-close:hover{color:#4d4d4d}body.reader-night-mode ._23ISFX-close:hover{color:#b3b3b3}._23ISFX-header{border-bottom:1px solid #eee;border-radius:4px 4px 0 0}._23ISFX-title{margin:0;font-size:18px;font-weight:bold}._23ISFX-body{line-height:1.5;word-wrap:break-word}._23ISFX-footer{border-top:1px solid #eee;border-radius:4px 4px 0 0;text-align:right}._23ISFX-footer,._23ISFX-header{padding:16px 24px}body.reader-night-mode ._23ISFX-footer,body.reader-night-mode ._23ISFX-header{border-color:#2f2f2f}._23ISFX.zoom-appear,._23ISFX.zoom-enter{-webkit-transform:none;-ms-transform:none;transform:none;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}.KdlMNE{height:480px;overflow-y:scroll;padding:0 24px}._2cxUIy{margin:0;padding:0;list-style:none}.LtPwLP{margin-bottom:16px;padding-bottom:16px;display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-pack:justify;-ms-flex-pack:justify;justify-content:space-between;-webkit-box-align:center;-ms-flex-align:center;align-items:center;border-bottom:1px solid #eee}.LtPwLP>div{min-height:100px;-webkit-box-flex:1;-ms-flex-positive:1;flex-grow:1}.LtPwLP img{width:150px;height:100px;border-radius:4px;border:1px solid #f2f2f2;-ms-flex-negative:0;flex-shrink:0}._2ssoa1{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;margin:30px 0;line-height:20px;border-radius:30px;background-color:#f2f2f2}body.reader-night-mode ._2ssoa1{background-color:#333}._2bdkP8{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;width:33.33%;height:60px;font-size:14px;font-weight:bold}._3dvb2i{height:20px;color:#8c8c8c;font-weight:normal;border-left:1px solid #eee;border-right:1px solid #eee;cursor:pointer}body.reader-night-mode ._3dvb2i{border-color:#2f2f2f}.ant-select{-webkit-box-sizing:border-box;box-sizing:border-box;color:rgba(0,0,0,.65);font-size:14px;font-variant:tabular-nums;line-height:1.5;-webkit-font-feature-settings:"tnum","tnum";font-feature-settings:"tnum","tnum";position:relative;display:inline-block;outline:0}.ant-select,.ant-select ol,.ant-select ul{margin:0;padding:0;list-style:none}.ant-select>ul>li>a{padding:0;background-color:#fff}.ant-select-arrow{display:inline-block;color:inherit;font-style:normal;line-height:0;text-align:center;text-transform:none;vertical-align:-.125em;text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;position:absolute;top:50%;right:11px;margin-top:-6px;color:rgba(0,0,0,.25);font-size:12px;line-height:1;-webkit-transform-origin:50% 50%;-ms-transform-origin:50% 50%;transform-origin:50% 50%}.ant-select-arrow>*{line-height:1}.ant-select-arrow svg{display:inline-block}.ant-select-arrow:before{display:none}.ant-select-arrow .ant-select-arrow-icon{display:block}.ant-select-arrow .ant-select-arrow-icon svg{-webkit-transition:-webkit-transform .3s;transition:-webkit-transform .3s;transition:transform .3s;transition:transform .3s,-webkit-transform .3s}.ant-select-selection{display:block;-webkit-box-sizing:border-box;box-sizing:border-box;background-color:#fff;border:1px solid #d9d9d9;border-top:1.02px solid #d9d9d9;border-radius:4px;outline:none;-webkit-transition:all .3s cubic-bezier(.645,.045,.355,1);transition:all .3s cubic-bezier(.645,.045,.355,1);-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}.ant-select-selection:hover{border-color:#fa9e87;border-right-width:1px!important}.ant-select-focused .ant-select-selection,.ant-select-selection:active,.ant-select-selection:focus{border-color:#fa9e87;border-right-width:1px!important;outline:0;-webkit-box-shadow:0 0 0 2px rgba(236,114,89,.2);box-shadow:0 0 0 2px rgba(236,114,89,.2)}.ant-select-selection__clear{position:absolute;top:50%;right:11px;z-index:1;display:inline-block;width:12px;height:12px;margin-top:-6px;color:rgba(0,0,0,.25);font-size:12px;font-style:normal;line-height:12px;text-align:center;text-transform:none;background:#fff;cursor:pointer;opacity:0;-webkit-transition:color .3s ease,opacity .15s ease;transition:color .3s ease,opacity .15s ease;text-rendering:auto}.ant-select-selection__clear:before{display:block}.ant-select-selection__clear:hover{color:rgba(0,0,0,.45)}.ant-select-selection:hover .ant-select-selection__clear{opacity:1}.ant-select-selection-selected-value{float:left;max-width:100%;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}.ant-select-no-arrow .ant-select-selection-selected-value{padding-right:0}.ant-select-disabled{color:rgba(0,0,0,.25)}.ant-select-disabled .ant-select-selection{background:#f5f5f5;cursor:not-allowed}.ant-select-disabled .ant-select-selection:active,.ant-select-disabled .ant-select-selection:focus,.ant-select-disabled .ant-select-selection:hover{border-color:#d9d9d9;-webkit-box-shadow:none;box-shadow:none}.ant-select-disabled .ant-select-selection__clear{display:none;visibility:hidden;pointer-events:none}.ant-select-disabled .ant-select-selection--multiple .ant-select-selection__choice{padding-right:10px;color:rgba(0,0,0,.33);background:#f5f5f5}.ant-select-disabled .ant-select-selection--multiple .ant-select-selection__choice__remove{display:none}.ant-select-selection--single{position:relative;height:32px;cursor:pointer}.ant-select-selection--single .ant-select-selection__rendered{margin-right:24px}.ant-select-no-arrow .ant-select-selection__rendered{margin-right:11px}.ant-select-selection__rendered{position:relative;display:block;margin-right:11px;margin-left:11px;line-height:30px}.ant-select-selection__rendered:after{display:inline-block;width:0;visibility:hidden;content:".";pointer-events:none}.ant-select-lg{font-size:16px}.ant-select-lg .ant-select-selection--single{height:40px}.ant-select-lg .ant-select-selection__rendered{line-height:38px}.ant-select-lg .ant-select-selection--multiple{min-height:40px}.ant-select-lg .ant-select-selection--multiple .ant-select-selection__rendered li{height:32px;line-height:32px}.ant-select-lg .ant-select-selection--multiple .ant-select-arrow,.ant-select-lg .ant-select-selection--multiple .ant-select-selection__clear{top:20px}.ant-select-sm .ant-select-selection--single{height:24px}.ant-select-sm .ant-select-selection__rendered{margin-left:7px;line-height:22px}.ant-select-sm .ant-select-selection--multiple{min-height:24px}.ant-select-sm .ant-select-selection--multiple .ant-select-selection__rendered li{height:16px;line-height:14px}.ant-select-sm .ant-select-selection--multiple .ant-select-arrow,.ant-select-sm .ant-select-selection--multiple .ant-select-selection__clear{top:12px}.ant-select-sm .ant-select-arrow,.ant-select-sm .ant-select-selection__clear{right:8px}.ant-select-disabled .ant-select-selection__choice__remove{color:rgba(0,0,0,.25);cursor:default}.ant-select-disabled .ant-select-selection__choice__remove:hover{color:rgba(0,0,0,.25)}.ant-select-search__field__wrap{position:relative;display:inline-block}.ant-select-search__field__placeholder,.ant-select-selection__placeholder{position:absolute;top:50%;right:9px;left:0;max-width:100%;height:20px;margin-top:-10px;overflow:hidden;color:#bfbfbf;line-height:20px;white-space:nowrap;text-align:left;text-overflow:ellipsis}.ant-select-search__field__placeholder{left:12px}.ant-select-search__field__mirror{position:absolute;top:0;left:0;white-space:pre;opacity:0;pointer-events:none}.ant-select-search--inline{position:absolute;width:100%;height:100%}.ant-select-search--inline .ant-select-search__field__wrap{width:100%;height:100%}.ant-select-search--inline .ant-select-search__field{width:100%;height:100%;font-size:100%;line-height:1;background:rgba(0,0,0,0);border-width:0;border-radius:4px;outline:0}.ant-select-search--inline>i{float:right}.ant-select-selection--multiple{min-height:32px;padding-bottom:3px;cursor:text;zoom:1}.ant-select-selection--multiple:after,.ant-select-selection--multiple:before{display:table;content:""}.ant-select-selection--multiple:after{clear:both}.ant-select-selection--multiple .ant-select-search--inline{position:static;float:left;width:auto;max-width:100%;padding:0}.ant-select-selection--multiple .ant-select-search--inline .ant-select-search__field{width:.75em;max-width:100%}.ant-select-selection--multiple .ant-select-selection__rendered{height:auto;margin-bottom:-3px;margin-left:5px}.ant-select-selection--multiple .ant-select-selection__placeholder{margin-left:6px}.ant-select-selection--multiple .ant-select-selection__rendered>ul>li,.ant-select-selection--multiple>ul>li{height:24px;margin-top:3px;line-height:22px}.ant-select-selection--multiple .ant-select-selection__choice{position:relative;float:left;max-width:99%;margin-right:4px;padding:0 20px 0 10px;overflow:hidden;color:rgba(0,0,0,.65);background-color:#fafafa;border:1px solid #e8e8e8;border-radius:2px;cursor:default;-webkit-transition:padding .3s cubic-bezier(.645,.045,.355,1);transition:padding .3s cubic-bezier(.645,.045,.355,1)}.ant-select-selection--multiple .ant-select-selection__choice__disabled{padding:0 10px}.ant-select-selection--multiple .ant-select-selection__choice__content{display:inline-block;max-width:100%;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;-webkit-transition:margin .3s cubic-bezier(.645,.045,.355,1);transition:margin .3s cubic-bezier(.645,.045,.355,1)}.ant-select-selection--multiple .ant-select-selection__choice__remove{color:inherit;font-style:normal;line-height:0;text-align:center;text-transform:none;vertical-align:-.125em;text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;position:absolute;right:4px;color:rgba(0,0,0,.45);font-weight:bold;line-height:inherit;cursor:pointer;-webkit-transition:all .3s;transition:all .3s;display:inline-block;font-size:12px;font-size:10px\9;-webkit-transform:scale(.83333333) rotate(0deg);-ms-transform:scale(.83333333) rotate(0deg);transform:scale(.83333333) rotate(0deg)}.ant-select-selection--multiple .ant-select-selection__choice__remove>*{line-height:1}.ant-select-selection--multiple .ant-select-selection__choice__remove svg{display:inline-block}.ant-select-selection--multiple .ant-select-selection__choice__remove:before{display:none}.ant-select-selection--multiple .ant-select-selection__choice__remove .ant-select-selection--multiple .ant-select-selection__choice__remove-icon{display:block}:root .ant-select-selection--multiple .ant-select-selection__choice__remove{font-size:12px}.ant-select-selection--multiple .ant-select-selection__choice__remove:hover{color:rgba(0,0,0,.75)}.ant-select-selection--multiple .ant-select-arrow,.ant-select-selection--multiple .ant-select-selection__clear{top:16px}.ant-select-allow-clear .ant-select-selection--single .ant-select-selection-selected-value{padding-right:16px}.ant-select-allow-clear .ant-select-selection--multiple .ant-select-selection__rendered,.ant-select-show-arrow .ant-select-selection--multiple .ant-select-selection__rendered{margin-right:20px}.ant-select-open .ant-select-arrow-icon svg{-webkit-transform:rotate(180deg);-ms-transform:rotate(180deg);transform:rotate(180deg)}.ant-select-open .ant-select-selection{border-color:#fa9e87;border-right-width:1px!important;outline:0;-webkit-box-shadow:0 0 0 2px rgba(236,114,89,.2);box-shadow:0 0 0 2px rgba(236,114,89,.2)}.ant-select-combobox .ant-select-arrow{display:none}.ant-select-combobox .ant-select-search--inline{float:none;width:100%;height:100%}.ant-select-combobox .ant-select-search__field__wrap{width:100%;height:100%}.ant-select-combobox .ant-select-search__field{position:relative;z-index:1;width:100%;height:100%;-webkit-box-shadow:none;box-shadow:none;-webkit-transition:all .3s cubic-bezier(.645,.045,.355,1),height 0s;transition:all .3s cubic-bezier(.645,.045,.355,1),height 0s}.ant-select-combobox.ant-select-allow-clear .ant-select-selection:hover .ant-select-selection__rendered,.ant-select-combobox.ant-select-show-arrow .ant-select-selection:hover .ant-select-selection__rendered{margin-right:20px}.ant-select-dropdown{margin:0;padding:0;color:rgba(0,0,0,.65);font-variant:tabular-nums;line-height:1.5;list-style:none;-webkit-font-feature-settings:"tnum","tnum",;font-feature-settings:"tnum","tnum",;position:absolute;top:-9999px;left:-9999px;z-index:1050;-webkit-box-sizing:border-box;box-sizing:border-box;font-size:14px;font-variant:normal;background-color:#fff;border-radius:4px;outline:none;-webkit-box-shadow:0 2px 8px rgba(0,0,0,.15);box-shadow:0 2px 8px rgba(0,0,0,.15)}.ant-select-dropdown.slide-up-appear.slide-up-appear-active.ant-select-dropdown-placement-bottomLeft,.ant-select-dropdown.slide-up-enter.slide-up-enter-active.ant-select-dropdown-placement-bottomLeft{-webkit-animation-name:antSlideUpIn;animation-name:antSlideUpIn}.ant-select-dropdown.slide-up-appear.slide-up-appear-active.ant-select-dropdown-placement-topLeft,.ant-select-dropdown.slide-up-enter.slide-up-enter-active.ant-select-dropdown-placement-topLeft{-webkit-animation-name:antSlideDownIn;animation-name:antSlideDownIn}.ant-select-dropdown.slide-up-leave.slide-up-leave-active.ant-select-dropdown-placement-bottomLeft{-webkit-animation-name:antSlideUpOut;animation-name:antSlideUpOut}.ant-select-dropdown.slide-up-leave.slide-up-leave-active.ant-select-dropdown-placement-topLeft{-webkit-animation-name:antSlideDownOut;animation-name:antSlideDownOut}.ant-select-dropdown-hidden{display:none}.ant-select-dropdown-menu{max-height:250px;margin-bottom:0;padding-left:0;overflow:auto;list-style:none;outline:none}.ant-select-dropdown-menu-item-group-list{margin:0;padding:0}.ant-select-dropdown-menu-item-group-list>.ant-select-dropdown-menu-item{padding-left:20px}.ant-select-dropdown-menu-item-group-title{height:32px;padding:0 12px;color:rgba(0,0,0,.45);font-size:12px;line-height:32px}.ant-select-dropdown-menu-item-group-list .ant-select-dropdown-menu-item:first-child:not(:last-child),.ant-select-dropdown-menu-item-group:not(:last-child) .ant-select-dropdown-menu-item-group-list .ant-select-dropdown-menu-item:last-child{border-radius:0}.ant-select-dropdown-menu-item{position:relative;display:block;padding:5px 12px;overflow:hidden;color:rgba(0,0,0,.65);font-weight:normal;line-height:22px;white-space:nowrap;text-overflow:ellipsis;cursor:pointer;-webkit-transition:background .3s ease;transition:background .3s ease}.ant-select-dropdown-menu-item:hover:not(.ant-select-dropdown-menu-item-disabled){background-color:#fff5f0}.ant-select-dropdown-menu-item:first-child{border-radius:4px 4px 0 0}.ant-select-dropdown-menu-item:last-child{border-radius:0 0 4px 4px}.ant-select-dropdown-menu-item-selected{color:rgba(0,0,0,.65);font-weight:600;background-color:#fafafa}.ant-select-dropdown-menu-item-disabled,.ant-select-dropdown-menu-item-disabled:hover{color:rgba(0,0,0,.25);cursor:not-allowed}.ant-select-dropdown-menu-item-active:not(.ant-select-dropdown-menu-item-disabled){background-color:#fff5f0}.ant-select-dropdown-menu-item-divider{height:1px;margin:1px 0;overflow:hidden;line-height:0;background-color:#e8e8e8}.ant-select-dropdown.ant-select-dropdown--multiple .ant-select-dropdown-menu-item{padding-right:32px}.ant-select-dropdown.ant-select-dropdown--multiple .ant-select-dropdown-menu-item .ant-select-selected-icon{position:absolute;top:50%;right:12px;color:rgba(0,0,0,0);font-weight:bold;font-size:12px;text-shadow:0 .1px 0,.1px 0 0,0 -.1px 0,-.1px 0;-webkit-transform:translateY(-50%);-ms-transform:translateY(-50%);transform:translateY(-50%);-webkit-transition:all .2s;transition:all .2s}.ant-select-dropdown.ant-select-dropdown--multiple .ant-select-dropdown-menu-item:hover .ant-select-selected-icon{color:rgba(0,0,0,.87)}.ant-select-dropdown.ant-select-dropdown--multiple .ant-select-dropdown-menu-item-disabled .ant-select-selected-icon{display:none}.ant-select-dropdown.ant-select-dropdown--multiple .ant-select-dropdown-menu-item-selected .ant-select-selected-icon,.ant-select-dropdown.ant-select-dropdown--multiple .ant-select-dropdown-menu-item-selected:hover .ant-select-selected-icon{display:inline-block;color:#ec7259}.ant-select-dropdown--empty.ant-select-dropdown--multiple .ant-select-dropdown-menu-item{padding-right:12px}.ant-select-dropdown-container-open .ant-select-dropdown,.ant-select-dropdown-open .ant-select-dropdown{display:block}.ant-empty{margin:0 8px;font-size:14px;line-height:22px;text-align:center}.ant-empty-image{height:100px;margin-bottom:8px}.ant-empty-image img{height:100%}.ant-empty-image svg{height:100%;margin:auto}.ant-empty-description{margin:0}.ant-empty-footer{margin-top:16px}.ant-empty-normal{margin:32px 0;color:rgba(0,0,0,.25)}.ant-empty-normal .ant-empty-image{height:40px}.ant-empty-small{margin:8px 0;color:rgba(0,0,0,.25)}.ant-empty-small .ant-empty-image{height:35px}._3kWNZz{text-align:center;padding:24px}.WVHbKq{font-size:24px;font-weight:500;margin-bottom:8px}._3eFswX{font-size:16px;color:#969696;margin-top:8px}._3eFswX>span{color:#da9e55}._1VQzqI{text-align:center;padding:24px 64px}._19gUNB{font-size:16px;font-weight:600;text-align:center;margin:16px 0}._1tunN3{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-pack:justify;-ms-flex-pack:justify;justify-content:space-between;-webkit-box-align:center;-ms-flex-align:center;align-items:center;height:72px;border-top:1px solid #eee}body.reader-night-mode ._1tunN3{border-color:#2f2f2f}._3ktw48{font-size:14px}._1iwqfH{font-size:28px;font-weight:500;float:right;color:#ec7259}._3b3lMj{font-size:14px}._1YY-Yc{font-size:12px;white-space:normal;overflow:hidden;-o-text-overflow:ellipsis;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}.ant-select-selection-selected-value ._1YY-Yc{display:none}._1Ye-SM{margin:24px 0;padding:6px 24px}._1P9XxY{text-align:left;font-size:13px;color:#969696}._3osc0S{display:block;margin-top:16px;margin-bottom:24px;text-align:center}._1FUlTu{font-size:14px;font-weight:500;margin-bottom:12px}.ekdgh6{font-size:14px;color:#969696;margin-bottom:16px}.aC6MAl{font-size:14px;font-weight:normal;padding:6px 20px}._1kCBjS{-webkit-box-pack:justify;-ms-flex-pack:justify;justify-content:space-between;font-size:14px;color:#969696;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}._1kCBjS,._3BUZPB,._18vaTa{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}._3BUZPB>span{margin-left:8px}._3BUZPB:not(:last-child){margin-right:12px}._2Bo4Th{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;width:40px;height:40px;color:#969696;border:1px solid #eee;border-radius:50%;font-size:18px;cursor:pointer}body.reader-night-mode ._2Bo4Th{border-color:#2f2f2f}._3Nksh7{background-color:#ec7259;color:#fff}._3Nksh7,body.reader-night-mode ._3Nksh7{border-color:#ec7259}._1LOh_5{cursor:pointer}._1LOh_5 .anticon{font-size:12px}._1x1ok9{cursor:pointer}._1x1ok9 .anticon{font-size:16px}._1yN79W{background-color:#f2f2f2}._1yN79W::-webkit-input-placeholder{color:#999}._1yN79W::-moz-placeholder{color:#999}._1yN79W:-ms-input-placeholder{color:#999}._1yN79W::-ms-input-placeholder{color:#999}._1yN79W::placeholder{color:#999}body.reader-night-mode ._1yN79W{background-color:#333}._3uZ5OL{text-align:center;padding:48px 64px}._2PLkjk{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;margin-bottom:24px}._2R1-48{min-width:50px;min-height:50px;width:50px;height:50px;border-radius:50%;border:1px solid #eee}._2h5tnQ{font-size:24px;font-weight:500;margin-left:16px}._1-bCJJ{-ms-flex-wrap:wrap;flex-wrap:wrap}._1-bCJJ,.LMa6S_{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center}.LMa6S_{-webkit-box-align:center;-ms-flex-align:center;align-items:center;width:162.5px;height:56px;font-size:16px;color:#969696;margin-bottom:12px;margin-right:12px;border-radius:10px;border:1px solid #eee;cursor:pointer;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}body.reader-night-mode .LMa6S_{border-color:#2f2f2f}.LMa6S_._1vONvL{color:#ec7259}.LMa6S_._1vONvL,body.reader-night-mode .LMa6S_._1vONvL{border-color:#ec7259}.LMa6S_._1sSZ6C{cursor:not-allowed;color:#969696;opacity:.5}.LMa6S_>i{font-size:20px}.LMa6S_>span{font-size:28px;font-style:italic}.LMa6S_:nth-child(3n){margin-right:0}.LMa6S_:nth-last-child(-n+3){margin-bottom:0}.LMa6S_:last-child{margin-right:0}._2ByDWa{position:relative;font-size:28px}._2ByDWa>span{font-size:16px;font-style:normal;opacity:1}._2ByDWa>input{position:absolute;top:50%;left:50%;width:100%;height:36px;margin:0 auto;text-align:center;-webkit-transform:translate(-50%,-50%);-ms-transform:translate(-50%,-50%);transform:translate(-50%,-50%);background-color:rgba(0,0,0,0);opacity:0;cursor:pointer}._2ByDWa>input::-webkit-inner-spin-button,._2ByDWa>input::-webkit-outer-spin-button{display:none}._2ByDWa._1vONvL>span{opacity:0}._2ByDWa._1vONvL>input{opacity:1;cursor:text}._3PA8BN>i{font-size:30px}._3PA8BN>span{font-size:16px;font-style:normal;margin-left:4px}._3PA8BN,._3PA8BN._1vONvL{color:#404040}body.reader-night-mode ._3PA8BN,body.reader-night-mode ._3PA8BN._1vONvL{color:#b3b3b3}._1yN79W{display:block;width:100%;height:80px;resize:none;margin-top:12px;padding:12px;border:none;border-radius:10px}._1_B577{font-size:15px;margin:12px 0}._3A-4KL{margin-top:24px;font-size:18px;font-weight:normal;padding:10px 48px}._3W59v5{display:block}.Uz-vZq,.VwEQ52{display:-webkit-box;display:-ms-flexbox;display:flex}.VwEQ52{-ms-flex-preferred-size:50%;flex-basis:50%;-webkit-box-flex:1;-ms-flex-positive:1;flex-grow:1;-webkit-box-align:center;-ms-flex-align:center;align-items:center;overflow:hidden}.VwEQ52:first-child{padding-right:20px}.VwEQ52:last-child{position:relative;padding-left:20px}.VwEQ52:last-child:before{content:"";position:absolute;width:1px;height:20px;left:0;background-color:#eee}body.reader-night-mode .VwEQ52:last-child:before{background-color:#2f2f2f}.VwEQ52:first-child:last-child{position:static;padding-left:0;padding-right:0}.VwEQ52:first-child:last-child:before{display:none}.VwEQ52 ._3nYIo3{min-width:54px;min-height:54px;width:54px;height:54px;border-radius:50%;border:1px solid #eee}body.reader-night-mode .VwEQ52 ._3nYIo3{border-color:#2f2f2f}.VwEQ52 ._2lfNuF{-webkit-box-flex:1;-ms-flex-positive:1;flex-grow:1;margin-left:10px;overflow:hidden}.VwEQ52 ._2lfNuF .Cqpr1X{color:#2d2d2d;font-weight:500;font-size:14px;margin-bottom:2px;overflow:hidden;-o-text-overflow:ellipsis;text-overflow:ellipsis;white-space:nowrap}body.reader-night-mode .VwEQ52 ._2lfNuF .Cqpr1X{color:#b3b3b3}.VwEQ52 ._2lfNuF ._2qBui4{color:#969696;font-size:12px}.VwEQ52+.VwEQ52 ._2lfNuF{margin-left:0}._2pnG2B{margin-top:20px}._2pnG2B:last-child{padding:0}._2pnG2B:before{display:none}._2pnG2B ._3nYIo3{width:54px;height:72px;min-width:54px;min-height:72px;border-radius:4px}._2pnG2B ._2lfNuF{margin-left:10px;margin-right:12px}._2pnG2B ._2lfNuF ._2WEj6j{margin-top:2px;overflow:hidden;-o-text-overflow:ellipsis;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}._13lIbp ._2qBui4{display:-webkit-inline-box;display:-ms-inline-flexbox;display:inline-flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}._13lIbp ._14FSyQ,._13lIbp .H4XBOO>img{width:24px;height:24px;min-width:24px;min-height:24px;border-radius:50%;border:2px solid #fff}body.reader-night-mode ._13lIbp ._14FSyQ,body.reader-night-mode ._13lIbp .H4XBOO>img{border-color:#3d3d3d}._14FSyQ{color:inherit;display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;color:#969696;background-color:#ececec}._14FSyQ:active,._14FSyQ:hover{color:inherit}body.reader-night-mode ._14FSyQ{background-color:#505050}.H4XBOO:not(:first-child){margin-left:-6px}.H4XBOO:last-of-type{margin-right:6px}._191KSt{cursor:pointer}._26JdYM{display:-webkit-box;display:-ms-flexbox;display:flex}._26JdYM ._3GKFE3{margin-top:0;margin-bottom:48px}._3LHFA-{width:40px;height:40px;border-radius:50%;border:1px solid #eee;margin-right:10px}body.reader-night-mode ._3LHFA-{border-color:#2f2f2f}._3GKFE3{-webkit-box-flex:1;-ms-flex-positive:1;flex-grow:1;margin-top:16px}._1u_H4i{padding:12px 16px;width:100%;height:90px;font-size:13px;border:1px solid #eee;border-radius:4px;background-color:#fafafa;resize:none;display:inline-block;vertical-align:top;outline-style:none}._1u_H4i::-webkit-input-placeholder{color:#999}._1u_H4i::-moz-placeholder{color:#999}._1u_H4i:-ms-input-placeholder{color:#999}._1u_H4i::-ms-input-placeholder{color:#999}._1u_H4i::placeholder{color:#999}body.reader-night-mode ._1u_H4i{background-color:#333;border-color:#2f2f2f}._3IXP9Q{-webkit-box-pack:justify;-ms-flex-pack:justify;justify-content:space-between;margin-top:16px;font-size:14px;color:#969696}._3IXP9Q,.SKZUyR{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}.SKZUyR{-ms-flex-negative:0;flex-shrink:0}._3MkVdm{font-size:18px;margin-right:12px}._3MkVdm:hover{color:#7d7d7d}._3Tp4of{-ms-flex-negative:0;flex-shrink:0;display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}._2lR7N6{padding:20px 0 30px;--base-color:#dfdfdf}body.reader-night-mode ._2lR7N6{--base-color:#737373}._2lR7N6 ._17_lFi{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;margin-bottom:16px}._2lR7N6 ._17_lFi ._3k5vgx{margin-right:6px;width:38px;height:38px;border-radius:50%;background-color:var(--base-color)}._2lR7N6 ._17_lFi .U36Th9{margin-bottom:6px;height:16px;width:60px;background-color:var(--base-color)}._2lR7N6 ._17_lFi ._9aTHBB{height:12px;width:120px;background-color:var(--base-color)}._2lR7N6 ._1Lq8tt{width:100%;height:16px;margin-bottom:8px;background-color:var(--base-color);-webkit-animation:_1i8o5w 1s ease-in-out infinite;animation:_1i8o5w 1s ease-in-out infinite}._2lR7N6 ._1muh0x{-webkit-animation-delay:-.5s;animation-delay:-.5s}._2lR7N6 ._3Pu4Wf{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;padding-top:4px;color:var(--base-color);font-size:16px}._2lR7N6 ._3Pu4Wf ._1mcOnW{height:14px;width:40px;margin-left:5px;margin-right:10px;background-color:var(--base-color)}@-webkit-keyframes _1i8o5w{0%{width:60%}50%{width:100%}to{width:60%}}@keyframes _1i8o5w{0%{width:60%}50%{width:100%}to{width:60%}}._1JPdR9{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-pack:start;-ms-flex-pack:start;justify-content:flex-start;-ms-flex-wrap:wrap;flex-wrap:wrap;width:345px;margin-top:12px}._3K5dOX{-ms-flex-negative:0;flex-shrink:0;width:110px;height:110px;margin-right:5px;margin-bottom:5px;border:1px solid #eee;border-radius:4px;background-position:50%;background-repeat:no-repeat;background-size:contain}body.reader-night-mode ._3K5dOX{border-color:#2f2f2f}._2IUqvs{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:start;-ms-flex-align:start;align-items:flex-start}._2IUqvs._3uuww8 ._1K9gkf{padding-bottom:0;border:none}._2IUqvs:last-child ._1K9gkf{margin-bottom:0;padding-bottom:0;border:none}._1_jhXc{width:40px;height:40px;border:1px solid #eee;border-radius:50%;overflow:hidden}body.reader-night-mode ._1_jhXc{border-color:#2f2f2f}._1K9gkf{-webkit-box-flex:1;-ms-flex-positive:1;flex-grow:1;margin-left:10px;margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid #eee}body.reader-night-mode ._1K9gkf{border-color:#2f2f2f}._1whZvR,._2ti5br{position:relative;display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;margin-top:12px;font-size:15px;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}._1whZvR:hover ._1NgfK-,._2ti5br:hover ._1NgfK-{visibility:visible;opacity:1}._1Jvkh4,._1NgfK-,._2GXD2V{cursor:pointer;margin-right:12px;color:#b0b0b0}._1Jvkh4:hover,._1NgfK-:hover,._2GXD2V:hover{color:#9c9c9c}._1NgfK-{position:absolute;right:0;visibility:hidden;opacity:0}._1NgfK-.ant-popover-open{visibility:visible;opacity:1}._2GXD2V{margin-right:16px}._2GXD2V._5LkTIL,._2GXD2V:hover{color:#ec7259}._23G05g{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;font-size:15px;font-weight:500}._1xqkrI{margin-top:2px;font-size:12px;color:#969696}._3pyYXB{display:-webkit-inline-box;display:-ms-inline-flexbox;display:inline-flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;margin-left:4px;padding:0 2px;font-size:12px;font-weight:normal;color:#ec7259;border:1px solid #ec7259;border-radius:4px;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}._2bDGm4{margin-top:10px;font-size:16px;line-height:1.5}._2kvBge{margin-top:20px}._3g0yKR{padding:20px 0 16px;border-top:1px solid #eee}._3g0yKR ._3d_vFY{display:-webkit-box;display:-ms-flexbox;display:flex}._3g0yKR:last-child{padding-bottom:0}body.reader-night-mode ._3g0yKR{border-color:#2f2f2f}._1Y3RXD{display:-webkit-inline-box;display:-ms-inline-flexbox;display:inline-flex;font-size:15px;margin:12px 0;color:#0681d0;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;cursor:pointer}._1whZvR{margin-top:16px;padding-top:16px;border-top:1px solid #eee}body.reader-night-mode ._1whZvR{border-color:#2f2f2f}.WliqwT{color:#969696;padding-left:12px;border-left:1px solid #eee}.T4mGDk{color:#0681d0;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;cursor:pointer}body.reader-night-mode .WliqwT{border-color:#2f2f2f}._13OjNv{display:-webkit-box;display:-ms-flexbox;display:flex;margin-top:24px;margin-bottom:8px;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;color:#969696}._3ubyu9,._13OjNv,.LaYREM{-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center}._3ubyu9,.LaYREM{display:-webkit-inline-box;display:-ms-inline-flexbox;display:inline-flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;width:32px;height:32px;line-height:32px;font-size:14px;margin:0 4px;border:1px solid #eee;border-radius:50%;cursor:pointer}body.reader-night-mode ._3ubyu9,body.reader-night-mode .LaYREM{border-color:#2f2f2f}._3ubyu9:hover,.LaYREM:hover{background-color:#f2f2f2}._1i9WqE._3ubyu9,.LaYREM._1i9WqE{color:#ec7259;border-color:#ec7259;pointer-events:none}._3ubyu9{width:auto;padding-left:12px;padding-right:12px;border-radius:20px}._10KzV0{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}._10KzV0 ._2R7vBo{margin-left:6px;font-size:14px;font-weight:normal}._2zSaYx{display:-webkit-box;display:-ms-flexbox;display:flex}._1ekjko,._393S4n{font-size:12px;font-weight:normal;color:#969696;margin-left:12px;cursor:pointer;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}body.reader-night-mode ._1ekjko{color:#666}._1ekjko._1BIpxf{color:#2d2d2d}body.reader-night-mode ._1ekjko._1BIpxf{color:#969696}._2gPNSa{margin-top:30px;margin-bottom:30px}._1DVmvZ{font-size:12px;font-weight:normal;color:#969696;margin-left:12px;padding:2px 8px;border:1px solid #eee;border-radius:16px;cursor:pointer;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}body.reader-night-mode ._1DVmvZ{border-color:#2f2f2f}._1DVmvZ._1BIpxf{color:#fff;background-color:#ec7259;border-color:#ec7259}body.reader-night-mode ._1DVmvZ._1BIpxf{color:#3d3d3d;border-color:#ec7259}._3SnN_k{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:justify;-ms-flex-pack:justify;justify-content:space-between;font-size:18px;padding-top:20px;padding-bottom:20px}._3b8Ibd{text-align:center}._3b8Ibd>img{width:169px;height:140px}._3b8Ibd ._1DiGFn{margin-top:28px;margin-bottom:8px;font-size:14px;color:#969696}._3b8Ibd ._1DiGFn ._3QdbM2{color:#ec7259}._1Kc1pc{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:justify;-ms-flex-pack:justify;justify-content:space-between;padding:20px 0}._1Kc1pc:not(:last-child){border-bottom:1px solid #eee}body.reader-night-mode ._1Kc1pc{border-color:#2f2f2f}._1Kc1pc ._3cgiY6{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}._1MTfTm{min-width:50px;min-height:50px;width:50px;height:50px;border-radius:4px;border:1px solid #eee}body.reader-night-mode ._1MTfTm{border-color:#2f2f2f}._1gXCcE{margin:0 12px}._3puJ3K{display:block;font-size:16px;font-weight:500;margin-bottom:2px}._1AkY7D{font-size:12px;color:#969696}._1v2f0N{height:480px;padding:24px;overflow-y:scroll}._3fC9Lb{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:justify;-ms-flex-pack:justify;justify-content:space-between}._2MEVQW{display:block;margin-left:24px;cursor:pointer}._2MEVQW>span{margin-left:4px}._3qtwqN,.q-2pty{display:block;text-align:center;margin:32px 0;color:#969696}._3qtwqN{cursor:pointer}.RtGuHg{padding:24px 0}.saTF2Q{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}._3sAsA5{margin-left:12px;font-size:14px;font-weight:normal;line-height:1;color:#969696;cursor:pointer}._3sAsA5>span{margin-left:3px}._99AOeY{display:-webkit-box;display:-ms-flexbox;display:flex;padding:16px 0}._99AOeY:not(:last-child){border-bottom:1px solid #eee}body.reader-night-mode ._99AOeY{border-color:#2f2f2f}._3CGUtf{-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;width:48px;margin-right:16px;font-family:Arial-BoldItalicMT,sans-serif;font-size:22px;font-weight:normal;color:#b3b3b3}._1euQZJ,._3CGUtf{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}._1euQZJ{margin-bottom:4px}._130BbT{display:block;text-align:center;font-size:12px;color:#da9e55;background-color:rgba(218,158,85,.15);margin-left:4px;padding:2px 10px;border-radius:12px;line-height:20px}._1JV12M{font-size:16px;font-weight:500}._1JV12M:hover{text-decoration:underline}.Fm0jls{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;font-size:12px;color:#969696}.Fm0jls ._17ywf4{color:#ec7259;margin-right:8px}._37OvKa{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;margin-top:16px;margin-bottom:32px}._37OvKa>i{color:#ec7259;font-size:20px;margin-right:8px}._2xV5A4{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-pack:justify;-ms-flex-pack:justify;justify-content:space-between;-webkit-box-align:center;-ms-flex-align:center;align-items:center;padding:16px 0}._2xV5A4:not(:last-child){border-bottom:1px solid #eee}body.reader-night-mode ._2xV5A4{border-color:#2f2f2f}._1MmGv5{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}._2E7TMH{width:50px;height:50px;border-radius:50%;border:1px solid #eee}._2eSeIY{font-size:16px;font-weight:500;margin-left:12px}._1NZ1BD{margin:32px 0}._2nF7af{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-orient:vertical;-webkit-box-direction:normal;-ms-flex-direction:column;flex-direction:column}._2nVyQz{margin-bottom:24px}._2CcN3T{font-size:14px;font-weight:400;line-height:18px;padding-left:5px;border-left:4px solid #ec7259}._3S34Y_{-webkit-box-flex:1;-ms-flex-positive:1;flex-grow:1;display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-orient:vertical;-webkit-box-direction:normal;-ms-flex-direction:column;flex-direction:column;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;margin:0}._3S34Y_>img{width:144px;height:144px;margin-bottom:12px}._2JdSds{line-height:18px;font-size:13px;font-weight:normal;color:#999;cursor:pointer}._2JdSds>span{margin-left:2px;pointer-events:none}._2Nttfz{-ms-flex-wrap:wrap;flex-wrap:wrap}._2Nttfz,._3s5t0Q,.H7E3vT{display:-webkit-box;display:-ms-flexbox;display:flex}._3s5t0Q,.H7E3vT{-ms-flex-negative:0;flex-shrink:0;-webkit-box-align:center;-ms-flex-align:center;align-items:center;margin-right:12px;margin-bottom:12px;cursor:pointer}._3s5t0Q{background-color:#f5f5f5;padding:5px 10px 5px 5px;border-radius:4px}body.reader-night-mode ._3s5t0Q{background-color:#4d4d4d}._3s5t0Q .anticon{margin-right:2px;font-size:12px}._1lsejJ{padding:7px 10px}._2vEwGY{-ms-flex-negative:0;flex-shrink:0;width:24px;height:24px;margin-right:8px;border-radius:2px}._2-Djqu{font-size:14px;line-height:20px}.H7E3vT{font-size:14px;color:#999}.H7E3vT .anticon{margin-left:4px;font-size:12px}._29KFEa{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;font-size:14px;font-weight:normal;line-height:18px}._29KFEa .anticon{margin-left:1px;font-size:12px}._1iTR78{margin-bottom:24px}._11jppn{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:justify;-ms-flex-pack:justify;justify-content:space-between;padding:20px 0;border-bottom:1px solid #eee}._11jppn:first-child{padding-top:0}._11jppn:last-child{padding-bottom:0;border:none}body.reader-night-mode ._11jppn{border-color:#2f2f2f}.em6wEs,.JB6qEE{overflow:hidden}.em6wEs{font-size:18px;font-weight:500;margin-bottom:4px;color:#404040;-o-text-overflow:ellipsis;text-overflow:ellipsis;white-space:nowrap}body.reader-night-mode .em6wEs{color:#b3b3b3}._2voXH8:active,._2voXH8:hover{text-decoration:underline}._3fvgn4{font-size:13px;color:#666;line-height:20px;overflow:hidden;-o-text-overflow:ellipsis;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical}._1pJt6F{margin-top:8px}._1pJt6F,._3IWz1q{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}._34VC_H{width:24px;height:24px;margin-right:4px;border-radius:50%}._3tPsL6{font-size:13px;color:#969696;overflow:hidden;-o-text-overflow:ellipsis;text-overflow:ellipsis;white-space:nowrap}._10MMAm{margin-left:20px}._3zGDUj{display:block;-ms-flex-negative:0;flex-shrink:0;width:150px;height:120px;border-radius:4px;border:1px solid hsla(0,0%,50.2%,.1)}._22bNOL{margin-bottom:10px;border-radius:4px;overflow:hidden}._3FPkr1{position:relative;display:block;width:100%;height:100%;background-position:50%;background-repeat:no-repeat;background-size:cover}._3Tj3M5{position:absolute;display:block;font-size:12px;padding:2px 6px;color:#fff;cursor:pointer}._2ibkP3,._3Tj3M5{bottom:0;right:0;background-color:rgba(0,0,0,.5)}._2ibkP3{position:fixed;top:0;left:0;height:100vh;z-index:1100;filter:alpha(opacity=50)}body.reader-night-mode ._2ibkP3{background-color:rgba(61,61,61,.75);filter:alpha(opacity=75)}._2jDHp5{position:fixed;top:0;right:0;bottom:0;left:0;z-index:1150;overflow:hidden;outline:0;-webkit-overflow-scrolling:touch}.L-NY99{height:auto;max-height:100vh;max-width:100%;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;cursor:-webkit-zoom-out;cursor:zoom-out;-webkit-transition:-webkit-transform .2s ease-in-out;transition:-webkit-transform .2s ease-in-out;-o-transition:transform .2s ease-in-out;transition:transform .2s ease-in-out;transition:transform .2s ease-in-out,-webkit-transform .2s ease-in-out;-webkit-transform-origin:0 0;-ms-transform-origin:0 0;transform-origin:0 0}._3G_AE-{-webkit-transition:none;-o-transition:none;transition:none}._3C00cT{position:fixed}._2kc3FH,._2TG34g{position:absolute;top:50%;-webkit-transform:translateY(-50%);-ms-transform:translateY(-50%);transform:translateY(-50%);width:60px;height:60px;font-size:24px;display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;border-radius:50%;color:#fff;cursor:pointer}._2kc3FH:hover,._2TG34g:hover{background-color:hsla(0,0%,100%,.1)}body.reader-night-mode ._2kc3FH,body.reader-night-mode ._2TG34g{color:#bfbfbf}._3yUKnr{cursor:default;opacity:.4}._3yUKnr:hover{background-color:rgba(0,0,0,0)}._2TG34g{left:24px}._2kc3FH{right:24px}._2Gw6nl{position:absolute;bottom:32px;left:50%;-webkit-transform:translate3d(-50%,0,0);transform:translate3d(-50%,0,0);padding:6px 16px;border-radius:20px;border:1px solid #fff;background-color:rgba(0,0,0,.4);font-size:14px;color:#fff}body.reader-night-mode ._2Gw6nl{color:#bfbfbf;border-color:#bfbfbf}._2Gw6nl:active,._2Gw6nl:focus,._2Gw6nl:hover{color:#fff}body.reader-night-mode ._2Gw6nl:active,body.reader-night-mode ._2Gw6nl:focus,body.reader-night-mode ._2Gw6nl:hover{color:#bfbfbf}._3Pnjry{position:fixed;top:216px;left:calc((100vw - 1000px)/2 - 78px);-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}._1pUUKr{-webkit-box-orient:vertical;-webkit-box-direction:normal;-ms-flex-direction:column;flex-direction:column;margin-bottom:16px;cursor:pointer;color:#969696}._1pUUKr,._2VdqdF{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}._2VdqdF{-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;width:48px;height:48px;font-size:18px;border-radius:50%;-webkit-box-shadow:0 1px 3px rgba(26,26,26,.1);box-shadow:0 1px 3px rgba(26,26,26,.1);background-color:#fff}body.reader-night-mode ._2VdqdF{background-color:#404040}.P63n6G{margin-top:4px;font-size:14px;text-align:center;color:#969696;overflow:hidden;height:19px}._2LKTFF{-webkit-transition:-webkit-transform .2s;transition:-webkit-transform .2s;-o-transition:transform .2s;transition:transform .2s;transition:transform .2s,-webkit-transform .2s}._1GPnWJ{display:block;height:19px}._1GPnWJ.RhY_sp{visibility:hidden;opacity:0}._1pUUKr._2Z1aZJ ._2VdqdF{color:#fff;background-color:#ec7259}._1pUUKr._2Z1aZJ .P63n6G{color:#ec7259}._1pUUKr._2Z1aZJ ._2LKTFF{-webkit-transform:translateY(-19px);-ms-transform:translateY(-19px);transform:translateY(-19px)}._3MOB7g{text-align:center;padding:24px}._1U9mRW{font-size:24px;font-weight:500;margin-bottom:16px}._2rxlQh{font-size:16px;margin-bottom:24px}._2mpYuT{margin-bottom:16px}._21FTIM{display:block;padding:16px 24px}._3qpYUS{margin-bottom:16px}._1I6Gjn,._3qpYUS{display:-webkit-box;display:-ms-flexbox;display:flex}._1I6Gjn{-webkit-box-align:center;-ms-flex-align:center;align-items:center;font-size:15px}._1I6Gjn>span{margin:0 8px}._21urAK{display:block;padding:12px 16px;width:100%;height:auto;font-size:14px;border:1px solid #eee;border-radius:4px;background-color:#f2f2f2;resize:none}._21urAK::-webkit-input-placeholder{color:#999}._21urAK::-moz-placeholder{color:#999}._21urAK:-ms-input-placeholder{color:#999}._21urAK::-ms-input-placeholder{color:#999}._21urAK::placeholder{color:#999}body.reader-night-mode ._21urAK{background-color:#333;border-color:#2f2f2f}._1RuRku{font-size:30px;font-weight:700;word-break:break-word}._21bLU4 .ant-back-top{bottom:96px}@media only screen and (max-width:900px){._21bLU4 .ant-back-top{display:none}}._3MyrRP{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;width:40px;height:40px;border-radius:50%;color:#8c8c8c;font-size:18px;-webkit-box-shadow:0 1px 3px rgba(26,26,26,.1);box-shadow:0 1px 3px rgba(26,26,26,.1);background-color:#fff}body.reader-night-mode ._3MyrRP{-webkit-box-shadow:0 1px 3px rgba(0,0,0,.3);box-shadow:0 1px 3px rgba(0,0,0,.3);background-color:#3d3d3d}._1KC9MV{position:absolute;width:40px;height:40px;top:-150%;background-image:url(data:image/png;base64,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);background-position:50%;background-repeat:no-repeat;background-size:cover}._3yPTTQ{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;height:40px;margin:0 -24px 20px;font-size:14px;line-height:14px;color:#0681d0;background:#e4f4fe}._3yPTTQ>i{font-size:16px;margin-right:4px}._3yPTTQ .anticon-spin{-webkit-animation-duration:1.5s;animation-duration:1.5s}._2C7CDc{width:960px;margin:0 auto;padding-top:80px;text-align:center}._35eZ2j{width:200px}._2Tso_9{font-size:32px;font-weight:500;color:#ec7259;margin-top:16px;margin-bottom:40px}._1aPG4O{font-size:20px;margin-top:4px}._2mcXeT{margin-top:32px}._33ha_L{display:inline-block;text-decoration:none}.xiRCyp{width:125px;height:125px}._3YhoEV{color:#404040;font-size:20px;margin-top:8px}body.reader-night-mode ._3YhoEV{color:#b3b3b3}</style>'
        content = _ + content

        return content

    async def _get_article_html(self, article_url, article_url_type) -> tuple:
        """
        获取文章的html
        :return:
        """
        video_url = ''
        body = ''
        try:
            if article_url_type == 'wx':
                return await unblock_func(
                    func_name=self.unblock_get_wx_article_html,
                    func_args=[
                        article_url,
                    ],
                    default_res=('', ''),
                    logger=self.lg, )

            elif article_url_type == 'tt':
                return await self._get_tt_article_html(article_url=article_url)

            elif article_url_type == 'js':
                return await self._get_js_article_html(article_url=article_url)

            elif article_url_type == 'kd':
                return await unblock_func(
                    func_name=self.unblock_get_kd_article_html,
                    func_args=[
                        article_url,
                    ],
                    default_res=('', ''),
                    logger=self.lg,)

            elif article_url_type == 'kb':
                return await unblock_func(
                    func_name=self.unblock_get_kb_article_html,
                    func_args=[
                        article_url,
                    ],
                    default_res=('', ''),
                    logger=self.lg,)

            elif article_url_type == 'df':
                return await self._get_df_article_html(article_url=article_url)

            elif article_url_type == 'sg':
                return await self._get_sg_article_html(article_url=article_url)

            elif article_url_type == 'bd':
                return await self._get_bd_article_html(article_url=article_url)

            elif article_url_type == 'zq':
                return await self._get_zq_article_html(article_url=article_url)

            elif article_url_type == 'yg':
                return await self._get_yg_article_html(article_url=article_url)

            elif article_url_type == 'xg':
                return await self._get_xg_article_html(article_url=article_url)

            elif article_url_type == 'fh':
                return await self._get_fh_article_html(article_url=article_url)

            elif article_url_type == 'ys':
                return await self._get_ys_article_html(article_url=article_url)

            elif article_url_type == 'cn':
                return await self._get_cn_article_html(article_url=article_url)

            elif article_url_type == 'if':
                return await self._get_if_article_html(article_url=article_url)

            elif article_url_type == 'ss':
                return await self._get_ss_article_html(article_url=article_url)

            elif article_url_type == 'jm':
                return await self._get_jm_article_html(article_url=article_url)

            elif article_url_type == 'pp':
                return await self._get_pp_article_html(article_url=article_url)

            elif article_url_type == 'hx':
                return await self._get_hx_article_html(article_url=article_url)

            elif article_url_type == 'nfzm':
                return await self._get_nfzm_article_html(article_url=article_url)

            elif article_url_type == 'hqx':
                return await self._get_hqx_article_html(article_url=article_url)

            elif article_url_type == 'ck':
                return await self._get_ck_article_html(article_url=article_url)

            elif article_url_type == 'lsp':
                return await unblock_func(
                    func_name=self.unblock_get_lsp_article_html,
                    func_args=[
                        article_url,
                    ],
                    default_res=('', ''),
                    logger=self.lg,)

            elif article_url_type == 'amz':
                return await self._get_amz_article_html(article_url=article_url)

            elif article_url_type == 'mp':
                return await unblock_func(
                    func_name=self.unblock_get_mp_article_html,
                    func_args=[
                        article_url,
                    ],
                    default_res=('', ''),
                    logger=self.lg,)

            elif article_url_type == 'hk':
                return await self._get_hk_article_html(article_url=article_url)

            elif article_url_type == '7y7':
                return await self._get_7y7_article_html(article_url=article_url)

            elif article_url_type == 'qqbb':
                return await self._get_qqbb_article_html(article_url=article_url)

            elif article_url_type == 'ft':
                return await self._get_ft_article_html(article_url=article_url)

            elif article_url_type == '91mt':
                return await self._get_91mt_article_html(article_url=article_url)

            elif article_url_type == 'xq':
                return await self._get_xq_article_html(article_url=article_url)

            elif article_url_type == '5h':
                return await self._get_5h_article_html(article_url=article_url)

            elif article_url_type == 'bdj':
                return await self._get_bdj_article_html(article_url=article_url)

            else:
                raise AssertionError('未实现的解析!')

        except AssertionError:
            self.lg.error('遇到错误:', exc_info=True)

            return body, video_url

    async def _get_bdj_article_html(self, article_url) -> tuple:
        """
        获取bdj html
        :param article_url:
        :return:
        """
        video_url = ''
        headers = await async_get_random_headers(connection_status_keep_alive=False)
        headers.update({
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.budejie.com/',
        })
        body = Requests.get_url_body(
            url=article_url,
            headers=headers,
            verify=False,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            num_retries=self.request_num_retries,)
        assert body != ''
        # self.lg.info(body)

        return body, video_url

    async def _get_5h_article_html(self, article_url) -> tuple:
        """
        获取5h html
        :param article_url:
        :return:
        """
        video_url = ''
        headers = await async_get_random_headers(
            user_agent_type=1,
            connection_status_keep_alive=False,)
        headers.update({
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://m.5h.com/',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            verify=False,
            num_retries=self.request_num_retries,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            logger=self.lg,)
        assert body != ''
        # self.lg.info(body)

        return body, video_url

    async def _get_xq_article_html(self, article_url) -> tuple:
        """
        获取雪球网 html
        :param article_url:
        :return:
        """
        video_url = ''
        headers = await async_get_random_headers()
        headers.update({
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Site': 'none',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            proxy_type=PROXY_TYPE_HTTPS,
            logger=self.lg,)
        assert body != ''
        # self.lg.info(body)

        hook_target_api_data_sel = {
            'method': 're',
            'selector': 'window\.SNOWMAN_STATUS = (.*?);window\.SNOWMAN_TARGET',
        }
        self.hook_target_api_data = json_2_dict(
            json_str=await async_parse_field(
                parser=hook_target_api_data_sel,
                target_obj=body,
                logger=self.lg,),
            default_res={},
            logger=self.lg,)
        assert self.hook_target_api_data != {}
        # pprint(self.hook_target_api_data)

        return body, video_url

    async def _get_91mt_article_html(self, article_url) -> tuple:
        """
        获取91觅糖 html
        :param article_url:
        :return:
        """
        parse_obj = await self._get_parse_obj(article_url_type='91mt')
        article_id = await async_parse_field(
            parser=parse_obj['article_id'],
            target_obj=article_url,
            logger=self.lg,)
        assert article_id != ''

        # 研究发现, 视频or图文文章的所有信息在视频详情页中都有, 故直接请求视频详情页
        headers = await async_get_random_headers(
            user_agent_type=1,
            cache_control='',)
        headers.update({
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Site': 'same-origin',
            'Referer': article_url,
        })
        video_detail_url = 'https://www.91mitang.com/pageDetails/{}'.format(article_id)
        body = await unblock_request(
            url=video_detail_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            logger=self.lg, )
        assert body != ''
        # self.lg.info(body)

        video_url_sel = {
            'method': 're',
            'selector': '\"contentUrl\": \"(.*?)\",',
        }
        video_url = await async_parse_field(
            parser=video_url_sel,
            target_obj=body,
            logger=self.lg,)
        if video_url != '':
            self.lg.info('此为视频文章!')
            self.lg.info('got video_url: {}'.format(video_url))
        else:
            self.lg.info('此为图文文章!')

        return body, video_url

    async def _get_ft_article_html(self, article_url) -> tuple:
        """
        获取ft 的html
        :param article_url:
        :return:
        """
        video_url = ''
        headers = await async_get_random_headers(user_agent_type=1)
        headers.update({
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Site': 'none',
            'Referer': 'https://m.fatiao.pro/',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            logger=self.lg,)
        assert body != ''
        # self.lg.info(body)

        if 'detail' in article_url:
            self.lg.info('此为视频文章')
            video_url_sel = {
                'method': 're',
                'selector': 'src: \[\"(.*?)\"\],',
            }
            video_url = await async_parse_field(
                parser=video_url_sel,
                target_obj=body,
                logger=self.lg,)
            self.lg.info('got video_url: {}'.format(video_url))
        else:
            pass

        return body, video_url

    async def _get_qqbb_article_html(self, article_url) -> tuple:
        """
        获取qqbb html
        :param article_url:
        :return:
        """
        async def get_next_page_body_by_page_num(article_url: str,
                                                 parse_obj: dict,
                                                 page_num: int=1) -> tuple:
            """
            根据page_num获取对应页码文章信息
            :param article_url:
            :param parse_obj:
            :param page_num:
            :return:
            """
            # 是否还有下一页
            had_next_page = False
            # 下一页的content
            next_content = ''

            self.lg.info('获取第{}页body...'.format(page_num))
            if page_num > 1:
                # eg:
                # 首页: https://m.qbaobei.com/a/1145214.html
                # 第二页: https://m.qbaobei.com/a/1145214_2.html
                article_url = article_url.replace('.html', '_{}.html'.format(page_num))
                if page_num > 2:
                    referer = re.compile('\.html')\
                        .sub('_{}\.html'.format(page_num-1), article_url)
                else:
                    # 2
                    referer = article_url
            else:
                referer = article_url
            # self.lg.info('article_url: {}'.format(article_url))

            headers = await async_get_random_headers(
                user_agent_type=1,
                connection_status_keep_alive=False,)
            headers.update({
                'authority': 'm.qbaobei.com',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-site': 'none',
                # 'referer': 'https://m.qbaobei.com/',
                'referer': referer,
                # 'cookie': 'Hm_lvt_3d8ae083091c839222c62a3e4ab746ee=1565660348; PHPSESSID=85ukti67lk3419g8hcnbogc025; Hm_lvt_4ba23929a20904dd1920a6e67b6258d3=1565660780; Hm_lvt_90f5390d52559687ed0ea6b8603e7018=1565660780; Hm_lpvt_4ba23929a20904dd1920a6e67b6258d3=1565671441; Hm_lpvt_90f5390d52559687ed0ea6b8603e7018=1565671441; Hm_lpvt_3d8ae083091c839222c62a3e4ab746ee=1565671441',
            })
            body = await unblock_request(
                url=article_url,
                headers=headers,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.lg,
                logger=self.lg,)
            assert body != ''
            # self.lg.info(body)

            had_next_text_sel = {
                'method': 'css',
                'selector': 'div.detail_page a[id^="href_"] ::text',
            }
            # 因为如果存在第三页的话, 第二页是有上一页和下一页的
            had_next_text_list = await async_parse_field(
                parser=had_next_text_sel,
                target_obj=body,
                logger=self.lg,
                is_first=False)
            if '下一页' in had_next_text_list:
                had_next_page = True
                # self.lg.info('有下一页!')
            else:
                pass
            if page_num > 1:
                next_content_sel = {
                    'method': 're',
                    'selector': '<article class=\"art-body art-body-\d+.*?\">(.*)<div class=\"detail_page\">',
                }
                next_content = await async_parse_field(
                    parser=next_content_sel,
                    target_obj=body,
                    logger=self.lg, )
                # self.lg.info(next_content)
            else:
                pass

            return body, next_content, had_next_page

        video_url = ''
        parse_obj = await self._get_parse_obj(article_url_type='qqbb')
        if 'video_' not in article_url:
            # 图文
            had_next_page = True
            page_num = 1
            last_body = ''
            while had_next_page:
                body, next_content, had_next_page = await get_next_page_body_by_page_num(
                    article_url=article_url,
                    parse_obj=parse_obj,
                    page_num=page_num, )
                if page_num > 1:
                    last_body = re.compile('<div class=\"detail_page\">') \
                        .sub(next_content + '<div class="detail_page">', last_body)
                else:
                    last_body = body
                # self.lg.info('last_body: {}'.format(last_body))
                page_num += 1

            # self.lg.info(last_body)

        else:
            self.lg.info('此为视频文章')
            last_body = (await get_next_page_body_by_page_num(
                article_url=article_url,
                parse_obj=parse_obj,
                page_num=1,))[0]
            # 视频文章
            video_url_sel = {
                'method': 're',
                'selector': '\"contentUrl\": \"(.*?)\",'
            }
            video_url = await async_parse_field(
                parser=video_url_sel,
                target_obj=last_body,
                logger=self.lg,)
            self.lg.info('got video_url: {}'.format(video_url))

        return last_body, video_url

    async def _get_7y7_article_html(self, article_url) -> tuple:
        """
        获取7y7 html
        :param article_url:
        :return:
        """
        async def get_next_page_body_by_page_num(article_url: str,
                                                 parse_obj: dict,
                                                 page_num: int=1) -> tuple:
            """
            获取下一页的body信息
            :param page_num:
            :return:
            """
            # 是否还有下一页
            had_next_page = False
            # 下一页的content
            next_content = ''

            self.lg.info('获取第{}页body...'.format(page_num))
            if page_num > 1:
                # eg:
                # 首页: https://i.7y7.com/caizhuang/47/385947.html
                # 第二页: https://i.7y7.com/caizhuang/47/385947_2.html
                article_url = article_url.replace('.html', '_{}.html'.format(page_num))
                if page_num > 2:
                    referer = re.compile('\.html').sub('_{}\.html'.format(page_num-1), article_url)
                else:
                    # 2
                    referer = article_url
            else:
                referer = article_url
            # self.lg.info('article_url: {}'.format(article_url))

            headers = await async_get_random_headers(
                user_agent_type=1,
                connection_status_keep_alive=False, )
            headers.update({
                'authority': 'i.7y7.com',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-site': 'none',
                # 'referer': 'https://i.7y7.com/',
                'referer': referer,                 # 请求下一页时必须使用上一页的地址
                # 'cookie': 'Hm_lvt_7905279f5e0979a49bdc161dbad2708d=1565659612; Hm_lvt_8257a196df3916574fa89d7567071790=1565659642; Hm_lvt_6557398d368c2c5d56b4ebf03da843a7=1565659990; Hm_lpvt_6557398d368c2c5d56b4ebf03da843a7=1565659990; Hm_lpvt_8257a196df3916574fa89d7567071790=1565660942; Hm_lpvt_7905279f5e0979a49bdc161dbad2708d=1565660942',
            })
            body = await unblock_request(
                url=article_url,
                headers=headers,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.request_num_retries,
                logger=self.lg, )
            assert body != ''
            # self.lg.info(body)

            had_next_text_sel = {
                'method': 'css',
                'selector': 'div.detail_page a[id^="href_"] ::text',
            }
            # 因为如果存在第三页的话, 第二页是有上一页和下一页的
            had_next_text_list = await async_parse_field(
                parser=had_next_text_sel,
                target_obj=body,
                logger=self.lg,
                is_first=False)
            if '下一页' in had_next_text_list:
                had_next_page = True
                # self.lg.info('有下一页!')
            else:
                pass
            if page_num > 1:
                next_content_sel = {
                    'method': 're',
                    'selector': '<div class=\"contents\">(.*?)</div><div class=\"detail_page\">',
                }
                next_content = await async_parse_field(
                    parser=next_content_sel,
                    target_obj=body,
                    logger=self.lg,)
                # self.lg.info(next_content)
            else:
                pass

            return body, next_content, had_next_page

        video_url = ''
        parse_obj = await self._get_parse_obj(article_url_type='7y7')
        had_next_page = True
        page_num = 1
        last_body = ''
        while had_next_page:
            body, next_content, had_next_page = await get_next_page_body_by_page_num(
                article_url=article_url,
                parse_obj=parse_obj,
                page_num=page_num,)
            if page_num > 1:
                last_body = re.compile('</div><div class=\"detail_page\">')\
                    .sub(next_content+'</div><div class="detail_page">', last_body)
            else:
                last_body = body
            # self.lg.info('last_body: {}'.format(last_body))
            page_num += 1

        # self.lg.info(last_body)

        return last_body, video_url

    async def _get_hk_article_html(self, article_url) -> tuple:
        """
        获取hk html
        :param article_url:
        :return:
        """
        parse_obj = await self._get_parse_obj(article_url_type='hk')
        video_id = await async_parse_field(
            parser=parse_obj['article_id'],
            target_obj=article_url,
            logger=self.lg,)
        assert video_id != ''
        headers = await async_get_random_headers(
            user_agent_type=1,
            connection_status_keep_alive=False,)
        headers.update({
            'authority': 'haokan.baidu.com',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-site': 'none',
            'referer': 'https://haokan.baidu.com/',
            # 'cookie': 'BAIDUID=1666ADBB95B083DBB2DA29E9BEFCB50B:FG=1; BIDUPSID=1666ADBB95B083DBB2DA29E9BEFCB50B; PSTM=1553750958; H_WISE_SIDS=130611_124610_128699_132218_131777_128065_130510_126064_130163_120216_131602_132213_131517_132261_118882_118872_131401_118851_118819_118796_130763_132244_131649_131576_131555_131536_131534_131529_130222_131295_131872_131391_129565_107313_131796_131392_130120_131874_130569_131196_130348_129647_131246_125086_131435_131686_131036_131906_132090_129838_130413_129646_124030_132204_130824_110085_131767_127969_131506_123289_130818_127417_131550_131826_131750_131264_131263_131662_131946_128808; BDUSS=RtNkhNbXFTQWY1flppR3ZOd281SGtuMGlOaHhuWX5QUX5XZ3Y2MFZ4cHNIaGRkSVFBQUFBJCQAAAAAAAAAAAEAAADfukJXAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGyR71xske9cRz; pgv_pvi=169221120; locale=zh; yjs_js_security_passport=66b912c3641c4e58bd4cd990686fb14faf28df5f_1565146880_js; Hm_lvt_4aadd610dfd2f5972f1efee2653a2bc5=1565229221; COMMON_LID=f3435a0e1c48660589c8fcd526e0f8bf; Hm_lvt_77ca61e523cd51ec7ac7a23bc4d24edf=1565229278; Hm_lpvt_4aadd610dfd2f5972f1efee2653a2bc5=1565229363; HK_CH_EXPIRED_TIME=1565279999000; HK_CH_IS_CLICKED=0; HK_SID=3116_2-3157_2-3168_1-3217_1-3265_1-3292_1; Hm_lpvt_77ca61e523cd51ec7ac7a23bc4d24edf=1565229372; HK_CH_REFRESH_TIMES=3; HK_CH_MAT_INDEX=0',
        })
        params = (
            ('vid', video_id),
            ('tab', 'recommend'),
        )
        url = 'https://haokan.baidu.com/v'
        body = await unblock_request(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            logger=self.lg,)
        # self.lg.info(body)
        assert body != '', '获取hk的body为空值!'

        video_url_sel = {
            'method': 'css',
            'selector': 'div.play1er-box video ::attr("src")',
        }
        video_url = await async_parse_field(
            parser=video_url_sel,
            target_obj=body,
            logger=self.lg,)
        self.lg.info('got hk video_url: {}'.format(video_url))
        assert video_url != ''

        return body, video_url

    def unblock_get_mp_article_html(self, article_url) -> tuple:
        """
        阻塞获取美拍的html
        :param article_url:
        :return:
        """
        driver = BaseDriver(
            # phantomjs被封, 无数据, 改用firefox
            type=FIREFOX,
            executable_path=FIREFOX_DRIVER_PATH,
            load_images=True,
            headless=True,
            user_agent_type=PHONE,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg,)
        driver.get_url_body(
            url=article_url,
            timeout=25,)
        # 点击播放按钮
        driver.find_element(value='div.Button.play-btn').click()
        sleep(2.)
        body = driver._wash_html(html=driver.page_source)
        # self.lg.info(body)

        video_url_sel = {
            'method': 'css',
            'selector': 'div.meipai-player video source ::attr("src")',
        }
        video_url = parse_field(
            parser=video_url_sel,
            target_obj=body,
            logger=self.lg,)
        self.lg.info('Get mp video_url: {}'.format(video_url))
        try:
            del driver
        except:
            try:
                del driver
            except:
                pass
        assert body != '', '获取到mp的body为空值!'
        assert video_url != '', 'mp 的video_url不为空值!'

        return body, video_url

    async def _get_amz_article_html(self, article_url) -> tuple:
        """
        获取amz html
        :param article_url:
        :return:
        """
        video_url = ''
        headers = await async_get_random_headers(
            user_agent_type=1,
            connection_status_keep_alive=False,)
        headers.update({
            'authority': 'aimozhen.com',
            'referer': 'https://aimozhen.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        # 只能获取到iframe, 故切入到视频文章中
        # todo request只能获取到部分的
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            logger=self.lg, )
        # self.lg.info(body)
        assert body != '', '获取hx的body为空值!'

        return body, video_url

    def unblock_get_lsp_article_html(self, article_url) -> tuple:
        """
        阻塞获取梨视频的html
        :param artice_url:
        :return:
        """
        driver = BaseDriver(
            # phantomjs失败率高, 改用firefox
            # type=PHANTOMJS,
            # executable_path=PHANTOMJS_DRIVER_PATH,
            type=FIREFOX,
            executable_path=FIREFOX_DRIVER_PATH,
            ip_pool_type=self.ip_pool_type,
            load_images=True,
            headless=True,
            logger=self.lg,)
        driver.get_url_body(
            url=article_url,
            timeout=25,)
        # driver.save_screenshot('tmp.png')
        # self.lg.info(driver._wash_html(html=driver.page_source))
        driver.find_element(value='i.play-icon.i-icon').click()
        sleep(2.)
        body = driver._wash_html(html=driver.page_source)
        # self.lg.info(body)

        video_url_sel = {
            'method': 'css',
            'selector': 'div.video-main video ::attr("src")',
        }
        video_url = parse_field(
            parser=video_url_sel,
            target_obj=body,
            logger=self.lg,)
        self.lg.info('Get lsp video_url: {}'.format(video_url))
        try:
            del driver
        except:
            pass
        assert video_url != '', 'lsp 的video_url不为空值!'
        assert body != '', '获取到lsp的body为空值!'

        return body, video_url

    async def _get_ck_article_html(self, article_url) -> tuple:
        """
        获取ck html
        :param article_url:
        :return:
        """
        # 走api
        # 获取article_id
        parse_obj = await self._get_parse_obj(article_url_type='ck')
        article_id = await async_parse_field(
            parser=parse_obj['article_id'],
            target_obj=article_url,
            logger=self.lg,)
        assert article_id != '', 'article_id != ""'
        # method1: driver 请求pc地址但是user_agent=phone
        # method2: driver pc 页面转phone, 可获得下方接口
        headers = await async_get_random_headers(
            user_agent_type=1,
            connection_status_keep_alive=False,)
        headers.update({
            'origin': 'https://h5.vmovier.com',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'accept': '*/*',
            'referer': 'https://h5.vmovier.com/index.html?id={}'.format(article_id),
            'authority': 'www.vmovier.com',
        })
        params = (
            ('id', str(article_id)),
        )
        url = 'https://www.vmovier.com/post/getViewData'
        body = await unblock_request(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            logger=self.lg,)
        # self.lg.info(body)
        assert body != '', '获取hx的body为空值!'
        self.hook_target_api_data = json_2_dict(
            json_str=body,
            logger=self.lg,
            default_res={},).get('data', {})
        assert self.hook_target_api_data != {}, 'ck的api data为空dict!'
        # pprint(self.hook_target_api_data)
        video_url = self.hook_target_api_data.get('video_link', '')
        assert video_url != "", 'video_url != ""'

        return body, video_url

    async def _get_hqx_article_html(self, article_url) -> tuple:
        """
        get hqx html
        :param article_url:
        :return:
        """
        video_url = ''
        headers = await async_get_random_headers(user_agent_type=1)
        headers.update({
            # 'Referer': 'http://m.qdaily.com/mobile/homes.html',
            'Referer': article_url,
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            verify=False,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            logger=self.lg,)
        # self.lg.info(body)
        assert body != '', '获取hqx的body为空值!'

        return body, video_url

    async def _get_nfzm_article_html(self, article_url) -> tuple:
        """
        get nfzm html
        :param article_url:
        :return:
        """
        async def get_nfzm_api2():
            """
            获取二版接口
            :return:
            """
            nonlocal article_id

            self.lg.info('getting nfzm 2 version api ...')
            headers = await async_get_random_headers(
                user_agent_type=1,
                connection_status_keep_alive=False,
                cache_control='',
                upgrade_insecure_requests=False,)
            headers.update({
                'accept': 'application/json, text/plain, */*',
                'referer': 'http://www.infzm.com/wap/',
                'origin': 'http://www.infzm.com',
            })
            params = (
                ('version', '1.1.19'),
                ('platform', 'wap'),
                ('machine_id', 'aad315f2d84daf16a62f0fe74131aac0'),
                ('user_id', '3360728'),
                # ('token', '18f407e66d82ba5920ebe88d539f4921x97c7'),
            )
            api_url = 'http://api.infzm.com/mobile/contents/{}'.format(article_id)
            body = await unblock_request(
                url=api_url,
                headers=headers,
                params=params,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.request_num_retries,
                verify=False,
                logger=self.lg,)
            # self.lg.info(body)
            assert body != '', '获取hx的body为空值!'
            hook_target_api_data = await self.get_nfzm_hook_target_api_data(
                body=body,)

            return hook_target_api_data

        # 走api
        video_url = ''
        headers = await async_get_random_headers(user_agent_type=1)
        headers.update({
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        params = (
            ('version', '1.1.15'),
            ('platform', 'wap'),
            ('user_id', ''),
            ('token', ''),
        )
        # 获取article_id
        parse_obj = await self._get_parse_obj(article_url_type='nfzm')
        article_id = await async_parse_field(
            parser=parse_obj['article_id'],
            target_obj=article_url,
            logger=self.lg, )
        assert article_id != '', 'nfzm的article_id != ""'
        api_url = 'http://api.infzm.com/mobile/contents/{}'.format(article_id)
        body = await unblock_request(
            url=api_url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            verify=False,
            logger=self.lg,)
        # self.lg.info(body)
        assert body != '', '获取hx的body为空值!'
        self.hook_target_api_data = await self.get_nfzm_hook_target_api_data(
            body=body,)
        # pprint(self.hook_target_api_data)
        if self.hook_target_api_data.get('content', {}).get('fulltext', '') == '':
            # 可能是会员文章, 用另一接口
            self.hook_target_api_data = await get_nfzm_api2()
        else:
            pass

        return body, video_url

    async def get_nfzm_hook_target_api_data(self, body) -> dict:
        hook_target_api_data = json_2_dict(
            json_str=body,
            logger=self.lg,
            default_res={},).get('data', {})
        assert hook_target_api_data != {}, 'nfzm的api data为空dict!'

        return hook_target_api_data

    async def _get_hx_article_html(self, article_url) -> tuple:
        """
        get hx html
        :param article_url:
        :return:
        """
        video_url = ''
        headers = await async_get_random_headers(
            user_agent_type=1,
            connection_status_keep_alive=False,)
        headers.update({
            'authority': 'm.huxiu.com',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            logger=self.lg,)
        # self.lg.info(body)
        assert body != '', '获取hx的body为空值!'
        has_video_url_sel = {
            'method': 'css',
            'selector': 'div#article-video-head',
        }
        has_video_url = await async_parse_field(
            parser=has_video_url_sel,
            target_obj=body,
            logger=self.lg,)
        if has_video_url != '':
            # 视频文章
            self.lg.info('此为视频文章')
            video_url_sel = {
                'method': 're',
                'selector': ",file: '(.*?)',ak:",
            }
            video_url = await async_parse_field(
                parser=video_url_sel,
                target_obj=body,
                logger=self.lg,)
            self.lg.info('video_url: {}'.format(video_url))
        else:
            pass

        return body, video_url

    async def _get_pp_article_html(self, article_url) -> tuple:
        """
        get pp html
        :param article_url:
        :return:
        """
        headers = await async_get_random_headers(user_agent_type=1)
        headers.update({
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            logger=self.lg, )
        # self.lg.info(body)
        assert body != '', '获取if的body为空值!'

        video_url_sel = {
            'method': 'css',
            'selector': 'div.news_content video source ::attr("src")',
        }
        video_url = await async_parse_field(
            parser=video_url_sel,
            target_obj=body,
            logger=self.lg, )
        if video_url != '':
            self.lg.info('此为视频文章')
            self.lg.info('pp_video_url: {}'.format(video_url))

        return body, video_url

    async def _get_jm_article_html(self, article_url) -> tuple:
        """
        get jm html
        :param article_url:
        :return:
        """
        video_url = ''
        headers = await async_get_random_headers()
        headers.update({
            'referer': 'https://www.jiemian.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            logger=self.lg, )
        # self.lg.info(body)
        assert body != '', '获取if的body为空值!'

        if '/video/' in article_url:
            self.lg.info('此为视频文章')
            video_url_sel = {
                'method': 'css',
                'selector': 'div.video-main video ::attr("src")',
            }
            video_url = await async_parse_field(
                parser=video_url_sel,
                target_obj=body,
                logger=self.lg, )
            self.lg.info('jm_video_url: {}'.format(video_url))

        return body, video_url

    async def _get_ss_article_html(self, article_url) -> tuple:
        """
        获取ss的html
        :param article_url:
        :return:
        """
        video_url = ''
        headers = await async_get_random_headers()
        headers.update({
            'referer': 'https://songshuhui.net/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            logger=self.lg,)
        # self.lg.info(body)
        assert body != '', '获取if的body为空值!'

        return body, video_url

    async def _get_if_article_html(self, article_url) -> tuple:
        """
        获取if的html
        :param article_url:
        :return:
        """
        headers = await async_get_random_headers()
        headers.update({
            'authority': 'www.ifanr.com',
            'referer': 'https://www.ifanr.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 'if-none-match': '"5d101f41-e0ce"',
            # 'if-modified-since': 'Mon, 24 Jun 2019 00:54:25 GMT',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            logger=self.lg,)
        # self.lg.info(body)
        assert body != '', '获取if的body为空值!'
        video_url_sel = {
            'method': 'css',
            'selector': 'iframe.js-video-src',
        }
        video_url = await async_parse_field(
            parser=video_url_sel,
            target_obj=body,
            logger=self.lg,)
        if video_url != '':
            self.lg.info('此为视频文章')
            self.lg.info('cn_video_url: {}'.format(video_url))

        return body, video_url

    async def _get_cn_article_html(self, article_url) -> tuple:
        """
        获取cn的html
        :param article_url:
        :return:
        """
        headers = await async_get_random_headers(user_agent_type=1)
        headers.update({
            'Referer': 'http://m.cnys.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            num_retries=self.request_num_retries,
            logger=self.lg,)
        # self.lg.info(body)
        assert body != '', '获取cn的body为空值!'
        video_url_sel = {
            'method': 'css',
            'selector': 'div.video-play-wrap mip-search-video ::attr("video-src")',
        }
        video_url = await async_parse_field(
            parser=video_url_sel,
            target_obj=body,
            logger=self.lg,)
        if video_url != '':
            self.lg.info('此为视频文章')
            self.lg.info('cn_video_url: {}'.format(video_url))

        return body, video_url

    async def _get_ys_article_html(self, article_url) -> tuple:
        """
        获取51ys的html
        :param article_url:
        :return:
        """
        video_url = ''
        headers = await async_get_random_headers()
        headers.update({
            'referer': 'http://www.51jkst.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            num_retries=self.request_num_retries,
            logger=self.lg,)
        # self.lg.info(body)
        assert body != '', '获取的ys的body为空值!'

        return body, video_url

    async def _get_fh_article_html(self, article_url) -> tuple:
        """
        获取fh的html
        :param article_url:
        :return:
        """
        async def _get_fh_video_url(body) -> str:
            """
            获取video_url
            :param article_url:
            :param body:
            :return:
            """
            vid_selector = {
                'method': 're',
                'selector': ',\"vid\":\"(\w+-\w+-\w+-\w+-\w+)\"',
            }
            m3u8_base_url_selector = {
                'method': 're',
                'selector': ',\"m3u8Url\":\"(.*?)\"',
            }
            vid = await async_parse_field(
                parser=vid_selector,
                target_obj=body,
                logger=self.lg, )
            assert vid != '', 'vid != ""'
            m3u8_base_url = await async_parse_field(
                parser=m3u8_base_url_selector,
                target_obj=body,
                logger=self.lg, )
            assert m3u8_base_url != '', 'm3u8_base_url != ""'
            self.lg.info('Getting auth_params ...')
            headers = await async_get_random_headers()
            headers.update({
                # 'Referer': 'https://v.ifeng.com/c/7n9OP680pzt',
            })
            url = 'https://shankapi.ifeng.com/feedflow/getVideoAuthUrl/{}/getVideoAuthPath'.format(vid)
            params = (
                ('callback', 'getVideoAuthPath'),
            )
            body = await unblock_request(
                url=url,
                headers=headers,
                params=params,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.request_num_retries,
                logger=self.lg)
            # self.lg.info(str(body))
            auth_params = json_2_dict(
                json_str=re.compile('\((.*)\)').findall(body)[0],
                logger=self.lg
            ).get('data', {}).get('authUrl', '')
            assert auth_params != '', 'auth_params != ""'
            self.lg.info('获取到视频auth_params: {}'.format(auth_params))

            video_url = m3u8_base_url.replace('http', 'https') + '?' + auth_params
            self.lg.info('m3u8_url: {}'.format(video_url))

            return video_url

        video_url = ''
        if 'v.ifeng.com' in article_url:
            # 视频
            # 用requests请求body(速度更快)
            # TODO 不用driver, 因为失败率太高!!
            headers = await async_get_random_headers()
            body = await unblock_request(
                url=article_url,
                headers=headers,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.request_num_retries,
                logger=self.lg,)

        else:
            # requests 无效, 无法获取article content
            body = await self._get_html_by_driver(
                url=article_url,
                _type=PHANTOMJS,
                load_images=False,)

        # self.lg.info(str(body))
        assert body != '', '获取fh的body不为空值!'
        if 'v.ifeng.com' in article_url:
            # 视频
            self.lg.info('此为视频文章')
            video_url = await _get_fh_video_url(
                body=body,)

        else:
            pass

        return body, video_url

    async def _get_yg_article_html(self, article_url) -> tuple:
        """
        获取yg article的html
        :param article_url:
        :return:
        """
        exec_code = '''
        # 等待视频自动播放后, 获取网页源码
        sleep(2.5)
        '''
        self.lg.info('此链接为视频链接')
        body = await self._get_html_by_driver(
            url=article_url,
            _type=FIREFOX,
            exec_code=exec_code,
            headless=True,
            load_images=True,)
        # self.lg.info(str(body))
        video_url_selector = {
            'method': 'css',
            'selector': 'div.index-content video ::attr("src")',
        }
        tmp_video_url = await async_parse_field(
            parser=video_url_selector,
            target_obj=body,
            logger=self.lg,)
        video_url = 'https:' + tmp_video_url if tmp_video_url != '' else ''
        # self.lg.info(video_url)

        return body, video_url

    async def _get_xg_article_html(self, article_url) -> tuple:
        """
        获取xg article的html
        :param article_url:
        :return:
        """
        exec_code = '''
        # 等待视频自动播放后, 获取网页源码
        sleep(2.5)
        '''
        self.lg.info('此链接为视频链接')
        body = await self._get_html_by_driver(
            url=article_url,
            _type=FIREFOX,
            exec_code=exec_code,
            headless=True,
            load_images=True,)
        # self.lg.info(str(body))
        video_url_selector = {
            'method': 'css',
            'selector': 'div video ::attr("src")',
        }
        tmp_video_url = await async_parse_field(
            parser=video_url_selector,
            target_obj=body,
            logger=self.lg, )
        video_url = 'https://' + tmp_video_url.replace('http://', '') if tmp_video_url != '' else ''
        # self.lg.info(video_url)

        return body, video_url

    async def _get_zq_article_html(self, article_url) -> tuple:
        """
        获取zq article的html
        :param article_url:
        :return:
        """
        video_url = ''

        # todo 下面这种类型手动需更改为标准的url格式
        # article_url = 'https://focus.youth.cn/mobile/detail?id=17197839#'
        # 标准的url: https://focus.youth.cn/mobile/detail/id/17230881#
        article_url = re.compile('detail\?id=').sub('detail/id/', article_url)
        # self.lg.info(article_url)

        headers = await async_get_random_headers(user_agent_type=1)
        headers.update({
            # 'Referer': 'https://focus.youth.cn/html/articleTop/mobile.html?type=1',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            proxy_type=PROXY_TYPE_HTTPS,
            logger=self.lg)
        # self.lg.info(body)
        assert body != '', '获取zq的body为空值!'

        return body, video_url

    async def _get_bd_article_html(self, article_url) -> tuple:
        """
        获取bd article的html
        :param article_url:
        :return:
        """
        async def _get_hk_params(article_id) -> tuple:
            """
            获取好看视频的article_id和params
            :param article_url:
            :return:
            """
            return (
                ('pd', 'wise'),
                ('vid', str(article_id)),
                ('is_invoke', '1'),
                ('innerIframe', '1'),
                ('type', 'share'),
            )

        async def _get_target_url_and_params_by_article_url(article_url) -> tuple:
            """
            获取最后请求的url跟parmas
            :param article_url:
            :return:
            """
            is_haokan = False
            # 只要是好看视频都可以进 https://haokan.baidu.com/videoui/page/searchresult进行搜索得到对应页面
            if 'm.baidu.com' in article_url:
                # 下面.com在article_url得参数里
                if 'mbd.baidu.com' in article_url:
                    article_id = re.compile('news_(\d+)').findall(article_url)[0]
                    url = 'https://mbd.baidu.com/newspage/data/landingpage'
                    params = (
                        ('context', dumps({
                            'nid': 'news_{}'.format(article_id),
                        })),
                        ('pageType', '1'),
                    )

                elif 'haokan.baidu.com' in article_url:
                    is_haokan = True
                    # 获取视频id
                    article_id = re.compile('vid%253D(\d+)').findall(article_url)[0]
                    # self.lg.info(article_id)
                    url = 'https://haokan.baidu.com/videoui/page/searchresult'
                    params = await _get_hk_params(article_id=article_id)

                else:
                    raise NotImplemented

            elif 'sv.baidu.com' in article_url:
                # 在二级域名上
                is_haokan = True
                # 获取视频id
                article_id = re.compile('sv_(\d+)').findall(article_url)[0]
                url = 'https://haokan.baidu.com/videoui/page/searchresult'
                params = await _get_hk_params(article_id=article_id)

            else:
                params = None
                url = article_url

            # if isinstance(params, tuple):
            #     self.lg.info(_get_url_contain_params(
            #         url=url,
            #         params=params,))

            return url, params, is_haokan

        # TODO bd的文字详情的图片在chrome中无法显示, 但是firefox中可以, 此处还未解决!
        video_url = ''
        headers = await async_get_random_headers(
            user_agent_type=1,)
        headers.update({
            'Referer': 'https://m.baidu.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        url, params, is_haokan = await _get_target_url_and_params_by_article_url(
            article_url=article_url,)

        body = await unblock_request(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
            logger=self.lg)
        # self.lg.info(body)
        assert body != '', '获取bd的body为空值!'

        if is_haokan:
            video_url_selector = {
                'method': 'css',
                'selector': 'div.play1er-box video ::attr("src")',
            }
            video_url = await async_parse_field(
                parser=video_url_selector,
                target_obj=body,
                logger=self.lg,)

        else:
            pass

        return body, video_url

    async def _get_sg_article_html(self, article_url) -> tuple:
        """
        获取搜狗新闻资讯article html
        :param article_url:
        :return:
        """
        headers = await async_get_random_headers(user_agent_type=1)
        headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'https://wap.sogou.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        if '/sgs_video.php' in article_url:
            self.lg.info('该文章含视频!')
            # body 为动态加载的, 需要driver
            body = await self._get_html_by_driver(
                # phantomjs 失败率高!
                # _type=PHANTOMJS,
                _type=FIREFOX,
                url=article_url,
                load_images=False,
                headless=True,)
        else:
            # 包含视频的url容易请求出错
            body = await unblock_request(
                url=article_url,
                headers=headers,
                params=None,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.request_num_retries,
                logger=self.lg)

        # self.lg.info(body)
        assert body != '', '获取sg的body为空值!'

        video_url = ''
        if '/sgs_video.php' in article_url:
            video_url_selector = {
                'method': 'css',
                # 'selector': 'video#my-video source ::attr("src")',
                'selector': 'div.ui-video video ::attr("src")',
            }
            video_url = await async_parse_field(
                parser=video_url_selector,
                target_obj=body,
                logger=self.lg,)
            self.lg.info('video_url: {}'.format(video_url))

        return body, video_url

    async def _get_df_article_html(self, article_url) -> tuple:
        """
        获取东方新闻的html
        :param article_url:
        :return:
        """
        headers = await async_get_random_headers(
            user_agent_type=1,
            connection_status_keep_alive=False,)
        headers.update({
            'Referer': 'http://toutiao.eastday.com/',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            params=None,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg,)
        # self.lg.info(body)
        assert body != '', '获取df的body为空值!'

        video_url = ''
        # self.lg.info(article_url)
        if '/video/' in article_url:
            # 表示该文章为视频文章
            self.lg.info('该文章包含视频!')
            video_url = await self._get_df_video_url(body=body)

        return body, video_url

    async def _get_df_video_url(self, body) -> str:
        """
        获取df的video_url
        :return:
        """
        video_selector = {
            'method': 'css',
            'selector': 'video#J_video ::attr("src")',
        }
        video_url = await async_parse_field(
            parser=video_selector,
            target_obj=body,
            logger=self.lg,)

        video_url = 'https:' + video_url if video_url != '' else ''

        return video_url

    def unblock_get_kd_article_html(self, article_url):
        """
        获取qq看点的html
        :param article_url:
        :return:
        """
        video_url = ''
        if '/kan/video' in article_url:
            self.lg.info('此链接为视频链接')
            driver = BaseDriver(
                # server上调用报: selenium.common.exceptions.WebDriverException: Message: invalid argument: can't kill an exited process
                type=FIREFOX,
                executable_path=FIREFOX_DRIVER_PATH,

                # type=CHROME,
                # executable_path=CHROME_DRIVER_PATH,
                load_images=True,
                # todo 必须是无头, 否则linux server启动驱动失败!!
                headless=True,
                user_agent_type=PHONE,
                ip_pool_type=self.ip_pool_type,
                logger=self.lg,)

            # 播放按钮
            play_btn_css_sel = 'div#video-play span.tvp_button_play'
            driver.get_url_body(
                url=article_url,
                # 必须存在, 否则无后续操作
                css_selector=play_btn_css_sel,
                timeout=25,)
            driver.find_element(value=play_btn_css_sel).click()
            sleep(2.)
            body = driver._wash_html(html=driver.page_source)
            # self.lg.info(body)
            try:
                del driver
            except:
                try:
                    del driver
                except:
                    pass
            video_url_sel = {
                'method': 'css',
                'selector': 'div video ::attr("src")',
            }
            video_url = parse_field(
                parser=video_url_sel,
                target_obj=body,
                logger=self.lg)
            self.lg.info('got kd video_url: {}'.format(video_url))

        else:
            headers = get_random_headers()
            headers.update({
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'authority': 'post.mp.qq.com',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'If-Modified-Since': 'Wed, 15 May 2019 10:17:11 GMT',
            })
            # self.lg.info(article_url)

            body = Requests.get_url_body(
                url=article_url,
                headers=headers,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.request_num_retries,)

        # self.lg.info(body)
        assert body != '', '获取到的kd的body为空值!'

        return body, video_url

    def unblock_get_kb_article_html(self, article_url):
        """
        获取天天快报的html
        :param article_url:
        :return:
        """
        def get_special_case_api_data() -> dict:
            """
            二类情况接口数据获取
            :return:
            """
            nonlocal parse_obj
            # # todo 有两种情况, 一种是文章, 一种是视频
            _id = parse_field(
                parser=parse_obj['article_id2'],
                target_obj=article_url,
                logger=self.lg,
                is_print_error=True,)
            self.lg.info('_id: {}'.format(_id))
            params = (
                ('id', str(_id)),  # eg: '20190721A0JCZT00'
                ('openid', ''),
                # ('ukey', 'ukey_155817081468585658'),
                ('style', 'json'),
            )
            body = Requests.get_url_body(
                url='https://kuaibao.qq.com/getSubNewsContent',
                headers=headers,
                params=params,
                ip_pool_type=self.ip_pool_type,
                # 只进行2次请求, 避免时间过长无法执行下步请求
                num_retries=3,)
            # self.lg.info(body)
            data = json_2_dict(
                json_str=body,
                default_res={},
                logger=self.lg,)
            assert data != {}, 'data 不管是视频或者文章都不为空值!'
            # pprint(data)

            return data

        video_url = ''
        headers = get_random_headers(
            user_agent_type=1,
            connection_status_keep_alive=False,)
        headers.update({
            'authority': 'kuaibao.qq.com',
        })
        body = Requests.get_url_body(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=2,)
        # self.lg.info(body)
        assert body != '', '获取到的kb的body为空值!'
        parse_obj = self.unblock_get_parse_obj(article_url_type='kb')
        article_title = parse_field(
            parser=parse_obj['title'],
            target_obj=body,
            logger=self.lg,)
        if article_title == '':
            self.hook_target_api_data = get_special_case_api_data()
            # pprint(self.hook_target_api_data)
            # todo play_url != ""表明是视频文章
            play_url = self.hook_target_api_data\
                .get('attribute', {})\
                .get('VIDEO_0', {})\
                .get('playurl', '')
            # self.lg.info('play_url: {}'.format(play_url))

            if play_url != '':
                # 单独处理含视频的
                # 表示title获取到为空值, 可能是含视频的
                # TODO 暂时先不获取天天快报含视频的
                self.lg.info('此article_url可能含有视频')
                driver = BaseDriver(
                    # type=FIREFOX,
                    # executable_path=FIREFOX_DRIVER_PATH,

                    # server上chrome成功, firefox一直显示超时, 故用chromedriver
                    type=CHROME,
                    executable_path=CHROME_DRIVER_PATH,
                    load_images=True,
                    headless=True,
                    user_agent_type=PHONE,
                    ip_pool_type=self.ip_pool_type,
                    logger=self.lg,)
                driver.get_url_body(
                    url=article_url,
                    # 必须等待这个显示后再关闭, 否则无video_url
                    css_selector='div#mainVideo video',
                    timeout=25,)
                # 点击播放按钮
                try:
                    # 第一类
                    driver.find_element(value='div.play-btn').click()
                except Exception:
                    self.lg.error('遇到错误:', exc_info=True)
                    # 第二类
                    driver.find_element(value='txpdiv.txp_btn_play').click()
                sleep(2.)
                body = driver._wash_html(html=driver.page_source)
                try:
                    del driver
                except:
                    try:
                        del driver
                    except:
                        pass
                # self.lg.info(body)
                # TODO 有多种视频类型格式, 先处理这种
                video_url_sel = {
                    'method': 'css',
                    'selector': 'div#mainVideo video:nth-child(1) ::attr("src")',
                }
                video_url = parse_field(
                    parser=video_url_sel,
                    target_obj=body,
                    logger=self.lg,)
                self.lg.info('video_url: {}'.format(video_url))

            else:
                self.lg.info('此文章为二类图文文章!')

        else:
            pass

        return body, video_url

    def _wash_wx_article_body(self, article_url, body) -> tuple:
        """
        清洗wx文章
        :return: body, video_url
        """
        # 处理微信防盗链
        body = re.compile('<head>').sub('<head><meta name=\"referrer\" content=\"never\">', body)
        body = re.compile('data-src=').sub('src=', body)

        video_url = ''
        # 单独处理含视频标签的
        try:
            # todo 现在wx的video iframe內值src 再去请求都是视频加载失败!(先不处理,)
            # videos_url_list = re.compile('<div class=\"tvp_video\"><video.*?src=\"(.*?)\"></video><div class=\"tvp_shadow\">').findall(body)
            videos_url_list = re.compile('<iframe class=\"video_iframe.*?\" .*? src=\"(.*?)\"></iframe>').findall(body)
            assert videos_url_list != []
            self.lg.info('视频list: {}'.format(videos_url_list))
            self.lg.info('此文章含视频! 正在重新获取文章html...')

            driver = BaseDriver(
                # type=PHANTOMJS,
                # executable_path=PHANTOMJS_DRIVER_PATH,
                type=FIREFOX,
                executable_path=FIREFOX_DRIVER_PATH,

                user_agent_type=PC,
                load_images=True,                   # 加载图片
                headless=False,
                logger=self.lg,
                ip_pool_type=self.ip_pool_type,
            )
            # driver.get_url_body(
            #     url=article_url,
            #     timeout=20,)
            # sleep(1.5)
            # try:
            #     driver.find_element(value='i.icon_mid_play').click()
            #     sleep(5.)
            # except Exception:
            #     self.lg.error('遇到错误: ', exc_info=True)
            #
            # video_body = driver._wash_html(html=driver.page_source)
            # self.lg.info('video_body: {}'.format(video_body))
            # 筛选出来的iframe src为无效url
            # video_iframe_list = re.compile('<iframe.*?>.*?</iframe>').findall(video_body)
            # pprint(video_iframe_list)
            # for item in video_iframe_list:
            #     print(item)
            # video_src_list_sel = {
            #     'method': 're',
            #     'selector': '<iframe.*? src=\"(.*?)\".*?>.*?</iframe>',
            # }
            # video_src_list = parse_field(
            #     parser=video_src_list_sel,
            #     target_obj=video_body,
            #     logger=self.lg,
            #     is_first=False,)
            # pprint(video_src_list)
            #
            # for item in video_src_list:
            #     item = re.compile('&amp;').sub('&', item)
            #     item = re.compile('&article_title=.*?......').sub('', item)
            #     item = re.compile('&random_num=.*?......').sub('', item)
            #     item = re.compile('&scene=.*?......').sub('', item)
            #     item = re.compile('%A8%E7%99%BD%E6%88%91%E4%BB%AC%E6%9C%80%E5%A5%BD%E7%9A%84%E2%80%9C%E9%98%BF%E4%B8%AD%E5%93%A5%E5%93%A5%E2%80%9D%EF%BC%8C%E8%BF%99%E4%BA%94%E4%B8%AA%E5%9F%8E%E5%B8%82%E7%8E%A9%E5%97%A8%E4%BA%86......').sub('', item)
            #     item = re.compile('&version=.*?\.js').sub('', item)
            #     item = 'https://mp.weixin.qq.com' + item
            #     print(item)

            # https://mp.weixin.qq.com/mp/videoplayer?video_h=186.75&amp;video_w=332&amp;scene=&amp;random_num=3913&amp;article_title=%E4%B8%BA%E8%A1%A8%E7%99%BD%E6%88%91%E4%BB%AC%E6%9C%80%E5%A5%BD%E7%9A%84%E2%80%9C%E9%98%BF%E4%B8%AD%E5%93%A5%E5%93%A5%E2%80%9D%EF%BC%8C%E8%BF%99%E4%BA%94%E4%B8%AA%E5%9F%8E%E5%B8%82%E7%8E%A9%E5%97%A8%E4%BA%86......&amp;source=4&amp;vid=wxv_970345944447320066&amp;mid=2654654251&amp;idx=1&amp;__biz=MjM5NzI1MTY0MQ==&amp;nodetailbar=0&amp;uin=&amp;key=&amp;pass_ticket=&amp;version=/mmbizwap/zh_CN/htmledition/js/appmsg/index480909.js&amp;devicetype=&amp;wxtoken=777&amp;sessionid=svr_11683bddae1&amp;preview=0
            # https://mp.weixin.qq.com/mp/videoplayer?video_h=186.75&amp;video_w=332&amp;scene=&amp;random_num=3913&amp;source=4&amp;vid=wxv_970345944447320066&amp;mid=2654654251&amp;idx=1&amp;__biz=MjM5NzI1MTY0MQ==&amp;nodetailbar=0&amp;uin=&amp;key=&amp;pass_ticket=&amp;version=/mmbizwap/zh_CN/htmledition/js/appmsg/index480909.js&amp;devicetype=&amp;wxtoken=777&amp;sessionid=svr_11683bddae1&amp;preview=0
            # 真实video_url: http://mpvideo.qpic.cn/tjg_3889235330_50000_ebf83ae259fd4629b6398d9b410e7334.f10002.mp4?dis_k=4034e2a5a2103ae29dd781b14286888d&amp;dis_t=1567481729

            tmp_body = driver.get_url_body(
                url=videos_url_list[0],
                timeout=20.,)
            # self.lg.info(tmp_body)
            assert tmp_body != '', 'tmp_body为空值!'

            try:
                del driver
            except:
                pass

            try:
                embed_div = re.compile('(<embed.*?)</div></div>').findall(tmp_body)[0]
                # self.lg.info(embed_div)
                # 获取video 的width, height
                video_width_and_height_tuple = re.compile('bgcolor=\".*?\" width=\"(\d+)px\" height=\"(\d+)px\"').findall(embed_div)[0]
                embed_div = '<embed width="{}px" height="{}px" src="{}" />'.format(
                    video_width_and_height_tuple[0],
                    video_width_and_height_tuple[1],
                    videos_url_list[0])
            except IndexError:
                raise IndexError('获取video_div时索引异常!')

            video_div = '<div style=\"text-align:center; width:100%; height:100%;\">' + embed_div + '</div>'
            # self.lg.info(video_div)
            # (只处理第一个视频)
            body = re.compile('<iframe class=\"video_iframe.*?\" .*?></iframe>').sub(
                repl=video_div,
                string=body,
                count=1,)
            video_url = videos_url_list[0]
        except AssertionError:
            pass
        except Exception:
            self.lg.error('遇到错误: ', exc_info=True)
        # self.lg.info(body)

        return body, video_url

    def unblock_get_parse_obj(self, article_url_type) -> dict:
        """
        获取到对应的解析对象
        :param article_url_type:
        :return:
        """
        for item in ARTICLE_ITEM_LIST:
            if article_url_type == item.get('short_name', ''):
                if item.get('obj_origin', '') == \
                        self.obj_origin_dict[article_url_type].get('obj_origin', ''):
                    parse_obj = item

                    return parse_obj

        raise NotImplementedError('未找到解析对象!')

    async def _get_parse_obj(self, article_url_type) -> dict:
        """
        获取到对应解析对象
        :return:
        """
        return self.unblock_get_parse_obj(
            article_url_type=article_url_type,)

    async def _get_praise_num(self, parse_obj, target_obj):
        """
        点赞数
        :param parse_obj:
        :param target_obj:
        :return:
        """
        praise_num = 0
        _ = await async_parse_field(
            parser=parse_obj['praise_num'],
            target_obj=target_obj,
            logger=self.lg)
        # self.lg.info(str(_))
        try:
            praise_num = int(_)
        except:
            pass

        return praise_num

    async def _get_fav_num(self, parse_obj, target_obj):
        """
        收藏数
        :param parse_obj:
        :param target_obj:
        :return:
        """
        short_name = parse_obj['short_name']
        fav_num = await async_parse_field(
            parser=parse_obj['fav_num'],
            target_obj=target_obj,
            logger=self.lg)

        if short_name == 'ck':
            fav_num = self.hook_target_api_data.get('count_like', 0)

        elif short_name == 'xq':
            fav_num = self.hook_target_api_data.get('fav_count', 0)

        else:
            pass

        try:
            fav_num = int(fav_num)
        except:
            fav_num = 0

        return fav_num

    async def _get_profile(self, parse_obj, target_obj):
        """
        推荐人简介或个性签名
        :param parse_obj:
        :param target_obj:
        :return:
        """
        short_name = parse_obj['short_name']

        profile = await async_parse_field(
            parser=parse_obj['profile'],
            target_obj=target_obj,
            logger=self.lg)

        if short_name == 'xq':
            profile = self.hook_target_api_data\
                .get('user', {})\
                .get('description', '')
        else:
            pass

        return profile

    async def _get_author(self, parse_obj, target_obj, video_url):
        """
        作者
        :param parse_obj:
        :param target_obj:
        :return:
        """
        short_name = parse_obj['short_name']
        author_selector = parse_obj['author']

        short_name_list = [
            'kb',
            'kd',
            'sg',
            'bd',
            'fh',
            'cn',
            'if',
            'ss',
            'jm',
            'pp',
            'hx',
            'hqx',
            'xg',
            'lsp',
            '7y7',
            'qqbb',
            'ft',
            '91mt',
            '5h',
            'bdj',
        ]
        if short_name in short_name_list:
            if video_url != '':
                author_selector = parse_obj['video_author']
            else:
                pass

        else:
            pass

        # self.lg.info(target_obj)
        author = await async_parse_field(
            parser=author_selector,
            target_obj=target_obj,
            logger=self.lg)
        if short_name == 'kb':
            if video_url != '':
                if author == '':
                    author_selector2 = parse_obj['video_author2']
                    author = await async_parse_field(
                        parser=author_selector2,
                        target_obj=target_obj,
                        logger=self.lg,)
                    if author == '':
                        author_selector3 = parse_obj['video_author3']
                        author = await async_parse_field(
                            parser=author_selector3,
                            target_obj=target_obj,
                            logger=self.lg, )
            else:
                if author == '':
                    author = self.hook_target_api_data\
                        .get('card', {})\
                        .get('chlname', '')
                else:
                    pass

        elif short_name == 'pp':
            if author == '':
                # 湃客发的文章
                author_selector2 = parse_obj['author2']
                author = await async_parse_field(
                    parser=author_selector2,
                    target_obj=target_obj,
                    logger=self.lg, )

        elif short_name == 'nfzm':
            author = self.hook_target_api_data['content']['author']

        elif short_name == 'ck':
            author = self.hook_target_api_data['editor_username']

        elif short_name == 'xq':
            author = self.hook_target_api_data.get('user', {}).get('screen_name', '')

        else:
            pass

        short_name_list2 = [
            'df',
            'bd',
            'fh',
            'ys',
            'cn',
            'if',
            'ss',
            'jm',
            'pp',
            'hx',
            'nfzm',
            'hqx',
            'xg',
            'ck',
            'lsp',
            'amz',
            'kd',
            '7y7',
            'qqbb',
            'ft',
            '91mt',
            'xq',
            '5h',
            'bdj',
        ]
        if short_name in short_name_list2:
            pass
        else:
            assert author != '', '获取到的author为空值!'

        return author

    async def _get_article_title(self, parse_obj, target_obj, video_url):
        """
        文章title
        :param parse_obj:
        :param target_obj:
        :return:
        """
        short_name = parse_obj['short_name']
        title_selector = parse_obj['title']
        # self.lg.info(target_obj)

        short_name_list = [
            'df',
            'kb',
            'kd',
            'sg',
            'bd',
            'fh',
            'cn',
            'if',
            'ss',
            'jm',
            'pp',
            'hx',
            'hqx',
            'xg',
            'lsp',
            '7y7',
            'qqbb',
            'ft',
            '91mt',
            '5h',
            'bdj',
        ]
        if short_name in short_name_list:
            if video_url != '':
                title_selector = parse_obj['video_title']
            else:
                pass
        else:
            pass

        # self.lg.info(target_obj)
        title = await async_parse_field(
            parser=title_selector,
            target_obj=target_obj,
            logger=self.lg)

        if short_name == 'kb':
            if video_url != '':
                if title == '':
                    # 情况1:
                    title_selector2 = parse_obj['video_title2']
                    # pprint(title_selector2)
                    title = await async_parse_field(
                        parser=title_selector2,
                        target_obj=target_obj,
                        logger=self.lg,)
                    if title == '':
                        # 情况2
                        title_selector3 = parse_obj['video_title3']
                        # pprint(title_selector3)
                        title = await async_parse_field(
                            parser=title_selector3,
                            target_obj=target_obj,
                            logger=self.lg, )
                    else:
                        pass
                else:
                    pass
            else:
                if title == '':
                    # 情况1
                    title = self.hook_target_api_data['title']
                else:
                    pass

        elif short_name == 'nfzm':
            # pprint(self.hook_target_api_data)
            title = self.hook_target_api_data['content']['subject']

        elif short_name == 'ck':
            title = self.hook_target_api_data['title']

        elif short_name == 'xq':
            title = self.hook_target_api_data.get('title', '')

        else:
            pass

        title = await self._wash_title(
            short_name=short_name,
            title=title)
        assert title != '', '获取到的title为空值!'
        # self.lg.info(title)

        return title

    async def _wash_title(self, short_name, title) -> str:
        """
        清洗title
        :param short_name:
        :param title:
        :return:
        """
        if short_name == 'tt':
            title = await self._wash_tt_title(title=title)
        else:
            pass

        return title

    @staticmethod
    async def _wash_tt_title(title: str) -> str:
        """
        :param title:
        :return:
        """
        title = fix_text(text=title[6:-6])

        return title

    async def _get_head_url(self, parse_obj, target_obj, video_url) -> str:
        """
        得到文章发布者的头像url
        :param parse_obj:
        :param target_obj:
        :return:
        """
        short_name = parse_obj['short_name']
        head_url_sel = parse_obj['head_url']

        short_name_list = [
            'kb',
            'kd',
            'hx',
            'hqx',
            'lsp',
            '7y7',
            'qqbb',
            'ft',
            '91mt',
            'bdj',
        ]
        if short_name in short_name_list:
            if video_url != '':
                head_url_sel = parse_obj['video_head_url']
            else:
                pass
        else:
            pass

        # self.lg.info(target_obj)
        head_url = await async_parse_field(
            parser=head_url_sel,
            target_obj=target_obj,
            logger=self.lg)

        if short_name == 'kb':
            if video_url != '':
                if head_url == '':
                    head_url_sel2 = parse_obj['video_head_url2']
                    head_url = await async_parse_field(
                        parser=head_url_sel2,
                        target_obj=target_obj,
                        logger=self.lg)
                else:
                    pass
            else:
                pass

        elif short_name == '7y7':
            if video_url != '':
                pass
            else:
                head_url = 'https://i.7y7.com' + head_url if head_url != '' else ''

        elif short_name == 'xq':
            head_url = ''

        elif short_name == 'bdj':
            # 小头像换成原图
            head_url = head_url.replace('_mini', '')

        else:
            pass

        # 天天快报存在头像为''
        if head_url != '' \
                and not head_url.startswith('http'):
            head_url = 'https:' + head_url
        else:
            pass

        return head_url

    async def _get_share_id(self, **kwargs) -> str:
        """
        得到唯一的share_id
        :return:
        """
        article_url_type = kwargs.get('article_url_type', '')
        article_url = kwargs.get('article_url', '')
        video_url = kwargs.get('video_url', '')
        parse_obj = kwargs.get('parse_obj', {})
        short_name = parse_obj.get('short_name', '')

        short_name_list = [
            'wx',
            'sg',
        ]
        if article_url_type in short_name_list:
            return get_uuid1()

        article_id_selector = await self._get_article_id_selector(
            article_url_type=article_url_type,
            article_url=article_url,)
        share_id = await async_parse_field(
            parser=article_id_selector,
            target_obj=article_url,
            logger=self.lg)

        short_name_list2 = [
            'kb',
            'zq',
        ]
        if short_name in short_name_list2:
            if share_id == '':
                share_id = await async_parse_field(
                    parser=parse_obj['article_id2'],
                    target_obj=article_url,
                    logger=self.lg)
            else:
                pass

        elif short_name == 'kd':
            if share_id == '':
                # 视频文章id
                share_id = get_uuid1()
            else:
                pass

        else:
            pass

        assert share_id != '', '获取到的share_id为空值!'

        return share_id

    async def _get_article_id_selector(self, article_url_type, article_url) -> (dict, None):
        """
        获取article_id的selector
        :param self:
        :param article_url_type:
        :return:
        """
        for item in ARTICLE_ITEM_LIST:
            if article_url_type == item.get('short_name', ''):
                if article_url_type == 'bd':
                    if 'haokan.baidu.com' in article_url:
                        return item['video_id']

                    elif 'sv.baidu.com' in article_url:
                        return item['video_id2']

                    else:
                        pass

                elif article_url_type == 'jm':
                    if '/video/' in article_url:
                        return item['video_id']

                else:
                    pass

                return item['article_id']

        raise NotImplementedError

    async def _get_comment_num(self, parse_obj, target_obj) -> int:
        """
        文章评论数
        :param parse_obj:
        :param target_obj:
        :return:
        """
        comment_num = 0
        short_name = parse_obj['short_name']

        _ = await async_parse_field(
            parser=parse_obj['comment_num'],
            target_obj=target_obj,
            logger=self.lg)
        # self.lg.info(str(_))

        if short_name == 'nfzm':
            comment_num = self.hook_target_api_data['content']['comment_count']

        elif short_name == 'ck':
            comment_num = self.hook_target_api_data['count_comment']

        elif short_name == 'kb':
            if _ == '':
                comment_num = self.hook_target_api_data\
                    .get('count_info', {})\
                    .get('comments', '')
            else:
                pass

        else:
            pass

        try:
            comment_num = int(_)
        except ValueError:      # 未提取到评论默认为0
            pass

        return comment_num

    async def _get_tags_list(self, parse_obj, video_url, target_obj) -> list:
        """
        获取文章的tags list
        :param parse_obj:
        :param target_obj:
        :return:
        """
        short_name = parse_obj['short_name']

        is_first = False
        if short_name == 'kd'\
                or short_name == 'bd':
            # 取第一个str
            is_first = True

        short_name_list = [
            'kd',
            '7y7',
            'qqbb',
            'ft',
        ]
        tags_list_sel = parse_obj['tags_list']
        if short_name in short_name_list:
            if video_url != '':
                tags_list_sel = parse_obj['video_tags_list']
            else:
                pass
        else:
            pass

        tags_list = await async_parse_field(
            parser=tags_list_sel,
            target_obj=target_obj,
            is_first=is_first,
            logger=self.lg)
        if tags_list == '':
            return []

        short_name_list2 = [
            'tt',
            'js',
            'kd',
            'if',
            'ss',
            'lsp',
            '7y7',
            'qqbb',
        ]
        if short_name in short_name_list2:
            tags_list = [{
                'keyword': i,
            } for i in tags_list]

        elif short_name == 'kd':
            tags_list = tags_list.split(',')

        elif short_name == 'bd':
            # self.lg.info(str(tags_list))
            if tags_list != '':
                ori_tag_json_data = tags_list + ']'
                tmp_tag_list = json_2_dict(
                    json_str=ori_tag_json_data,
                    default_res=[],
                    logger=self.lg)
                # pprint(tmp_tag_list)
                tags_list = []
                for item in tmp_tag_list:
                    try:
                        name = item.get('name', '')
                        assert name != '', 'name != ""'
                    except AssertionError:
                        continue
                    tags_list.append({
                        'keyword': name,
                    })
                # pprint(tags_list)

            else:
                pass

        elif short_name == 'nfzm':
            tags_list = []
            ori_tags_list = self.hook_target_api_data['content']['tags']
            for item in ori_tags_list:
                try:
                    tag_name = item.get('title', '')
                    assert tag_name != ''
                except AssertionError:
                    continue
                tags_list.append({
                    'keyword': tag_name,
                })

        else:
            pass

        tags_list = list_remove_repeat_dict_plus(
            target=tags_list,
            repeat_key='keyword',)

        return tags_list

    async def _get_article_create_time(self, parse_obj, target_obj, video_url, article_url) -> str:
        """
        文章创建时间点
        :param parse_obj:
        :param target_obj:
        :return:
        """
        async def parse_create_time(short_name, create_time) -> str:
            """
            解析create_time
            :param create_time:
            :return:
            """
            try:
                create_time = str(date_parse(create_time))
            except ValueError:
                self.lg.error('获取article create_time时, 遇到错误:', exc_info=True)
                self.lg.info('默认设置当前时间为文章创建时间点!')
                create_time = str(get_shanghai_time())

            return create_time

        short_name = parse_obj['short_name']
        create_time_selector = parse_obj['create_time']

        short_name_list = [
            'sg',
            'bd',
            'cn',
            'if',
            'ss',
            'jm',
            'pp',
            'hx',
            'hqx',
            'xg',
            'lsp',
            'kd',
            '7y7',
            'qqbb',
            'ft',
            '91mt',
            'xq',
            '5h',
            'bdj',
        ]
        if short_name in short_name_list:
            if video_url != '':
                create_time_selector = parse_obj['video_create_time']
            else:
                pass

        elif short_name == 'fh':
            if video_url != '':
                create_time_selector = parse_obj['video_create_time']
            else:
                if 'feng.ifeng.com' in article_url:
                    create_time_selector = parse_obj['create_time2']
                else:
                    pass

        else:
            pass

        # self.lg.info(target_obj)
        create_time = await async_parse_field(
            parser=create_time_selector,
            target_obj=target_obj,
            logger=self.lg)
        # self.lg.info(create_time)
        short_name_list2 = [
            'cn',
            'if',
            'ss',
            'jm',
            'pp',
            'hx',
            'hqx',
            'lsp',
            'mp',
            '7y7',
            'qqbb',
            'ft',
            '91mt',
            '5h',
        ]
        short_name_list3 = [
            'js',
            'kd',
            'bdj',
        ]
        if short_name == 'sg':
            if video_url != '':
                # 原先为2019/05/05 11:13, 替换为标准的
                create_time = await parse_create_time(
                    short_name=short_name,
                    create_time=create_time,)

            else:
                create_time = create_time.replace('/', '-')

        elif short_name == 'bd':
            if video_url != '':
                pass

            else:
                if create_time != '':
                    try:
                        create_time = str(timestamp_to_regulartime(create_time[:10]))
                    except Exception:
                        self.lg.error('遇到错误:', exc_info=True)
                        create_time = ''

        elif short_name in short_name_list2:
            if create_time != '':
                create_time = await parse_create_time(
                    short_name=short_name,
                    create_time=create_time)

        elif short_name == 'kb':
            if create_time == '':
                create_time = await parse_create_time(
                    short_name=short_name,
                    create_time=self.hook_target_api_data.get('pub_time', ''),)
            else:
                pass

        elif short_name in short_name_list3:
            if create_time != '':
                # eg: ori_data = '1565402168'
                create_time = create_time[0:10] if isinstance(create_time, str) else create_time
                create_time = str(timestamp_to_regulartime(int(create_time)))
                # self.lg.info(create_time)
            else:
                pass

        elif short_name == 'nfzm':
            create_time = await parse_create_time(
                short_name=short_name,
                create_time=self.hook_target_api_data['content']['publish_time'])

        elif short_name == 'ck':
            create_time = str(timestamp_to_regulartime(int(self.hook_target_api_data['publish_time'])))

        elif short_name == 'hk':
            if create_time != '':
                # 原先'2019年7月9日'
                create_time = create_time.replace('年', '-').replace('月', '-').replace('日', '-')
                create_time = await parse_create_time(
                    short_name=short_name,
                    create_time=create_time)

        elif short_name == 'xq':
            try:
                create_time = timestamp_to_regulartime(
                    int(str(self.hook_target_api_data.get('created_at', ''))[0:10]))
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)

        else:
            pass

        if create_time == '':
            create_time = str(get_shanghai_time())
        else:
            pass
        # assert create_time != '', '获取到的create_time为空值!'

        return create_time

    async def _get_article_content(self, parse_obj, target_obj, article_url, video_url) -> str:
        """
        article content
        :return:
        """
        short_name = parse_obj.get('short_name', '')
        content_selector = parse_obj['content']

        short_name_list = [
            'kb',
            'kd',
            'cn',
            'if',
            'ss',
            'jm',
            'pp',
            'hx',
            'hqx',
            'xg',
            'lsp',
            '7y7',
            'qqbb',
            'ft',
            '91mt',
            '5h',
            'bdj',
        ]
        if short_name in short_name_list:
            if video_url != '':
                content_selector = parse_obj['video_article_content']
            else:
                pass

        elif short_name == 'fh':
            if video_url != '':
                content_selector = parse_obj['video_article_content']
            else:
                if 'feng.ifeng.com' in article_url:
                    content_selector = parse_obj['content2']
                else:
                    pass
        else:
            pass

        # self.lg.info(str(target_obj))
        # pprint(content_selector)
        content = await async_parse_field(
            parser=content_selector,
            target_obj=target_obj,
            logger=self.lg)

        short_name_list3 = [
            'hx',
            'hqx',
        ]
        short_name_list4 = [
            '7y7',
            'qqbb',
        ]
        if short_name in short_name_list3:
            if video_url == '' and content != '':
                # 加上主图
                article_main_img_div = await async_parse_field(
                    parser=parse_obj['article_main_img'],
                    target_obj=target_obj,
                    logger=self.lg)
                content = article_main_img_div + content
            else:
                pass

        elif short_name == 'kb':
            if video_url != '':
                pass
            else:
                if content == '':
                    # 第二类图文
                    content = self.hook_target_api_data.get('cnt_html_origin', '')
                    if content == '':
                        # 第三类图文
                        ori_content = self.hook_target_api_data.get('orig_content', [])
                        for item in ori_content:
                            try:
                                _type = item.get('type' '')
                                if _type == 'img_url':
                                    img_url = item.get('img_url', '')
                                    assert img_url != ''
                                    content += '<img src=\"{}\">'.format(img_url)
                                elif _type == 'cnt_article':
                                    _desc = item.get('desc', '')
                                    assert _desc != ''
                                    content += '<p>{}</p>'.format(_desc)
                                else:
                                    raise ValueError('_type: {}, 值异常!'.format(_type))

                            except (AssertionError, Exception):
                                # self.lg.error('遇到错误:', exc_info=True)
                                continue

                    else:
                        pass
                    if content == '':
                        # 第四类图文
                        kb_attribute = self.hook_target_api_data.get('attribute', {})
                        # eg: '<P>这个男厕的将小便池和洗手池结合的一体化设计，洗手的水顺便也能清理小便池，充分利用了水资源！</P><P><!--IMG_0--></P>'
                        kb_content = self.hook_target_api_data\
                            .get('content', {})\
                            .get('text', '')

                        # pprint(kb_attribute)
                        # self.lg.info(kb_content)
                        for key, value in kb_attribute.items():
                            # eg: key = 'IMG_0'
                            try:
                                img_url = value.get('url', '')
                                assert img_url != ''
                                kb_content = kb_content.replace('<!--{}-->'.format(key), '<img src=\"{}\">'.format(img_url))
                            except (AssertionError, Exception):
                                # self.lg.error('遇到错误:', exc_info=True)
                                continue

                        # self.lg.info(str(kb_content))
                        content = kb_content

                    else:
                        pass
                else:
                    pass

        elif short_name == 'nfzm':
            content = self.hook_target_api_data['content']['fulltext']

        elif short_name == 'ck':
            content = self.hook_target_api_data['content']

        elif short_name == 'xq':
            content = self.hook_target_api_data.get('text', '')

        elif short_name == 'amz':
            # 不管content是否为空, 都进入
            video_iframe = await self._get_amz_video_iframe(
                parse_obj=parse_obj,
                target_obj=target_obj,)
            self.lg.info('video_iframe: {}'.format(video_iframe))
            # 视频iframe在前面
            content = video_iframe + content

        elif short_name in short_name_list4:
            if video_url != '':
                pass
            else:
                if content != '':
                    # 加上最上方描述div
                    desc_div = await async_parse_field(
                        parser=parse_obj['desc_div'],
                        target_obj=target_obj,
                        logger=self.lg)
                    if desc_div != '':
                        content = '<p>{}</p>'.format(desc_div) + content
                    else:
                        pass
                else:
                    pass

        else:
            pass

        short_name_list2 = [
            'df',
            'sg',
            'bd',
            'kb',
            'kd',
            'yg',
            'fh',
            'cn',
            'if',
            'ss',
            'jm',
            'pp',
            'hx',
            'nfzm',
            'hqx',
            'xg',
            'ck',
            'lsp',
            'mp',
            'hk',
            '7y7',
            'qqbb',
            'ft',
            '91mt',
            'xq',
            '5h',
            'bdj',
        ]
        if short_name in short_name_list2:
            if video_url != '':
                pass
            else:
                assert content != '', '获取到的content为空值!'

        else:
            assert content != '', '获取到的content为空值!'

        content = await self._wash_article_content(
            short_name=short_name,
            content=content,)
        content = await self.unify_wash_article_content(
            short_name=short_name,
            content=content,)
        # hook 防盗链
        content = '<meta name=\"referrer\" content=\"never\">' + content if content != '' else ''
        print(content)
        # cp后台处理, 此处不处理
        # content = await self._wash_my_style_in_content(content=content)
        # self.lg.info(content)

        return content

    @staticmethod
    async def unify_wash_article_content(short_name: str, content) -> str:
        """
        统一清洗
        :param content:
        :return:
        """
        content = wash_sensitive_info(
            data=content,
            replace_str_list=None,
            add_sensitive_str_list=[
                '<br>',
                '禁止转发',
                '禁止转载',
                '私自转载',
                '追究法律责任',
                '图片来源于网络，如有侵权请联系删除',
                '图文原创',
                '搬运必究',
            ],
            is_default_filter=False,
            is_lower=False,)
        if content != '':
            content += '<br><p><strong>免责声明: 文章来源于网络, 仅供个人研究学习, 不涉及商业盈利目的, 如有侵权请及时联系管理员删除! 谢谢!</strong></p>'
        else:
            pass

        return content

    @staticmethod
    async def _wash_my_style_in_content(content: str) -> str:
        """
        清洗掉自己的样式
        :param self:
        :param content:
        :return:
        """
        content = wash_sensitive_info(
            data=content,
            replace_str_list=None,
            add_sensitive_str_list=[
                '<meta name=\"referrer\" content=\"never\">',
                # 图片居中, p, 原生style
                '<style type=\"text/css\">.*?</style>',
            ],
            is_default_filter=False,
            is_lower=False,)

        return content

    async def _get_amz_video_iframe(self, parse_obj, target_obj) -> str:
        """
        获取amz video_iframe
        :param parse_obj:
        :param target_obj:
        :return:
        """
        video_iframe = await async_parse_field(
            parser=parse_obj['video_iframe'],
            target_obj=target_obj,
            logger=self.lg, )
        if video_iframe == '':
            # 第二种情况视频处理, 生成iframe(eg: 优酷视频云)
            client_id = await async_parse_field(
                parser=parse_obj['client_id'],
                target_obj=target_obj,
                logger=self.lg, )
            assert client_id != ''
            vid = await async_parse_field(
                parser=parse_obj['vid'],
                target_obj=target_obj,
                logger=self.lg, )
            assert vid != ''
            # eg: https://player.youku.com/embed/XNDExMjEzMzMxNg==?client_id=53c06c7e23bff2b5&amp;password=&amp;autoplay=true#aimozhen.com
            iframe_src = 'https://player.youku.com/embed/{vid}?client_id={client_id}&amp;password=&amp;autoplay=true#aimozhen.com'.format(
                vid=vid,
                client_id=client_id, )
            self.lg.info('生成的iframe_src: {}'.format(iframe_src))
            video_iframe = '<iframe width=\"100%\" height=\"100%\" allow=\"autoplay\" src=\"{iframe_src}\" name=\"iframeId\" id=\"iframeId\" frameborder=\"0\" allowfullscreen=\"true\" scrolling=\"no\"></iframe>'.format(
                iframe_src=iframe_src, )
        else:
            pass
        assert video_iframe != '', 'amz的video_iframe不为空值!'

        return video_iframe

    async def _wash_article_content(self, short_name: str, content: str) -> str:
        """
        清洗content
        :param short_name:
        :param content:
        :return:
        """
        if short_name == 'tt':
            # html乱码纠正
            content = await self._wash_tt_article_content(content=content)

        elif short_name == 'js':
            # 图片处理
            content = await self._wash_js_article_content(content=content)

        elif short_name == 'kd':
            # 图片处理
            content = await self._wash_kd_article_content(content=content)

        elif short_name == 'kb':
            # css 处理为原生的
            content = await self._wash_kb_article_content(content=content)

        elif short_name == 'wx':
            content = await self._wash_wx_article_content(content=content)

        elif short_name == 'df':
            content = await self._wash_df_article_content(content=content)

        elif short_name == 'sg':
            content = await self._wash_sg_article_content(content=content)

        elif short_name == 'bd':
            content = await self._wash_bd_article_content(content=content)

        elif short_name == 'zq':
            content = await self._wash_zq_article_content(content=content)

        elif short_name == 'fh':
            content = await self._wash_fh_article_content(content=content)

        elif short_name == 'ys':
            content = await self._wash_ys_article_content(content=content)

        elif short_name == 'cn':
            content = await self._wash_cn_article_content(content=content)

        elif short_name == 'if':
            content = await self._wash_if_article_content(content=content)

        elif short_name == 'ss':
            content = await self._wash_ss_article_content(content=content)

        elif short_name == 'jm':
            content = await self._wash_jm_article_content(content=content)

        elif short_name == 'pp':
            content = await self._wash_pp_article_content(content=content)

        elif short_name == 'hx':
            content = await self._wash_hx_article_content(content=content)

        elif short_name == 'nfzm':
            content = await self._wash_nfzm_article_content(content=content)

        elif short_name == 'hqx':
            content = await self._wash_hqx_article_content(content=content)

        elif short_name == 'ck':
            content = await self._wash_ck_article_content(content=content)

        elif short_name == 'lsp':
            content = await self._wash_lsp_article_content(content=content)

        elif short_name == 'amz':
            content = await self._wash_amz_article_content(content=content)

        elif short_name == 'mp':
            content = await self._wash_mp_article_content(content=content)

        elif short_name == '7y7':
            content = await self._wash_7y7_article_content(content=content)

        elif short_name == 'qqbb':
            content = await self._wash_qqbb_article_content(content=content)

        elif short_name == 'ft':
            content = await self._wash_ft_article_content(content=content)

        elif short_name == '91mt':
            content = await self._wash_91mt_article_content(content=content)

        elif short_name == 'xq':
            content = await self._wash_xq_article_content(content=content)

        elif short_name == '5h':
            content = await self._wash_5h_article_content(content=content)

        elif short_name == 'bdj':
            content = await self._wash_bdj_article_content(content=content)

        else:
            pass

        return content

    @staticmethod
    async def _wash_bdj_article_content(content: str) -> str:
        if '<img' in content:
            # 有图的文章, 则把文章标题过滤
            content = re.compile('<h1>.*?</h1>').sub('', content)
        else:
            pass
        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_5h_article_content(content: str) -> str:
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                # 图片替换
                ('<img src=\"', '<img src=\"http://www.5h.com'),
            ],
            add_sensitive_str_list=[],
            is_default_filter=False,
            is_lower=False, )

        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_xq_article_content(content: str) -> str:
        content = wash_sensitive_info(
            data=content,
            replace_str_list=None,
            add_sensitive_str_list=[
                '<p>作者：\w+</p>',
                '<p>编辑：\w+</p>',
                '<p><b>作者：\w+</b></p>',
                '<p>来源：.*?</p>',
                '<p><b>免责申明：以上内容仅供参考，不作为买卖依据，据此操作，盈亏自负！</b></p>',
                '<p><a href=\"http://xueqiu\.com/n/今日话题\" target=\"_blank\">@今日话题</a> </p>',
                '<p>原文链接：<a href=\"http.*?\" title=\"http.*?\" target=\"_blank\" class=\"status-link\">网页链接</a></p>',
            ],
            is_default_filter=False,
            is_lower=False,)

        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_91mt_article_content(content: str) -> str:
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                # 视频详情介绍
                ('<mip-img popup', '<img'),
                ('</mip-img>', '</img>'),
            ],
            add_sensitive_str_list=None,
            is_default_filter=False,
            is_lower=False,)

        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_ft_article_content(content: str) -> str:
        content = wash_sensitive_info(
            data=content,
            replace_str_list=None,
            add_sensitive_str_list=[
                '<em>查看全部<i class=\"iconfont icon-xiajiantou\"></i></em>',
            ],
            is_default_filter=False,
            is_lower=False,)

        content = modify_body_img_centering(content=content)

        return content

    async def _wash_qqbb_article_content(self, content: str) -> str:
        content = wash_sensitive_info(
            data=content,
            replace_str_list=None,
            add_sensitive_str_list=[
                # 洗掉下一页或上一页
                '<div class=\"detail_page\">.*?</div>',
                # 洗掉推荐
                '<section class=\"hotwrap about-rec-ul dis-bot tab-box\">.*?</section>',
                # 查看更多
                '<div class=\"art-body-fold-\d+\">查看全文</div>',
                # 洗掉视频文章中的额查看更多
                '<div class=\"more\">展开查看全文<img src=\"http.*?\" alt=\"\"></div>',
                # 洗掉脚本
                '<script type=\"text/javascript\" src=\".*?\"></script>',
                '<footer><footer>©2019 QBAOBEI.COM</footer>.*?</footer>',
            ],
            is_default_filter=False,
            is_lower=False,)

        # 把下一页中的div.item-nub em.nub替换成正确的顺序
        em_nub_list_sel = {
            'method': 'css',
            'selector': 'div.item-nub em.nub ::text',
        }
        em_nub_list = await async_parse_field(
            parser=em_nub_list_sel,
            target_obj=content,
            is_first=False,
            # 不打印
            logger=None,)
        # eg: ['1', '2', '3', '4', '1', '2']
        # pprint(em_nub_list)
        index = 1
        replace_str_list = []
        for num in em_nub_list:
            # self.lg.info(num, index)
            replace_str_list.append([
                '<em class=\"nub\">{}</em>'.format(num), '<em class=\"nub\" id=\"fz\">{}</em>'.format(index),
            ])
            index += 1
        # pprint(replace_str_list)
        for item in replace_str_list:
            content = content.replace(item[0], item[1], 1)

        # item 的css
        content = '<style type="text/css">.art-body .item {position: relative;background-color: #fff;border-radius: 5px;border: 1px solid #e9ebed; padding: 10px;margin-top: 10px;overflow: hidden;}</style>'\
            + content if content != '' else content

        ## dl dd ul的css
        content = '<style type="text/css">ul {display: block;list-style-type: disc;margin-block-start: 1em;margin-block-end: 1em;margin-inline-start: 0px;margin-inline-end: 0px;padding-inline-start: 40px;} dl {display: block;margin-block-start: 1em;margin-block-end: 1em;margin-inline-start: 0px;margin-inline-end: 0px;} dd {line-height: 25px;}</style>'\
            + content if content != '' else content

        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_7y7_article_content(content: str) -> str:
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('<p><br></p>', '<br>'),
            ],
            add_sensitive_str_list=[
                # 洗掉下一页或上一页
                '<div class=\"detail_page\">.*?</div>',
                '<div class=\"adver\"></div>',
                # 洗掉推荐
                '<section id=\"related\" class=\"y7-sec y7-sec-3\">.*</div>',
                # 洗掉了解更多
                '<div class=\"box gzh_div\" style=\"display: none\">.*?</div>',
                # 洗掉展开更多
                '<div onclick=\"showfullcontent\(\)\" id=\"show_more\">.*?</div>',
                '<div class=\"befo_fa\"><div class=\"beforead\"></div></div>',
                '<div class=\"relativ\"></div>',
                # 洗掉脚本
                '<script type=\"text/javascript\" src=\".*?\"></script>',
            ],
            is_default_filter=False,
            is_lower=False, )

        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_mp_article_content(content) -> str:
        return content

    @staticmethod
    async def _wash_amz_article_content(content) -> str:
        # firefox上正常显示, chrome变形, 后台可以改下iframe的属性, 使其自适应
        return content

    @staticmethod
    async def _wash_lsp_article_content(content) -> str:
        return content

    @staticmethod
    async def _wash_ck_article_content(content) -> str:
        return content

    @staticmethod
    async def _wash_hqx_article_content(content) -> str:
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('好奇心日报', '优秀网'),
                # figure 里面img src处理
                ('data-format=\"jpeg\" class=\"lazyload\" data-src=', 'data-format=\"jpeg\" class=\"lazyload\" src='),
                # a标签跳转处理
                ('<a href=\".*?\">', '<a href=\"\">'),
            ],
            add_sensitive_str_list=[
                '<p class=\"\"><br></p>',
                '<p>题图来源：<a href=\".*?\" rel=\"nofollow\">pixabay</a></p>',
                '<p>题图来自.*?</p>',
                '<p class=\"\">题图：<a href=\"\">.*?</a>.*?<a href=\"\">.*?</a>  <br></p>',
                '<p>翻译：.*?</p>',
            ],
            is_default_filter=False,
            is_lower=False,)

        content = modify_body_img_centering(content=content)
        content = modify_body_p_typesetting(content=content)

        return content

    @staticmethod
    async def _wash_nfzm_article_content(content) -> str:
        content = re.compile('\n').sub('', content)

        content = modify_body_img_centering(content=content)
        content = modify_body_p_typesetting(content=content)

        return content

    @staticmethod
    async def _wash_hx_article_content(content) -> str:
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                # 去除图片惰性加载
                ('<img class=\"lazy\" data-original=', '<img class=\"lazy\" src='),
                ('虎嗅网', '优秀网'),
                ('虎嗅', '优秀'),
            ],
            add_sensitive_str_list=[
                # 去除段落空行
                '<p><br></p>',
                '<p></p>',
                '<p class=\"img-center-box\"><br></p>',
                '<p label=\"正文\" class=\"text-normal\"><br></p>',
                # 立场去除
                '<div class=\"neirong-shouquan\">.*?</div>',
                # 引用去除
                '<span class=\"text-remarks\" label=\"备注\">.*?</span>',
                '<span class=\"text-remarks\">.*?</span>',
                # 去除点击展开全文
                '<divclass js-hmt-detection data-detection=\"文章详情页,展开全文,点击\">.*?</divclass>',
                # 去除尾部作者盒子图片
                '<img src=\"https://img.huxiucdn.com/authorCard/\d+.jpg\?\d+\">',
                # 去除不让转载
                '<span style=\".*?\">本文首发于腾讯科技，未经授权，不得转载。</span>',
            ],
            is_default_filter=False,
            is_lower=False,)

        content = modify_body_img_centering(content=content)
        content = modify_body_p_typesetting(content=content)

        return content

    @staticmethod
    async def _wash_pp_article_content(content) -> str:
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                # 清洗末尾额外补充说明
                ('<div class=\"news_infor_extra\">.*</div> <div class=\"relations_div\">', '<div class="relations_div">'),
                ('澎湃新闻', '优秀网'),
                ('湃客', '秀客'),
            ],
            add_sensitive_str_list=[
                '<strong>“湃客·镜相”栏目首发独家非虚构作品，版权所有，任何媒体或平台不得未经许可转载。</strong>',
                '<a href=\".*?\" target=\"_blank\">阅读原文</a>',
            ],
            is_default_filter=False,
            is_lower=False,)

        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_jm_article_content(content) -> str:
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('界面新闻', '优秀网'),
            ],
            add_sensitive_str_list=[
                # 洗掉末尾广告
                '<div id=\"ad_content\">.*?</div>',
                '<div class=\"article-source\">.*?</div>',
                # 洗掉图片来源
                '<span>图片来源：.*?</span>',
                '<p>图片来源：.*?</p>',
                '<figcaption>图片来源：.*?</figcaption>',
                # 洗掉摄影
                '<span>摄影：.*?</span>',
                # 洗掉记者
                '<p>记者 \| .*?</p>',
                # 洗掉撰文
                '<p>撰文 \| .*?</p>',
            ],
            is_default_filter=False,
            is_lower=False,)

        content = modify_body_img_centering(content=content)
        content = modify_body_p_typesetting(content=content)

        return content

    @staticmethod
    async def _wash_ss_article_content(content) -> str:
        # 洗掉本文禁止商业转载
        content = re.compile('<blockquote>.*?</blockquote>').sub('', content)
        content = re.compile('<strong>为您推荐</strong>').sub('', content)
        # 洗掉推荐文章
        content = re.compile('<div class=\"my-related-posts-box\".*?>.*?</div>').sub('', content)
        # 洗掉图片来源
        content = re.compile('<p class=\"wp-caption-text\">图片来源：.*?</p>').sub('', content)
        # 把img标签原先的固定大小置空
        content = re.compile('width=\"\d+\" height=\"\d+\" class=\"size-large wp-image-')\
            .sub('class=\"size-large wp-image-', content)
        # 并且把img src的url, 改成非固定大小(测试发现没用, pass)
        # content = re.compile('-\d+x\d+\.jpg')\
        #     .sub('.jpg', content)
        # 洗掉分享标签
        content = re.compile('<div class=\"bshare-custom icon-medium\">.*?</div>')\
            .sub('', content)

        content = modify_body_img_centering(content=content,)

        return content

    @staticmethod
    async def _wash_if_article_content(content) -> str:
        # 避免a标签调转
        content = re.compile('<a href=\".*?\">').sub('<a href=\"\">', content)
        content = modify_body_img_centering(content=content)
        content = modify_body_p_typesetting(content=content)

        return content

    @staticmethod
    async def _wash_cn_article_content(content) -> str:
        content = re.compile('<mip-img').sub('<img', content)
        content = re.compile('</mip-img>').sub('</img>', content)
        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_ys_article_content(content) -> str:
        """
        51健康养生网
        :param content:
        :return:
        """
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('alt=\".*?\" src=\"\/\/', 'alt=\"\" src=\"http://'),
            ],
            add_sensitive_str_list=[],
            is_default_filter=False,
            is_lower=False,)
        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_fh_article_content(content) -> str:
        content = re.compile('凤凰网汽车讯').sub('', content)
        # TODO chrome 显示content时会带上手机默认客户端的css样式, 导致显示异常, 用firefox查看是正常的!!
        content = modify_body_img_centering(content=content)
        content = modify_body_p_typesetting(content=content)

        return content

    @staticmethod
    async def _wash_zq_article_content(content) -> str:
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('<img data-src=', '<img src='),
                ('data-width=\"\d+\" data-height=\"\d+\" data-src=', 'src='),
            ],
            add_sensitive_str_list=[
                '<br>',
            ],
            is_default_filter=False,
            is_lower=False, )

        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_bd_article_content(content) -> str:
        # TODO firefox正常显示, 但是chrome无图, 原因图片地址无响应!
        # 顶部空白替换
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('<div style=\"padding-top:\d+\.\d+%\">', '<div>'),
                ('<div style=\"padding-top:\d+%\">', '<div>'),
                ('&amp;', '&'),
            ],
            add_sensitive_str_list=[],
            is_default_filter=False,
            is_lower=False, )

        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_sg_article_content(content) -> str:
        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_df_article_content(content) -> str:
        content = re.compile('<p class=\"section txt\">对此你怎么看，欢迎大家在评论区留言！</p>').sub('', content)

        return content

    @staticmethod
    async def _wash_wx_article_content(content: str) -> str:
        # print(content)
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                ('<p><br></p>', '<br>'),
            ],
            add_sensitive_str_list=[
                # 洗掉编辑, 校对
                '<span style=\"max-width: 100%;.*?\">编辑：.*?</span>',
                '<span style=\"max-width: 100%;.*?\">校对：.*?</span>',
                # 空行
                '<p><span style=\"color: rgb\(217, 33, 66\);font-size: 14px;\"><strong><br></strong></span></p>',
                # 空行过多, 洗掉
                '<br>',
                # 最下方a标签: 洗掉往期回顾 or 推荐内容
                '<p style=\".*?\"><a href=\".*?mp.weixin.qq.com/s.*?\" target=\"_blank\" data-itemshowtype=\"0\" data-linktype=\"2\".*?>.*?</a>.*?</p>',

                # todo section容易错洗, 导致正常内容无法显示, 不处理
                # '<section .*? data-tools=\"新媒体排版\".*?>.*?</section>',
            ],
            is_default_filter=False,
            is_lower=False,)

        return content

    @staticmethod
    async def _wash_kd_article_content(content) -> str:
        content = wash_sensitive_info(
            data=content,
            replace_str_list=[
                # 替换掉img 标签中src为svg的
                (' src=\"data:image/svg\+xml;.*?\" ', ' '),
                # 处理图片
                (' data-src=', ' src='),
                ('data-lazy=\"\d+\"', 'style=\"height:auto;width:100%;\"'),
            ],
            add_sensitive_str_list=[
                '<svg .*?>.*?</svg>',
                '<a class=\"jubao\"><i></i>举报内容</a>',
            ],
            is_default_filter=False,
            is_lower=False,)

        # 给与原装的css
        content = '<link rel="stylesheet" href="//mp.gtimg.cn/themes/default/client/article/article.css?_bid=2321&v=2017082501">' + \
            content if content != '' else ''

        return content

    @staticmethod
    async def _wash_kb_article_content(content) -> str:
        # 给与原生的css
        content = r'<link href="//mat1.gtimg.com/www/cssn/newsapp/cyshare/cyshare_20181121.css" type="text/css" rel="stylesheet">' + \
            content if content != '' else content
        content = modify_body_img_centering(content=content)
        content = modify_body_p_typesetting(content=content)

        return content

    async def is_child_can_debug(self, article_url) -> bool:
        """
        判断是否是子对象, 以及是否debug是打开
        :return:
        """
        for item in ARTICLE_ITEM_LIST:
            item_debug = item.get('debug', False)
            if item.get('short_name', '') == 'df':
                if 'mini.eastday.com' in article_url:
                    if item_debug:
                        return True

            elif item.get('short_name', '') == 'bd':
                if 'mbd.baidu.com' in article_url\
                        or 'sv.baidu.com' in article_url:
                    if item_debug:
                        return True
                else:
                    if item.get('obj_origin', '') in article_url:
                        if item_debug:
                            return True

            elif item.get('short_name', '') == 'fh':
                if await self._in_fh_two_level_domain_name(article_url):
                    if item_debug:
                        return True
                else:
                    if item.get('obj_origin', '') in article_url:
                        if item_debug:
                            return True

            else:
                if item.get('obj_origin', '') in article_url:
                    if item_debug:
                        return True

        return False

    async def _in_fh_two_level_domain_name(self, article_url) -> bool:
        """
        是否在可抓取的fh 的二级域名里
        :param article_url:
        :return:
        """
        if 'news.ifeng.com' in article_url\
                or 'feng.ifeng.com' in article_url\
                or 'finance.ifeng.com' in article_url\
                or 'ent.ifeng.com' in article_url\
                or 'sports.ifeng.com' in article_url\
                or 'fashion.ifeng.com' in article_url\
                or 'auto.ifeng.com' in article_url\
                or 'tech.ifeng.com' in article_url\
                or 'culture.ifeng.com' in article_url\
                or 'history.ifeng.com' in article_url\
                or 'mil.ifeng.com' in article_url\
                or 'travel.ifeng.com' in article_url\
                or 'fo.ifeng.com' in article_url\
                or 'health.ifeng.com' in article_url\
                or 'guoxue.ifeng.com' in article_url\
                or 'v.ifeng.com' in article_url:
            return True

        else:
            return False

    async def _get_site_id(self, article_url_type) -> int:
        """
        获取文章的site_id
        :return:
        """
        # 肯定在里面, 否则无法走到这一步
        return self.obj_origin_dict.get(article_url_type, {}).get('site_id', '')

    async def _judge_url_type(self, article_url) -> str:
        """
        判断url类别
        :return:
        """
        for key, value in self.obj_origin_dict.items():
            if key == 'df':
                if 'mini.eastday.com' in article_url:
                    return key

            elif key == 'bd':
                if 'mbd.baidu.com' in article_url\
                        or 'sv.baidu.com' in article_url:
                    return key

                else:
                    if value.get('obj_origin') in article_url:
                        return key

            elif key == 'fh':
                if await self._in_fh_two_level_domain_name(article_url):
                    return key

            else:
                if value.get('obj_origin',) in article_url:
                    return key

        raise ValueError('未知的文章url!')

    def __del__(self):
        try:
            del self.lg
            del self.user_agent_type
            del self.ip_pool_type
            del self.request_num_retries
            del self.hook_target_api_data
            del self.concurrency
        except:
            pass
        try:
            del self.loop
        except:
            pass
        try:
            self.obj_origin_dict
        except:
            pass
        collect()

def modify_body_img_centering(content: str,) -> str:
    """
    修改body图片居中
    :param content:
    :return:
    """
    # 图片居中, 放前后作用一样, img里面的实际值还是会被加载, 故统一放最前面
    content = '<style type="text/css">img {visibility: visible !important;height: auto !important;width: 100% !important;}</style>' + \
              content if content != '' else ''

    return content

def modify_body_p_typesetting(content: str) -> str:
    """
    修改body p标签的排版
    :param content:
    :return:
    """
    # p标签文字修饰(自己添加, 目的: 让其自适应phone端, 添加在后端以覆盖原有p标签属性)
    content = '<style type="text/css">p {width: 100%; height: auto; word-wrap:break-word; word-break:break-all; overflow: hidden;}</style>' + \
              content if content != '' else ''

    return content

def main():
    _ = ArticleParser()
    loop = get_event_loop()
    # wx公众号
    # 存在链接过期的情况
    # https://mp.weixin.qq.com/s?__biz=MzA4MjQxNjQzMA==&mid=2768396229&idx=1&sn=&scene=0#wechat_redirect
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1542166201&ver=1243&signature=qYsoi7Sn3*tmw9x-lXxo6sJfSYDGGyHewzZyJCjgovA8taCXuTtENN7X2d4dPnOz1TvEnO2LsYJR1W3IwozcIzLyfhcdcZgOoqyzPLhz469ssieB15ojFrdtA2y83*As&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1564036201&ver=1749&signature=XCTMLVFytVL3FzjyURHVRICZb2bM1kLWhSpUrNeb8SGD1jvxgHkJgicFiMNBOl6W0Ow6m*Gzke*tlPVCzOJTcDx4WYv2FyOsY1FtMzB-pHIOErSsuq4H3T-yUeyMq9vg&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1565314201&ver=1779&signature=3RxHcLiybXKqNJH95V5UekL6udEBs6tZFNnqPKCxEbXHOWcnQ2djUfXBA1hrMOerxiKAIKVyvPOYW9Frj-rwmPDpnzZE8WuiSZWZCFhIoLUKVRHD5AfsH90C1vupHvUH&new=1'
    url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1568689203&ver=1857&signature=2ABS59Q9ciRvm27MYTS694lYxq1qsyp1KUJ9AU6oqFREk8-en2OeSbE9jLKFGwGSHIj*C9CmVeJxD6ImtYgs18bluEISV8o2rEZM-WUzwWTYCcdF*mSyQeAmleT4lwOz&new=1'
    # 含视频
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1563850802&ver=1745&signature=kF7BFCtTqr9OlfBzqLSgUfnD413Ig9JfMVKCc1ew8YQ8maPdhL8zFXgrctDdl5Z3HfI0ZOb7yThhKR1QHrtuUjVQE*gTTPBvBOTagAA5wN*bylpMTtwBqwv7ctFh-j5P&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1567476001&ver=1829&signature=WRtVmIbd-R3jJmAMe4ILMN2C12-Yd7QRJhZbZLLle7NmAyLSLTooaJqQPjtb0WHH288LVqanz2vvl0wmIpVNyL-iG5zNwGDsl4oZt4lXXZGXNv7*aQ7sy8ZgyS7l0kTU&new=1'

    # 今日头条(视频切入到content中了)    [https://www.toutiao.com/]
    # url = 'https://www.toutiao.com/a6623290873448759815/'
    # url = 'https://www.toutiao.com/a6623125148088140291/'
    # url = 'https://www.toutiao.com/a6694437682031886852/'
    # url = 'https://www.toutiao.com/a6707502560892158468/'
    # url = 'https://www.toutiao.com/a6714969589630894605/'
    # url = 'https://www.toutiao.com/a6716696808971567630/'
    # url = 'https://www.toutiao.com/a6716489299614761484/'
    # 问答不采集
    # url = 'https://www.toutiao.com/a6661496988099412238/'
    # 含视频
    # url = 'https://www.toutiao.com/a6623325882381500931/'

    # 简书
    # url = 'https://www.jianshu.com/p/ec1e9f6129bd'
    # url = 'https://www.jianshu.com/p/a02313dd3875'
    # url = 'https://www.jianshu.com/p/1a60bdc3098b'
    # url = 'https://www.jianshu.com/p/2876ca9e3ae7'
    # url = 'https://www.jianshu.com/p/9ba3eb7bc524'
    # url = 'https://www.jianshu.com/p/675bf3a17d54'
    # url = 'https://www.jianshu.com/p/dceebde3caf8'

    # QQ看点
    # url = 'https://post.mp.qq.com/kan/article/2184322959-232584629.html?_wv=2147483777&sig=24532a42429f095b9487a2754e6c6f95&article_id=232584629&time=1542933534&_pflag=1&x5PreFetch=1&web_ch_id=0&s_id=gnelfa_3uh3g5&share_source=0'
    # url = 'https://post.mp.qq.com/kan/article/3082663893-394335551.html?sig=8807b10464215f5eac164824c23729c1&article_id=394335551&_pflag=1&_wv=2147483777&x5PreFetch=1&time=1558074607'
    # url = 'https://post.mp.qq.com/kan/article/1001000209370-558421494.html?sig=cce26570d9dd6093f0416112420b6c07&article_id=558421494&_pflag=1&_wv=2147483777&x5PreFetch=1&time=1565108260'
    # url = 'https://post.mp.qq.com/kan/article/3341167918-561135106.html?_wv=2147483777&sig=2005d9c1366770c1de75f447d143f9a6&article_id=561135106&time=1565237253&_pflag=1&x5PreFetch=1&web_ch_id=0&sourcefrom=6'
    # todo 含视频(本地可以, server也可以)
    #  server失败[原因原先以为是selenium版本 在linux中与firefox和geckodriver不兼容导致启动geckodriver失败, 即使firefox和geckodriver皆为最新版本])
    #  后来发现是headless=True导致无法启动驱动
    # geckodriver download_url: https://github.com/mozilla/geckodriver/releases
    # url = 'http://post.mp.qq.com/kan/video/201271541-2525bea9bc8295ah-x07913jkmml.html?_wv=2281701505&sig=50b27393b64a188ffe7f646092dbb04f&time=1542102407&iid=Mjc3Mzg2MDk1OQ==&sourcefrom=0'
    # url = 'http://post.mp.qq.com/kan/video/200553568-1375d3f1b48697ah-j0906gh4g62.html?_wv=2281701505&sig=e1dfb38fc2d5eaa0fd4400b05c94d17c&time=1564417414&iid=Mjc3Mzg2MDk1OQ==&sourcefrom=6'

    # 天天快报
    # url = 'https://kuaibao.qq.com/s/NEW2018120200710400?refer=kb_news&titleFlag=2&omgid=78610c582f61e3b1f414134f9d4fa0ce'
    # url = 'https://kuaibao.qq.com/s/20181201A0VJE800?refer=kb_news&titleFlag=2&omgid=78610c582f61e3b1f414134f9d4fa0ce'
    # url = 'https://kuaibao.qq.com/s/20190515A06XAW00?refer=kb_news&coral_uin=ec30afdb64e74038ca7991e4e282153af308670081f17d0ee4fc3e473b0b5dda2f&omgid=22c4ac23307a6a33267184cafd2df8b6&chlid=news_news_top&atype=0&from=groupmessage&isappinstalled=0'
    # url = 'https://kuaibao.qq.com/s/20190908AZPIWP00?refer=kb_news&amp;titleFlag=2&amp;coral_uin=ec2fef55983f2b0f322a43dc540c8dda94190bf70c60ca0d998400a23f576204fb&amp;omgid=7a157262f3d303c6f2d089446406d22e&from=groupmessage&isappinstalled=0'
    # 第二类图文文章
    # url = 'https://kuaibao.qq.com/s/20190710AZOJ0B00?from=groupmessage&isappinstalled=0'
    # 第三类图文文章(跟第二类是同一接口但是字段不同)
    # url = 'https://kuaibao.qq.com/s/20190708A0INL100?refer=kb_news&amp;coral_uin=ec30afdb64e74038ca7991e4e282153af308670081f17d0ee4fc3e473b0b5dda2f&amp;omgid=22c4ac23307a6a33267184cafd2df8b6&amp;chlid=daily_timeline&amp;atype=0&from=groupmessage&isappinstalled=0'
    # url = 'https://kuaibao.qq.com/s/20190721A0JCZT00?refer=kb_news&amp;coral_uin=ec30afdb64e74038ca7991e4e282153af308670081f17d0ee4fc3e473b0b5dda2f&amp;omgid=22c4ac23307a6a33267184cafd2df8b6&amp;chlid=daily_timeline&amp;atype=0&from=groupmessage&isappinstalled=0'
    # url = 'https://kuaibao.qq.com/s/20190723A0IRBX00?refer=kb_news&amp;titleFlag=2&amp;coral_uin=ec30afdb64e74038ca7991e4e282153af308670081f17d0ee4fc3e473b0b5dda2f&amp;omgid=22c4ac23307a6a33267184cafd2df8b6&from=groupmessage&isappinstalled=0'
    # TODO 含视频(本地可以，server也成功[firefox失败, 用的chrome]) [有一定失败率多尝试]
    # url = 'https://kuaibao.qq.com/s/20180906V1A30P00?refer=kb_news&titleFlag=2&omgid=78610c582f61e3b1f414134f9d4fa0ce'
    # 第一种类型
    # url = 'https://kuaibao.qq.com/s/20190322V0DCSY00?refer=kb_news&amp;coral_uin=ec2fef55983f2b0f322a43dc540c8dda94190bf70c60ca0d998400a23f576204fb&amp;omgid=7a157262f3d303c6f2d089446406d22e&amp;chlid=daily_timeline&amp;atype=4&from=groupmessage&isappinstalled=0'
    # 第二种类型
    # url = 'https://kuaibao.qq.com/s/20190221V170RM00?refer=kb_news&amp;titleFlag=2&amp;coral_uin=ec2fef55983f2b0f322a43dc540c8dda94190bf70c60ca0d998400a23f576204fb&amp;omgid=7a157262f3d303c6f2d089446406d22e&from=groupmessage&isappinstalled=0'
    # url = 'https://kuaibao.qq.com/s/20190505V0FMTX00?refer=kb_news&amp;titleFlag=2&amp;coral_uin=ec2fef55983f2b0f322a43dc540c8dda94190bf70c60ca0d998400a23f576204fb&amp;omgid=7a157262f3d303c6f2d089446406d22e&from=groupmessage&isappinstalled=0'
    # url = 'https://kuaibao.qq.com/s/20190509V0JOTG00?refer=kb_news&amp;titleFlag=2&amp;coral_uin=ec2fef55983f2b0f322a43dc540c8dda94190bf70c60ca0d998400a23f576204fb&amp;omgid=7a157262f3d303c6f2d089446406d22e&from=groupmessage&isappinstalled=0'
    # url = 'https://kuaibao.qq.com/s/20190328V0E9OX00?refer=kb_news&amp;titleFlag=2&amp;omgid=7a157262f3d303c6f2d089446406d22e&amp;coral_uin=ec2fef55983f2b0f322a43dc540c8dda94190bf70c60ca0d998400a23f576204fb&from=groupmessage&isappinstalled=0'

    # 东方头条新闻
    # url = 'https://mini.eastday.com/mobile/190505214138491.html?qid=null&idx=1&recommendtype=crb_a579c9a168dd382c_1_1_0_&ishot=1&fr=toutiao&pgnum=1&suptop=0'
    # url = 'https://mini.eastday.com/mobile/190507061239214.html?qid=null&idx=2&recommendtype=-1_a579c9a168dd382c_1_2_0_&ishot=1&fr=toutiao&pgnum=1&suptop=0001'
    # 含视频
    # url = 'https://mini.eastday.com/video/vgaoxiao/20190506/190506045241686142077.html?qid=null&idx=6&recommendtype=-1_a579c9a168dd382c_1_6_0_&ishot=1&fr=toutiao&pgnum=1&suptop=0'
    # url = 'https://mini.eastday.com/video/vgaoxiao/20190425/190425154440387159259.html?qid=null&idx=2&fr=https://mini.eastday.com/video/vgaoxiao/20190506/190506045241686142077.html&ishot=0&recommendtype=vs'

    # 搜狗新闻资讯
    # url = 'https://sa.sogou.com/sgsearch/sgs_tc_news.php?req=gNWjMh9kjpEtYgjReTdUXZS0Q2CO6DjsS87Col9-QZE=&user_type=wappage'
    # url = 'https://sa.sogou.com/sgsearch/sgs_tc_news.php?req=xtgTQEURkeIQnw4p57aSHd9gihe6nAvIBk6JzKMSwdJ_9aBUCJivLpPO9-B-sc3i&user_type=wappage'
    # url = 'https://sa.sogou.com/sgsearch/sgs_tc_news.php?req=SKbJyHwsObNfXcwSUF_VoWrnmpkThJtfiHZ54FsQFNk=&user_type=wappage'
    # url = 'https://sa.sogou.com/sgsearch/sgs_tc_news.php?req=35zB-k94kWvc1SfKHhqXM1_UEnQCOA83_2msaXw6lPs=&user_type=wappage'
    # 含视频
    # url = 'http://sa.sogou.com/sgsearch/sgs_video.php?mat=11&docid=sf_307868465556099072&vl=http%3A%2F%2Fsofa.resource.shida.sogoucdn.com%2F114ecd2b-b876-46a1-a817-e3af5a4728ca2_1_0.mp4'
    # url = 'http://sa.sogou.com/sgsearch/sgs_video.php?mat=11&docid=286635193e7a63a24629a1956b3dde76&vl=http%3A%2F%2Fresource.yaokan.sogoucdn.com%2Fvideodown%2F4506%2F557%2Fd55cd7caceb1e60a11c8d3fff71f3c45.mp4'
    # url = 'http://sa.sogou.com/sgsearch/sgs_video.php?mat=11&docid=open_doc_prod6562107&vl=http%3A%2F%2F1400094915.vod2.myqcloud.com%2F3df4ea08vodtransgzp1400094915%2Feb5e8f815285890789528268277%2Fv.f20.mp4'

    # 百度m站
    # url = 'https://mbd.baidu.com/newspage/data/landingpage?s_type=news&dsp=wise&context=%7B%22nid%22%3A%22news_9512351987809643964%22%7D&pageType=1&n_type=1&p_from=-1'
    # url = 'https://mbd.baidu.com/newspage/data/landingpage?s_type=news&dsp=wise&context=%7B%22nid%22%3A%22news_9423330273641956666%22%7D&pageType=1&n_type=1&p_from=-1'
    # url = 'https://mbd.baidu.com/newspage/data/landingshare?context=%7B%22nid%22%3A%22news_8934756170017529467%22%2C%22ssid%22%3A%22%22%7D&pageType=1'
    # url = 'https://m.baidu.com/#iact=wiseindex%2Ftabs%2Fnews%2Factivity%2Fnewsdetail%3D%257B%2522linkData%2522%253A%257B%2522name%2522%253A%2522iframe%252Fmib-iframe%2522%252C%2522id%2522%253A%2522feed%2522%252C%2522index%2522%253A0%252C%2522url%2522%253A%2522https%253A%252F%252Fmbd.baidu.com%252Fnewspage%252Fdata%252Flandingpage%253Fs_type%253Dnews%2526dsp%253Dwise%2526context%253D%25257B%252522nid%252522%25253A%252522news_8934756170017529467%252522%25257D%2526pageType%253D1%2526n_type%253D1%2526p_from%253D-1%2526innerIframe%253D1%2522%252C%2522isThird%2522%253Afalse%252C%2522title%2522%253Anull%257D%257D'
    # url = 'https://m.baidu.com/#iact=wiseindex%2Ftabs%2Fnews%2Factivity%2Fnewsdetail%3D%257B%2522linkData%2522%253A%257B%2522name%2522%253A%2522iframe%252Fmib-iframe%2522%252C%2522id%2522%253A%2522feed%2522%252C%2522index%2522%253A0%252C%2522url%2522%253A%2522https%253A%252F%252Fmbd.baidu.com%252Fnewspage%252Fdata%252Flandingpage%253Fs_type%253Dnews%2526dsp%253Dwise%2526context%253D%25257B%252522nid%252522%25253A%252522news_9292806054300264081%252522%25257D%2526pageType%253D1%2526n_type%253D1%2526p_from%253D-1%2526innerIframe%253D1%2522%252C%2522isThird%2522%253Afalse%252C%2522title%2522%253Anull%257D%257D'
    # url = 'https://m.baidu.com/#iact=wiseindex%2Ftabs%2Fnews%2Factivity%2Fnewsdetail%3D%257B%2522linkData%2522%253A%257B%2522name%2522%253A%2522iframe%252Fmib-iframe%2522%252C%2522id%2522%253A%2522feed%2522%252C%2522index%2522%253A0%252C%2522url%2522%253A%2522https%253A%252F%252Fmbd.baidu.com%252Fnewspage%252Fdata%252Flandingpage%253Fs_type%253Dnews%2526dsp%253Dwise%2526context%253D%25257B%252522nid%252522%25253A%252522news_10217781133566637087%252522%25257D%2526pageType%253D1%2526n_type%253D1%2526p_from%253D-1%2526innerIframe%253D1%2522%252C%2522isThird%2522%253Afalse%252C%2522title%2522%253Anull%257D%257D'
    # url = 'https://m.baidu.com/#iact=wiseindex%2Ftabs%2Fnews%2Factivity%2Fnewsdetail%3D%257B%2522linkData%2522%253A%257B%2522name%2522%253A%2522iframe%252Fmib-iframe%2522%252C%2522id%2522%253A%2522feed%2522%252C%2522index%2522%253A0%252C%2522url%2522%253A%2522https%253A%252F%252Fmbd.baidu.com%252Fnewspage%252Fdata%252Flandingpage%253Fs_type%253Dnews%2526dsp%253Dwise%2526context%253D%25257B%252522nid%252522%25253A%252522news_9575607690617582637%252522%25257D%2526pageType%253D1%2526n_type%253D1%2526p_from%253D-1%2526innerIframe%253D1%2522%252C%2522title%2522%253Anull%257D%257D'
    # 含视频(好看视频)
    # url = 'https://m.baidu.com/#iact=wiseindex%2Ftabs%2Fnews%2Factivity%2Fnewsdetail%3D%257B%2522linkData%2522%253A%257B%2522name%2522%253A%2522iframe%252Fmib-iframe%2522%252C%2522id%2522%253A%2522feed%2522%252C%2522index%2522%253A0%252C%2522url%2522%253A%2522https%253A%252F%252Fhaokan.baidu.com%252Fvideoui%252Fpage%252Fsearchresult%253Fpd%253Dwise%2526vid%253D15928130604529794109%2526is_invoke%253D1%2526innerIframe%253D1%2522%252C%2522isThird%2522%253Afalse%252C%2522title%2522%253Anull%257D%257D'
    # url = 'https://m.baidu.com/#iact=wiseindex%2Ftabs%2Fnews%2Factivity%2Fnewsdetail%3D%257B%2522linkData%2522%253A%257B%2522name%2522%253A%2522iframe%252Fmib-iframe%2522%252C%2522id%2522%253A%2522feed%2522%252C%2522index%2522%253A0%252C%2522url%2522%253A%2522https%253A%252F%252Fhaokan.baidu.com%252Fvideoui%252Fpage%252Fsearchresult%253Fpd%253Dwise%2526vid%253D12574625425386503733%2526is_invoke%253D1%2526innerIframe%253D1%2522%252C%2522isThird%2522%253Afalse%252C%2522title%2522%253Anull%257D%257D'
    # url = 'https://m.baidu.com/#iact=wiseindex%2Ftabs%2Fnews%2Factivity%2Fnewsdetail%3D%257B%2522linkData%2522%253A%257B%2522name%2522%253A%2522iframe%252Fmib-iframe%2522%252C%2522id%2522%253A%2522feed%2522%252C%2522index%2522%253A0%252C%2522url%2522%253A%2522https%253A%252F%252Fhaokan.baidu.com%252Fvideoui%252Fpage%252Fsearchresult%253Fpd%253Dwise%2526vid%253D5077289958594474520%2526is_invoke%253D1%2526innerIframe%253D1%2522%252C%2522isThird%2522%253Afalse%252C%2522title%2522%253Anull%257D%257D'
    # url = 'https://m.baidu.com/#iact=wiseindex%2Ftabs%2Fnews%2Factivity%2Fnewsdetail%3D%257B%2522linkData%2522%253A%257B%2522name%2522%253A%2522iframe%252Fmib-iframe%2522%252C%2522id%2522%253A%2522feed%2522%252C%2522index%2522%253A0%252C%2522url%2522%253A%2522https%253A%252F%252Fhaokan.baidu.com%252Fvideoui%252Fpage%252Fsearchresult%253Fpd%253Dwise%2526vid%253D8197562812859491736%2526innerIframe%253D1%2522%252C%2522isThird%2522%253Afalse%252C%2522title%2522%253Anull%257D%257D'
    # 推荐栏上边点击视频进入的tab, 所得的到视频地址
    # url = 'https://sv.baidu.com/videoui/page/videoland?context=%7B%22nid%22%3A%22sv_7865563634675285012%22%7D&pd=feedtab_h5&pagepdSid='
    # url = 'https://sv.baidu.com/videoui/page/videoland?context=%7B%22nid%22%3A%22sv_2051009680729321124%22%7D&pd=feedtab_h5&pagepdSid='

    # 中青看点(左上角点击全部进行文章类型选择, 因为其只显示前2页, 下滑点击加载更多, 会被跳转到https://cpu.baidu.com, 只需要回退页面直接返回)
    # url = 'https://focus.youth.cn/mobile/detail/id/15547200#'
    # url = 'https://focus.youth.cn/mobile/detail/id/15561509#'
    # url = 'https://focus.youth.cn/mobile/detail/id/17240154#'
    # url = 'https://focus.youth.cn/mobile/detail/id/17229127#'
    # url = 'https://focus.youth.cn/mobile/detail/id/17230881#'
    # url = 'https://focus.youth.cn/mobile/detail?id=17197839#'

    # 阳光宽频网(短视频)
    # 旧版
    # url = 'https://www.365yg.com/a6693050837997978126/#mid=1568175129542657'
    # url = 'https://www.365yg.com/a6689279176827994638/#mid=1607129585526787'
    # 新版(即西瓜视频)
    # url = 'https://www.ixigua.com/i6711509850636943876/'

    # 西瓜视频(短视频)
    # url = 'https://www.ixigua.com/i6711509850636943876/'
    # url = 'https://www.ixigua.com/i6693050837997978126/#mid=1568175129542657'
    # url = 'https://www.ixigua.com/i6689557180368028173/'
    # url = 'https://www.ixigua.com/i6623552886510977540/'

    # 凤凰网
    # 资讯
    # url = 'https://news.ifeng.com/c/7nDvcZ4NtW1'
    # url = 'https://news.ifeng.com/c/7nEJ63GSOWW'
    # url = 'https://news.ifeng.com/c/7nEFqgSjZiq'
    # url = 'https://news.ifeng.com/c/7nE9cR3x2VH'
    # url = 'https://news.ifeng.com/c/7pdYc1BqNgY'
    # url = 'https://news.ifeng.com/c/7q1JRd1MzcO'
    # 大风号
    # url = 'https://feng.ifeng.com/c/7nE6wahrgJg'
    # url = 'https://feng.ifeng.com/c/7nE8Gmm6iR4'
    # 财经
    # url = 'http://finance.ifeng.com/c/7nEMfALohyC'
    # 娱乐
    # url = 'https://ent.ifeng.com/c/7nESdTWykLm'
    # url = 'https://ent.ifeng.com/c/7nDvPWE79UF'
    # 体育
    # url = 'https://sports.ifeng.com/c/7nDzc9Lrspg'
    # 时尚
    # url = 'https://fashion.ifeng.com/c/7nDykbExSVc'
    # url = 'https://fashion.ifeng.com/c/7nDxh4ZgED2'
    # url = 'https://fashion.ifeng.com/c/7q0a30KckYy'
    # 汽车
    # url = 'https://auto.ifeng.com/c/7nE86ZB9Y3s'
    # url = 'https://auto.ifeng.com/c/7nEFmnQAbiK'
    # TODO 房产未实现, 页面结构完全不同
    # 科技
    # url= 'https://tech.ifeng.com/c/7nE6KwElcwq'
    # 文化
    # url = 'http://culture.ifeng.com/c/7nDOfYV9Ma2'
    # 历史
    # url = 'https://history.ifeng.com/c/7n9wJLKFkKx'
    # 军事
    # url = 'https://mil.ifeng.com/c/7nD84weEtS9'
    # 旅游
    # url = 'https://travel.ifeng.com/c/7nDM9G2yG5A'
    # 佛教
    # url = 'https://fo.ifeng.com/c/7nE4JqoNnIu'
    # url = 'https://fo.ifeng.com/c/7nCq7vTkOjj'
    # 健康
    # url = 'https://health.ifeng.com/c/7n7k5Gc95yC'
    # url = 'https://health.ifeng.com/c/7nD69v4BFqk'
    # TODO 家居未实现, 页面结构非文章格式, 全是图片
    # 国学
    # url = 'https://guoxue.ifeng.com/c/7nCOLefbTeq'
    # 视频
    # url = 'https://v.ifeng.com/c/7n9OP680pzt'
    # url = 'https://v.ifeng.com/c/7msqjIm1dUe'
    # url = 'https://v.ifeng.com/c/7nEV3crGcwC'
    # url = 'https://v.ifeng.com/c/7nE1XJY8fL6'

    # 51健康养生网
    # url = 'http://www.51jkst.com/article/275371/index.html'
    # url = 'http://www.51jkst.com/article/275373/index.html'
    # url = 'http://www.51jkst.com/article/252943/index.html'
    # url = 'http://www.51jkst.com/article/275308/index.html'

    # 彩牛养生网(权威医生解说的短视频)
    # 视频
    # url = 'http://m.cnys.com/yiliao/1784.html'
    # url = 'http://m.cnys.com/yiliao/1783.html'
    # url = 'http://m.cnys.com/yiliao/1376.html'
    # url = 'http://m.cnys.com/yiliao/1202.html'
    # 文章
    # url = 'http://m.cnys.com/yangshengzixun/2178.html'
    # url = 'http://m.cnys.com/yangshengzixun/2167.html'
    # url = 'http://m.cnys.com/yangshengzixun/2157.html'
    # url = 'http://m.cnys.com/yangshengzixun/2158.html'

    # 爱范儿
    # url = 'https://www.ifanr.com/1226698'
    # url = 'https://www.ifanr.com/1226793'
    # 生活
    # url = 'https://www.ifanr.com/1226718'
    # 早报
    # url = 'https://www.ifanr.com/1227727'
    # 公司(行业)
    # url = 'https://www.ifanr.com/1227626'
    # 评测
    # url = 'https://www.ifanr.com/1227452'
    # 董车会
    # url = 'https://www.ifanr.com/1227475'
    # appSo
    # url = 'https://www.ifanr.com/app/1216511'
    # url = 'https://www.ifanr.com/app/1257907'
    # 人物
    # url = 'https://www.ifanr.com/1227137'
    # url = 'https://www.ifanr.com/1227137'
    # 小程序
    # url = 'https://www.ifanr.com/minapp/1225964'
    # 汽车
    # url = 'https://www.ifanr.com/1226588'
    # 产品(新锐产品)
    # url = 'https://www.ifanr.com/1227642'
    # 玩物志
    # url = 'https://www.ifanr.com/coolbuy/1227328'
    # 游戏
    # url = 'https://www.ifanr.com/1223605'
    # 视频(其视频都为内切的bilibili页面, 拿到iframe其中的代码即可, 但是原始video_url还存在问题, 先不处理)
    # url = 'https://www.ifanr.com/video/1227199'
    # url = 'https://www.ifanr.com/video/1201702'
    # url = 'https://www.ifanr.com/video/1195120'

    # 科学松鼠会
    # 工程
    # url = 'https://songshuhui.net/archives/105917'
    # 心理
    # url = 'https://songshuhui.net/archives/105965'
    # 健康
    # url = 'https://songshuhui.net/archives/105900'
    # 生物
    # url = 'https://songshuhui.net/archives/105950'
    # 医学
    # url = 'https://songshuhui.net/archives/105960'
    # 化学
    # url = 'https://songshuhui.net/archives/105163'
    # 天文
    # url = 'https://songshuhui.net/archives/105581'
    # 数学
    # url = 'https://songshuhui.net/archives/102949'
    # 环境
    # url = 'https://songshuhui.net/archives/104506'
    # 计算机
    # url = 'https://songshuhui.net/archives/104767'
    # 松鼠快评
    # url = 'https://songshuhui.net/archives/82224'
    # 少儿科普
    # url = 'https://songshuhui.net/archives/88788'
    # 媒体导读
    # url = 'https://songshuhui.net/archives/56553'
    # 活动
    # url = 'https://songshuhui.net/archives/103225'
    # 其他
    # url = 'https://songshuhui.net/archives/101270'

    # 界面新闻
    # url = 'https://www.jiemian.com/article/3265195.html'
    # url = 'https://www.jiemian.com/article/3267594.html'
    # url = 'https://www.jiemian.com/article/3503663.html'
    # 天下
    # url = 'https://www.jiemian.com/article/3267499.html'
    # url = 'https://www.jiemian.com/article/3262717.html'
    # 中国
    # url = 'https://www.jiemian.com/article/3266951.html'
    # 地方
    # url = 'https://www.jiemian.com/article/3267357.html'
    # 宏观
    # url = 'https://www.jiemian.com/article/3267391.html'
    # 数据
    # url = 'https://www.jiemian.com/article/3264008.html'
    # url = 'https://www.jiemian.com/article/3252963.html'
    # url = 'https://www.jiemian.com/article/3227712.html'
    # 评论
    # url = 'https://www.jiemian.com/article/3265615.html'
    # 文娱
    # url = 'https://www.jiemian.com/article/3265618.html'
    # 体育
    # url = 'https://www.jiemian.com/article/3267782.html'
    # 时尚
    # url = 'https://www.jiemian.com/article/3267630.html'
    # 文化
    # url = 'https://www.jiemian.com/article/3263646.html'
    # 旅行
    # url = 'https://www.jiemian.com/article/3264141.html'
    # 生活
    # url = 'https://www.jiemian.com/article/3263390.html'
    # 游戏
    # url = 'https://www.jiemian.com/article/3263543.html'
    # 歪楼
    # url= 'https://www.jiemian.com/article/3263035.html'
    # 影像
    # url = 'https://www.jiemian.com/article/3259950.html'
    # 商业
    # url = 'https://www.jiemian.com/article/3267974.html'
    # 科技
    # url = 'https://www.jiemian.com/article/3267974.html'
    # 交通
    # url = 'https://www.jiemian.com/article/3266169.html'
    # 投资
    # url = 'https://www.jiemian.com/article/3267363.html'
    # 管理
    # url = 'https://www.jiemian.com/article/3265243.html'
    # 健康
    # url = 'https://www.jiemian.com/article/3266728.html'
    # 视频
    # url = 'https://www.jiemian.com/video/AGQCNwhhB24BP1Vq.html'
    # url = 'https://www.jiemian.com/video/AGQCNwhhB24BPlVi.html'
    # url = 'https://www.jiemian.com/video/AGQCNwhhB24BPFVq.html'
    # 箭厂视频
    # url = 'https://www.jiemian.com/video/AGQCNwhhB2ABOVVi.html'
    # 面谈视频
    # url = 'https://www.jiemian.com/video/AGQCNwhhB2MBPVVk.html'
    # 歪楼小分队
    # url = 'https://www.jiemian.com/video/AGQCNwhnB2YBPFVn.html'
    # 番茄社视频
    # url = 'https://www.jiemian.com/video/AGQCNwhhB2EBMFVk.html'
    # 观见直播
    # url = 'https://www.jiemian.com/video/AGQCNwhhB24BP1Vh.html'

    # 澎湃网
    # 财经
    # url = 'https://m.thepaper.cn/newsDetail_forward_3839103'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3839853'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3846838'
    # 时事
    # url = 'https://m.thepaper.cn/newsDetail_forward_3840446'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3838988'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3846825'
    # TODO 时事中的这个不支持
    # url = 'http://news.cctv.com/2019/07/04/ARTIF52wrNXdxkXpjQYgWUp7190704.shtml'
    # 湃客
    # url = 'https://m.thepaper.cn/newsDetail_forward_3838888'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3840135'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3783807'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3840119'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3839964'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3835189'
    # 思想
    # url = 'https://m.thepaper.cn/newsDetail_forward_3817762'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3846862'
    # 问政
    # url = 'https://m.thepaper.cn/newsDetail_forward_3842458'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3845652'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3845265'
    # 生活
    # url = 'https://m.thepaper.cn/newsDetail_forward_3846718'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3838792'
    # 问吧
    # TODO 问吧不支持
    # url = 'https://m.thepaper.cn/asktopic_detail_10016331'
    # 媒体
    # url = 'https://m.thepaper.cn/newsDetail_forward_3846513'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3847138'
    # 视频
    # url = 'https://m.thepaper.cn/newsDetail_forward_3771975'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3846917'
    # 七环视频
    # url = 'https://m.thepaper.cn/newsDetail_forward_3847170'
    # url = 'https://m.thepaper.cn/newsDetail_forward_3844360'
    # 一级视场
    # url = 'https://m.thepaper.cn/newsDetail_forward_3840047'
    # 温度计
    # url = 'https://m.thepaper.cn/newsDetail_forward_3838786'
    # world湃
    # url = 'https://m.thepaper.cn/newsDetail_forward_3844360'
    # 澎湃科技
    # url = 'https://m.thepaper.cn/newsDetail_forward_3840018'
    # 健寻记
    # url = 'https://m.thepaper.cn/newsDetail_forward_3829764'
    # 城市漫步
    # url = 'https://m.thepaper.cn/newsDetail_forward_3778088'
    # 大都会
    # url = 'https://m.thepaper.cn/newsDetail_forward_3790389'
    # @所有人
    # url = 'https://m.thepaper.cn/newsDetail_forward_3839854'

    # 虎嗅网
    # url = 'https://m.huxiu.com/article/312411.html'
    # url = 'https://m.huxiu.com/article/309642.html'
    # url = 'https://m.huxiu.com/article/312390.html'
    # url = 'https://m.huxiu.com/article/314704.html'
    # 医疗健康
    # url = 'https://m.huxiu.com/article/308324.html'
    # url = 'https://m.huxiu.com/article/308204.html'
    # url = 'https://m.huxiu.com/article/307905.html'
    # url = 'https://m.huxiu.com/article/307743.html'
    # 电商消费
    # url = 'https://m.huxiu.com/article/308473.html'
    # url = 'https://m.huxiu.com/article/308467.html'
    # url = 'https://m.huxiu.com/article/308442.html'
    # 娱乐淘金
    # url = 'https://m.huxiu.com/article/308523.html'
    # url = 'https://m.huxiu.com/article/308340.html'
    # 车与出行
    # url = 'https://m.huxiu.com/article/308465.html'
    # url = 'https://m.huxiu.com/article/308022.html'
    # 人工智能
    # url = 'https://m.huxiu.com/article/307650.html'
    # 年轻一代
    # url = 'https://m.huxiu.com/article/308441.html'
    # 智能终端
    # url = 'https://m.huxiu.com/article/308527.html'
    # 文化教育
    # url = 'https://m.huxiu.com/article/308471.html'
    # 金融地产
    # url = 'https://m.huxiu.com/article/308425.html'
    # 企业服务
    # url = 'https://m.huxiu.com/article/308152.html'
    # 创业维艰
    # url = 'https://m.huxiu.com/article/308496.html'
    # 社交通讯
    # url = 'https://m.huxiu.com/article/308505.html'
    # 全球热点
    # url = 'https://m.huxiu.com/article/308509.html'
    # 生活腔调
    # url = 'https://m.huxiu.com/article/308510.html'
    # 视频
    # url = 'https://m.huxiu.com/article/308402.html'
    # url = 'https://m.huxiu.com/article/307339.html'
    # todo collection非图文, pass
    # url = 'https://m.huxiu.com/collection/381.html'

    # 南方周末(其中只有部分文章可用, 不推荐使用)
    # url = 'http://www.infzm.com/wap/#/content/153845'
    # url = 'http://www.infzm.com/wap/#/content/153862'
    # url = 'http://www.infzm.com/wap/#/content/158165'
    # TODO 无法查看文章内容:
    #  1. 含有redirect为非正常url
    #  2. or 包括部分文章只能在app内打开(即标题边上有南方周末小img的，即会员才能查看), 这部分url无法处理
    # url = 'http://www.infzm.com/wap/#/content/153536?redirect=%2Fcontent%2F153500'
    # 新闻
    # url = 'http://www.infzm.com/wap/#/content/153500'
    # url = 'http://www.infzm.com/wap/#/content/153849'
    # url = 'http://www.infzm.com/wap/#/content/153851'
    # url = 'http://www.infzm.com/wap/#/content/153760'
    # 文化
    # url = 'http://www.infzm.com/wap/#/content/153854'
    # 人物
    # url = 'http://www.infzm.com/wap/#/content/153334'
    # 生活
    # url = 'http://www.infzm.com/wap/#/content/152879'
    # 社会
    # url = 'http://www.infzm.com/wap/#/content/153416'
    # 教育
    # url = 'http://www.infzm.com/wap/#/content/152819'
    # 财富
    # url = 'http://www.infzm.com/wap/#/content/147544'

    # 好奇心日报
    # todo 文章为书的介绍的不做采集
    # 商业
    # url = 'http://m.qdaily.com/mobile/articles/64092.html'
    # url = 'http://m.qdaily.com/mobile/articles/64087.html'
    # url = 'http://m.qdaily.com/mobile/articles/64084.html'
    # 时尚
    # url = 'http://m.qdaily.com/mobile/articles/64089.html'
    # 智能
    # url = 'http://m.qdaily.com/mobile/articles/64078.html'
    # 娱乐
    # url = 'http://m.qdaily.com/mobile/articles/64072.html'
    # 文化
    # url = 'http://m.qdaily.com/mobile/articles/64060.html'
    # url = 'http://m.qdaily.com/mobile/articles/63484.html'
    # 文化长文章
    # url = 'http://m.qdaily.com/mobile/articles/63974.html'
    # 设计
    # url = 'http://m.qdaily.com/mobile/articles/64056.html'
    # 游戏
    # url = 'http://m.qdaily.com/mobile/articles/64050.html'

    # 场库
    # url = 'https://www.vmovier.com/57050?from=index_new_title'
    # url = 'https://www.vmovier.com/57057?from=index_new_title'
    # url = 'https://www.vmovier.com/57035?from=index_new_title'
    # url = 'https://www.vmovier.com/56985?from=index_hot_week_title'
    # url = 'https://www.vmovier.com/57028?from=index_hot_week_title'
    # url = 'https://www.vmovier.com/56442?from=index_rand_title'

    # 梨视频
    # url = 'https://www.pearvideo.com/video_1584072'
    # url = 'https://www.pearvideo.com/video_1583852'
    # 新知
    # url = 'https://www.pearvideo.com/video_1584002'
    # url = 'https://www.pearvideo.com/video_1583149'
    # 社会
    # url = 'https://www.pearvideo.com/video_1583889'
    # 世界
    # url = 'https://www.pearvideo.com/video_1584109'
    # 体育
    # url = 'https://www.pearvideo.com/video_1584079'
    # 生活
    # url = 'https://www.pearvideo.com/video_1570493'
    # 科技
    # url = 'https://www.pearvideo.com/video_1584259'
    # 娱乐
    # url = 'https://www.pearvideo.com/video_1584141'
    # 财富
    # url = 'https://www.pearvideo.com/video_1584122'
    # 汽车
    # url = 'https://www.pearvideo.com/video_1584113'
    # 美食
    # url = 'https://www.pearvideo.com/video_1584089'
    # 音乐
    # url = 'https://www.pearvideo.com/video_1584314'
    # 拍客
    # url = 'https://www.pearvideo.com/video_1584404'
    # todo 万象, 图文文章(多为国家相关, 不采集)
    # todo 直播不采集
    # url = 'https://www.pearvideo.com/living_1583854'

    # 艾墨镇
    # url = 'https://aimozhen.com/view/15994/'
    # url = 'https://aimozhen.com/view/15770/'
    # url = 'https://aimozhen.com/view/15537/'
    # url = 'https://aimozhen.com/view/15505/'
    # url = 'https://aimozhen.com/view/15996/'
    # url = 'https://aimozhen.com/view/15993/'
    # url = 'https://aimozhen.com/view/2789/'
    # url = 'https://aimozhen.com/view/10345/'
    # url = 'https://aimozhen.com/view/15620/'
    # url = 'https://aimozhen.com/view/15960/'

    # 美拍
    # url = 'https://www.meipai.com/media/1129488204'
    # url = 'https://www.meipai.com/media/1119174156'
    # url = 'https://www.meipai.com/media/1131644923'
    # url = 'https://www.meipai.com/media/1133207409'
    # url = 'https://www.meipai.com/media/1132365942'
    # url = 'https://www.meipai.com/media/1131644923'
    # todo 直播不采集

    # 百度好看视频
    # 推荐
    # url = 'https://haokan.baidu.com/v?vid=4136323293933620725&tab=recommend'
    # url = 'https://haokan.baidu.com/v?vid=13905274734303307712&tab=recommend'
    # 影视
    # url = 'https://haokan.baidu.com/v?vid=17753035492617182944&tab=yingshi'
    # 音乐
    # url = 'https://haokan.baidu.com/v?vid=15566590767854893570&tab=yinyue'
    # 搞笑
    # url = 'https://haokan.baidu.com/v?vid=11049055717053789925&tab=gaoxiao'
    # vlog
    # url = 'https://haokan.baidu.com/v?vid=18364192214912567672&tab=vlog'
    # 娱乐
    # url = 'https://haokan.baidu.com/v?vid=2039585784239075755&tab=yule'
    # 动漫
    # url = 'https://haokan.baidu.com/v?vid=13669502144755223017&tab=dongman'
    # 生活
    # url = 'https://haokan.baidu.com/v?vid=6013186501247664939&tab=shenghuo'
    # 小品
    # url = 'https://haokan.baidu.com/v?vid=1950334490626075127&tab=xiaopin'
    # 综艺
    # url = 'https://haokan.baidu.com/v?vid=3543129372355380096&tab=zongyi'
    # 游戏
    # url = 'https://haokan.baidu.com/v?vid=16045267043621223572&tab=youxi'
    # 秒懂
    # url = 'https://haokan.baidu.com/v?vid=8764292721309064181&tab=miaodong'
    # 教育
    # url = 'https://haokan.baidu.com/v?vid=13019064242738140769&tab=jiaoyu'
    # 军事
    # url = 'https://haokan.baidu.com/v?vid=9293974956392010975&tab=junshi'
    # 科技
    # url = 'https://haokan.baidu.com/v?vid=3788911623189008455&tab=keji'
    # 汽车
    # url = 'https://haokan.baidu.com/v?vid=8655585633607378937&tab=qiche'
    # 纪录片
    # url = 'https://haokan.baidu.com/v?vid=11997191395202643272&tab=record'
    # 体育
    # url = 'https://haokan.baidu.com/v?vid=16107732794840639604&tab=tiyu'
    # 文化
    # url = 'https://haokan.baidu.com/v?vid=7456588810512052606&tab=wenhua'
    # 亲子
    # url = 'https://haokan.baidu.com/v?vid=15546006886814520106&tab=qinzi'
    # 社会
    # url = 'https://haokan.baidu.com/v?vid=648167893261511164&tab=shehui'
    # 三农
    # url = 'https://haokan.baidu.com/v?vid=4161801005423552525&tab=sannong'
    # 宠物
    # url = 'https://haokan.baidu.com/v?vid=9740175951467494081&tab=chongwu'
    # 美食
    # url = 'https://haokan.baidu.com/v?vid=11754326304031754679&tab=meishi'
    # 时尚
    # url = 'https://haokan.baidu.com/v?vid=17448170737812377575&tab=shishang'

    # 七丽女性网
    # url = 'https://i.7y7.com/hufu/84/385784.html'
    # url = 'https://i.7y7.com/remenzixun/31/386631.html'
    # url = 'https://i.7y7.com/hufu/42/386542.html'
    # 时尚
    # url = 'https://i.7y7.com/fushi/04/386404.html'
    # url = 'https://i.7y7.com/fushi/62/385562.html'
    # 护肤
    # url = 'https://i.7y7.com/hufu/35/386635.html'
    # url = 'https://i.7y7.com/hufu/37/385737.html'
    # 彩妆
    # url = 'https://i.7y7.com/caizhuang/36/386636.html'
    # 减肥
    # url = 'https://i.7y7.com/shoushen/93/386493.html'
    # 美发
    # url = 'https://i.7y7.com/meifa/28/386628.html'
    # 医美
    # url = 'https://i.7y7.com/yimei/91/386491.html'
    # 博主
    # url = 'https://i.7y7.com/bozhu/93/338893.html'
    # 街拍
    # url = 'https://i.7y7.com/jiepai/34/383734.html'
    # 星座
    # url = 'https://i.7y7.com/xingzuo/05/386605.html'
    # 情感
    # url = 'https://i.7y7.com/qinggan/24/384924.html'
    # 健康
    # url = 'https://i.7y7.com/jiankang/36/386536.html'
    # 亲子
    # url = 'https://i.7y7.com/qinzi/37/386237.html'
    # 美甲
    # url = 'https://i.7y7.com/meijia/60/386260.html'
    # 时装
    # url = 'https://i.7y7.com/shizhuang/77/386177.html'
    # 优品
    # url = 'https://i.7y7.com/youpin/13/384213.html'
    # 秀场
    # url = 'https://i.7y7.com/xiuchang/84/364884.html'
    # 明星
    # url = 'https://i.7y7.com/mingxing/25/384425.html'
    # 大片(多为纯图, 不提取)
    # 影视
    # url = 'https://i.7y7.com/yingshi/48/381648.html'
    # 家居
    # url = 'https://i.7y7.com/jiaju/97/386197.html'
    # todo 广场不采集, 纯图文章不采集

    # 亲亲宝贝
    # todo 听声音cp后台无法转, pass
    # url = 'https://m.qbaobei.com/a/1372873.html'
    # 备孕
    # url = 'https://m.qbaobei.com/a/1372711.html'
    # url = 'https://m.qbaobei.com/a/1365780.html'
    # 怀孕
    # url = 'https://m.qbaobei.com/a/1145214.html'
    # 分娩
    # url = 'https://m.qbaobei.com/a/1103497.html'
    # 产后
    # url = 'https://m.qbaobei.com/a/1064188.html'
    # 新生儿
    # url = 'https://m.qbaobei.com/a/1372717.html'
    # url = 'https://m.qbaobei.com/a/387813.html'
    # 0-1岁
    # url = 'https://m.qbaobei.com/a/470111.html'
    # 1-3岁
    # url = 'https://m.qbaobei.com/a/807352.html'
    # 3-6岁
    # url = 'https://m.qbaobei.com/a/442792.html'
    # 早教
    # url = 'https://m.qbaobei.com/a/1192626.html'
    # 食谱
    # url = 'https://m.qbaobei.com/a/1191509.html'
    # 百科
    # url = 'https://m.qbaobei.com/a/439598.html'
    # url = 'https://m.qbaobei.com/a/671501.html'
    # 用品
    # url = 'https://m.qbaobei.com/a/1000502.html'
    # 奶粉
    # url = 'https://m.qbaobei.com/a/1361544.html'
    # 视频
    # url = 'https://m.qbaobei.com/v/video_2972.html'
    # url = 'https://m.qbaobei.com/v/video_8.html'
    # url = 'https://m.qbaobei.com/v/video_25.html'
    # todo 小时光, 听听 不采集

    # 发条网
    # 视频
    # url = 'https://mart.fatiao.pro/detail/1522.html'
    # url = 'https://mart.fatiao.pro/detail/2268.html'
    # url = 'https://mlive.fatiao.pro/detail/8755.html'
    # url = 'https://mlive.fatiao.pro/detail/8909.html'
    # url = 'https://mlive.fatiao.pro/detail/8772.html'
    # url = 'https://mnatural.fatiao.pro/detail/4194.html'
    # url = 'https://mqtwj.fatiao.pro/detail/8937.html'
    # 图文
    # url = 'https://mpet.fatiao.pro/article/7858.html'
    # url = 'https://mpet.fatiao.pro/article/1093.html'
    # url = 'https://mpet.fatiao.pro/article/5137.html'
    # url = 'https://mpet.fatiao.pro/article/9477.html'
    # url = 'https://mbeauty.fatiao.pro/article/52633.html'
    # url = 'https://mbeauty.fatiao.pro/article/28785.html'
    # url = 'https://mlive.fatiao.pro/article/52761.html'

    # 觅糖
    # 视频
    # url = 'https://www.91mitang.com/pages/2019011772010'
    # 时尚
    # url = 'https://www.91mitang.com/pages/81047'
    # 美食
    # url = 'https://www.91mitang.com/pages/2019011771915'
    # 生活百科
    # url = 'https://www.91mitang.com/pages/2019011751000'
    # 教育
    # url = 'https://www.91mitang.com/pages/2019011772120'
    # 其他
    # url = 'https://www.91mitang.com/pages/2019011761003'
    # 诗词朗诵
    # url = 'https://www.91mitang.com/pages/71225'
    # 节日风俗
    # url = 'https://www.91mitang.com/pages/70006'
    # 课程学习
    # url = 'https://www.91mitang.com/pages/71115'
    # 家常菜谱
    # url = 'https://www.91mitang.com/pages/72014'
    # 风味小吃
    # url = 'https://www.91mitang.com/pages/72176'
    # 旅游出行
    # url = 'https://www.91mitang.com/pages/83527'
    # 美妆护肤
    # url = 'https://www.91mitang.com/pages/81047'
    # 娱乐
    # url = 'https://www.91mitang.com/pages/91022'
    # 图文文章
    # url = 'https://www.91mitang.com/pages/2106103'
    # url = 'https://www.91mitang.com/pages/2106106'

    # 雪球网
    # 推荐
    # url = 'https://xueqiu.com/8036802659/131021825'
    # url = 'https://xueqiu.com/3075122481/131022515'
    # 沪深
    # url = 'https://xueqiu.com/S/SH600309/131099947'
    # url = 'https://xueqiu.com/8992033978/131027969'
    # url = 'https://xueqiu.com/9220236682/131126259'
    # 科创板
    # url = 'https://xueqiu.com/1896346964/130972987'
    # 港股
    # url = 'https://xueqiu.com/1055336715/129835730'
    # 基金
    # url = 'https://xueqiu.com/7298671747/131128718'
    # 美股
    # url = 'https://xueqiu.com/S/DL/131099586'
    # url = 'https://xueqiu.com/8041756563/131102425'
    # 房产
    # url = 'https://xueqiu.com/1428373799/130981044'
    # 私募
    # url = 'https://xueqiu.com/3186487370/130986249'
    # 汽车
    # url = 'https://xueqiu.com/4828772707/130482225'
    # 保险
    # url = 'https://xueqiu.com/5157574024/130400677'

    # 5号女性网
    # url = 'http://m.5h.com/mr/161290.html'
    # url = 'http://m.5h.com/mr/140547.html'
    # 化妆
    # url = 'http://m.5h.com/mr/152296.html'
    # url = 'http://m.5h.com/mr/157448.html'
    # 护肤
    # url = 'http://m.5h.com/mr/152431.html'
    # 减肥
    # url = 'http://m.5h.com/mr/151883.html'
    # 发型
    # url = 'http://m.5h.com/mr/157448.html'
    # 时尚
    # url = 'http://m.5h.com/mr/152413.html'
    # 情感
    # url = 'http://m.5h.com/ys/152131.html'
    # 亲子
    # url = 'http://m.5h.com/qz/153147.html'
    # 整形
    # url = 'http://m.5h.com/mr/152342.html'
    # 饮食
    # url = 'http://m.5h.com/ys/152432.html'
    # 养生
    # url = 'http://m.5h.com/ys/153185.html'
    # 医疗
    # url = 'http://m.5h.com/yl/153612.html'
    # 看病
    # url = 'http://m.5h.com/yl/148912.html'
    # todo 不支持专题,

    # 百思不得姐
    # url = 'http://www.budejie.com/detail-29745738.html'
    # url = 'http://www.budejie.com/detail-29752780.html'
    # url = 'http://www.budejie.com/detail-29752170.html'
    # url = 'http://www.budejie.com/detail-29752481.html'
    # url = 'http://www.budejie.com/detail-29752617.html'
    # url = 'http://www.budejie.com/detail-29160596.html'
    # 纯文字
    # url = 'http://www.budejie.com/detail-29752862.html'
    # todo 声音不支持

    # 文章url 测试
    print('article_url: {}'.format(url))
    article_parse_res = loop.run_until_complete(
        future=_._parse_article(article_url=url))
    pprint(article_parse_res)
    # print(dumps(article_parse_res))

    # article spiders intro
    # tmp = loop.run_until_complete(_.get_article_spiders_intro())
    # print(tmp)

    # 文章列表
    # tmp = loop.run_until_complete(_.get_article_list_by_article_type(
    #     article_type='zq',))
    # pprint(tmp)

if __name__ == '__main__':
    main()