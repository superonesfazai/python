# coding:utf-8

'''
@author = super_fazai
@File    : 嗅事多线程.py
@Time    : 2016/12/17 22:08
@connect : superonesfazai@gmail.com
'''

"""
简单实现多线程抓取
"""

import requests
from lxml import etree
from retrying import retry
import json
from queue import Queue
import threading

class QiushiSpider:
    def __init__(self):
        self.url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_queue = Queue()

    def get_url_list(self):
        for i in range(1, 14):
            self.url_queue.put(self.url.format(i))

    @retry(stop_max_attempt_number=3)
    def _parse_url(self, url):
        response = requests.get(url, headers=self.headers, timeout=5)
        assert response.status_code == 200
        html  = etree.HTML(response.content)

        return html

    def parse_url(self):
        while True:
            url = self.url_queue.get()
            try:
                html = self._parse_url(url)
            except Exception as e:
                print(e)
                return None
            self.html_queue.put(html)
            self.url_queue.task_done()

    def get_content_list(self):
        while True:
            html = self.html_queue.get()
            if html is not None:
                div_list = html.xpath("//div[contains(@class,'qiushi_tag_')]")
                content_list = []
                for div in div_list:
                    item={}
                    src = div.xpath("./div[@class='author clearfix']/a[1]/img/@src")
                    item["src"] = "https:" + src[0] if len(src) > 0 else None
                    author_name = div.xpath("./div[@class='author clearfix']/a[1]/img/@alt")
                    item["author_name"] = author_name[0] if len(author_name) > 0 else None
                    author_gender = div.xpath(".//div[contains(@class,'articleGender')]/@class")
                    item["author_gender"] = author_gender[0].split(" ")[-1].replace("Icon", "") if len(author_gender) > 0 else None
                    author_content = div.xpath(".//div[@class='content']/span/text()")
                    item["author_content"] = [i.replace("\n", "") for i in author_content]
                    author_age = div.xpath(".//div[contains(@class,'articleGender')]/text()")
                    item["author_age"] = author_age[0] if len(author_age) > 0 else None
                    content_list.append(item)
                self.content_queue.put(content_list)
            self.html_queue.task_done()

    def save_content_list(self):
        while True:
            content_list = self.content_queue.get()
            with open("duanzizizi.txt", "a") as f:
                for content in content_list:
                    f.write(json.dumps(content, ensure_ascii=False, indent=4))
                    f.write("\n")

            self.content_queue.task_done()

    def run(self):
        threading_list = []
        t_url = threading.Thread(target=self.get_url_list)
        threading_list.append(t_url)
        for i in range(10):
            t_parse_url = threading.Thread(target=self.parse_url)
            threading_list.append(t_parse_url)

        t_get_content = threading.Thread(target=self.get_content_list)
        threading_list.append(t_get_content)

        t_save = threading.Thread(target=self.save_content_list)
        threading_list.append(t_save)
        for t in threading_list:
            t.setDaemon(True)
            t.start()

        for q in [self.url_queue, self.html_queue, self.content_queue]:
            q.join()

if __name__ == '__main__':
    qiushi = QiushiSpider()
    qiushi.run()