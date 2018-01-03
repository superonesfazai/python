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
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from taobao_tiantiantejia import TaoBaoTianTianTeJia
import gc
from time import sleep
import os, re, pytz, datetime
import json
from settings import IS_BACKGROUND_RUNNING
import datetime


def run_forever():
    #### 实时更新数据
    while True:
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        try:
            result = list(tmp_sql_server.select_taobao_tiantian_tejia_all_goods_id())
        except TypeError as e:
            print('TypeError错误, 原因数据库连接失败...(可能维护中)')
            result = None
        if result is None:
            pass
        else:
            print('------>>> 下面是数据库返回的所有符合条件的goods_id <<<------')
            print(result)
            print('--------------------------------------------------------')

            print('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))
            index = 1
            tmp_taobao_tiantiantejia = TaoBaoTianTianTeJia()
            for item in result:  # 实时更新数据
                data = {}
                if index % 50 == 0:  # 每50次重连一次，避免单次长连无响应报错
                    print('正在重置，并与数据库建立新连接中...')
                    # try:
                    #     del tmp_sql_server
                    # except:
                    #     pass
                    # gc.collect()
                    tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
                    print('与数据库的新连接成功建立...')

                if tmp_sql_server.is_connect_success:
                    tejia_end_time = item[2]
                    # print(tejia_end_time)

                    if item[1] == 1:
                        tmp_sql_server.delete_taobao_tiantiantejia_expired_goods_id(goods_id=item[0])
                        print('该商品goods_id[{0}]已售完, 删除成功!'.format(item[0]))

                    elif tejia_end_time < datetime.datetime.now():
                        '''
                        过期的不删除, 降为更新为常规爆款促销商品
                        '''
                        # tmp_sql_server.delete_taobao_tiantiantejia_expired_goods_id(goods_id=item[0])
                        # print('该商品goods_id({0})已过期, 天天特价结束时间为 [{1}], 删除成功!'.format(item[0], item[2].strftime('%Y-%m-%d %H:%M:%S')))
                        print('++++++>>>| 此为过期商品, 正在更新! |<<<++++++')
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (item[0], index))
                        taobao = TaoBaoLoginAndParse()
                        taobao.get_goods_data(item[0])
                        goods_data = taobao.deal_with_data(goods_id=item[0])
                        if goods_data != {}:
                            goods_data['goods_id'] = item[0]
                            taobao.update_expired_goods_id_taobao_tiantiantejia_table(data=goods_data, pipeline=tmp_sql_server)
                        else:
                            pass
                        sleep(2)
                        index += 1
                        gc.collect()

                    else:
                        '''
                        下面为天天特价商品信息更新
                        '''
                        '''
                        先检查该商品在对应的子分类中是否已经被提前下架, 并获取到该商品的上下架时间
                        '''
                        # &extQuery=tagId%3A1010142     要post的数据, 此处直接用get模拟
                        tmp_url = 'https://metrocity.taobao.com/json/fantomasItems.htm?appId=9&pageSize=1000&_input_charset=utf-8&blockId={0}&extQuery=tagId%3A{1}'.format(
                            str(item[3]), item[4]
                        )
                        # print(tmp_url)

                        if index % 6 == 0:
                            tmp_taobao_tiantiantejia = TaoBaoTianTianTeJia()

                        tmp_body = tmp_taobao_tiantiantejia.get_url_body(url=tmp_url)
                        tejia_goods_list = tmp_taobao_tiantiantejia.get_tiantiantejia_goods_list(body=tmp_body)
                        # print(tejia_goods_list)
                        sleep(.45)
                        # print('111')

                        '''
                        研究发现已经上架的天天特价商品不会再被官方提前下架，所以此处什么都不做，跳过
                        '''
                        # if is_in_child_sort(tejia_goods_list, goods_id=item[0]) is False:     # 表示被官方提前下架
                        #     # tmp_sql_server.delete_taobao_tiantiantejia_expired_goods_id(goods_id=item[0])
                        #     # print('该商品goods_id[{0}]已被官方提前下架, 删除成功!'.format(item[0]))
                        #     print('222')
                        #     pass

                        # else:       # 表示商品未被提前下架
                        print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (item[0], index))
                        taobao = TaoBaoLoginAndParse()
                        taobao.get_goods_data(item[0])
                        goods_data = taobao.deal_with_data(goods_id=item[0])
                        if goods_data != {}:
                            tmp_time = get_this_goods_id_tejia_time(tejia_goods_list, goods_id=item[0])
                            if tmp_time != []:
                                begin_time, end_time = tmp_time

                                goods_data['goods_id'] = item[0]
                                goods_data['schedule'] = [{
                                    'begin_time': begin_time,
                                    'end_time': end_time,
                                }]
                                goods_data['tejia_begin_time'], goods_data['tejia_end_time'] = tmp_taobao_tiantiantejia.get_tejia_begin_time_and_tejia_end_time(schedule=goods_data.get('schedule', [])[0])
                                taobao.update_taobao_tiantiantejia_table(data=goods_data, pipeline=tmp_sql_server)
                            else:
                                pass
                        else:
                            pass
                        sleep(1.5)
                        index += 1
                        gc.collect()

                else:  # 表示返回的data值为空值
                    print('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                gc.collect()
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        if get_shanghai_time().hour == 0:  # 0点以后不更新
            sleep(60 * 60 * 5.5)
        else:
            sleep(5)
        gc.collect()

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

def get_this_goods_id_tejia_time(tejia_goods_list, goods_id):
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
