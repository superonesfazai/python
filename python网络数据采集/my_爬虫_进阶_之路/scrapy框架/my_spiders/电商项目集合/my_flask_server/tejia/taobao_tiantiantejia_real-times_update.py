# coding:utf-8

'''
@author = super_fazai
@File    : taobao_tiantiantejia_real-times_update.py
@Time    : 2018/1/2 11:42
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from taobao_parse import TaoBaoLoginAndParse

from taobao_tiantiantejia import TaoBaoTianTianTeJia
import gc
from time import sleep
import re
import json
from settings import IS_BACKGROUND_RUNNING, TAOBAO_REAL_TIMES_SLEEP_TIME, MY_SPIDER_LOGS_PATH
import datetime
from logging import INFO, ERROR
import asyncio

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from fzutils.log_utils import set_logger
from fzutils.time_utils import (
    get_shanghai_time,
)
from fzutils.linux_utils import (
    daemon_init,
    restart_program,
)

async def run_forever():
    #### 实时更新数据
    # ** 不能写成全局变量并放在循环中, 否则会一直记录到同一文件中, 不能实现每日一志
    my_lg = set_logger(
        log_file_name=MY_SPIDER_LOGS_PATH + '/淘宝/天天特价/' + str(get_shanghai_time())[0:10] + '.txt',
        console_log_level=INFO,
        file_log_level=ERROR
    )

    tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
    # 由于不处理下架的商品，所以is_delete=0
    sql_str = '''
    select goods_id, is_delete, tejia_end_time, block_id, tag_id 
    from dbo.taobao_tiantiantejia 
    where site_id=19 and is_delete=0 and GETDATE()-modfiy_time>2 and MainGoodsID is not null
    '''

    try:
        result = list(tmp_sql_server._select_table(sql_str=sql_str))
    except TypeError:
        my_lg.error('TypeError错误, 导致原因: 数据库连接失败...(可能维护中)')
        return None

    my_lg.info('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
    my_lg.info(str(result))
    my_lg.info('--------------------------------------------------------')
    my_lg.info('待更新的goods_id个数: {0}'.format(len(result)))

    my_lg.info('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
    index = 1
    # tmp_taobao_tiantiantejia = TaoBaoTianTianTeJia(logger=my_lg)
    for item in result:     # 实时更新数据
        if index % 50 == 0:
            my_lg.info('正在重置，并与数据库建立新连接中...')
            # try: del tmp_sql_server
            # except: pass
            # gc.collect()
            tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
            my_lg.info('与数据库的新连接成功建立...')

        if tmp_sql_server.is_connect_success:
            tejia_end_time = item[2]
            # my_lg.info(str(tejia_end_time))

            if item[1] == 1:    # 原先下架的商品，扫描到不处理
                # tmp_sql_server.delete_taobao_tiantiantejia_expired_goods_id(goods_id=item[0])
                # my_lg.info('该商品goods_id[{0}]已售完, 删除成功!'.format(item[0]))
                my_lg.info('&&&&&& 该商品({0})原先状态为is_delete=1, 不进行实际删除操作! 索引为({1})'.format(item[0], str(index)))
                index += 1
                pass

            elif tejia_end_time < datetime.datetime.now():
                # 过期的不删除, 降为更新为常规爆款促销商品
                index = await update_expired_goods_to_normal_goods(
                    goods_id=item[0],
                    index=index,
                    tmp_sql_server=tmp_sql_server,
                    logger=my_lg
                )
                pass

            else:
                # 下面为天天特价商品信息更新
                '''
                ** 由于天天特价不会提前下架商品，就不对应更新特价时间段
                '''
                # # 先检查该商品在对应的子分类中是否已经被提前下架, 并获取到该商品的上下架时间
                # if index % 6 == 0:
                #     try: del tmp_taobao_tiantiantejia
                #     except: pass
                #     gc.collect()
                #     tmp_taobao_tiantiantejia = TaoBaoTianTianTeJia(logger=my_lg)
                #
                # tmp_body = await tmp_taobao_tiantiantejia.get_one_api_body(current_page=item[4], category=item[3])
                # if tmp_body == '':
                #     msg = '获取到的tmp_body为空str! 出错category为: ' + item[3]
                #     my_lg.error(msg)
                #     continue
                #
                # try:
                #     tmp_body = re.compile(r'\((.*?)\)').findall(tmp_body)[0]
                # except IndexError:
                #     msg = 're筛选body时出错, 请检查! 出错category为: ' + item[3]
                #     my_lg.error(msg)
                #     continue
                # tmp_sort_data = await tmp_taobao_tiantiantejia.get_sort_data_list(body=tmp_body)
                # if tmp_sort_data == 'no items':
                #     my_lg.info('该api接口获取到的item_list为no items!请检查')
                #     break
                # tejia_goods_list = await tmp_taobao_tiantiantejia.get_tiantiantejia_goods_list(data=tmp_sort_data)
                # # my_lg.info(str(tejia_goods_list))
                # await asyncio.sleep(.45)
                # # my_lg.info('111')

                '''
                研究发现已经上架的天天特价商品不会再被官方提前下架，所以此处什么都不做，跳过
                '''
                # if is_in_child_sort(tejia_goods_list, goods_id=item[0]) is False:     # 表示被官方提前下架
                #     # tmp_sql_server.delete_taobao_tiantiantejia_expired_goods_id(goods_id=item[0])
                #     # print('该商品goods_id[{0}]已被官方提前下架, 删除成功!'.format(item[0]))
                #     print('222')
                #     pass

                # else:       # 表示商品未被提前下架
                my_lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (item[0], str(index)))
                taobao = TaoBaoLoginAndParse(logger=my_lg)
                taobao.get_goods_data(item[0])
                goods_data = taobao.deal_with_data(goods_id=item[0])
                if goods_data != {}:
                    # tmp_time = await get_this_goods_id_tejia_time(tejia_goods_list, goods_id=item[0])
                    # if tmp_time != []:
                    #     begin_time, end_time = tmp_time
                    #
                    #     goods_data['goods_id'] = item[0]
                    #     goods_data['schedule'] = [{
                    #         'begin_time': begin_time,
                    #         'end_time': end_time,
                    #     }]
                    #     goods_data['tejia_begin_time'], goods_data['tejia_end_time'] = await tmp_taobao_tiantiantejia.get_tejia_begin_time_and_tejia_end_time(schedule=goods_data.get('schedule', [])[0])
                    #     await taobao.update_taobao_tiantiantejia_table(data=goods_data, pipeline=tmp_sql_server)
                    # else:
                    #     my_lg.info('该goods_id不在该api接口的商品中!!')
                    #     pass

                    goods_data['goods_id'] = item[0]
                    '''不专门更新上下架时间段'''
                    # goods_data['schedule'] = [{
                    #     'begin_time': begin_time,
                    #     'end_time': end_time,
                    # }]
                    # goods_data['tejia_begin_time'], goods_data['tejia_end_time'] = await tmp_taobao_tiantiantejia.get_tejia_begin_time_and_tejia_end_time(schedule=goods_data.get('schedule', [])[0])
                    if goods_data.get('is_delete', 0) == 1:
                        my_lg.info('@该商品已下架...')

                    await taobao.update_taobao_tiantiantejia_table(data=goods_data, pipeline=tmp_sql_server)

                else:
                    await asyncio.sleep(4)    # 否则休息4秒
                    pass

                await asyncio.sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)
                index += 1
                gc.collect()

        else:  # 表示返回的data值为空值
            my_lg.error('数据库连接失败，数据库可能关闭或者维护中')
            pass
        gc.collect()
    my_lg.info('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
    if get_shanghai_time().hour == 0:  # 0点以后不更新
        # sleep(60 * 60 * .5)
        pass

    else:
        sleep(5)
    gc.collect()

    return True

async def update_expired_goods_to_normal_goods(goods_id, index, tmp_sql_server, logger):
    '''
    过期的不删除, 降为更新为常规爆款促销商品
    :param goods_id:
    :param index:
    :param tmp_sql_server:
    :param logger:
    :return: index
    '''
    # tmp_sql_server.delete_taobao_tiantiantejia_expired_goods_id(goods_id=item[0])
    # logger.info('该商品goods_id({0})已过期, 天天特价结束时间为 [{1}], 删除成功!'.format(item[0], str(item[2].strftime('%Y-%m-%d %H:%M:%S'))))
    logger.info('++++++>>>| 此为过期商品, 正在更新! |<<<++++++')
    logger.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id, str(index)))
    taobao = TaoBaoLoginAndParse(logger=logger)
    data_before = taobao.get_goods_data(goods_id)
    if data_before.get('is_delete') == 1:  # 单独处理下架状态的商品
        data_before['goods_id'] = goods_id
        data_before['schedule'] = []
        '''不更新特价时间段'''
        # data_before['tejia_begin_time'], data_before['tejia_end_time'] = '', ''

        # logger.info('------>>>| 爬取到的数据为: %s' % str(data_before))
        await taobao.update_taobao_tiantiantejia_table(data_before, pipeline=tmp_sql_server)
        await asyncio.sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)  # 避免服务器更新太频繁
        index += 1
        try: del taobao
        except: pass
        gc.collect()

        return index

    goods_data = taobao.deal_with_data(goods_id=goods_id)
    if goods_data != {}:
        goods_data['goods_id'] = goods_id
        await taobao.update_expired_goods_id_taobao_tiantiantejia_table(data=goods_data, pipeline=tmp_sql_server)
    else:
        await asyncio.sleep(4)  # 否则休息4秒
        pass
    await asyncio.sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)
    index += 1
    try: del taobao
    except: pass
    gc.collect()

    return index

def is_in_child_sort(tejia_goods_list, goods_id):
    '''
    判断该商品在对应的子分类中是否已经被提前下架
    :param tejia_goods_list: 子类的分类list  [{'goods_id': , 'start_time': , 'end_time': ,}, ...]
    :param goods_id: 商品id
    :return: True(未被提前下架) or False(被提前下架)
    '''
    tmp_list = [item.get('goods_id', '') for item in tejia_goods_list]
    if tmp_list in tmp_list:
        return True
    else:
        return False

async def get_this_goods_id_tejia_time(tejia_goods_list, goods_id):
    '''
    得到该goods_id的上下架时间
    :param tejia_goods_list: 子类的分类list  [{'goods_id': , 'start_time': , 'end_time': ,}, ...]
    :param goods_id: 商品id
    :return: ['tejia_start_time', 'tejia_end_time'] or []
    '''
    for item in tejia_goods_list:
        if goods_id == item.get('goods_id', ''):
            return [item.get('start_time', ''), item.get('end_time', '')]
        else:
            pass
    return []

def main_2():
    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_forever())
        try: loop.close()
        except: pass
        gc.collect()
        restart_program()

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    main_2()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        main_2()
