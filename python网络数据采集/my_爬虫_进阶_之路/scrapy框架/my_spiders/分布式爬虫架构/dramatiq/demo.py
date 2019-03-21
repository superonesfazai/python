# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

"""
运行方式:

1. 在一个终端
$ dramatiq demo
2. 另一个终端
$ python3 example.py https://github.com
"""

import dramatiq
from sys import argv
from fzutils.spider.fz_requests import Requests

@dramatiq.actor
def count_words(url):
    response = Requests.get_url_body(url=url, use_proxy=False)
    count = len(response.text.split(" "))
    print(f"There are {count} words at {url!r}.")

if __name__ == "__main__":
    count_words.send(argv[1])