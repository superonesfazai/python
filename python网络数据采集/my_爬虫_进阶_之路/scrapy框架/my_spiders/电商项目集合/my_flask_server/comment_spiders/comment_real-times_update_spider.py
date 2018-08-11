# coding:utf-8

'''
@author = super_fazai
@File    : comment_real-times_update_spider.py
@Time    : 2018/4/18 12:36
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_pipeline import CommentInfoSaveItemPipeline

from settings import IS_BACKGROUND_RUNNING, MY_SPIDER_LOGS_PATH

from ali_1688_comment_parse import ALi1688CommentParse
from taobao_comment_parse import TaoBaoCommentParse
from tmall_comment_parse import TmallCommentParse
from jd_comment_parse import JdCommentParse

import gc
from logging import INFO, ERROR
from time import sleep
from json import dumps

from fzutils.log_utils import set_logger
from fzutils.linux_utils import daemon_init
from fzutils.time_utils import get_shanghai_time

class CommentRealTimeUpdateSpider(object):
    def __init__(self):
        self._set_logger()
        self.msg = ''
        self.debugging_api = self._init_debugging_api()
        self._set_func_name_dict()
        self.sql_str = r'update dbo.all_goods_comment set modify_time=%s, comment_info=%s where goods_id=%s'

        if self._init_debugging_api().get(2):
            self.my_lg.info('初始化 1688 phantomjs中...')
            self.ali_1688 = ALi1688CommentParse(logger=self.my_lg)

        if self._init_debugging_api().get(3) is True \
                or self._init_debugging_api().get(4) is True\
                or self._init_debugging_api().get(6) is True:
            self.my_lg.info('初始化 天猫 phantomjs中...')
            self.tmall = TmallCommentParse(logger=self.my_lg)

        if self._init_debugging_api().get(7) is True \
                or self._init_debugging_api().get(8) is True\
                or self._init_debugging_api().get(9) is True\
                or self._init_debugging_api().get(10) is True:
            self.my_lg.info('初始化 京东 phantomjs中...')
            self.jd = JdCommentParse(logger=self.my_lg)

    def _set_logger(self):
        self.my_lg = set_logger(
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
            1: True,
            2: True,
            3: True,
            4: True,
            6: True,
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
            self._comment_pipeline = CommentInfoSaveItemPipeline(logger=self.my_lg)
            #  and GETDATE()-a.modify_time>1
            sql_str = '''
            select goods_id, SiteID as site_id 
            from dbo.GoodsInfoAutoGet as a, dbo.all_goods_comment as b 
            where a.GoodsID=b.goods_id and a.MainGoodsID is not null and a.IsDelete=0
            order by b.id asc'''
            try:
                result = list(self._comment_pipeline._select_table(sql_str=sql_str))
            except TypeError:
                self.my_lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
                continue

            self.my_lg.info('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
            self.my_lg.info(str(result))
            self.my_lg.info('--------------------------------------------------------')
            self.my_lg.info('待更新个数: {0}'.format(len(result)))

            self.my_lg.info('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))

            # 1.淘宝 2.阿里 3.天猫 4.天猫超市 5.聚划算 6.天猫国际 7.京东 8.京东超市 9.京东全球购 10.京东大药房  11.折800 12.卷皮 13.拼多多 14.折800秒杀 15.卷皮秒杀 16.拼多多秒杀 25.唯品会
            for index, item in enumerate(result):     # item: ('xxxx':goods_id, 'y':site_id)
                if not self.debugging_api.get(item[1]):
                    self.my_lg.info('api为False, 跳过! 索引值[%s]' % str(index))
                    continue

                if index % 20 == 0:
                    try: del self._comment_pipeline
                    except: pass
                    self._comment_pipeline = CommentInfoSaveItemPipeline(logger=self.my_lg)

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
                exec_code = compile(switch[item[1]].format(index, item[0], item[1]), '', 'exec')
                exec(exec_code)
                sleep(1.1)

    def _update_taobao_comment(self, index, goods_id, site_id):
        '''
        处理淘宝的商品comment
        :param index: 索引
        :param goods_id:
        :param site_id:
        :return:
        '''
        if self.debugging_api.get(site_id):
            self.my_lg.info('------>>>| 淘宝\t\t索引值(%s)' % str(index))

            taobao = TaoBaoCommentParse(logger=self.my_lg)
            _r = taobao._get_comment_data(goods_id=str(goods_id))

            if _r.get('_comment_list', []) != []:
                if self._comment_pipeline.is_connect_success:
                    self._comment_pipeline._update_table(sql_str=self.sql_str, params=self._get_db_update_params(item=_r))
            else:
                self.my_lg.info('该商品_comment_list为空list! 此处跳过!')

            try:
                del taobao
            except:
                self.my_lg.info('del taobao失败!')
            gc.collect()
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
            self.my_lg.info('------>>>| 阿里1688\t\t索引值(%s)' % str(index))

            if index % 5 == 0:
                try: del self.ali_1688
                except: self.my_lg.error('del ali_1688失败!')
                gc.collect()
                self.ali_1688 = ALi1688CommentParse(logger=self.my_lg)

            _r = self.ali_1688._get_comment_data(goods_id=goods_id)
            if _r.get('_comment_list', []) != []:
                if self._comment_pipeline.is_connect_success:
                    self._comment_pipeline._update_table(sql_str=self.sql_str, params=self._get_db_update_params(item=_r))
            else:
                self.my_lg.info('该商品_comment_list为空list! 此处跳过!')

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
            self.my_lg.info('------>>>| 天猫\t\t索引值(%s)' % str(index))

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
                    self.my_lg.info('del tmall失败!')
                gc.collect()
                self.tmall = TmallCommentParse(logger=self.my_lg)

            _r = self.tmall._get_comment_data(type=_type, goods_id=str(goods_id))
            if _r.get('_comment_list', []) != []:
                if self._comment_pipeline.is_connect_success:
                    self._comment_pipeline._update_table(sql_str=self.sql_str, params=self._get_db_update_params(item=_r))
            else:
                self.my_lg.info('该商品_comment_list为空list! 此处跳过!')
            gc.collect()
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
            self.my_lg.info('------>>>| 京东\t\t索引值(%s)' % str(index))

            if index % 5 == 0:
                try: del self.jd
                except: self.my_lg.info('del jd失败!')
                gc.collect()
                self.jd = JdCommentParse(logger=self.my_lg)

            _r = self.jd._get_comment_data(goods_id=str(goods_id))
            if _r.get('_comment_list', []) != []:
                if self._comment_pipeline.is_connect_success:
                    self._comment_pipeline._update_table(sql_str=self.sql_str, params=self._get_db_update_params(item=_r))
            else:
                self.my_lg.info('该商品_comment_list为空list! 此处跳过!')
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
            pass
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

    def _get_db_update_params(self, item):
        return (
            item['modify_time'],
            dumps(item['_comment_list'], ensure_ascii=False),

            item['goods_id'],
        )

    def __del__(self):
        try:
            del self.my_lg
            del self.msg
            del self.debugging_api
        except:
            pass
        try: del self._comment_pipeline
        except: pass
        try:
            del self.tmall
        except:
            pass
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        _tmp = CommentRealTimeUpdateSpider()
        _tmp._just_run()
        # try:
        #     del _tmp
        # except:
        #     pass
        gc.collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60*5)

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