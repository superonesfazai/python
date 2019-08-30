# coding:utf-8

'''
@author = super_fazai
@File    : proxy_checker_plus.py
@connect : superonesfazai@gmail.com
'''

from threading import (
    Thread,
    current_thread,
)
from queue import Queue
from fzutils.sql_utils import BaseSqlite3Cli
from fzutils.spider.async_always import *

from settings import (
    MIN_SCORE,
)
from utils import (
    _get_proxy_list,
    _get_local_ip,
    _add_to_white_list,
    _get_db_old_data,
    proxy_checker_welcome_page,
    _add_to_checked_proxy_list,
    _check_one_proxy,
    _insert_into_db,
    _delete_proxy_item,
    _update_db,
    _select_all_proxy_data_in_db,
    _get_ip_activity_time,
    _delete_proxy_in_db,
)
from db_controller import (
    create_proxy_obj_table,
    empty_db_proxy_data,
)

max_tri_proxy_num = 2000
db_path = 'proxy.db'

class TriProxyProducer(Thread):
    """
    三方代理获取的生产者
    """
    def run(self):
        global tri_proxy_queue, tri_id
        while True:
            try:
                if tri_proxy_queue.qsize() < max_tri_proxy_num:
                    proxy_list = _get_proxy_list(id=tri_id)
                    if proxy_list == []:
                        if tri_id == 1:
                            # 只短暂休眠, server(请求频繁)一允许通过就会成功拿到数据
                            # print('sleep {}s ...'.format(.5))
                            sleep(.5)
                        else:
                            # print('sleep {}s ...'.format(4.5))
                            sleep(4.5)

                    new_proxy_count = 0
                    for item in proxy_list:
                        tri_proxy_queue.put(item)
                        new_proxy_count += 1

                    if new_proxy_count > 0:
                        print('get_new_proxy_count: {}'.format(new_proxy_count))
                    else:
                        pass

                else:
                    print('tri_proxy_queue > 1000, pass')
                    continue

            except Exception as e:
                print(e)

class ProxyCheckerConsumer(Thread):
    """
    新获取到代理检测的消费者
    """
    def run(self):
        global tri_proxy_queue, tri_id, local_ip
        global new_checked_proxy_queue

        while True:
            try:
                if tri_proxy_queue.qsize() >= 1:
                    proxy_item = tri_proxy_queue.get()
                    ip = proxy_item.get('ip', '')
                    print('{}消费ing ip: {} ...'.format(
                        self.name,
                        ip,))
                    res = _check_one_proxy(local_ip=local_ip, item=proxy_item)
                    new_checked_proxy_queue.put(res)

                else:
                    continue

            except Exception as e:
                print(e)

class NewCheckedProxyConsumer(Thread):
    """
    新检测的代理的消费者(新代理符合要求的进行入库操作)
    """
    def run(self):
        global new_checked_proxy_queue
        while True:
            try:
                if new_checked_proxy_queue.qsize() >= 1:
                    checked_proxy_item = new_checked_proxy_queue.get()
                    used_label = checked_proxy_item.get('used', False)
                    if used_label:
                        print('{} new add 高匿ip 1个'.format(
                            self.name,))
                    else:
                        continue

                    sqlite3_cli = BaseSqlite3Cli(db_path=db_path)
                    _insert_into_db(
                        checked_proxy_list=[
                            checked_proxy_item,
                        ],
                        sqlite3_cli=sqlite3_cli,)

                else:
                    continue

            except Exception as e:
                print(e)

class ExpireProxyConsumer(Thread):
    """
    过期代理消费者(删除过期代理)
    """
    def run(self):
        while True:
            try:
                sqlite3_cli = BaseSqlite3Cli(db_path=db_path)
                db_proxy_item_list = _select_all_proxy_data_in_db(sqlite3_cli=sqlite3_cli)

                # 删除过期ip
                delete_count = 0
                activity_time = _get_ip_activity_time(id=tri_id)
                # print(activity_time)
                if isinstance(db_proxy_item_list, (list, tuple)):
                    for proxy_item in db_proxy_item_list:
                        ip = proxy_item[1]
                        score = proxy_item[3]
                        check_time = string_to_datetime(proxy_item[5])
                        now_time = get_shanghai_time()

                        # 两个判断条件分开: 针对不同情况进行优先级判断
                        time_diff = datetime_to_timestamp(now_time) - datetime_to_timestamp(check_time)
                        if time_diff < activity_time - 10:
                            continue

                        if score < MIN_SCORE:
                            continue

                        # print('now_time: {}, item_check_time: {}'.format(
                        #     now_time,
                        #     check_time, ))
                        delete_res = _delete_proxy_in_db(
                            ip=ip,
                            sqlite3_cli=sqlite3_cli)
                        if delete_res:
                            delete_count += 1
                        else:
                            pass
                else:
                    pass

                if delete_count > 0:
                    print('{}过期消费者 delete_ip_count: {}'.format(
                        self.name,
                        delete_count))
                else:
                    pass

            except Exception as e:
                print(e)

            finally:
                sleep(6.)

if __name__ == '__main__':
    # todo activity_time为None的先不进行处理, 默认activity_time都有实值,
    #  即不处理分数低的proxy, 只处理过期的
    tri_id = 1

    proxy_checker_welcome_page()
    local_ip = _get_local_ip()
    create_proxy_obj_table()
    # 每次启动先清空一次过期table
    print('Empty db old ip...')
    empty_db_proxy_data()
    # 添加本机到白名单
    _add_to_white_list(
        tri_id=tri_id,
        local_ip=local_ip,)

    # 新获取的代理的队列
    tri_proxy_queue = Queue()
    # 新代理已被检测的队列
    new_checked_proxy_queue = Queue()

    for i in range(1):
        tri_proxy_producer = TriProxyProducer()
        tri_proxy_producer.start()

    for i in range(15):
        proxy_checker_consumer = ProxyCheckerConsumer()
        proxy_checker_consumer.start()

    for i in range(5):
        new_checked_proxy_consumer = NewCheckedProxyConsumer()
        new_checked_proxy_consumer.start()

    for i in range(1):
        expire_proxy_consumer = ExpireProxyConsumer()
        expire_proxy_consumer.start()
