# coding:utf-8

'''
@author = super_fazai
@File    : 多进程+多线程_spider_demo.py
@connect : superonesfazai@gmail.com
'''

import etree
import time
import random
import urllib.request as request
from multiprocessing.pool import Pool
from threading import Thread

url = 'http://www.quanjing.com/creative/SearchCreative.aspx?id=7'

def get_pic_src(url:str)->list:
    response = request.urlopen(url)
    wb_data = response.read()
    html = etree.HTML(wb_data)
    pic_urls = html.xpath('//a[@class="item lazy"]/img/@src')

    return pic_urls

def allot(pic_urls:list,n:int)->list:
    # 根据给定的组数，分配url给每一组
    _len = len(pic_urls)
    base = int(_len / n)
    remainder = _len % n
    groups = [pic_urls[i * base:(i + 1) * base] for i in range(n)]
    remaind_group = pic_urls[n * base:]
    for i in range(remainder):
        groups[i].append(remaind_group[i])

    return [i for i in groups if i]

def download_one_pic(url:str,name:str,suffix:str='jpg'):
    path = '.'.join([name, suffix])
    response = request.urlopen(url)
    wb_data = response.read()
    with open(path,'wb') as f:
        f.write(wb_data)

def run_multithread_crawler(pic_urls:list,threads:int):
    begin = 0
    start = time.time()
    while 1:
        _threads = []
        urls = pic_urls[begin: begin + threads]
        if not urls:
            break
        for i in urls:
            ts = str(int(time.time()*10000))+str(random.randint(1,100000))
            t = Thread(target=download_one_pic, args=(i,ts))
            _threads.append(t)
        for t in _threads:
            t.setDaemon(True)
            t.start()
        for t in _threads:
            t.join()
        begin += threads
    end = time.time()
    print(u'下载完成,%d张图片,耗时:%.2fs' % (len(pic_urls), (end - start)))

# 下面使用多进程（进程数为CPU数，4）+ 多线程 （线程数设为50）
def mixed_process_thread_crawler(processors:int,threads:int):
    """
    main
    :param processors:
    :param threads:
    :return:
    """
    pool = Pool(processors)
    pic_urls = get_pic_src(url)
    url_groups = allot(pic_urls,processors)
    for group in url_groups:
        pool.apply_async(run_multithread_crawler, args=(group,threads))
    pool.close()
    pool.join()

mixed_process_thread_crawler(4,50)