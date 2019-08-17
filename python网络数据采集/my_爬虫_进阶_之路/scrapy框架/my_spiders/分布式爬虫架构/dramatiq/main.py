# coding:utf-8

'''
@author = super_fazai
@File    : main.py
@connect : superonesfazai@gmail.com
'''

from tasks import get_url_body
from dramatiq import group as dramatiq_group
from dramatiq import pipeline as dramatiq_pipeline
from fzutils.spider.fz_requests import PROXY_TYPE_HTTPS
from fzutils.spider.async_always import *

def main():
    # target_url = 'https://httpbin.org/get'
    target_url = 'http://0.0.0.0:8001/get_all'
    target_url_list = [target_url for i in range(200)]

    tasks = []
    for target_url in target_url_list:
        # count_words.send(target_url)
        tasks.append(get_url_body.send_with_options(
            args=[
                target_url,
                False if '0.0.0.0' in target_url else True,
                PROXY_TYPE_HTTPS,
                6,
            ],
            delay=None,))

    # 测试, 获取结果失败
    # group = dramatiq_group(children=tasks).run()
    # group.wait(timeout=50)
    # for res in group.get_results(
    #         block=True,
    #         timeout=5 * 1000):
    #     print(res)

    # 获取成功
    _consumer(tasks=tasks, target_url=target_url)

@func_time
def _consumer(tasks: list, target_url):
    for message in tasks:
        try:
            res = message.get_result(
                block=True,)
        except Exception as e:
            print(e)
            continue

        if 'httpbin' in target_url:
            data = json_2_dict(
                json_str=res,
                default_res={}).get('origin', '')
            print(data)
        elif '0.0.0.0' in target_url:
            data = json_2_dict(
                json_str=res,
                default_res=[])
            print(len(data))

        else:
            print(res)

if __name__ == "__main__":
    main()