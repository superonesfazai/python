# coding:utf-8

'''
@author = super_fazai
@File    : pc_headline.py
@connect : superonesfazai@gmail.com
'''

"""
淘宝pc版头条
    第一次返回的接口中有后续的publishId参数, 后续直接提交即可
"""

from pprint import pprint
from queue import Queue
from multiprocessing import Pool
from fzutils.spider.fz_requests import Requests
from fzutils.internet_utils import get_random_pc_ua
from fzutils.common_utils import json_2_dict

def get_all_headline_articles():
    '''
    得到淘宝所有的头条文章
    :return:
    '''
    def get_one_page_list(publish_id='0') -> list:
        '''得到一个文章接口的数据'''
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            # 'referer': 'https://headline.taobao.com/feed/feedList.htm?spm=a21bo.2017.226762.2.5af911d91DLSyX',
            'authority': 'headline.taobao.com',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = (
            ('columnId', '0'),
            ('publishId', publish_id),
        )
        url = 'https://headline.taobao.com/feed/feedQuery.do'
        data = json_2_dict(Requests.get_url_body(url=url, headers=headers, params=params)).get('data', [])
        if data == []:
            return []

        return data

    def one_task(publish_id) -> list:
        '''一个任务'''
        nonlocal queue, all

        one = get_one_page_list(publish_id=publish_id)
        # pprint(one)
        if one != []:
            [queue.put(item.get('publishId', '')) for item in one]

        label = '+' if one != [] else '-'
        print('[{}] {}'.format(label, publish_id))

        return one

    def add_all(one) -> bool:
        '''修改all'''
        nonlocal all
        all += one

        return True

    queue = Queue()
    pool = Pool(processes=3)
    first_page_info = get_one_page_list()
    [queue.put(item.get('publishId', '')) for item in first_page_info]

    all = first_page_info
    results = []
    while not queue.empty():
        publish_id = queue.get()
        print(publish_id)
        results.append(pool.apply_async(func=one_task, args=(publish_id,)))

    print('请耐心等待所有进程完成...')
    pool.close()    # 等待所有完成
    pool.join()
    for i in results:
        add_all(i.get())
    # while results != []:
    #     for i in results:
    #         print(i)
    #         try:
    #             success_res = i.successful()
    #         except AssertionError:
    #             success_res = False
    #         if success_res:
    #             print(i.get())
    #             try:
    #                 results.remove(i)
    #             except:
    #                 pass
    #         else:
    #             pass


    # 根据发布publishId的大小, 进行排序, 最新发布在最前面
    all = list(reversed(sorted(all, key=lambda item: int(item.get('publishId')))))
    # pprint(all)
    print(len(all))

    return all

if __name__ == '__main__':
    get_all_headline_articles()