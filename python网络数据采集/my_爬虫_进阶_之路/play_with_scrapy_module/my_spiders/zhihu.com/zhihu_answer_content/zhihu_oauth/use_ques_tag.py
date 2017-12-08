# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

import random

from zhihu_oauth import ZhihuClient, ActType
from zhihu_oauth import ts2str
from zhihu_oauth.exception import NeedCaptchaException
import requests
from bs4 import BeautifulSoup
import os
import time
import json
from zhihu_oauth import ZhihuClient
from random import randint

import pandas as pd

USER_TRY_CSV_PATH = '/users/gliam/desktop/user_try.csv'     # user_try.csv 的path
SAVE_TO_CSV_A_PATH = 'd:/data_answer_info.csv'              # 存储的位置

def save_to_csv_a(links):
    file = SAVE_TO_CSV_A_PATH
    with open(file, "a", encoding='utf-8') as f:
        for i in links:
            if i is not None:
                output = ""
                for j in i:
                    output = "%s, %s" % (output, j)
                f.write(output[2:] + "\n")
    print("Data saved!")

class MyCrawler:
    def __init__(self, id ,client):
        self.id = id
        self.client = client

    def crawling_answer(self, line):
        client1 = self.client.people(line)
        links = []
        try:
            for act in client1.activities:
                if act.type == ActType.CREATE_ANSWER:
                    print(ts2str(act.target.created_time))
                    b = random.randint(1, 3)
                    time.sleep(2 + b)

                    print('id', client1.id)
                    links.append(client1.id)

                    links.append(act.target.id)

                    links.append(act.target.question.id)

                    if act.target.question.created_time:
                        links.append(ts2str(act.target.question.created_time))
                    else:
                        links.append("null")

                    if act.target.created_time:
                        links.append(ts2str(act.target.created_time))
                    else:
                        links.append("null")
                    # print(act.target.question.title)
                    if act.target.question.title:
                        str_title = act.target.question.title
                        str_title1 = str_title.replace('，', '_')
                        str_title2 = str_title1.replace(',', '_')
                        links.append(str_title2)
                    else:
                        links.append("null")

                    # act.target.save(path='C:/Users/gliam/Desktop/data_answer_info',filename=act.target.id)

                    if act.target.can_comment.status:
                        # print(act.target.can_comment.status)
                        links.append(act.target.can_comment.status)
                    else:
                        links.append("null")
                    # print(act.target.comment_count)

                    links.append(act.target.comment_count)
                    links.append(act.target.thanks_count)
                    links.append(act.target.voteup_count)
                    print(links)

                    for x in act.target.question.topics:
                        links.append(x.name)
                        links.append(x.question_count)
                        links.append(x.best_answer_count)
                        links.append(x.unanswered_count)
                        links.append(x.follower_count)
                    print([x.name for x in act.target.question.topics])
                    # links.append([x.name for x in act.target.question.topics])
                    # print(links)
                    # if act.target.quesion.topics:
                        # links.append(act.target.question.topic.question_count)
                        # links.append(act.target.question.topic.best_answer_count)
                        # links.append(act.target.question.topic.follower_count)
                        # links.append(act.target.question.topic.unanswered_count)

                    while len(links) % 60 != 0:
                        links.append('')
            return links
        except:
            while len(links) % 60 != 0:
                links.append('')
            return links


'''
    def loginnew(self):
        tmp_proxies = {
            'http': self.proxies['http'][randint(1, 100)]
        }

        #print ("Tmp Proxy:", tmp_proxies)
        try:
            # client.login('wuli791xi@163.com', 'durant')
            self.client.set_proxy(tmp_proxies)
            print(tmp_proxies)
        except NeedCaptchaException:
            print("Login New Error")
            with open('a.gif', 'wb') as f:
                f.write(self.client.get_captcha())
            captcha = input('please input captcha:')
            self.client.login('wuli791xi@163.com', 'durant', captcha)

    def get_proxy_ip_from_ip_pool(self):

        base_url = 'http://127.0.0.1:8000'
        result = requests.get(base_url).json()

        result_ip_list = {}
        result_ip_list['http'] = []
        for item in result:
            tmp_url = 'http://' + str(item[0]) + ':' + str(item[1])
            result_ip_list['http'].append(tmp_url)

        self.proxies = result_ip_list
        # pprint(result_ip_list)

        return result_ip_list
'''


def main():
    client = ZhihuClient()

    try:
        client.login('wuli791xi@163.com', 'durant')

    except NeedCaptchaException:
        print("Login Error")
        with open('a.gif', 'wb') as f:
            f.write(client.get_captcha())
        captcha = input('please input captcha:')
        client.login('wuli791xi@163.com', 'durant', captcha)

    max_lines = 1
    line_saved = 0
    data_out_list_a = list()

    with open(USER_TRY_CSV_PATH) as f:
        for line in f.readlines():

            craw_id = line.strip("\n")
            craw = MyCrawler(craw_id, client)
            print(craw_id)

            data_a = craw.crawling_answer(craw_id)
            if len(data_a) % 60 == 0:
                times = int(len(data_a)/60)
                for i in range(times):
                    data_out_list_a.append(data_a[60*i : 60*(i+1)])
            else:
                print("Invalid Output")

            a = random.randint(1, 5)
            time.sleep(a)

            line_saved += 1

            if line_saved == max_lines:
                save_to_csv_a(data_out_list_a)

                data_out_list_a = list()

                line_saved = 0

if __name__=="__main__":
    main()
