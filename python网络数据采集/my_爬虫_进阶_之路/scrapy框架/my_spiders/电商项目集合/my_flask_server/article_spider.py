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
    
not supported:
    1. 新华网(http://m.xinhuanet.com)
    2. 36氪(https://36kr.com)
    3. 太平洋时尚网(https://www.pclady.com.cn/)
    4. 网易新闻
    
news_media_ranking_url(https://top.chinaz.com/hangye/index_news.html)
"""

from os import getcwd
from os.path import abspath
from gc import collect
from ftfy import fix_text
from requests import session
from my_items import WellRecommendArticle
from settings import (
    ARTICLE_ITEM_LIST,
    MY_SPIDER_LOGS_PATH,
    PHANTOMJS_DRIVER_PATH,
    FIREFOX_DRIVER_PATH,
    IP_POOL_TYPE,)

from fzutils.spider.fz_driver import (
    PHANTOMJS,
    FIREFOX,
    PC,
    PHONE,
    BaseDriver,)
from fzutils.internet_utils import _get_url_contain_params
from fzutils.data.list_utils import list_remove_repeat_dict_plus
from fzutils.spider.selector import (
    async_parse_field,
    parse_field,)
from fzutils.spider.fz_requests import PROXY_TYPE_HTTPS
from fzutils.spider.async_always import *

class ArticleParser(AsyncCrawler):
    """article spider"""
    def __init__(self, logger=None, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            logger=logger,
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
            print(content)
            create_time = await self._get_article_create_time(
                parse_obj=parse_obj,
                target_obj=article_html,
                video_url=video_url,
                article_url=article_url,)
            comment_num = await self._get_comment_num(parse_obj=parse_obj, target_obj=article_html)
            fav_num = await self._get_fav_num(parse_obj=parse_obj, target_obj=article_html)
            praise_num = await self._get_praise_num(parse_obj=parse_obj, target_obj=article_html)
            tags_list = await self._get_tags_list(parse_obj=parse_obj, target_obj=article_html)
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

    @staticmethod
    async def _get_obj_origin() -> dict:
        """
        设置obj_origin_dict
        :return:
        """
        return {
            'wx': {
                'obj_origin': 'mp.weixin.qq.com',
                'site_id': 4,
            },
            'tt': {
                'obj_origin': 'www.toutiao.com',
                'site_id': 5,
            },
            'js': {
                'obj_origin': 'www.jianshu.com',
                'site_id': 6,
            },
            'kd': {
                'obj_origin': 'post.mp.qq.com',
                'site_id': 7,
            },
            'kb': {
                'obj_origin': 'kuaibao.qq.com',
                'site_id': 8,
            },
            'df': {
                'obj_origin': 'toutiao.eastday.com',
                'site_id': 9,
            },
            'sg': {
                'obj_origin': 'sa.sogou.com',
                'site_id': 10,
            },
            'bd': {
                'obj_origin': 'm.baidu.com',
                'site_id': 11,
            },
            'zq': {
                'obj_origin': 'focus.youth.cn',
                'site_id': 12,
            },
            'yg': {
                'obj_origin': 'www.365yg.com',
                'site_id': 13,
            },
            'fh': {
                'obj_origin': 'news.ifeng.com',
                'site_id': 14,
            },
            'ys': {
                'obj_origin': 'www.51jkst.com',
                'site_id': 15,
            },
            'cn': {
                'obj_origin': 'm.cnys.com',
                'site_id': 16,
            },
            'if': {
                'obj_origin': 'www.ifanr.com',
                'site_id': 17,
            },
            'ss': {
                'obj_origin': 'songshuhui.net',
                'site_id': 18,
            },
            'jm': {
                'obj_origin': 'www.jiemian.com',
                'site_id': 19,
            },
            'pp': {
                'obj_origin': 'm.thepaper.cn',
                'site_id': 20,
            },
            'hx': {
                'obj_origin': 'm.huxiu.com',
                'site_id': 21,
            },
            'nfzm': {
                'obj_origin': 'www.infzm.com',
                'site_id': 22,
            },
            'hqx': {
                'obj_origin': 'm.qdaily.com',
                'site_id': 23,
            },
            'xg': {
                'obj_origin': 'www.ixigua.com',
                'site_id': 24,
            },
            'ck': {
                'obj_origin': 'www.vmovier.com',
                'site_id': 25,
            },
            'lsp': {
                'obj_origin': 'www.pearvideo.com',
                'site_id': 26,
            },
            'amz': {
                'obj_origin': 'aimozhen.com',
                'site_id': 27,
            },
            'mp': {
                'obj_origin': 'www.meipai.com',
                'site_id': 28,
            },
        }

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

    async def _get_wx_article_html(self, article_url) -> tuple:
        """
        得到wx文章内容
        :return: body, video_url
        """
        body = await unblock_request(
            url=article_url,
            headers=await self._get_random_pc_headers(),
            ip_pool_type=self.ip_pool_type,
            logger=self.lg)
        # self.lg.info(body)
        assert body != '', '获取到wx的body为空值!'

        return await self._wash_wx_article_body(body=body)

    async def _get_tt_article_html(self, article_url) -> tuple:
        """
        得到头条文章内容
        :param article_url:
        :return: body, video_url
        """
        headers = await self._get_random_pc_headers()
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
        headers = await self._get_random_pc_headers()
        headers.update({
            'authority': 'www.jianshu.com',
            'referer': 'https://www.jianshu.com/',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg,)
        # self.lg.info(str(body))
        assert body != '', '获取到的js的body为空值!'

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
        # 处理图片
        content = re.compile(' data-original-src=').sub(' src=', content)
        content = re.compile(' data-original-filesize=\".*?\"').sub(' style=\"height:auto;width:100%;\"', content)

        # 附加上原生的style
        # 此法在server上getcwd()得到的是'/', os.path.abspath('.')得到的才是当前目录, 还是'/', 改用云存
        # now_path = abspath('.') + '/tmp/jianshu_style.txt'
        # print(now_path)
        # with open(now_path, 'r') as f:
        #     _ = Requests._wash_html(f.read())
        #     self.lg.info(str(_))

        # 云存储
        # jianshu_style_txt_url = 'http://pimkvjbu6.bkt.clouddn.com/jianshu_style.txt'
        # with session() as s:
        #     _ = Requests._wash_html(s.get(url=jianshu_style_txt_url).content.decode('utf-8'))
        # assert _ != '', '云端jianshu_style_txt获取失败!'

        # 直接处理到原js
        _ = '<style type="text/css">@charset "UTF-8";.image-package .image-container{position:relative;z-index:2;background-color:#eee;-webkit-transition:background-color .1s linear;-o-transition:background-color .1s linear;transition:background-color .1s linear;margin:0 auto}body.reader-night-mode .image-package .image-container{background-color:#545454}.image-package .image-container-fill{z-index:1}.image-package .image-container .image-view{position:absolute;top:0;left:0;width:100%;height:100%;overflow:hidden}.image-package .image-container .image-view-error:after{content:"图片获取失败，请点击重试";position:absolute;top:50%;left:50%;width:100%;-webkit-transform:translate(-50%,-50%);-ms-transform:translate(-50%,-50%);transform:translate(-50%,-50%);color:#888;font-size:14px}.image-package .image-mage-view img.image-loading{opacity:.3}.image-package .image-container .image-view img{-webkit-transition:all .15s linear;-o-transition:all .15s linear;transition:all .15s linear;z-index:2;opacity:1}</style><style type="text/css">fieldset[disabled] .multiselect {pointer-events: none;}.multiselect__spinner {position: absolute;right: 1px;top: 1px;width: 48px;height: 35px;background: #fff;display: block;}.multiselect__spinner:after,.multiselect__spinner:before {position: absolute;content: "";top: 50%;left: 50%;margin: -8px 0 0 -8px;width: 16px;height: 16px;border-radius: 100%;border-color: #41b883 transparent transparent;border-style: solid;border-width: 2px;box-shadow: 0 0 0 1px transparent;}.multiselect__spinner:before {animation: a 2.4s cubic-bezier(.41,.26,.2,.62);animation-iteration-count: infinite;}.multiselect__spinner:after {animation: a 2.4s cubic-bezier(.51,.09,.21,.8);animation-iteration-count: infinite;}.multiselect__loading-enter-active,.multiselect__loading-leave-active {transition: opacity .4s ease-in-out;opacity: 1;}.multiselect__loading-enter,.multiselect__loading-leave-active {opacity: 0;}.multiselect,.multiselect__input,.multiselect__single {font-family: inherit;font-size: 14px;-ms-touch-action: manipulation;touch-action: manipulation;}.multiselect {box-sizing: content-box;display: block;position: relative;width: 100%;min-height: 40px;text-align: left;color: #35495e;}.multiselect * {box-sizing: border-box;}.multiselect:focus {outline: none;}.multiselect--disabled {opacity: .6;}.multiselect--active {z-index: 1;}.multiselect--active:not(.multiselect--above) .multiselect__current,.multiselect--active:not(.multiselect--above) .multiselect__input,.multiselect--active:not(.multiselect--above) .multiselect__tags {border-bottom-left-radius: 0;border-bottom-right-radius: 0;}.multiselect--active .multiselect__select {transform: rotate(180deg);}.multiselect--above.multiselect--active .multiselect__current,.multiselect--above.multiselect--active .multiselect__input,.multiselect--above.multiselect--active .multiselect__tags {border-top-left-radius: 0;border-top-right-radius: 0;}.multiselect__input,.multiselect__single {position: relative;display: inline-block;min-height: 20px;line-height: 20px;border: none;border-radius: 5px;background: #fff;padding: 0 0 0 5px;width: 100%;transition: border .1s ease;box-sizing: border-box;margin-bottom: 8px;vertical-align: top;}.multiselect__tag~.multiselect__input,.multiselect__tag~.multiselect__single {width: auto;}.multiselect__input:hover,.multiselect__single:hover {border-color: #cfcfcf;}.multiselect__input:focus,.multiselect__single:focus {border-color: #a8a8a8;outline: none;}.multiselect__single {padding-left: 6px;margin-bottom: 8px;}.multiselect__tags-wrap {display: inline;}.multiselect__tags {min-height: 40px;display: block;padding: 8px 40px 0 8px;border-radius: 5px;border: 1px solid #e8e8e8;background: #fff;}.multiselect__tag {position: relative;display: inline-block;padding: 4px 26px 4px 10px;border-radius: 5px;margin-right: 10px;color: #fff;line-height: 1;background: #41b883;margin-bottom: 5px;white-space: nowrap;overflow: hidden;max-width: 100%;text-overflow: ellipsis;}.multiselect__tag-icon {cursor: pointer;margin-left: 7px;position: absolute;right: 0;top: 0;bottom: 0;font-weight: 700;font-style: normal;width: 22px;text-align: center;line-height: 22px;transition: all .2s ease;border-radius: 5px;}.multiselect__tag-icon:after {content: "\D7";color: #266d4d;font-size: 14px;}.multiselect__tag-icon:focus,.multiselect__tag-icon:hover {background: #369a6e;}.multiselect__tag-icon:focus:after,.multiselect__tag-icon:hover:after {color: #fff;}.multiselect__current {min-height: 40px;overflow: hidden;padding: 8px 12px 0;padding-right: 30px;white-space: nowrap;border-radius: 5px;border: 1px solid #e8e8e8;}.multiselect__current,.multiselect__select {line-height: 16px;box-sizing: border-box;display: block;margin: 0;text-decoration: none;cursor: pointer;}.multiselect__select {position: absolute;width: 40px;height: 38px;right: 1px;top: 1px;padding: 4px 8px;text-align: center;transition: transform .2s ease;}.multiselect__select:before {position: relative;right: 0;top: 65%;color: #999;margin-top: 4px;border-style: solid;border-width: 5px 5px 0;border-color: #999 transparent transparent;content: "";}.multiselect__placeholder {color: #adadad;display: inline-block;margin-bottom: 10px;padding-top: 2px;}.multiselect--active .multiselect__placeholder {display: none;}.multiselect__content-wrapper {position: absolute;display: block;background: #fff;width: 100%;max-height: 240px;overflow: auto;border: 1px solid #e8e8e8;border-top: none;border-bottom-left-radius: 5px;border-bottom-right-radius: 5px;z-index: 1;-webkit-overflow-scrolling: touch;}.multiselect__content {list-style: none;display: inline-block;padding: 0;margin: 0;min-width: 100%;vertical-align: top;}.multiselect--above .multiselect__content-wrapper {bottom: 100%;border-bottom-left-radius: 0;border-bottom-right-radius: 0;border-top-left-radius: 5px;border-top-right-radius: 5px;border-bottom: none;border-top: 1px solid #e8e8e8;}.multiselect__content::webkit-scrollbar {display: none;}.multiselect__element {display: block;}.multiselect__option {display: block;padding: 12px;min-height: 40px;line-height: 16px;text-decoration: none;text-transform: none;vertical-align: middle;position: relative;cursor: pointer;white-space: nowrap;}.multiselect__option:after {top: 0;right: 0;position: absolute;line-height: 40px;padding-right: 12px;padding-left: 20px;}.multiselect__option--highlight {background: #41b883;outline: none;color: #fff;}.multiselect__option--highlight:after {content: attr(data-select);background: #41b883;color: #fff;}.multiselect__option--selected {background: #f3f3f3;color: #35495e;font-weight: 700;}.multiselect__option--selected:after {content: attr(data-selected);color: silver;}.multiselect__option--selected.multiselect__option--highlight {background: #ff6a6a;color: #fff;}.multiselect__option--selected.multiselect__option--highlight:after {background: #ff6a6a;content: attr(data-deselect);color: #fff;}.multiselect--disabled {background: #ededed;pointer-events: none;}.multiselect--disabled .multiselect__current,.multiselect--disabled .multiselect__select,.multiselect__option--disabled {background: #ededed;color: #a6a6a6;}.multiselect__option--disabled {cursor: text;pointer-events: none;}.multiselect__option--disabled.multiselect__option--highlight {background: #dedede!important;}.multiselect-enter-active,.multiselect-leave-active {transition: all .15s ease;}.multiselect-enter,.multiselect-leave-active {opacity: 0;}.multiselect__strong {margin-bottom: 8px;line-height: 20px;display: inline-block;vertical-align: top;}[dir=rtl] .multiselect {text-align: right;}[dir=rtl] .multiselect__select {right: auto;left: 1px;}[dir=rtl] .multiselect__tags {padding: 8px 8px 0 40px;}[dir=rtl] .multiselect__content {text-align: right;}[dir=rtl] .multiselect__option:after {right: auto;left: 0;}[dir=rtl] .multiselect__clear {right: auto;left: 12px;}[dir=rtl] .multiselect__spinner {right: auto;left: 1px;}@keyframes a {0% {transform: rotate(0);}to {transform: rotate(2turn);}}</style><style>.image-container-fill{z-index:1}</style>'

        content = _ + content
        # 清洗
        content = re.compile('<div class=\"image-caption\">图片发自简书App</div>').sub('', content)

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
                return await self._get_wx_article_html(article_url=article_url)

            elif article_url_type == 'tt':
                return await self._get_tt_article_html(article_url=article_url)

            elif article_url_type == 'js':
                return await self._get_js_article_html(article_url=article_url)

            elif article_url_type == 'kd':
                return await self._get_kd_article_html(article_url=article_url)

            elif article_url_type == 'kb':
                return await self._get_kb_article_html(article_url=article_url)

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

            else:
                raise AssertionError('未实现的解析!')

        except AssertionError:
            self.lg.error('遇到错误:', exc_info=True)

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
        headers = await self._get_random_phone_headers()
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
            type=PHANTOMJS,
            executable_path=PHANTOMJS_DRIVER_PATH,
            # type=FIREFOX,
            # executable_path=FIREFOX_DRIVER_PATH,
            ip_pool_type=self.ip_pool_type,
            load_images=True,
            headless=True,
            logger=self.lg,)
        driver.get_url_body(
            url=article_url,
            timeout=25,)
        driver.find_element(value='i.play-icon').click()
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
        parser_obj = await self._get_parse_obj(article_url_type='ck')
        article_id = await async_parse_field(
            parser=parser_obj['article_id'],
            target_obj=article_url,
            logger=self.lg,)
        assert article_id != '', 'article_id != ""'
        # method1: driver 请求pc地址但是user_agent=phone
        # method2: driver pc 页面转phone, 可获得下方接口
        headers = await self._get_random_phone_headers()
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
        headers = await self._get_random_phone_headers()
        headers.update({
            'Connection': 'keep-alive',
            # 'Referer': 'http://m.qdaily.com/mobile/homes.html',
            'Referer': article_url,
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
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
        # 走api
        video_url = ''
        headers = await self._get_random_phone_headers()
        headers.update({
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        params = (
            ('version', '1.1.15'),
            ('platform', 'wap'),
            ('user_id', ''),
            ('token', ''),
        )
        # 获取article_id
        parser_obj = await self._get_parse_obj(article_url_type='nfzm')
        article_id = await async_parse_field(
            parser=parser_obj['article_id'],
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
        self.hook_target_api_data = json_2_dict(
            json_str=body,
            logger=self.lg,
            default_res={},).get('data', {})
        assert self.hook_target_api_data != {}, 'nfzm的api data为空dict!'
        # pprint(self.hook_target_api_data)

        return body, video_url

    async def _get_hx_article_html(self, article_url) -> tuple:
        """
        get hx html
        :param article_url:
        :return:
        """
        video_url = ''
        headers = await self._get_random_phone_headers()
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
        video_url = ''
        headers = await self._get_phone_headers()
        headers.update({
            'Connection': 'keep-alive',
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
        headers = await self._get_random_pc_headers()
        headers.update({
            'Referer': 'https://www.jiemian.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
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
        headers = await self._get_random_pc_headers()
        headers.update({
            'Referer': 'https://songshuhui.net/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
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
        headers = await self._get_random_pc_headers()
        headers.update({
            'authority': 'www.ifanr.com',
            'referer': 'https://www.ifanr.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
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
        headers = await self._get_phone_headers()
        headers.update({
            'Connection': 'keep-alive',
            'Referer': 'http://m.cnys.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
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
        headers = await self._get_random_pc_headers()
        headers.update({
            'Referer': 'http://www.51jkst.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
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
            headers = await self._get_random_pc_headers()
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
            headers = await self._get_random_pc_headers()
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
        video_url = 'https:' + tmp_video_url if tmp_video_url != '' else ''
        # self.lg.info(video_url)

        return body, video_url

    async def _get_zq_article_html(self, article_url) -> tuple:
        """
        获取zq article的html
        :param article_url:
        :return:
        """
        video_url = ''
        headers = await self._get_phone_headers()
        headers.update({
            'Connection': 'keep-alive',
            # 'Referer': 'https://focus.youth.cn/html/articleTop/mobile.html?type=1',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.request_num_retries,
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
        headers = await self._get_phone_headers()
        headers.update({
            'Connection': 'keep-alive',
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
        headers = await self._get_phone_headers()
        headers.update({
            'Connection': 'keep-alive',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'https://wap.sogou.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        if '/sgs_video.php' in article_url:
            # body 为动态加载的, 需要driver
            body = await self._get_html_by_driver(
                url=article_url,
                load_images=False,)
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
            self.lg.info('该文章含视频!')
            video_url_selector = {
                'method': 'css',
                'selector': 'video#my-video source ::attr("src")',
            }
            video_url = await async_parse_field(
                parser=video_url_selector,
                target_obj=body,
                logger=self.lg,)

        return body, video_url

    async def _get_df_article_html(self, article_url) -> tuple:
        """
        获取东方新闻的html
        :param article_url:
        :return:
        """
        headers = await self._get_phone_headers()
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

    async def _get_kd_article_html(self, article_url):
        """
        获取qq看点的html
        :param article_url:
        :return:
        """
        headers = await self._get_random_pc_headers()
        headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'authority': 'post.mp.qq.com',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'If-Modified-Since': 'Wed, 15 May 2019 10:17:11 GMT',
        })
        # self.lg.info(article_url)

        if '/kan/video' in article_url:
            self.lg.info('此链接为视频链接')
            body = await self._get_html_by_driver(
                url=article_url,
                load_images=True,)

            # TODO 用firefox可获得
            # url = 'http://post.mp.qq.com/kan/video/200553568-3955cc7c7ca772bk-m0866r0q1xn.html?_wv=2281701505&sig=b6e3ce15444e66d4fa4d6b40814b6858&time=1557141250&iid=MTY3MTk0MzU2Mw=='
            # d = BaseDriver(
            #     type=FIREFOX,
            #     executable_path=FIREFOX_DRIVER_PATH,
            #     load_images=False,
            #     headless=False,
            #     ip_pool_type=tri_ip_pool, )
            # body = d.get_url_body(url=url, timeout=25)
            # print(body)

        else:
            body = await unblock_request(
                url=article_url,
                headers=headers,
                ip_pool_type=self.ip_pool_type,
                logger=self.lg,
                num_retries=3,)
        # self.lg.info(body)
        assert body != '', '获取到的kd的body为空值!'

        return body, ''

    async def _get_kb_article_html(self, article_url):
        """
        获取天天快报的html
        :param article_url:
        :return:
        """
        async def get_special_case_api_data() -> dict:
            """
            二类情况接口数据获取
            :return:
            """
            nonlocal parse_obj
            # # todo 有两种情况, 一种是文章, 一种是视频
            _id = await async_parse_field(
                parser=parse_obj['article_id2'],
                target_obj=article_url,
                logger=self.lg,
                is_print_error=True, )
            self.lg.info('_id: {}'.format(_id))
            params = (
                ('id', str(_id)),  # eg: '20190721A0JCZT00'
                ('openid', ''),
                # ('ukey', 'ukey_155817081468585658'),
                ('style', 'json'),
            )
            body = await unblock_request(
                url='https://kuaibao.qq.com/getSubNewsContent',
                headers=headers,
                params=params,
                ip_pool_type=self.ip_pool_type,
                logger=self.lg,
                # 只进行2次请求, 避免时间过长无法执行下步请求
                num_retries=3,)
            # self.lg.info(body)
            data = json_2_dict(
                json_str=body,
                default_res={},
                logger=self.lg,)
            # pprint(data)
            assert data != {}, 'data 不管是视频或者文章都不为空值!'

            return data

        video_url = ''
        headers = await self._get_phone_headers()
        headers.update({
            'authority': 'kuaibao.qq.com',
        })
        body = await unblock_request(
            url=article_url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg,)
        # self.lg.info(body)
        assert body != '', '获取到的kb的body为空值!'
        parse_obj = await self._get_parse_obj(article_url_type='kb')
        article_title = await async_parse_field(
            parser=parse_obj['title'],
            target_obj=body,
            logger=self.lg,)
        if article_title == '':
            self.hook_target_api_data = await get_special_case_api_data()
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
                # 点击播放按钮
                exec_code = '''
                self.driver.find_element_by_css_selector('div.play-btn').click() 
                sleep(2)
                '''
                body = await self._get_html_by_driver(
                    url=article_url,
                    _type=FIREFOX,
                    load_images=True,
                    headless=True,
                    css_selector='div#mainVideo video',     # 必须等待这个显示后再关闭, 否则无video_url
                    exec_code=exec_code,
                    user_agent_type=PHONE,
                    timeout=25,)
                # self.lg.info(body)
                # TODO 有多种视频类型格式, 先处理这种
                video_url_sel = {
                    'method': 'css',
                    'selector': 'div#mainVideo video:nth-child(1) ::attr("src")',
                }
                video_url = await async_parse_field(
                    parser=video_url_sel,
                    target_obj=body,
                    logger=self.lg,)

                self.lg.info('video_url: {}'.format(video_url))

            else:
                self.lg.info('此文章为二类图文文章!')

        else:
            pass

        return body, video_url

    async def _wash_wx_article_body(self, body) -> tuple:
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
            # videos_url_list = re.compile('<div class=\"tvp_video\"><video.*?src=\"(.*?)\"></video><div class=\"tvp_shadow\">').findall(body)
            videos_url_list = re.compile('<iframe class=\"video_iframe.*?\" .*? src=\"(.*?)\"></iframe>').findall(body)
            assert videos_url_list != []
            self.lg.info('视频list: {}'.format(videos_url_list))
            self.lg.info('此文章含视频! 正在重新获取文章html...')

            tmp_body = await self._get_html_by_driver(
                url=videos_url_list[0],
                load_images=True,)
            # self.lg.info(tmp_body)
            assert tmp_body != '', 'tmp_body为空值!'
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

    async def _get_parse_obj(self, article_url_type) -> dict:
        """
        获取到对应解析对象
        :return:
        """
        for item in ARTICLE_ITEM_LIST:
            if article_url_type == item.get('short_name', ''):
                if item.get('obj_origin', '') == \
                        self.obj_origin_dict[article_url_type].get('obj_origin'):
                    parse_obj = item

                    return parse_obj

        raise NotImplementedError('未找到解析对象!')

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
            fav_num = self.hook_target_api_data['count_like']

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
        profile = await async_parse_field(
            parser=parse_obj['profile'],
            target_obj=target_obj,
            logger=self.lg)

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
            'hx',
            'hqx',
            'lsp',
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

        if article_url_type == 'wx'\
                or article_url_type == 'sg':
            return get_uuid1()

        article_id_selector = await self._get_article_id_selector(
            article_url_type=article_url_type,
            article_url=article_url,)
        share_id = await async_parse_field(
            parser=article_id_selector,
            target_obj=article_url,
            logger=self.lg)

        if short_name == 'kb':
            if share_id == '':
                share_id = await async_parse_field(
                    parser=parse_obj['article_id2'],
                    target_obj=article_url,
                    logger=self.lg)
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

    async def _get_tags_list(self, parse_obj, target_obj) -> list:
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

        tags_list = await async_parse_field(
            parser=parse_obj['tags_list'],
            target_obj=target_obj,
            is_first=is_first,
            logger=self.lg)
        if tags_list == '':
            return []

        if parse_obj.get('obj_origin', '') \
                == self.obj_origin_dict['kd'].get('obj_origin'):
            tags_list = tags_list.split(',')

        short_name_list = [
            'tt',
            'js',
            'kd',
            'if',
            'ss',
            'lsp',
        ]
        if short_name in short_name_list:
            tags_list = [{
                'keyword': i,
            } for i in tags_list]

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

        create_time = await async_parse_field(
            parser=create_time_selector,
            target_obj=target_obj,
            logger=self.lg)

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
        ]
        if short_name == 'sg':
            if video_url != '':
                # 原先为05-05 11:13, 替换为标准的
                create_time = str(get_shanghai_time())[:4] + '-' + create_time \
                    if create_time != '' else ''
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

        elif short_name == 'nfzm':
            create_time = await parse_create_time(
                short_name=short_name,
                create_time=self.hook_target_api_data['content']['publish_time'])

        elif short_name == 'ck':
            create_time = str(timestamp_to_regulartime(int(self.hook_target_api_data['publish_time'])))

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
            'cn',
            'if',
            'ss',
            'jm',
            'pp',
            'hx',
            'hqx',
            'xg',
            'lsp',
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
        # TODO 先不处理QQ看点的视频
        # if content == '' \
        #         and parse_obj.get('short_name', '') == 'kd':
        #     # 单独处理QQ看点含视频的content
        #     html = await self._get_html_by_driver(url=article_url, load_images=True)
        #     print(html)

        short_name_list3 = [
            'hx',
            'hqx',
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
                else:
                    pass

        elif short_name == 'nfzm':
            content = self.hook_target_api_data['content']['fulltext']

        elif short_name == 'ck':
            content = self.hook_target_api_data['content']

        elif short_name == 'amz':
            # 不管content是否为空, 都进入
            video_iframe = await self._get_amz_video_iframe(
                parse_obj=parse_obj,
                target_obj=target_obj,)
            self.lg.info('video_iframe: {}'.format(video_iframe))
            # 视频iframe在前面
            content = video_iframe + content

        else:
            pass

        short_name_list2 = [
            'df',
            'sg',
            'bd',
            'kb',
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
        # hook 防盗链
        content = '<meta name=\"referrer\" content=\"never\">' + content if content != '' else ''

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

        else:
            pass

        return content

    @staticmethod
    async def _wash_mp_article_content(content) -> str:
        """
        清洗mp content
        :param content:
        :return:
        """
        return content

    @staticmethod
    async def _wash_amz_article_content(content) -> str:
        """
        清洗amz content
        :param content:
        :return:
        """
        # firefox上正常显示, chrome变形, 后台可以改下iframe的属性, 使其自适应
        return content

    @staticmethod
    async def _wash_lsp_article_content(content) -> str:
        """
        清洗lsp content
        :param content:
        :return:
        """
        return content

    @staticmethod
    async def _wash_ck_article_content(content) -> str:
        """
        清洗ck 的content
        :param content:
        :return:
        """
        return content

    @staticmethod
    async def _wash_hqx_article_content(content) -> str:
        """
        清洗hqx content
        :param content:
        :return:
        """
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
        """
        清洗nfzm content
        :param content:
        :return:
        """
        content = re.compile('\n').sub('', content)

        content = modify_body_img_centering(content=content)
        content = modify_body_p_typesetting(content=content)

        return content

    @staticmethod
    async def _wash_hx_article_content(content) -> str:
        """
        清洗hx content
        :param content:
        :return:
        """
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
        """
        清洗pp content
        :param content:
        :return:
        """
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
        """
        清洗jm content
        :param content:
        :return:
        """
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
        """
        清洗ss content
        :param content:
        :return:
        """
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
        """
        清洗if content
        :param content:
        :return:
        """
        # 避免a标签调转
        content = re.compile('<a href=\".*?\">').sub('<a href=\"\">', content)
        content = modify_body_img_centering(content=content)
        content = modify_body_p_typesetting(content=content)

        return content

    @staticmethod
    async def _wash_cn_article_content(content) -> str:
        """
        清洗cn content
        :param content:
        :return:
        """
        content = re.compile('<mip-img').sub('<img', content)
        content = re.compile('</mip-img>').sub('</img>', content)
        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_ys_article_content(content) -> str:
        """
        清洗ys content
        :param content:
        :return:
        """
        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_fh_article_content(content) -> str:
        """
        清洗fh content
        :param content:
        :return:
        """
        content = re.compile('凤凰网汽车讯').sub('', content)
        # TODO chrome 显示content时会带上手机默认客户端的css样式, 导致显示异常, 用firefox查看是正常的!!
        content = modify_body_img_centering(content=content)
        content = modify_body_p_typesetting(content=content)

        return content

    @staticmethod
    async def _wash_zq_article_content(content) -> str:
        """
        清洗zq content
        :param content:
        :return:
        """
        content = re.compile('<img data-src=').sub('<img src=', content)
        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_bd_article_content(content) -> str:
        """
        清洗bd content
        :param content:
        :return:
        """
        # TODO firefox正常显示, 但是chrome无图, 原因图片地址无响应!
        # 顶部空白替换
        content = re.compile('<div style=\"padding-top:\d+\.\d+%\">').sub('<div>', content)
        content = re.compile('<div style=\"padding-top:\d+%\">').sub('<div>', content)
        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_sg_article_content(content) -> str:
        """
        清洗sg的content
        :param content:
        :return:
        """
        content = modify_body_img_centering(content=content)

        return content

    @staticmethod
    async def _wash_df_article_content(content) -> str:
        """
        清洗df的content
        :param content:
        :return:
        """
        content = re.compile('<p class=\"section txt\">对此你怎么看，欢迎大家在评论区留言！</p>').sub('', content)

        return content

    @staticmethod
    async def _wash_wx_article_content(content) -> str:
        """
        清洗wx content
        :param content:
        :return:
        """
        content = re.compile('<p><br></p>').sub('<br>', content)

        return content

    @staticmethod
    async def _wash_kd_article_content(content) -> str:
        """
        清洗QQ看点content
        :param content:
        :return:
        """
        # 处理图片
        content = re.compile('<svg .*?>.*?</svg>').sub('', content)
        # 替换掉img 标签中src为svg的
        _ = re.compile(' src=\"data:image/svg\+xml;.*?\" ')
        # pprint(_.findall(content))
        content = _.sub(' ', content)
        content = re.compile(' data-src=').sub(' src=', content)
        content = re.compile('data-lazy=\"\d+\"').sub('style=\"height:auto;width:100%;\"', content)
        content = re.compile('<a class=\"jubao\"><i></i>举报内容</a>').sub('', content)

        # 给与原装的css
        content = '<link rel="stylesheet" href="//mp.gtimg.cn/themes/default/client/article/article.css?_bid=2321&v=2017082501">' + \
            content

        return content

    @staticmethod
    async def _wash_kb_article_content(content) -> str:
        """
        清洗kb content
        :param content:
        :return:
        """
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

    @staticmethod
    async def _get_random_pc_headers():
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    @staticmethod
    async def _get_random_phone_headers():
        return {
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_phone_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

    async def _get_phone_headers(self):
        return {
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_phone_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
    
    def __del__(self):
        try:
            del self.lg
            del self.user_agent_type
            del self.ip_pool_type
            del self.request_num_retries
            del self.hook_target_api_data
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
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1545195601&ver=1283&signature=0wD3ij5dP9cs5hAXeHqb12I6CgxVu8HmadJhszmKuGI-PSMqcIoYd66qvE4Mg5ejrxCxWTgDC-s1xMaKviWC4Noe9GjwKzZpFCXLyRt6IkTne1YF4Yc8qmDvBVgb3w5c&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1557019801&ver=1587&signature=7nrWhsLUvCvON5P2eyyDS9--DnPJegyCz94JSJiSxIlt4i4X4p*r-CRx13dyqa0OWH7ZOM2WESEdS4nvSNV6UwuPKrdz1xFN8aJztHuRlRV59EIflvbd8jxBnduHRajo&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1557019801&ver=1587&signature=kf9hmcbFbQtaBCqoj6pCgVNA6CjurCbsTBTA5g4ZesH2I5hMGp*HKdwqLrxJvQL5X-AELkcj5V*ukSgC8kQlWtS8-ELZuwmezs*H8OHLc4dSy0wWfr3s*Th8dMQYoIBm&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1557111601&ver=1589&signature=ALBo1FMtv3X*yJa8CzViSYK*FV-Cr7rHblhsr-96NCZDD5jK8ra2daIg2QWCSVnnqJ4H4KJG*n820P0PULQ6PIQblWXUf*7R69P8ObOCR7UJmpRlKU8s2FgRFiUMrR7N&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1563850802&ver=1745&signature=3-AY5oIX1fgkA7pyqxT2rcYtdtBH*8zx0AmORHLICAIH5GaAl6K6omx5qrLStNbXXLoMGm7i9O8KFuJdA4hRjN4yFadybiTCiT13AKSipinfc5IvHbGS5xraz3qvduhe&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1563850802&ver=1745&signature=3-AY5oIX1fgkA7pyqxT2rcYtdtBH*8zx0AmORHLICAJWtC2d6WpK9-7eXo8niLCVfbsKlVmU1gvrp1eoRxXK-TCKkqDRLlgytD-w2Lq-SmsjWqXRbHZxWqrqOPE9D6il&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1564034408&ver=1749&signature=k7JY7Vn53aacavzffafWSHvLQDRhHPebhFWU*BiYdgYi8ycBZOIRoYyevdlFNp0Sli1O17jyEV3citlGNDPhUrMnMIdOsoKtPbGcnsSxs-vZVfd2Jl6w*7MHDkdgFDDD&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1564034408&ver=1749&signature=pgKGltfxEKGAtEOOIvBeugmKyND1YusPHnj4sw6EeOXRQlUIP5ylyZcv4egYs8PLyKXx5EpKZlHEIt6YOBAA9zl0tDR4Z4jWQb859xvPFmMXKbYTVmh1W73js0eaCKCX&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1564034409&ver=1749&signature=Pyxx187vCIJeDbnqZSehHm3XDpGkY*eXx9LO-Zrf6tCWOmxo2RnKk9C9iA*LvScDq3D0Wm2cTdA4nKNDm-UUem71qzZdZoNqNvT1J5WJrkG1KCFQVK4pO4F7oxKC8Hxw&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1564036201&ver=1749&signature=XCTMLVFytVL3FzjyURHVRICZb2bM1kLWhSpUrNeb8SGD1jvxgHkJgicFiMNBOl6W0Ow6m*Gzke*tlPVCzOJTcDx4WYv2FyOsY1FtMzB-pHIOErSsuq4H3T-yUeyMq9vg&new=1'
    # 含视频
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1563850802&ver=1745&signature=kF7BFCtTqr9OlfBzqLSgUfnD413Ig9JfMVKCc1ew8YQ8maPdhL8zFXgrctDdl5Z3HfI0ZOb7yThhKR1QHrtuUjVQE*gTTPBvBOTagAA5wN*bylpMTtwBqwv7ctFh-j5P&new=1'

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
    # url = 'https://www.jianshu.com/p/7160ad815557'
    # url = 'https://www.jianshu.com/p/1a60bdc3098b'
    # url = 'https://www.jianshu.com/p/cfca1ba1e44c'
    # url = 'https://www.jianshu.com/p/2876ca9e3ae7'
    # url = 'https://www.jianshu.com/p/9ba3eb7bc524'

    # QQ看点
    # url = 'https://post.mp.qq.com/kan/article/2184322959-232584629.html?_wv=2147483777&sig=24532a42429f095b9487a2754e6c6f95&article_id=232584629&time=1542933534&_pflag=1&x5PreFetch=1&web_ch_id=0&s_id=gnelfa_3uh3g5&share_source=0'
    # 含视频
    # url = 'http://post.mp.qq.com/kan/video/201271541-2525bea9bc8295ah-x07913jkmml.html?_wv=2281701505&sig=50b27393b64a188ffe7f646092dbb04f&time=1542102407&iid=Mjc3Mzg2MDk1OQ==&sourcefrom=0'
    # url = 'http://post.mp.qq.com/kan/video/200553568-3955cc7c7ca772bk-m0866r0q1xn.html?_wv=2281701505&sig=b6e3ce15444e66d4fa4d6b40814b6858&time=1557141250&iid=MTY3MTk0MzU2Mw=='

    # 天天快报
    # url = 'https://kuaibao.qq.com/s/NEW2018120200710400?refer=kb_news&titleFlag=2&omgid=78610c582f61e3b1f414134f9d4fa0ce'
    # url = 'https://kuaibao.qq.com/s/20181201A0VJE800?refer=kb_news&titleFlag=2&omgid=78610c582f61e3b1f414134f9d4fa0ce'
    # url = 'https://kuaibao.qq.com/s/20190515A06XAW00?refer=kb_news&coral_uin=ec30afdb64e74038ca7991e4e282153af308670081f17d0ee4fc3e473b0b5dda2f&omgid=22c4ac23307a6a33267184cafd2df8b6&chlid=news_news_top&atype=0&from=groupmessage&isappinstalled=0'
    # 第二类图文文章
    # url = 'https://kuaibao.qq.com/s/20190710AZOJ0B00?from=groupmessage&isappinstalled=0'
    # 第三类图文文章(跟第二类是同一接口但是字段不同)
    # url = 'https://kuaibao.qq.com/s/20190708A0INL100?refer=kb_news&amp;coral_uin=ec30afdb64e74038ca7991e4e282153af308670081f17d0ee4fc3e473b0b5dda2f&amp;omgid=22c4ac23307a6a33267184cafd2df8b6&amp;chlid=daily_timeline&amp;atype=0&from=groupmessage&isappinstalled=0'
    # url = 'https://kuaibao.qq.com/s/20190721A0JCZT00?refer=kb_news&amp;coral_uin=ec30afdb64e74038ca7991e4e282153af308670081f17d0ee4fc3e473b0b5dda2f&amp;omgid=22c4ac23307a6a33267184cafd2df8b6&amp;chlid=daily_timeline&amp;atype=0&from=groupmessage&isappinstalled=0'
    # url = 'https://kuaibao.qq.com/s/20190723A0IRBX00?refer=kb_news&amp;titleFlag=2&amp;coral_uin=ec30afdb64e74038ca7991e4e282153af308670081f17d0ee4fc3e473b0b5dda2f&amp;omgid=22c4ac23307a6a33267184cafd2df8b6&from=groupmessage&isappinstalled=0'
    # TODO 含视频(先不处理, 本地可以，但是server无法请求到body)
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
    # 汽车
    # url = 'https://auto.ifeng.com/c/7nE86ZB9Y3s'
    # url = 'https://auto.ifeng.com/c/7nEFmnQAbiK'
    # TODO 房产未实现, 页面结构完全不同
    # 科技
    # url = 'https://tech.ifeng.com/c/7nAhlwq9hFW'
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

    # 南方周末(其中只有部分文章可用, 不推荐使用)
    # url = 'http://www.infzm.com/wap/#/content/153845'
    # url = 'http://www.infzm.com/wap/#/content/153862'
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
    url = 'https://www.meipai.com/media/1131644923'
    # todo 直播不采集

    print('article_url: {}'.format(url))
    article_parse_res = loop.run_until_complete(
        future=_._parse_article(article_url=url))
    pprint(article_parse_res)
    # print(dumps(article_parse_res))

if __name__ == '__main__':
    main()