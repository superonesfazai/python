# coding:utf-8

'''
@author = super_fazai
@File    : juanpi_pintuan_real-times_update.py
@Time    : 2017/12/23 14:31
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from juanpi_parse import JuanPiParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

import gc
from time import sleep
import json
from settings import IS_BACKGROUND_RUNNING
import time

from sql_str_controller import (
    jp_select_str_2,
    jp_delete_str_1,
    jp_delete_str_2,
    jp_update_str_7,)
from multiplex_code import (
    _block_get_new_db_conn,
    _handle_goods_shelves_in_auto_goods_table,
    _block_print_db_old_data,)

from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,
)
from fzutils.linux_utils import daemon_init

def run_forever():
    while True:
        #### 实时更新数据
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        try:
            sql_cli._delete_table(sql_str=jp_delete_str_1)
            result = list(sql_cli._select_table(sql_str=jp_select_str_2))
        except TypeError:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            _block_print_db_old_data(result=result)
            index = 1
            # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
            juanpi_pintuan = JuanPiParse()
            for item in result:  # 实时更新数据
                goods_id = item[0]
                if index % 6 == 0:
                    try:
                        del juanpi_pintuan
                    except:
                        pass
                    gc.collect()
                    juanpi_pintuan = JuanPiParse()

                sql_cli = _block_get_new_db_conn(db_obj=sql_cli, index=index, remainder=50)
                if sql_cli.is_connect_success:
                    try:
                        pintuan_end_time = json.loads(item[1])[0].get('end_time')
                    except IndexError:
                        print('获取pintuan_end_time时索引异常!出错goods_id:{0}'.format(goods_id))
                        _handle_goods_shelves_in_auto_goods_table(
                            goods_id=goods_id,
                            sql_cli=sql_cli,
                            update_sql_str=jp_update_str_7,)
                        continue
                    pintuan_end_time = int(str(time.mktime(time.strptime(pintuan_end_time, '%Y-%m-%d %H:%M:%S')))[0:10])
                    # print(pintuan_end_time)

                    if item[2] == 1 or pintuan_end_time < int(datetime_to_timestamp(get_shanghai_time())):
                        _handle_goods_shelves_in_auto_goods_table(
                            goods_id=goods_id,
                            sql_cli=sql_cli,
                            update_sql_str=jp_update_str_7,)
                        print('该goods_id[{0}]已过期或者售完，逻辑删除成功!'.format(goods_id))
                    else:
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (goods_id, index))
                        juanpi_pintuan.get_goods_data(goods_id=goods_id)
                        data = juanpi_pintuan.deal_with_data()
                        if data == {}:
                            continue

                        data['goods_id'] = goods_id
                        juanpi_pintuan.to_right_and_update_pintuan_data(data=data, pipeline=sql_cli)

                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                index += 1
                gc.collect()
                sleep(1.2)
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(5 * 60)
        gc.collect()

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    run_forever()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        run_forever()