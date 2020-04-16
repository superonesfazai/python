# coding:utf-8

'''
@author = super_fazai
@File    : recommend_good_ops.py
@connect : superonesfazai@gmail.com
'''

from sys import path as sys_path
sys_path.append('..')

from settings import (
    IP_POOL_TYPE,
    MY_SPIDER_LOGS_PATH,
    CHROME_DRIVER_PATH,
    FIREFOX_DRIVER_PATH,
)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from my_exceptions import (
    SqlServerConnectionException,
    ArticleTitleOverLongException,
    LoginFailException,
    ArticleTitleContainSensitiveWordsException,
    PublishOneArticleFailException,
    EnterTargetPageFailException,
)
from multiplex_code import (
    get_new_sql_cli,
    ARTICLE_TITLE_SENSITIVE_STR_TUPLE,
)
from article_spider import ArticleParser

import nest_asyncio
from random import randint
from random import sample as random_sample
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import TimeoutException as SeleniumTimeoutException

from fzutils.data.str_utils import target_str_contain_some_char_check
from fzutils.spider.fz_driver import (
    BaseDriver,
    CHROME,
    FIREFOX,
)
from fzutils.time_utils import TimeoutError as FZTimeoutError
from fzutils.spider.selenium_always import *
from fzutils.spider.async_always import *

nest_asyncio.apply()

class RecommendGoodOps(AsyncCrawler):
    """荐好ops"""
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            log_print=True,
            is_new_loop=False,
            log_save_path=MY_SPIDER_LOGS_PATH + '/荐好/ops/',
            ip_pool_type=IP_POOL_TYPE,
        )
        self.request_num_retries = 6
        self.article_type = 'zq'
        self.yx_username = input('请输入yx_username:')
        self.yx_password = input('请输入yx_password:')
        self.lg.info('yx_username: {}, yx_password: {}'.format(
            self.yx_username,
            self.yx_password))
        # 不支持https了, 原先支持
        self.publish_url = 'http://configadmin.yiuxiu.com/Business/Index'
        self.select_sql0 = 'SELECT unique_id FROM dbo.recommend_good_ops_article_id_duplicate_removal'
        self.insert_sql0 = 'INSERT INTO dbo.recommend_good_ops_article_id_duplicate_removal(unique_id, create_time) values(%s, %s)'
        self.min_article_id = 0
        self.max_article_id = 0
        self.driver_headless = True
        # 必须使用代理, yx限制ip频繁
        self.driver_use_proxy = True
        # 荐好管理label
        self.recommend_good_label_css_selector = 'span.nav-label'
        # 设置开眼的min_article_id, max_article_id
        self.ky_min_article_id, self.ky_max_article_id = 4000, 60000
        # article_id 截取数
        self.zq_intercept_num = 1
        self.hk_intercept_num = 1
        self.lfd_intercept_num = 1
        self.gxg_intercept_num = 1
        self.pp_intercept_num = 2
        self.kr_intercept_num = 1
        self.dfsp_intercept_num = 1
        self.jrxsp_intercept_num = 1
        self.ky_intercept_num = 1
        self.jhrx_intercept_num = 1
        # 增加全屏视频数
        self.lsp_intercept_num = 2
        self.mp_intercept_num = 1
        self.klm_intercept_num = 2
        self.jhgzw_intercept_num = 1
        self.article_parser = None
        # 暂存好看视频list的dict
        self.hk_cache_dict = {}
        self.lfd_cache_dict = {}
        self.gxg_cache_dict = {}
        self.pp_cache_dict = {}
        self.kr_cache_dict = {}
        self.dfsp_cache_dict = {}
        self.lsp_cache_dict = {}
        self.mp_cache_dict = {}
        self.klm_cache_dict = {}
        self.jrxsp_cache_dict = {}
        self.jhgzw_cache_dict = {}
        self.jhrx_cache_dict = {}
        # 隔多久更新一次列表数据, 单位秒
        self.wait_to_update_time0 = 60 * 60
        self.wait_to_update_time1 = 40 * 60

    async def _fck_run(self):
        # 休眠7.5分钟, 避免频繁发!(5分钟还是太快, 删不过来)(增加较多视频, 失败率较高故还是5分钟)
        # sleep_time = 0.
        sleep_time = 60 * 2.
        self.db_article_id_list = await self.get_db_unique_id_list()
        assert self.db_article_id_list != []
        self.lg.info('db_article_id_list_len: {}'.format(len(self.db_article_id_list)))

        _timeout = await self.get_auto_publish_articles_timeout()
        while True:
            if get_shanghai_time().hour == 0:
                # 夜晚休眠
                await async_sleep(60 * 60 * 4.)
            else:
                pass
            try:
                try:
                    await async_wait_for(
                        self.auto_publish_articles(),
                        timeout=_timeout,)
                except AsyncTimeoutError:
                    raise PublishOneArticleFailException

            except (
                    ArticleTitleOverLongException,
                    LoginFailException,
                    ArticleTitleContainSensitiveWordsException,
                    PublishOneArticleFailException,
                    EnterTargetPageFailException,):
                self.lg.error('遇到错误:', exc_info=True)
                continue

            except Exception:
                self.lg.error('遇到错误:', exc_info=True)

            self.lg.info('休眠{}s...'.format(sleep_time))
            await async_sleep(sleep_time)

    async def get_auto_publish_articles_timeout(self):
        """
        获取自动发布文章的超时时长
        :return:
        """
        all_intercept_num = self.zq_intercept_num \
                            + self.hk_intercept_num \
                            + self.lfd_intercept_num \
                            + self.gxg_intercept_num \
                            + self.pp_intercept_num \
                            + self.kr_intercept_num \
                            + self.dfsp_intercept_num \
                            + self.lsp_intercept_num \
                            + self.mp_intercept_num \
                            + self.klm_intercept_num \
                            + self.jrxsp_intercept_num \
                            + self.ky_intercept_num \
                            + self.jhgzw_intercept_num \
                            + self.jhrx_intercept_num
        _timeout = all_intercept_num * 2.5 * 60

        return _timeout

    async def get_db_unique_id_list(self) -> list:
        """
        获取db的unique_id_list
        :return:
        """
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        if not self.sql_cli.is_connect_success:
            raise SqlServerConnectionException

        res = []
        try:
            res = self.sql_cli._select_table(
                sql_str=self.select_sql0,
                logger=self.lg,)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)

        res = [] if res is None else res

        return [item[0] for item in res]

    async def auto_publish_articles(self):
        """
        自动发布文章
        :return:
        """
        self.sql_cli = get_new_sql_cli(sql_cli=self.sql_cli)
        if not self.sql_cli.is_connect_success:
            raise SqlServerConnectionException
        else:
            pass

        if self.min_article_id == 0\
            or self.max_article_id == 0:
            self.article_parser = ArticleParser(logger=self.lg)
            article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                article_type=self.article_type,))
            assert article_list != []

            self.min_article_id, self.max_article_id = self.get_latest_max_and_min_artcile_id_from_article_list(
                article_list=article_list,)
            self.lg.info('最新的min_article_id: {}, max_article_id: {}'.format(
                self.min_article_id,
                self.max_article_id,))
        else:
            pass

        # todo shadow模式下老是登录失败, 建议关闭shadow, 不使用其 or lantern or 使用shadow其全局代理模式即可

        # 创建目标集合
        # zq_article_list = []
        # hk_article_list = []
        # lfd_article_list = []
        # gxg_article_list = []
        # pp_article_list = []
        # kr_article_list = []
        # dfsp_article_list = []
        # lsp_article_list = []
        # mp_article_list = []
        # klm_article_list = []
        # jrxsp_article_list = []
        # ky_article_list = []
        # jhgzw_article_list = []
        zq_article_list = self.get_zq_own_create_article_id_list(
            min_article_id=self.min_article_id,
            max_article_id=self.max_article_id,)
        hk_article_list = self.get_hk_article_id_list()
        lfd_article_list = self.get_lfd_article_id_list()
        gxg_article_list = self.get_gxg_article_id_list()
        pp_article_list = self.get_pp_article_id_list()
        kr_article_list = self.get_kr_article_id_list()
        dfsp_article_list = self.get_dfsp_article_id_list()
        lsp_article_list = self.get_lsp_article_id_list()
        mp_article_list = self.get_mp_article_id_list()
        klm_article_list = self.get_klm_article_id_list()
        jrxsp_article_list = self.get_jrxsp_article_id_list()
        ky_article_list = self.get_ky_own_create_article_id_list()
        jhgzw_article_list = self.get_jhgzw_own_create_article_id_list()
        jhrx_article_list = self.get_jhrx_own_create_article_id_list()

        # 测试用
        # article_id = '17300123'
        # article_list = [{
        #     'uid': get_uuid3(target_str='{}::{}'.format('zq', article_id)),
        #     'article_type': 'zq',
        #     'article_id': article_id,
        #     'title': '未知',
        #     'article_url': 'https://focus.youth.cn/mobile/detail/id/{}#'.format(article_id),
        # }]

        # 文章在前的发布顺序, 视频在后(避免视频发过多)
        # 本地新闻先放前面
        article_list = jhrx_article_list \
                       + jhgzw_article_list \
                       + zq_article_list \
                       + pp_article_list \
                       + kr_article_list \
                       + dfsp_article_list \
                       + hk_article_list \
                       + klm_article_list \
                       + jrxsp_article_list \
                       + mp_article_list \
                       + lsp_article_list \
                       + ky_article_list \
                       + lfd_article_list \
                       + gxg_article_list

        assert article_list != []
        # pprint(article_list)

        target_article_list = self.get_target_article_list(article_list=article_list)
        if target_article_list == []:
            self.lg.info('待发布的target_article_list为空list, pass!')
            return

        driver = None
        try:
            try:
                # rasp上代理模式启动chromedriver具有一定的失败率, 故还是mac
                driver = BaseDriver(
                    type=CHROME,
                    executable_path=CHROME_DRIVER_PATH,
                    # 本地老是出错
                    # type=FIREFOX,
                    # executable_path=FIREFOX_DRIVER_PATH,
                    load_images=True,
                    logger=self.lg,
                    headless=self.driver_headless,
                    driver_use_proxy=self.driver_use_proxy,
                    ip_pool_type=self.ip_pool_type, )
                self.login_bg(driver=driver)
                self.get_into_recommend_good_manage(driver=driver)
            except (FZTimeoutError, WebDriverException):
                raise LoginFailException

            for item in target_article_list:
                uid = item.get('uid', '')
                title = item.get('title', '')
                article_url = item.get('article_url', '')
                self.lg.info('正在发布文章 title: {}, article_url: {} ...'.format(title, article_url))
                try:
                    self.publish_one_article(
                        driver=driver,
                        article_url=article_url,)
                except FZTimeoutError:
                    raise PublishOneArticleFailException

                # 新增, 以及插入db
                self.db_article_id_list.append(uid)
                self.sql_cli._insert_into_table_2(
                    sql_str=self.insert_sql0,
                    params=(
                        uid,
                        get_shanghai_time(),
                    ),
                    logger=self.lg,)
        except (
                ArticleTitleOverLongException,
                LoginFailException,
                ArticleTitleContainSensitiveWordsException,
                PublishOneArticleFailException,
                EnterTargetPageFailException,) as e:
            # 抛出异常
            raise e
        except Exception:
            try:
                self.lg.error('遇到错误:', exc_info=True)
            except Exception as e:
                print(e)

        finally:
            try:
                # ** 注意: 不可直接del driver, 测试发现浏览器未被正确关闭, 还存在!!
                # del driver
                # 关闭浏览器
                driver.driver.quit()
                # 只关闭当前窗口, 不关闭浏览器
                # driver.driver.close()
                self.lg.info('driver 释放成功!')
            except:
                try:
                    driver.driver.quit()
                except:
                    pass
            collect()

        return

    def get_jhrx_own_create_article_id_list(self):
        """
        获取jhrx article_list
        :return:
        """
        if not isinstance(self.article_parser, ArticleParser):
            self.article_parser = ArticleParser(logger=self.lg)
        else:
            pass

        if self.jhrx_cache_dict == {}:
            # 首次启动
            article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                article_type='jhrx',))
            self.jhrx_cache_dict['data'] = article_list
            self.jhrx_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
        else:
            cache_time = self.jhrx_cache_dict['cache_time']
            if datetime_to_timestamp(get_shanghai_time()) - cache_time > self.wait_to_update_time0:
                # jhrx 每日更新数量有限, 每过40分钟重新获取一次
                article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                    article_type='jhrx',))
                self.jhrx_cache_dict['data'] = article_list
                self.jhrx_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
            else:
                article_list = self.jhrx_cache_dict['data']

        if article_list != []:
            # 截取1个(与图文穿插)
            article_list = random_sample(article_list, self.jhrx_intercept_num)

        return article_list

    def get_jhgzw_own_create_article_id_list(self):
        """
        获取jhgzw article_list
        :return:
        """
        if not isinstance(self.article_parser, ArticleParser):
            self.article_parser = ArticleParser(logger=self.lg)
        else:
            pass

        if self.jhgzw_cache_dict == {}:
            # 首次启动
            article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                article_type='jhgzw',))
            self.jhgzw_cache_dict['data'] = article_list
            self.jhgzw_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
        else:
            cache_time = self.jhgzw_cache_dict['cache_time']
            if datetime_to_timestamp(get_shanghai_time()) - cache_time > self.wait_to_update_time0:
                # jhgzw 每日更新数量有限, 每过40分钟重新获取一次
                article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                    article_type='jhgzw',))
                self.jhgzw_cache_dict['data'] = article_list
                self.jhgzw_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
            else:
                article_list = self.jhgzw_cache_dict['data']

        if article_list != []:
            # 截取1个(与图文穿插)
            article_list = random_sample(article_list, self.jhgzw_intercept_num)

        return article_list

    def get_ky_own_create_article_id_list(self):
        """
        获取ky article_list
        :return:
        """
        article_id_list = [str(article_id) for article_id in range(self.ky_min_article_id, self.ky_max_article_id)]

        # 截取
        article_id_list = random_sample(article_id_list, self.ky_intercept_num)
        res = [{
            'uid': get_uuid3(target_str='{}::{}'.format('ky', article_id)),
            'article_type': 'ky',
            'title': '未知',
            'article_id': article_id,
            'article_url': 'https://www.kaiyanapp.com/detail.html?vid={}'.format(article_id),
        } for article_id in article_id_list]

        return res

    def get_jrxsp_article_id_list(self):
        """
        获取目标article_list
        :return:
        """
        if not isinstance(self.article_parser, ArticleParser):
            self.article_parser = ArticleParser(logger=self.lg)
        else:
            pass

        if self.jrxsp_cache_dict == {}:
            # 首次启动
            article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                article_type='jrxsp',))
            self.jrxsp_cache_dict['data'] = article_list
            self.jrxsp_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
        else:
            cache_time = self.jrxsp_cache_dict['cache_time']
            if datetime_to_timestamp(get_shanghai_time()) - cache_time > self.wait_to_update_time0:
                # klm 每日更新数量有限, 每过40分钟重新获取一次
                article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                    article_type='jrxsp',))
                self.jrxsp_cache_dict['data'] = article_list
                self.jrxsp_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
            else:
                article_list = self.jrxsp_cache_dict['data']

        if article_list != []:
            # 截取1个(与图文穿插)
            article_list = random_sample(article_list, self.jrxsp_intercept_num)

        return article_list

    def get_klm_article_id_list(self):
        """
        获取目标article_id_list
        :return:
        """
        if not isinstance(self.article_parser, ArticleParser):
            self.article_parser = ArticleParser(logger=self.lg)
        else:
            pass

        if self.klm_cache_dict == {}:
            # 首次启动
            article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                article_type='klm',))
            self.klm_cache_dict['data'] = article_list
            self.klm_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
        else:
            cache_time = self.klm_cache_dict['cache_time']
            if datetime_to_timestamp(get_shanghai_time()) - cache_time > self.wait_to_update_time0:
                # klm 每日更新数量有限, 每过30分钟重新获取一次
                article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                    article_type='klm',))
                self.klm_cache_dict['data'] = article_list
                self.klm_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
            else:
                article_list = self.klm_cache_dict['data']

        if article_list != []:
            # 截取1个(与图文穿插)
            article_list = random_sample(article_list, self.klm_intercept_num)

        return article_list

    def get_mp_article_id_list(self):
        """
        获取mp 目标article_id_list
        :return:
        """
        if not isinstance(self.article_parser, ArticleParser):
            self.article_parser = ArticleParser(logger=self.lg)
        else:
            pass

        if self.mp_cache_dict == {}:
            # 首次启动
            article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                article_type='mp',))
            self.mp_cache_dict['data'] = article_list
            self.mp_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
        else:
            cache_time = self.mp_cache_dict['cache_time']
            if datetime_to_timestamp(get_shanghai_time()) - cache_time > self.wait_to_update_time0:
                # mp 每日更新数量有限, 每过30分钟重新获取一次
                article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                    article_type='mp',))
                self.mp_cache_dict['data'] = article_list
                self.mp_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
            else:
                article_list = self.mp_cache_dict['data']

        if article_list != []:
            # 截取1个(与图文穿插)
            article_list = random_sample(article_list, self.mp_intercept_num)

        return article_list

    def get_lsp_article_id_list(self):
        """
        获取lsp 目标article_id_list
        :return:
        """
        if not isinstance(self.article_parser, ArticleParser):
            self.article_parser = ArticleParser(logger=self.lg)
        else:
            pass

        if self.lsp_cache_dict == {}:
            # 首次启动
            article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                article_type='lsp',))
            self.lsp_cache_dict['data'] = article_list
            self.lsp_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
        else:
            cache_time = self.lsp_cache_dict['cache_time']
            if datetime_to_timestamp(get_shanghai_time()) - cache_time > self.wait_to_update_time0:
                # dfsp 每日更新数量有限, 每过30分钟重新获取一次
                article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                    article_type='lsp',))
                self.lsp_cache_dict['data'] = article_list
                self.lsp_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
            else:
                article_list = self.lsp_cache_dict['data']

        if article_list != []:
            # 截取1个(与图文穿插)
            article_list = random_sample(article_list, self.lsp_intercept_num)

        return article_list

    def get_dfsp_article_id_list(self):
        """
        获取dfsp 目标article_id_list
        :return:
        """
        if not isinstance(self.article_parser, ArticleParser):
            self.article_parser = ArticleParser(logger=self.lg)
        else:
            pass

        if self.dfsp_cache_dict == {}:
            # 首次启动
            article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                article_type='dfsp',))
            self.dfsp_cache_dict['data'] = article_list
            self.dfsp_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
        else:
            cache_time = self.dfsp_cache_dict['cache_time']
            if datetime_to_timestamp(get_shanghai_time()) - cache_time > self.wait_to_update_time0:
                # dfsp 每日更新数量有限, 每过30分钟重新获取一次
                article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                    article_type='dfsp',))
                self.dfsp_cache_dict['data'] = article_list
                self.dfsp_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
            else:
                article_list = self.dfsp_cache_dict['data']

        if article_list != []:
            # 截取1个(与图文穿插)
            article_list = random_sample(article_list, self.dfsp_intercept_num)

        return article_list

    def get_kr_article_id_list(self):
        """
        获取kr 目标article_id_list
        :return:
        """
        if not isinstance(self.article_parser, ArticleParser):
            self.article_parser = ArticleParser(logger=self.lg)
        else:
            pass

        if self.kr_cache_dict == {}:
            # 首次启动
            article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                article_type='kr',))
            self.kr_cache_dict['data'] = article_list
            self.kr_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
        else:
            cache_time = self.kr_cache_dict['cache_time']
            if datetime_to_timestamp(get_shanghai_time()) - cache_time > self.wait_to_update_time0:
                # pp 每日更新数量有限, 每过30分钟重新获取一次
                article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                    article_type='kr',))
                self.kr_cache_dict['data'] = article_list
                self.kr_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
            else:
                article_list = self.kr_cache_dict['data']

        if article_list != []:
            # 截取1个(与图文穿插)
            article_list = random_sample(article_list, self.kr_intercept_num)

        return article_list

    def get_pp_article_id_list(self):
        """
        获取pp目标article_id_list
        :return:
        """
        if not isinstance(self.article_parser, ArticleParser):
            self.article_parser = ArticleParser(logger=self.lg)
        else:
            pass

        if self.pp_cache_dict == {}:
            # 首次启动
            article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                article_type='pp',))
            self.pp_cache_dict['data'] = article_list
            self.pp_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
        else:
            cache_time = self.pp_cache_dict['cache_time']
            if datetime_to_timestamp(get_shanghai_time()) - cache_time > self.wait_to_update_time1:
                # pp 每日更新数量有限, 每过30分钟重新获取一次
                article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                    article_type='pp',))
                self.pp_cache_dict['data'] = article_list
                self.pp_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
            else:
                article_list = self.pp_cache_dict['data']

        if article_list != []:
            # 截取1个(与图文穿插)
            article_list = random_sample(article_list, self.pp_intercept_num)

        return article_list

    def get_gxg_article_id_list(self):
        """
        获取gxg目标article_id_list
        :return:
        """
        if not isinstance(self.article_parser, ArticleParser):
            self.article_parser = ArticleParser(logger=self.lg)
        else:
            pass

        if self.gxg_cache_dict == {}:
            # 首次启动
            article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                article_type='gxg',))
            self.gxg_cache_dict['data'] = article_list
            self.gxg_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
        else:
            cache_time = self.gxg_cache_dict['cache_time']
            if datetime_to_timestamp(get_shanghai_time()) - cache_time > self.wait_to_update_time0:
                # gxg 每日更新数量有限, 每过30分钟重新获取一次
                article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                    article_type='gxg',))
                self.gxg_cache_dict['data'] = article_list
                self.gxg_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
            else:
                article_list = self.gxg_cache_dict['data']

        if article_list != []:
            # 截取1个(与图文穿插)
            article_list = random_sample(article_list, self.gxg_intercept_num)

        return article_list

    def get_lfd_article_id_list(self):
        """
        获取lfd目标article_id_list
        :return:
        """
        if not isinstance(self.article_parser, ArticleParser):
            self.article_parser = ArticleParser(logger=self.lg)
        else:
            pass

        if self.lfd_cache_dict == {}:
            # 首次启动
            article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                article_type='lfd',))
            self.lfd_cache_dict['data'] = article_list
            self.lfd_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
        else:
            cache_time = self.lfd_cache_dict['cache_time']
            if datetime_to_timestamp(get_shanghai_time()) - cache_time > self.wait_to_update_time1:
                # lfd 每日更新数量有限, 每过30分钟重新获取一次
                article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                    article_type='lfd',))
                self.lfd_cache_dict['data'] = article_list
                self.lfd_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
            else:
                article_list = self.lfd_cache_dict['data']

        if article_list != []:
            # 截取1个(与图文穿插)
            article_list = random_sample(article_list, self.lfd_intercept_num)

        return article_list

    def get_hk_article_id_list(self):
        """
        获取hk 目标article_id_list
        :return:
        """
        if not isinstance(self.article_parser, ArticleParser):
            self.article_parser = ArticleParser(logger=self.lg)
        else:
            pass

        if self.hk_cache_dict == {}:
            # 首次启动
            article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                article_type='hk',))
            self.hk_cache_dict['data'] = article_list
            self.hk_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
        else:
            cache_time = self.hk_cache_dict['cache_time']
            if datetime_to_timestamp(get_shanghai_time()) - cache_time > self.wait_to_update_time0:
                # 每过12分钟重新获取一次
                article_list = self.loop.run_until_complete(self.article_parser.get_article_list_by_article_type(
                    article_type='hk',))
                self.hk_cache_dict['data'] = article_list
                self.hk_cache_dict['cache_time'] = datetime_to_timestamp(get_shanghai_time())
            else:
                article_list = self.hk_cache_dict['data']

        if article_list != []:
            # 截取1个(与图文穿插)
            article_list = random_sample(article_list, self.hk_intercept_num)

        return article_list

    def get_latest_max_and_min_artcile_id_from_article_list(self, article_list) -> tuple:
        """
        获取最新范围的article_id最大, 最小的article_id(目的动态的自己创建值)
        :return: (int, int)
        """
        latest_article_id_list = []
        for item in article_list:
            # eg: zq是'17296475'
            article_id = item.get('article_id', '')
            if len(article_id) >= 8:
                latest_article_id_list.append(int(article_id))
            else:
                continue

        assert latest_article_id_list != []
        latest_article_id_list = sorted(latest_article_id_list)
        # pprint(latest_article_id_list)

        return (latest_article_id_list[0], latest_article_id_list[-1])

    def get_zq_own_create_article_id_list(self, min_article_id: int, max_article_id: int):
        """
        自己create的article_id_list
        :return:
        """
        # 取中间值, 避免老是在发老新闻, 取更接近新的文章
        middle_article_id = int((min_article_id + max_article_id) / 2)
        middle_article_id = int((middle_article_id + max_article_id) / 2)
        middle_article_id = int((middle_article_id + max_article_id) / 2)
        self.lg.info('middle_article_id: {}'.format(middle_article_id))
        article_id_list = [str(article_id) for article_id in range(middle_article_id, max_article_id)]

        # 截取3
        article_id_list = random_sample(article_id_list, self.zq_intercept_num)
        res = [{
            'uid': get_uuid3(target_str='{}::{}'.format('zq', article_id)),
            'article_type': 'zq',
            'title': '未知',
            'article_id': article_id,
            'article_url': 'https://focus.youth.cn/mobile/detail/id/{}#'.format(article_id),
        } for article_id in article_id_list]

        new_res = res

        # 本地不检测了
        # article_parser = ArticleParser(logger=self.lg)
        # # article_list = self.loop.run_until_complete(article_parser.get_article_list_by_article_type(
        # #     article_type=self.article_type,))
        # new_res = []
        # for item in res:
        #     article_url = item.get('article_url', '')
        #     try:
        #         self.lg.info('本地检测url: {}'.format(article_url))
        #         _ = self.loop.run_until_complete(article_parser._parse_article(
        #             article_url=article_url,))
        #         title = _.get('title', '')
        #         assert title != ''
        #         # 标题必须小于等于30
        #         assert len(title) <= 30
        #     except Exception:
        #         continue
        #
        #     item.update({
        #         'title': title,
        #     })
        #     new_res.append(item)

        return new_res

    def get_target_article_list(self, article_list: list) -> list:
        """
        获取未被发布的item
        :return:
        """
        target_article_list = []
        for item in article_list:
            try:
                title = item.get('title', '')
                assert title != ''
                uid = item.get('uid', '')
                assert uid != ''
                article_url = item.get('article_url', '')
                assert article_url != ''
                if uid not in self.db_article_id_list:
                    target_article_list.append(item)
                else:
                    # 已发布的跳过
                    self.lg.info('该文章之前已被发布![where title: {}, url: {}]'.format(title, article_url))
                    continue
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                continue

        return target_article_list

    @fz_set_timeout(seconds=1.5 * 60)
    def login_bg(self, driver: BaseDriver):
        """
        login
        :return:
        """
        self.lg.info('login ...')
        body = driver.get_url_body(
            url=self.publish_url,
            timeout=30,)
        try:
            assert body != ''
            driver.find_element(value='input#loginName').send_keys(self.yx_username)
            driver.find_element(value='input#loginPwd').send_keys(self.yx_password)
            driver.find_element(value='button#subbut').click()
        except (
                NoSuchElementException,
                SeleniumTimeoutException,
                AssertionError,
                WebDriverException,
                AttributeError,):
            # 抛出登录异常
            raise LoginFailException

        try:
            self.wait_for_recommend_good_label_appear(driver=driver)
        except FZTimeoutError:
            # 进入目标页失败, 则抛出异常!
            raise EnterTargetPageFailException

    @fz_set_timeout(seconds=10.)
    def wait_for_recommend_good_label_appear(self, driver: BaseDriver):
        """
        直到出现荐好管理label
        :param driver:
        :return:
        """
        while True:
            recommend_good_label_text = driver.find_element(
                value=self.recommend_good_label_css_selector).text
            # self.lg.info('recommend_good_label_text: {}'.format(recommend_good_label_text))
            if recommend_good_label_text == '荐好管理':
                break
            else:
                continue

        self.lg.info('login success!')

    @fz_set_timeout(seconds=60.)
    def get_into_recommend_good_manage(self, driver: BaseDriver):
        """
        进入荐好管理
        :param driver:
        :return:
        """
        try:
            driver.find_element(value=self.recommend_good_label_css_selector).click()
            # 等待下方标签出现
            sleep(.5)
            driver.find_element(value='a.J_menuItem').click()
        except SeleniumTimeoutException:
            # 进入目标页失败, 则抛出异常!
            raise EnterTargetPageFailException

    @fz_set_timeout(seconds=2.5 * 60)
    def publish_one_article(self, driver: BaseDriver, article_url: str):
        """
        发布一篇图文
        :param driver:
        :param article_url:
        :return:
        """
        try:
            # 切换到目标iframe(用index有时候不准, pass)
            # driver.switch_to_frame(frame_reference=1)

            iframe_ele_list = driver.find_elements(by=By.TAG_NAME, value='iframe')
            # pprint(iframe_ele_list)
            assert iframe_ele_list != []
            target_iframe_ele = iframe_ele_list[1] if len(iframe_ele_list) > 1 else iframe_ele_list[0]
            driver.switch_to_frame(frame_reference=target_iframe_ele)
        except (NoSuchFrameException,) as e:
            # 没匹配到frame(可能是原先就在目标iframe, eg: title过长的, 再切回iframe, 但是iframe_ele_list为0)
            raise e

        try:
            # 清空输入框
            input_box_ele = driver.find_element(value='input#SnatchUrl')
            input_box_ele.clear()
            # 输入待采集地址
            input_box_ele.send_keys(article_url)
            # 点击采集按钮
            driver.find_elements(value='span.input-group-btn button')[0].click()

            self.wait_for_delete_img_appear(driver=driver)
        except (FZTimeoutError, NoSuchElementException, WebDriverException):
            # 发布某文章超时失败or无元素存在, 则抛出发布异常
            raise PublishOneArticleFailException

        # 获取输入框的值
        title = driver.find_element(value='input#RecommendName').get_attribute('value')
        self.lg.info('title: {}'.format(title))
        if target_str_contain_some_char_check(
                target_str=title,
                check_char_obj=ARTICLE_TITLE_SENSITIVE_STR_TUPLE):
            raise ArticleTitleContainSensitiveWordsException
        else:
            pass
        if isinstance(title, str) and len(title) > 30:
            # 标题过长则return, 不发布
            self.lg.info('@@@ title 标题过长, 无法发布!! 跳过!')
            # 由于标题过长后, 无法处理后续文章, 故不return, 直接抛出异常
            # return
            raise ArticleTitleOverLongException
        else:
            pass

        try:
            # 点击发布按钮
            driver.find_elements(value='span.input-group-btn button')[1].click()
        except WebDriverException:
            # 处理发布单篇异常!
            # 处理报错: Message: unknown error: Element <iframe class="J_iframe" name="iframe0"
            raise PublishOneArticleFailException

        # 切换至主页面
        driver.switch_to_default_content()
        # 填写被发布人
        random_phone = self.get_random_phone()
        driver.find_element(value='input.layui-layer-input').send_keys(random_phone)
        # 点击确定
        driver.find_element(value='a.layui-layer-btn0').click()

        self.lg.info('url: {} 发布成功!'.format(article_url))
        # 发布成功, 等待8.5秒, 等待页面元素置空
        sleep(8.5)

        return

    @fz_set_timeout(seconds=70.)
    def wait_for_delete_img_appear(self, driver: BaseDriver):
        """
        直至出现图片, 超时退出(并且避免发布无图文章)
        :return:
        """
        while True:
            # 改用 不宜用下面方式 长期跑电脑卡死
            try:
                delete_btn_text = driver.find_element(value='div.deletebut').text
            except NoSuchElementException:
                # 处理这个异常, 并继续等待
                sleep(.3)
                continue

            # 原先 但是老是发布失败!!
            # delete_btn_text = driver.find_element(value='div.deletebut').text

            # self.lg.info('delete_btn_text: {}'.format(delete_btn_text))
            if delete_btn_text == '删除':
                break
            else:
                continue

        self.lg.info('该url采集完毕!')

    def get_random_phone(self) -> int:
        """
        随机个手机号
        :return:
        """
        phone_list = []
        with open('../tools/phone.txt', 'r') as f:
            for line in f:
                try:
                    phone_list.append(int(line.replace('\n', '')))
                except Exception:
                    continue

        # pprint(phone_list)
        random_phone = phone_list[randint(0, len(phone_list) - 1)]
        self.lg.info('random_phone: {}'.format(random_phone))

        return random_phone

    def __del__(self):
        try:
            del self.lg
            del self.loop
            del self.db_article_id_list
            del self.publish_url
            del self.article_parser
            del self.hk_cache_dict
        except:
            pass
        collect()

def main():
    _ = RecommendGoodOps()
    loop = get_event_loop()
    loop.run_until_complete(_._fck_run())

if __name__ == '__main__':
    main()