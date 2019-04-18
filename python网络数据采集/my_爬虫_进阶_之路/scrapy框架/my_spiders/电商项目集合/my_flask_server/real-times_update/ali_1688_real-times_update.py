# coding:utf-8

'''
@author = super_fazai
@File    : ali_1688_real-times_update.py
@Time    : 2017/10/28 07:24
@connect : superonesfazai@gmail.com
'''

"""
本地长期更新(server可更新!), 部分goods_id采集会被强制登录(ip被封), 但是不是所有!
推荐放在server上更新!(目前只放在server上更新)
本地ip被封时, 可通过重启路由器来获取新ip
"""

import sys
sys.path.append('..')

from ali_1688_parse import ALi1688LoginAndParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from gc import collect

from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,)

from sql_str_controller import al_select_str_6
from multiplex_code import (
    _get_sku_price_trans_record,
    _get_spec_trans_record,
    _get_stock_trans_record,
    _get_new_db_conn,
    _get_async_task_result,
    _print_db_old_data,)

from fzutils.cp_utils import _get_price_change_info
from fzutils.spider.async_always import *

"""
39.97那台无法更新已被封禁
放本地更新
"""

class ALUpdater(AsyncCrawler):
    """1688常规商品数据更新"""
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self, 
            *params, 
            **kwargs,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/1688/实时更新/')
        self.sql_cli = None
        self.goods_index = 1
        self.concurrency = 10        # 并发量

    async def _get_db_old_data(self) -> (list, None):
        '''
        获取db需求更新的数据
        :return:
        '''
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        result = None
        try:
            result = list(self.sql_cli._select_table(sql_str=al_select_str_6))
        except TypeError:
            self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')

        await _print_db_old_data(logger=self.lg, result=result)

        return result

    async def _get_new_ali_obj(self, index) -> None:
        if index % 10 == 0:         # 不能共享一个对象了, 否则驱动访问会异常!
            try:
                del self.ali_1688
            except:
                pass
            collect()
            self.ali_1688 = ALi1688LoginAndParse(logger=self.lg)

    async def _get_one_data(self, ali_1688, goods_id):
        return ali_1688.get_ali_1688_data(goods_id)

    async def _update_one_goods_info(self, item, index) -> list:
        '''
        更新一个goods的信息
        :param index: 索引值
        :return: ['goods_id', bool:'成功与否']
        '''
        res = False
        goods_id = item[0]
        await self._get_new_ali_obj(index=index)
        self.sql_cli = await _get_new_db_conn(db_obj=self.sql_cli, index=index, logger=self.lg)
        if self.sql_cli.is_connect_success:
            self.lg.info('------>>>| 正在更新的goods_id为({0}) | --------->>>@ 索引值为({1})'.format(goods_id, index))
            # data = ali_1688.get_ali_1688_data(goods_id)
            data = await self._get_one_data(ali_1688=self.ali_1688, goods_id=goods_id)
            if isinstance(data, int):  # 单独处理返回tt为4041
                self.goods_index += 1
                return [goods_id, res]

            if data.get('is_delete') == 1:
                # self.lg.info('test')
                # 单独处理【原先插入】就是 下架状态的商品
                data['goods_id'] = goods_id
                data['shelf_time'], data['delete_time'] = get_shelf_time_and_delete_time(
                    tmp_data=data,
                    is_delete=item[1],
                    shelf_time=item[4],
                    delete_time=item[5])
                try:
                    self.ali_1688.to_right_and_update_data(data, pipeline=self.sql_cli)
                except Exception:
                    self.lg.error(exc_info=True)

                await async_sleep(1.5)
                self.goods_index += 1
                res = True

                return [goods_id, res]

            data = self.ali_1688.deal_with_data()
            if data != {}:
                data['goods_id'] = goods_id
                data['shelf_time'], data['delete_time'] = get_shelf_time_and_delete_time(
                    tmp_data=data,
                    is_delete=item[1],
                    shelf_time=item[4],
                    delete_time=item[5])
                # self.lg.info('上架时间:{0}, 下架时间:{1}'.format(data['shelf_time'], data['delete_time']))

                # 监控纯价格变动
                price_info_list = old_sku_info = json_2_dict(item[6], default_res=[])
                try:
                    old_sku_info = format_price_info_list(price_info_list=price_info_list, site_id=2)
                except AttributeError:  # 处理已被格式化过的
                    pass
                new_sku_info = format_price_info_list(data['sku_map'], site_id=2)
                data['_is_price_change'], data['sku_info_trans_time'], price_change_info = _get_sku_price_trans_record(
                    old_sku_info=old_sku_info,
                    new_sku_info=new_sku_info,
                    is_price_change=item[7] if item[7] is not None else 0,
                    db_price_change_info=json_2_dict(item[9], default_res=[]),
                    old_price_trans_time=item[12],)

                # 处理单规格的情况
                # _price_change_info这个字段不进行记录, 还是记录到price, taobao_price
                data['_is_price_change'], data['_price_change_info'] = _get_price_change_info(
                    old_price=item[2],
                    old_taobao_price=item[3],
                    new_price=data['price'],
                    new_taobao_price=data['taobao_price'],
                    is_price_change=data['_is_price_change'],
                    price_change_info=price_change_info)
                if data['_is_price_change'] == 1:
                    self.lg.info('价格变动!!')
                # self.lg.info('_is_price_change: {}, sku_info_trans_time: {}'.format(data['_is_price_change'], data['sku_info_trans_time']))

                # 监控纯规格变动
                data['is_spec_change'], data['spec_trans_time'] = _get_spec_trans_record(
                    old_sku_info=old_sku_info,
                    new_sku_info=new_sku_info,
                    is_spec_change=item[8] if item[8] is not None else 0,
                    old_spec_trans_time=item[13],)
                if data['is_spec_change'] == 1:
                    self.lg.info('规格属性变动!!')
                # self.lg.info('is_spec_change: {}, spec_trans_time: {}'.format(data['is_spec_change'], data['spec_trans_time']))

                # 监控纯库存变动
                data['is_stock_change'], data['stock_trans_time'], data['stock_change_info'] = _get_stock_trans_record(
                    old_sku_info=old_sku_info,
                    new_sku_info=new_sku_info,
                    is_stock_change=item[10] if item[10] is not None else 0,
                    db_stock_change_info=json_2_dict(item[11], default_res=[]),
                    old_stock_trans_time=item[14],)
                if data['is_stock_change'] == 1:
                    self.lg.info('规格的库存变动!!')
                # self.lg.info('is_stock_change: {}, stock_trans_time: {}, stock_change_info: {}'.format(data['is_stock_change'], data['stock_trans_time'], data['stock_change_info']))

                # 单独处理起批量>=1的
                begin_greater_than_1 = await self.judge_begin_greater_than_1(price_info=data['price_info'], logger=self.lg)
                if begin_greater_than_1:
                    self.lg.info('该商品 起批量 大于1, 下架!!')
                    data['is_delete'] = 1

                res = self.ali_1688.to_right_and_update_data(data, pipeline=self.sql_cli)
                await async_sleep(.3)

            else:  # 表示返回的data值为空值
                pass

        else:  # 表示返回的data值为空值
            self.lg.error('数据库连接失败，数据库可能关闭或者维护中')

        index += 1
        self.goods_index = index
        collect()
        await async_sleep(2.)       # 避免被发现使用代理

        return [goods_id, res]

    async def judge_begin_greater_than_1(self, price_info: list, logger) -> bool:
        '''
        判断起批量是否大于1, 大于1则返回True, <=1 返回False
        :return:
        '''
        if price_info == []:
            return False

        try:
            price_info.sort(key=lambda item: int(item.get('begin')))
            # pprint(price_info)
            if int(price_info[0]['begin']) > 1:
                return True
            else:
                return False
        except Exception:
            logger.error('遇到错误:', exc_info=True)
            return True

    async def _update_db(self):
        '''
        常规数据实时更新
        :return:
        '''
        # 记录已更新的goods_id, 这样导致只进行一次更新, 下次更新必须重启脚本
        # record_updated_goods_id_list = []
        while True:
            self.lg = await self._get_new_logger(logger_name=get_uuid1())
            result = await self._get_db_old_data()
            if result is None:
                pass
            else:
                self.goods_index = 1
                tasks_params_list = TasksParamsListObj(tasks_params_list=result, step=self.concurrency)
                self.ali_1688 = ALi1688LoginAndParse(logger=self.lg)
                index = 1
                while True:
                    try:
                        slice_params_list = tasks_params_list.__next__()
                        # self.lg.info(str(slice_params_list))
                    except AssertionError:  # 全部提取完毕, 正常退出
                        break

                    tasks = []
                    for item in slice_params_list:
                        goods_id = item[0]
                        # if goods_id not in record_updated_goods_id_list:
                        #     record_updated_goods_id_list.append(goods_id)
                        # else:
                        #     self.lg.info('该goods_id[{}]前面loop已检测更新! 跳过!'.format(goods_id))
                        #     continue

                        self.lg.info('创建 task goods_id: {}'.format(goods_id))
                        tasks.append(self.loop.create_task(self._update_one_goods_info(item=item, index=index)))
                        index += 1
                    if tasks != []:
                        await _get_async_task_result(tasks=tasks, logger=self.lg)
                    else:
                        pass

                self.lg.info('全部数据更新完毕'.center(100, '#'))
            if get_shanghai_time().hour == 0:  # 0点以后不更新
                await async_sleep(60 * 60 * 5.5)
            else:
                await async_sleep(5.5)
            try:
                del self.ali_1688
            except:
                pass
            collect()

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
    # 遇到: PermissionError: [Errno 13] Permission denied: 'ghostdriver.log'
    # 解决方案: sudo touch /ghostdriver.log && sudo chmod 777 /ghostdriver.log
    _ = ALUpdater()
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
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    _fck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        _fck_run()
