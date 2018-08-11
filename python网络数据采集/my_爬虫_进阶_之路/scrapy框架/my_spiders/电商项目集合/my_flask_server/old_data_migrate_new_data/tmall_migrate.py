# coding:utf-8

'''
@author = super_fazai
@File    : tmall_migrate.py
@Time    : 2018/3/15 09:42
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from tmall_parse import TmallParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
import gc
from time import sleep
import os, re, pytz, datetime
from settings import IS_BACKGROUND_RUNNING

def run_forever():
    while True:
        #### 实时更新数据
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        sql_str = 'select SiteID, GoodsID, IsDelete, MyShelfAndDownTime, Price, TaoBaoPrice from dbo.GoodsInfoAutoGet where SiteID=3 or SiteID=4 or SiteID=6 order by ID desc'
        sql_str_2 = 'select GoodsOutUrl, goods_id from db_k85u.dbo.goodsinfo where OutGoodsType<=13 and onoffshelf=1 and not exists (select maingoodsid from gather.dbo.GoodsInfoAutoGet c where c.maingoodsid=goodsinfo.goods_id)'
        try:
            result = list(tmp_sql_server._select_table(sql_str=sql_str))
            result_2 = list(tmp_sql_server._select_table(sql_str=sql_str_2, params=None))
        except TypeError as e:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
            result_2 = []
        if result is None:
            pass
        else:
            print('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
            print(result_2)
            print('--------------------------------------------------------')

            print('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
            index = 1
            # 释放内存,在外面声明就会占用很大的，所以此处优化内存的方法是声明后再删除释放
            tmall = TmallParse()
            for item in result_2:  # 实时更新数据
                if index % 5 == 0:
                    tmall = TmallParse()
                    gc.collect()

                if index % 50 == 0:    # 每50次重连一次，避免单次长连无响应报错
                    print('正在重置，并与数据库建立新连接中...')
                    # try:
                    #     del tmp_sql_server
                    # except:
                    #     pass
                    # gc.collect()
                    tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                    print('与数据库的新连接成功建立...')

                if tmp_sql_server.is_connect_success:
                    goods_id = tmall.get_goods_id_from_url(item[0])
                    if goods_id == []:
                        print('@@@ 原地址为: ', item[0])
                        continue
                    else:
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (goods_id[1], index))
                        data = tmall.get_goods_data(goods_id=goods_id)
                        if isinstance(data, int):
                            continue

                        if data.get('is_delete') == 1:
                            data['goods_id'] = goods_id[1]

                            # 改进判断，根据传入数据判断是天猫，还是天猫超市，还是天猫国际
                            #####################################################
                            if goods_id[0] == 0:  # [0, '1111']
                                wait_to_deal_with_url = 'https://detail.tmall.com/item.htm?id=' + goods_id[1]  # 构造成标准干净的天猫商品地址
                            elif goods_id[0] == 1:  # [1, '1111']
                                wait_to_deal_with_url = 'https://chaoshi.detail.tmall.com/item.htm?id=' + goods_id[1]
                            elif goods_id[0] == 2:  # [2, '1111', 'https://xxxxx']
                                wait_to_deal_with_url = str(goods_id[2]) + '?id=' + goods_id[1]
                            else:
                                continue
                            data['goods_url'] = wait_to_deal_with_url
                            data['username'] = '18698570079'
                            data['main_goods_id'] = item[1]

                            # print('------>>>| 爬取到的数据为: ', data)
                            result = tmall.old_tmall_goods_insert_into_new_table(data, pipeline=tmp_sql_server)
                            if result is False:
                                print('出错商品的地址为: ', item[0])
                            else:
                                pass
                            index += 1
                            gc.collect()
                            sleep(1.2)
                            continue
                        else:
                            pass

                        data = tmall.deal_with_data()
                        if data != {}:
                            data['goods_id'] = goods_id[1]

                            # 改进判断，根据传入数据判断是天猫，还是天猫超市，还是天猫国际
                            #####################################################
                            if goods_id[0] == 0:  # [0, '1111']
                                wait_to_deal_with_url = 'https://detail.tmall.com/item.htm?id=' + goods_id[1]  # 构造成标准干净的天猫商品地址
                            elif goods_id[0] == 1:  # [1, '1111']
                                wait_to_deal_with_url = 'https://chaoshi.detail.tmall.com/item.htm?id=' + goods_id[1]
                            elif goods_id[0] == 2:  # [2, '1111', 'https://xxxxx']
                                wait_to_deal_with_url = str(goods_id[2]) + goods_id[1]
                            else:
                                continue
                            data['goods_url'] = wait_to_deal_with_url
                            data['username'] = '18698570079'
                            data['main_goods_id'] = item[1]

                            # print('------>>>| 爬取到的数据为: ', data)
                            tmall.old_tmall_goods_insert_into_new_table(data, pipeline=tmp_sql_server)
                        else:  # 表示返回的data值为空值
                            pass
                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                index += 1
                # try:
                #     del tmall
                # except:
                #     pass
                gc.collect()
                sleep(2)
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(5)
        # del ali_1688
        gc.collect()

def get_shanghai_time():
    '''
    时区处理，时间处理到上海时间
    '''
    tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
    now_time = datetime.datetime.now(tz)

    # 处理为精确到秒位，删除时区信息
    now_time = re.compile(r'\..*').sub('', str(now_time))
    # 将字符串类型转换为datetime类型
    now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

    return now_time

def daemon_init(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    '''
    杀掉父进程，独立子进程
    :param stdin:
    :param stdout:
    :param stderr:
    :return:
    '''
    sys.stdin = open(stdin, 'r')
    sys.stdout = open(stdout, 'a+')
    sys.stderr = open(stderr, 'a+')
    try:
        pid = os.fork()
        if pid > 0:     # 父进程
            os._exit(0)
    except OSError as e:
        sys.stderr.write("first fork failed!!" + e.strerror)
        os._exit(1)

    # 子进程， 由于父进程已经退出，所以子进程变为孤儿进程，由init收养
    '''setsid使子进程成为新的会话首进程，和进程组的组长，与原来的进程组、控制终端和登录会话脱离。'''
    os.setsid()
    '''防止在类似于临时挂载的文件系统下运行，例如/mnt文件夹下，这样守护进程一旦运行，临时挂载的文件系统就无法卸载了，这里我们推荐把当前工作目录切换到根目录下'''
    os.chdir("/")
    '''设置用户创建文件的默认权限，设置的是权限“补码”，这里将文件权限掩码设为0，使得用户创建的文件具有最大的权限。否则，默认权限是从父进程继承得来的'''
    os.umask(0)

    try:
        pid = os.fork()  # 第二次进行fork,为了防止会话首进程意外获得控制终端
        if pid > 0:
            os._exit(0)  # 父进程退出
    except OSError as e:
        sys.stderr.write("second fork failed!!" + e.strerror)
        os._exit(1)

    # 孙进程
    #   for i in range(3, 64):  # 关闭所有可能打开的不需要的文件，UNP中这样处理，但是发现在python中实现不需要。
    #       os.close(i)
    sys.stdout.write("Daemon has been created! with pid: %d\n" % os.getpid())
    sys.stdout.flush()  # 由于这里我们使用的是标准IO，这里应该是行缓冲或全缓冲，因此要调用flush，从内存中刷入日志文件。

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