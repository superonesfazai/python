# coding:utf-8

'''
@author = super_fazai
@File    : comment_real-times_update_spider.py
@Time    : 2018/4/18 12:36
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,)

from ali_1688_comment_parse import ALi1688CommentParse
from taobao_comment_parse import TaoBaoCommentParse
from tmall_comment_parse import TmallCommentParse
from jd_comment_parse import JdCommentParse
from zhe_800_comment_parse import Zhe800CommentParse

from gc import collect
from logging import INFO, ERROR
from time import sleep

from multiplex_code import (
    _block_get_new_db_conn,
    _save_comment_item_r,
    _block_print_db_old_data,)

from sql_str_controller import (
    cm_select_str_1,
)

from fzutils.log_utils import set_logger
from fzutils.linux_utils import daemon_init
from fzutils.time_utils import get_shanghai_time

class CommentRealTimeUpdateSpider(object):
    def __init__(self):
        self._set_logger()
        self.msg = ''
        self.debugging_api = self._init_debugging_api()
        self._set_func_name_dict()

        if self._init_debugging_api().get(2):
            self.lg.info('初始化 1688 phantomjs中...')
            self.ali_1688 = ALi1688CommentParse(logger=self.lg)

        if self._init_debugging_api().get(3) is True \
                or self._init_debugging_api().get(4) is True\
                or self._init_debugging_api().get(6) is True:
            self.lg.info('初始化 天猫 phantomjs中...')
            self.tmall = TmallCommentParse(logger=self.lg)

        if self._init_debugging_api().get(7) is True \
                or self._init_debugging_api().get(8) is True\
                or self._init_debugging_api().get(9) is True\
                or self._init_debugging_api().get(10) is True:
            self.lg.info('初始化 京东 phantomjs中...')
            self.jd = JdCommentParse(logger=self.lg)

    def _set_logger(self):
        self.lg = set_logger(
            log_file_name=MY_SPIDER_LOGS_PATH + '/all_comment/实时更新/' + str(get_shanghai_time())[0:10] + '.txt',
            console_log_level=INFO,
            file_log_level=ERROR
        )

    def _init_debugging_api(self):
        '''
        用于设置待抓取的商品的site_id
        :return: dict
        '''
        return {
            1: False,
            2: False,
            3: False,
            4: False,
            6: False,
            7: True,
            8: True,
            9: True,
            10: True,
            11: False,
            12: False,
            13: False,
            25: False,
        }

    def _set_func_name_dict(self):
        self.func_name_dict = {
            'taobao': 'self._update_taobao_comment({0}, {1}, {2})',
            'ali': 'self._update_ali_1688_comment({0}, {1}, {2})',
            'tmall': 'self._update_tmall_comment({0}, {1}, {2})',
            'jd': 'self._update_jd_comment({0}, {1}, {2})',
            'zhe_800': 'self._update_zhe_800_comment({0}, {1}, {2})',
            'juanpi': 'self._update_juanpi_comment({0}, {1}, {2})',
            'pinduoduo': 'self._update_pinduoduo_comment({0}, {1}, {2})',
            'vip': 'self._update_vip_comment({0}, {1}, {2})',
        }

    def _just_run(self):
        while True:
            #### 更新数据
            self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
            try:
                # 获取待更新的数据
                result = list(self.sql_cli._select_table(sql_str=cm_select_str_1, logger=self.lg))
            except TypeError:
                self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
                sleep(30)
                continue

            _block_print_db_old_data(result=result, logger=self.lg)
            # 1.淘宝 2.阿里 3.天猫 4.天猫超市 5.聚划算 6.天猫国际 7.京东 8.京东超市 9.京东全球购 10.京东大药房  11.折800 12.卷皮 13.拼多多 14.折800秒杀 15.卷皮秒杀 16.拼多多秒杀 25.唯品会
            for index, item in enumerate(result):     # item: ('xxxx':goods_id, 'y':site_id)
                goods_id, site_id = item
                if not self.debugging_api.get(site_id):
                    self.lg.info('api为False, 跳过! 索引值[%s]' % str(index))
                    continue

                self.sql_cli = _block_get_new_db_conn(
                    db_obj=self.sql_cli,
                    index=index,
                    logger=self.lg,
                    remainder=5,)
                switch = {
                    1: self.func_name_dict.get('taobao'),       # 淘宝
                    2: self.func_name_dict.get('ali'),          # 阿里1688
                    3: self.func_name_dict.get('tmall'),        # 天猫
                    4: self.func_name_dict.get('tmall'),        # 天猫超市
                    6: self.func_name_dict.get('tmall'),        # 天猫国际
                    7: self.func_name_dict.get('jd'),           # 京东
                    8: self.func_name_dict.get('jd'),           # 京东超市
                    9: self.func_name_dict.get('jd'),           # 京东全球购
                    10: self.func_name_dict.get('jd'),          # 京东大药房
                    11: self.func_name_dict.get('zhe_800'),     # 折800
                    12: self.func_name_dict.get('juanpi'),      # 卷皮
                    13: self.func_name_dict.get('pinduoduo'),   # 拼多多
                    25: self.func_name_dict.get('vip'),         # 唯品会
                }
                # 动态执行
                exec_code = compile(switch[site_id].format(index, goods_id, site_id), '', 'exec')
                exec(exec_code)
                sleep(2)

    def _update_taobao_comment(self, index, goods_id, site_id):
        '''
        处理新增的淘宝商品comment
        :param index: 索引
        :param goods_id:
        :param site_id:
        :return:
        '''
        if self.debugging_api.get(site_id):
            self.lg.info('------>>>| 淘宝\t\t索引值(%s)' % str(index))

            taobao = TaoBaoCommentParse(logger=self.lg)
            _r = taobao._get_comment_data(goods_id=str(goods_id))
            if _r.get('_comment_list', []) != []:
                if self.sql_cli.is_connect_success:
                    _save_comment_item_r(
                        _r=_r,
                        goods_id=goods_id,
                        sql_cli=self.sql_cli,
                        logger=self.lg,)

            else:
                self.lg.info('该商品_comment_list为空list! 此处跳过!')

            try:
                del taobao
            except:
                self.lg.info('del taobao失败!')
            collect()
        else:
            pass

    def _update_ali_1688_comment(self, index, goods_id, site_id):
        '''
        处理阿里1688的商品comment
        :param index: 索引
        :param goods_id:
        :param site_id:
        :return:
        '''
        if self.debugging_api.get(site_id):
            self.lg.info('------>>>| 阿里1688\t\t索引值(%s)' % str(index))

            if index % 5 == 0:
                try: del self.ali_1688
                except: self.lg.error('del ali_1688失败!')
                collect()
                self.ali_1688 = ALi1688CommentParse(logger=self.lg)

            _r = self.ali_1688._get_comment_data(goods_id=goods_id)
            if _r.get('_comment_list', []) != []:
                if self.sql_cli.is_connect_success:
                    _save_comment_item_r(
                        _r=_r,
                        goods_id=goods_id,
                        sql_cli=self.sql_cli,
                        logger=self.lg, )

            else:
                self.lg.info('该商品_comment_list为空list! 此处跳过!')

        else:
            pass

    def _update_tmall_comment(self, index, goods_id, site_id):
        '''
        处理tmall商品的comment
        :param index:
        :param goods_id:
        :param site_id:
        :return:
        '''
        if self.debugging_api.get(site_id):
            self.lg.info('------>>>| 天猫\t\t索引值(%s)' % str(index))

            if site_id == 3:
                _type = 0
            elif site_id == 4:
                _type = 1
            elif site_id == 6:
                _type = 2
            else:
                return None

            if index % 5 == 0:
                try:
                    del self.tmall
                except:
                    self.lg.info('del tmall失败!')
                collect()
                self.tmall = TmallCommentParse(logger=self.lg)

            _r = self.tmall._get_comment_data(type=_type, goods_id=str(goods_id))
            if _r.get('_comment_list', []) != []:
                if self.sql_cli.is_connect_success:
                    _save_comment_item_r(
                        _r=_r,
                        goods_id=goods_id,
                        sql_cli=self.sql_cli,
                        logger=self.lg, )

            else:
                self.lg.info('该商品_comment_list为空list! 此处跳过!')
            collect()
        else:
            pass

    def _update_jd_comment(self, index, goods_id, site_id):
        '''
        处理京东商品的comment
        :param index:
        :param goods_id:
        :param site_id:
        :return:
        '''
        if self.debugging_api.get(site_id):
            self.lg.info('------>>>| 京东\t\t索引值(%s)' % str(index))

            if index % 5 == 0:
                try: del self.jd
                except: self.lg.info('del jd失败!')
                collect()
                self.jd = JdCommentParse(logger=self.lg)

            _r = self.jd._get_comment_data(goods_id=str(goods_id))
            if _r.get('_comment_list', []) != []:
                if self.sql_cli.is_connect_success:
                    _save_comment_item_r(
                        _r=_r,
                        goods_id=goods_id,
                        sql_cli=self.sql_cli,
                        logger=self.lg, )

            else:
                self.lg.info('该商品_comment_list为空list! 此处跳过!')
        else:
            pass

    def _update_zhe_800_comment(self, index, goods_id, site_id):
        '''
        处理折800商品的comment
        :param index:
        :param goods_id:
        :param site_id:
        :return:
        '''
        if self.debugging_api.get(site_id):
            self.lg.info('------>>>| zhe800\t\t索引值(%s)' % str(index))

            zhe800 = Zhe800CommentParse(logger=self.lg)
            _r = zhe800._get_comment_data(goods_id=str(goods_id))
            if _r.get('_comment_list', []) != []:
                if self.sql_cli.is_connect_success:
                    _save_comment_item_r(
                        _r=_r,
                        goods_id=goods_id,
                        sql_cli=self.sql_cli,
                        logger=self.lg, )

            else:
                self.lg.info('该商品_comment_list为空list! 此处跳过!')

            try:
                del zhe800
            except:
                self.lg.info('del taobao失败!')
            collect()
        else:
            pass

    def _update_juanpi_comment(self, index, goods_id, site_id):
        '''
        处理卷皮商品的comment
        :param index:
        :param goods_id:
        :param site_id:
        :return:
        '''
        if self.debugging_api.get(site_id):
            pass
        else:
            pass

    def _update_pinduoduo_comment(self, index, goods_id, site_id):
        '''
        处理拼多多的comment
        :param index:
        :param goods_id:
        :param site_id:
        :return:
        '''
        if self.debugging_api.get(site_id):
            pass
        else:
            pass

    def _update_vip_comment(self, index, goods_id, site_id):
        '''
        处理唯品会的comment
        :param index:
        :param goods_id:
        :param site_id:
        :return:
        '''
        if self.debugging_api.get(site_id):
            pass
        else:
            pass

    def __del__(self):
        try:
            del self.lg
            del self.msg
            del self.debugging_api
        except:
            pass
        try: del self.sql_cli
        except: pass
        try:
            del self.tmall
        except:
            pass
        collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        _tmp = CommentRealTimeUpdateSpider()
        _tmp._just_run()
        # try:
        #     del _tmp
        # except:
        #     pass
        collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60*5)

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()