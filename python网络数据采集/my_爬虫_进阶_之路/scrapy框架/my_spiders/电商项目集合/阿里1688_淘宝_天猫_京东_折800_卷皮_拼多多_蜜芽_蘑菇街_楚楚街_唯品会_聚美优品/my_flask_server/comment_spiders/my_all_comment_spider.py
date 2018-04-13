# coding:utf-8

'''
@author = super_fazai
@File    : my_all_comment_spider.py
@Time    : 2018/4/9 15:24
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from my_logging import set_logger
from my_utils import daemon_init, get_shanghai_time

from settings import IS_BACKGROUND_RUNNING, MY_SPIDER_LOGS_PATH

from ali_1688_comment_parse import ALi1688CommentParse
from taobao_comment_parse import TaoBaoCommentParse
from tmall_comment_parse import TmallCommentParse

import gc
from logging import INFO, ERROR
from time import sleep

class MyAllCommentSpider(object):
    def __init__(self):
        self.my_lg = set_logger(
            log_file_name=MY_SPIDER_LOGS_PATH + '/all_comment/_/' + str(get_shanghai_time())[0:10] + '.txt',
            console_log_level=INFO,
            file_log_level=ERROR
        )
        self.msg = ''

    def _just_run(self):
        while True:
            #### 实时更新数据
            tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
            try:
                result = list(tmp_sql_server.select_all_goods_info_from_GoodsInfoAutoGet_table())
            except TypeError:
                self.my_lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
                result = None
            if result is None:
                pass
            else:
                self.my_lg.info('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
                self.my_lg.info(str(result))
                self.my_lg.info('--------------------------------------------------------')

                self.my_lg.info('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))

                for index, item in enumerate(result):     # item: ('xxxx':goods_id, 'y':site_id)
                    switch = {
                        1: 'self.taobao_comment({0}, {1}, {2})',
                        2: 'self.ali_1688_comment({0}, {1}, {2})',
                        3: 'self.tmall_comment({0}, {1}, {2})',
                        4: 'self.tmall_comment({0}, {1}, {2})',
                        6: 'self.tmall_comment({0}, {1}, {2})',
                    }

                    # 动态执行
                    exec_code = compile(switch[item[1]].format(index, item[0], item[1]), '', 'exec')
                    exec(exec_code)

    def taobao_comment(self, index, goods_id, site_id):
        '''
        处理淘宝的商品comment
        :param index: 索引
        :param goods_id:
        :param site_id:
        :return:
        '''
        self.my_lg.info('淘宝\t\t\t索引值(%s)' % str(index))
        taobao = TaoBaoCommentParse(logger=self.my_lg)
        taobao._get_comment_data(goods_id=str(goods_id))

        try:
            del taobao
        except:
            self.my_lg.info('del taobao失败!')
        gc.collect()

    def ali_1688_comment(self, index, goods_id, site_id):
        '''
        处理阿里1688的商品comment
        :param index: 索引
        :param goods_id:
        :param site_id:
        :return:
        '''
        self.my_lg.info('阿里1688\t\t\t索引值(%s)' % str(index))
        ali_1688 = ALi1688CommentParse(logger=self.my_lg)
        ali_1688._get_comment_data(goods_id=goods_id)

        try:
            del ali_1688
        except:
            self.my_lg.info('del ali_1688失败!')
        gc.collect()

    def tmall_comment(self, index, goods_id, site_id):
        '''
        处理tmall商品的comment
        :param index:
        :param goods_id:
        :param site_id:
        :return:
        '''
        self.my_lg.info('天猫\t\t\t索引值(%s)' % str(index))
        tmall = TmallCommentParse(logger=self.my_lg)
        if site_id == 3:
            _type = 0
        elif site_id == 4:
            _type = 1
        elif site_id == 6:
            _type = 2
        else:
            return None

        tmall._get_comment_data(type=_type, goods_id=str(goods_id))
        try: del tmall
        except: pass
        gc.collect()

    def __del__(self):
        try:
            del self.my_lg
            del self.msg
        except:
            pass
        gc.collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        _tmp = MyAllCommentSpider()
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

