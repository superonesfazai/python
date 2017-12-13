# coding:utf-8

'''
@author = super_fazai
@File    : my_zhihu_use_oauth.py
@Time    : 2017/12/12 11:58
@connect : superonesfazai@gmail.com
'''

from __future__ import unicode_literals, print_function
from zhihu_oauth import (ZhihuClient, ActType, ts2str)
from zhihu_oauth.exception import NeedCaptchaException
from my_yun_da_ma import my_yun_da_ma
from settings import (email_or_phone, password, USER_CSV_PATH, CSV_SAVE_PATH, TOKEN_FILE)
from time import sleep
from random import randint
import os
import requests

class MyCrawler(object):
    def __init__(self, id ,client):
        super().__init__()
        self.id = id
        self.client = client

    def crawling_answer(self, line):
        client1 = self.client.people(line)
        links = []
        try:
            for act in client1.activities:
                if act.type == ActType.CREATE_ANSWER:
                    # CREATE_ANSWER      回答问题          :any:`Answer`
                    print(ts2str(act.target.created_time))
                    # sleep(randint(1, 3))

                    # print('------>>>| 正在爬取的用户id为: ', client1.id)
                    links.append(client1.id)
                    links.append(act.target.id)
                    links.append(act.target.question.id)

                    if act.target.question.created_time:
                        # 问题创建的时间
                        links.append(ts2str(act.target.question.created_time))
                    else:
                        links.append("null")

                    if act.target.created_time:
                        links.append(ts2str(act.target.created_time))
                    else:
                        links.append("null")

                    # 问题的标题
                    if act.target.question.title:
                        title = act.target.question.title
                        title = title.replace('，', '_')
                        title = title.replace(',', '_')
                        links.append(title)
                    else:
                        title = 'null'
                        links.append(title)
                    print('------>>>| 问题的标题为: ', title)

                    # act.target.save(path='C:/Users/gliam/Desktop/data_answer_info',filename=act.target.id)

                    if act.target.can_comment.status:
                        # 当允许评论status为True时
                        # print(act.target.can_comment.status)
                        links.append(act.target.can_comment.status)
                    else:
                        links.append("null")
                    # print(act.target.comment_count)

                    comment_count = act.target.comment_count        # 评论数
                    thanks_count = act.target.thanks_count          # 感谢数
                    voteup_count = act.target.voteup_count          # 赞成数
                    links.append(comment_count)
                    links.append(thanks_count)
                    links.append(voteup_count)
                    # print(links)
                    print(comment_count, ', ', thanks_count, ', ', voteup_count)

                    for x in act.target.question.topics:
                        name = x.name                               # 用户昵称
                        question_count = x.question_count           # 问题计数
                        best_answer_count = x.best_answer_count     # 最佳评论数
                        unanswered_count = x.unanswered_count       # 没有回答的问题计数
                        follower_count = x.follower_count           # follwer人数
                        links.append(name)
                        links.append(question_count)
                        links.append(best_answer_count)
                        links.append(unanswered_count)
                        links.append(follower_count)
                        print(name, ' ',  question_count, ' ', best_answer_count, ' ', unanswered_count, ' ', follower_count)

                    print('问题的类型为: ', [x.name for x in act.target.question.topics])
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

def save_to_csv_a(links, client):
    file = CSV_SAVE_PATH
    # print(links)
    if links == []:
        print('links为[]，此处跳过!')
        with open('./data/b.png', 'wb') as f:
            f.write(client.my_get_captcha())
        result = my_yun_da_ma()
        client.my_captcha_appeal_post(result)
        # my_captcha_appeal = input('请输入操作频繁获取到的验证码: ')
        pass
    else:
        with open(file, "a", encoding='utf-8') as f:
            for i in links:
                if i is not None:
                    output = ""
                    for j in i:
                        output = "%s, %s" % (output, j)
                    f.write(output[2:] + "\n")
        print("该data已经被保存!")

def main():
    client = ZhihuClient()

    try:
        # client.login(email_or_phone, password)
        client.login_in_terminal(username=email_or_phone, password=password)
        client.save_token(TOKEN_FILE)          # 保存登录会话,留着以后登录用
        # raise NeedCaptchaException
    except NeedCaptchaException:
        # 保存验证码并提示输入，重新登录
        with open('a.gif', 'wb') as f:
            f.write(client.get_captcha())
        captcha = input('请输入验证码: ')
        client.login(email_or_phone, password, captcha)

    data_out_list_a = []
    line_saved = 0
    max_lines = 1

    with open(USER_CSV_PATH) as file:
        for line in file.readlines():
            crawl_id = line.strip('\n')
            my_crawl = MyCrawler(crawl_id, client)
            print('------>>>| 待爬取的用户的知乎id为: ', crawl_id)

            data_a = my_crawl.crawling_answer(crawl_id)
            print('该用户爬取完毕'.center(60, '*'))
            if len(data_a) % 60 == 0:
                tmp_time = int(len(data_a) / 60)
                for i in range(tmp_time):
                    data_out_list_a.append(data_a[60*i:60*(i+1)])
            else:
                print('无用的输出!')

            # sleep(randint(1, 3))
            line_saved += 1

            if line_saved == max_lines:
                save_to_csv_a(data_out_list_a, client)
                data_out_list_a = []
                line_saved = 0

    print('全部用户采集完毕'.center(40, '*'))

if __name__ == '__main__':
    main()