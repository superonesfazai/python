# coding:utf-8

'''
@author = super_fazai
@File    : ali_1688_real-times_update.py
@Time    : 2017/10/28 07:24
@connect : superonesfazai@gmail.com
'''

"""
我们需要两台服务器一台拿来专门更新数据，一台拿来专门处理客服入信息
"""

import sys
sys.path.append('..')

from taobao_parse import TaoBaoLoginAndParse
from my_pipeline import (
    SqlServerMyPageInfoSaveItemPipeline,
    SqlPools,
)

from settings import TAOBAO_REAL_TIMES_SLEEP_TIME
from gc import collect
from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,
)

from sql_str_controller import tb_select_str_3
from multiplex_code import (
    _get_sku_price_trans_record,
    _get_spec_trans_record,
    _get_async_task_result,
    _get_new_db_conn,
    _get_stock_trans_record,
    _print_db_old_data,)

from fzutils.cp_utils import _get_price_change_info
from fzutils.spider.async_always import *

class TBUpdater(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/淘宝/实时更新/')
        self.tmp_sql_server = None
        self.goods_index = 1
        self.concurrency = 50  # 并发量

    async def _get_db_old_data(self) -> (list, None):
        '''
        获取db需求更新的数据
        :return:
        '''
        # self.tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        self.tmp_sql_server = SqlPools()  # 使用sqlalchemy管理数据库连接池
        result = None
        try:
            # result = list(self.tmp_sql_server.select_taobao_all_goods_id())
            result = self.tmp_sql_server._select_table(sql_str=tb_select_str_3,)
        except TypeError:
            self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')

        await _print_db_old_data(logger=self.lg, result=result)

        return result

    async def _get_new_tb_obj(self, index) -> None:
        if index % 10 == 0:
            try:
                del self.taobao
            except:
                pass
            collect()
            self.taobao = TaoBaoLoginAndParse(logger=self.lg)

    async def _update_one_goods_info(self, item, index):
        '''
        更新单个goods
        :return:
        '''
        res = False
        goods_id = item[0]
        await self._get_new_tb_obj(index=index)
        self.tmp_sql_server = await _get_new_db_conn(db_obj=self.tmp_sql_server, index=index, logger=self.lg, db_conn_type=2, remainder=50)
        if self.tmp_sql_server.is_connect_success:
            self.lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id, str(index)))
            oo = self.taobao.get_goods_data(goods_id=goods_id)
            oo_is_delete = oo.get('is_delete', 0)  # 避免下面解析data错误休眠
            data = self.taobao.deal_with_data(goods_id=goods_id)
            if data != {}:
                data['goods_id'] = goods_id
                data['shelf_time'], data['delete_time'] = get_shelf_time_and_delete_time(
                    tmp_data=data,
                    is_delete=item[1],
                    shelf_time=item[4],
                    delete_time=item[5])
                price_info_list = old_sku_info = json_2_dict(item[6], default_res=[])
                try:
                    old_sku_info = format_price_info_list(price_info_list=price_info_list, site_id=1)
                except AttributeError:  # 处理已被格式化过的
                    pass
                new_sku_info = format_price_info_list(data['price_info_list'], site_id=1)
                # if len(new_sku_info) <= 6:
                #     self.lg.info('old_sku_info:')
                #     pprint(old_sku_info)
                #     self.lg.info('new_sku_info:')
                #     pprint(new_sku_info)

                data['_is_price_change'], data['sku_info_trans_time'], price_change_info = _get_sku_price_trans_record(
                    old_sku_info=old_sku_info,
                    new_sku_info=new_sku_info,
                    is_price_change=item[7] if item[7] is not None else 0,
                    db_price_change_info=json_2_dict(item[9], default_res=[]),
                    old_price_trans_time=item[12])
                data['_is_price_change'], data['_price_change_info'] = _get_price_change_info(
                    old_price=item[2],
                    old_taobao_price=item[3],
                    new_price=data['price'],
                    new_taobao_price=data['taobao_price'],
                    is_price_change=data['_is_price_change'],
                    price_change_info=price_change_info)
                if data['_is_price_change'] == 1:
                    self.lg.info('价格变动!!')
                    # pprint(data['_price_change_info'])

                # 监控纯规格变动
                data['is_spec_change'], data['spec_trans_time'] = _get_spec_trans_record(
                    old_sku_info=old_sku_info,
                    new_sku_info=new_sku_info,
                    is_spec_change=item[8] if item[8] is not None else 0,
                    old_spec_trans_time=item[13])
                if data['is_spec_change'] == 1:
                    self.lg.info('规格属性变动!!')

                # 监控纯库存变动
                data['is_stock_change'], data['stock_trans_time'], data['stock_change_info'] = _get_stock_trans_record(
                    old_sku_info=old_sku_info,
                    new_sku_info=new_sku_info,
                    is_stock_change=item[10] if item[10] is not None else 0,
                    db_stock_change_info=json_2_dict(item[11], default_res=[]),
                    old_stock_trans_time=item[14])
                if data['is_stock_change'] == 1:
                    self.lg.info('规格的库存变动!!')
                # self.lg.info('is_stock_change: {}, stock_trans_time: {}, stock_change_info: {}'.format(data['is_stock_change'], data['stock_trans_time'], data['stock_change_info']))

                res = self.taobao.to_right_and_update_data(data, pipeline=self.tmp_sql_server)

            else:
                if oo_is_delete == 1:
                    pass
                else:
                    self.lg.info('------>>>| 休眠8s中...')
                    await async_sleep(delay=8, loop=self.loop)

        else:  # 表示返回的data值为空值
            self.lg.error('数据库连接失败，数据库可能关闭或者维护中')
            await async_sleep(delay=10, loop=self.loop)

        index += 1
        self.goods_index = index
        collect()
        # 国外服务器上可以缩短时间, 可以设置为0s
        await async_sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)  # 不能太频繁，与用户请求错开尽量

        return [goods_id, res]

    async def _update_db(self):
        '''
        实时更新数据
        :return:
        '''
        while True:
            self.lg = await self._get_new_logger(logger_name=get_uuid1())
            result = await self._get_db_old_data()
            if result is None:
                pass
            else:
                self.goods_index = 1
                tasks_params_list = TasksParamsListObj(tasks_params_list=result, step=self.concurrency)
                self.taobao = TaoBaoLoginAndParse(logger=self.lg)
                index = 1
                while True:
                    try:
                        slice_params_list = tasks_params_list.__next__()
                    except AssertionError:  # 全部提取完毕, 正常退出
                        break

                    tasks = []
                    for item in slice_params_list:
                        self.lg.info('创建 task goods_id: {}'.format(item[0]))
                        tasks.append(self.loop.create_task(self._update_one_goods_info(item=item, index=index)))
                        index += 1

                    res = await _get_async_task_result(tasks=tasks, logger=self.lg)
                    await self._except_sleep(res=res)

                self.lg.info('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
            if get_shanghai_time().hour == 0:  # 0点以后不更新
                await async_sleep(60 * 60 * 5.5)
            else:
                await async_sleep(10)
            collect()

    async def _except_sleep(self, res):
        '''
        异常休眠
        :param res:
        :return:
        '''
        count = 0
        all_count_fail_sleep_time = 100.
        sleep_time = 60.
        for item in res:
            try:
                if not item[1]:
                    count += 1
            except IndexError:
                pass
        self.lg.info('Fail count: {}个, 并发量: {}个'.format(count, self.concurrency))
        if count/self.concurrency >= .9:
            # 全失败的休眠方式
            self.lg.info('抓取异常!! 休眠{}s中...'.format(all_count_fail_sleep_time))
            await async_sleep(all_count_fail_sleep_time)

        else:
            if count >= int(self.concurrency/5):
                self.lg.info('抓取异常!! 休眠{}s中...'.format(sleep_time))
                await async_sleep(sleep_time)

        return None

    def __del__(self):
        try:
            del self.lg
        except:
            pass
        try:
            del self.loop
        except:
            pass
        collect()

def _fck_run():
    _ = TBUpdater()
    loop = get_event_loop()
    loop.run_until_complete(_._update_db())
    try:
        del loop
    except:
        pass

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    _fck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        _fck_run()