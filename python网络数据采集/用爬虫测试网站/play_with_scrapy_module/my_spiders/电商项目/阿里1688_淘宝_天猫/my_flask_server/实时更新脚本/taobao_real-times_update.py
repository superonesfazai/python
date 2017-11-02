# coding:utf-8

'''
@author = super_fazai
@File    : ali_1688_real-times_update.py
@Time    : 2017/10/28 07:24
@connect : superonesfazai@gmail.com
'''
import sys
sys.path.append('..')

from taobao_login_and_parse_idea2 import TaoBaoLoginAndParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
import gc
from time import sleep

if __name__ == '__main__':
    #### 实时更新数据
    while True:
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        try:
            result = list(tmp_sql_server.select_taobao_all_goods_id())
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
            for item in result:  # 实时更新数据
                data = {}
                taobao = TaoBaoLoginAndParse()
                print('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%d)' % (item[0], index))
                taobao.get_goods_data(item[0])
                data = taobao.deal_with_data(goods_id=item[0])
                if data != {}:
                    data['goods_id'] = item[0]
                    # print('------>>>| 爬取到的数据为: ', data)

                    taobao.to_right_and_update_data(data, pipeline=tmp_sql_server)
                else:  # 表示返回的data值为空值
                    pass
                index += 1
                sleep(.2)
                del taobao
                gc.collect()
            print('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
        sleep(2)
        del tmp_sql_server
        del result
        gc.collect()


