# -*- coding: utf-8 -*-
import scrapy
import requests
from MySQLdb import *
from ..settings import COOKIES
from ..settings import HEADERS
from ..settings import MONTH
from ..tools.cookies_to_dict import stringToDict
from ..tools.filter_emoji_str import filter_emoji_str
import re
from random import randint
from pprint import pprint
import time

from ..items import SinaWeiboArticlesItem
from ..items import SinaWeiboReviewsItem
from ..my_pipelines import MySinaWeiboReviewsItemPipeline

from ..pipelines import SinaWeiboReviewsItemPipeline

"""
######################

** 单博主所有微博和评论提取(根据主页跟个人信息页进行的分析)

-- 第一个url模板代表的是某条微博的id，打开这个url会返回该微博某页的评论
https://m.weibo.cn/api/comments/show?id={id}&page={page}

-- 第二个url模板代表的是微博用户所发微博的列表，打开该url，返回的是某页的微博列表
https://m.weibo.cn/api/container/getIndex?containerid={oid}&type=uid&value={uid}&page={page}

-- 第三个url模板代表的其实是微博用户主页	
https://m.weibo.cn/api/container/getIndex?type=uid&value={usr_id}

访问第一个url需要id，但要访问了第二个url才能获得id

访问第二个url需要oid、uid，但是oid、uid需要访问了第三个url才能获得。

# 思路就是这样，那我们就此展开

下面是不同的主页类型可以获得的手机版主页的地址:
(转为手机版主页总共下面四类)

* 第一种类型: (注意短数字为uid)
https://weibo.com/273091100
(手机版: https://m.weibo.cn/u/5416630439)
    > 第三个url模板的用户主页:
    https://m.weibo.cn/api/container/getIndex?type=uid&value=5416630439

* 第二种类型:
https://weibo.com/u/3976064268
(手机版: https://m.weibo.cn/u/3976064268)
    > 第三个url模板的用户主页:
    https://m.weibo.cn/api/container/getIndex?type=uid&value=3976064268


* 第三种类型:
https://weibo.com/mczhe
(其个人信息页为: 
https://weibo.com/p/1005053671188734
)
1005053671188734 为 containerid
(手机版: https://m.weibo.cn/p/1005053671188734)

    请求地址为这个: https://m.weibo.cn/api/container/getIndex?containerid=1076033671188734
    
    第一个uid极为该博主的uid(正则匹配到第一个)
    {"id":3671188734,"screen_name":"Mc\u963f\u54f2-","profile_image_url":"https:\/\/tvax4.sinaimg.cn\/crop.0.0.1242.1242.180\/dad1e4fely8fi4qzaf8w1j20yi0yimzm.jpg","profile_url":"https:\/\/m.weibo.cn\/u\/3671188734?uid=3671188734&luicode=10000011&lfid=1076033671188734&featurecode=20000320","statuses_count":1129,"verified":true,"verified_type":0,"verified_type_ext":1,"verified_reason":"YY\u5a31\u4e50\u91d1\u724c\u827a\u4eba","description":"YY\u76f4\u64ad\u95f4ID\uff1a2893\uff0c    \u539f\u521b\u6b4c\u66f2  \uff08\u6709\u4f60\uff09 \uff08\u505a\u4f60\u7684\u5144\u5f1f\uff09 \uff08\u522b\u65e0\u6240\u6c42\uff09\u3002\u3002","gender":"m","mbtype":12,"urank":37,"mbrank":6,"follow_me":false,"following":false,"followers_count":3009739,"follow_count":37,"cover_image_phone":"https:\/\/wx4.sinaimg.cn\/crop.0.0.640.640.640\/dad1e4fely1fb2326pkgmj20u00u0dgg0.jpg","avatar_hd":"https:\/\/wx4.sinaimg.cn\/orj480\/dad1e4fely8fi4qzaf8w1j20yi0yimzm.jpg"}
    
    > 第三个url模板的用户主页:
    https://m.weibo.cn/api/container/getIndex?type=uid&value=3671188734

* 第四种类型:
https://weibo.com/atmangu
(其个人信息页为:
https://weibo.com/2918003193/about
)
(手机版为:
https://m.weibo.cn/2918003193
)
    > 第三个url模板的用户主页:
    https://m.weibo.cn/api/container/getIndex?type=uid&value=2918003193


(更简陋的微博版本：weibo.cn)
"""

class SimpleBozhuAllWeiboSpiderSpider(scrapy.Spider):
    name = 'simple_bozhu_all_weibo_spider'
    # allowed_domains = ['weibo.cn']
    start_urls = ['http://www.baidu.com/']

    def __init__(self):
        super().__init__()
        self.conn = connect(
            host='localhost',
            port=3306,
            db='python',
            user='root',
            passwd='lrf654321',
            # charset='utf-8',
        )

        self.headers = HEADERS
        self.cookie = stringToDict(COOKIES)
        self.personal_deal_info_from_db = self.get_nick_name_and_and_nick_name_url_and_personal_deal_info_url()
        self.index = 2
        self.month = MONTH

        self.proxies = self.get_proxy_ip_from_ip_pool()

    def parse(self, response):
        while True:
            if self.index > len(self.personal_deal_info_from_db)-1:     # 判断是否所有数据已经爬取完毕
                print('-' * 100 + '| 所有微博号的数据都已经爬取完毕, 即将退出此爬虫 ! 感谢使用 ! |')
                break
            else:
                nick_name = self.personal_deal_info_from_db[self.index][0]
                nick_name_url = self.personal_deal_info_from_db[self.index][1]
                personal_deal_info_url = self.personal_deal_info_from_db[self.index][2]
                phone_home_url_and_phone_home_json_url_and_uid_and_containerid = self\
                    .get_right_phone_home_url_and_phone_home_json_url_and_uid_and_containerid(
                        nick_name_url, personal_deal_info_url
                )

                if phone_home_url_and_phone_home_json_url_and_uid_and_containerid == []:
                    print('-' * 40 + '| 该博主手机版微博地址为: 空')
                    print('-' * 40 + '| 即将跳过该微博号进行下一个微博号的爬取 ... |')
                    self.index += 1
                    pass
                else:
                    uid = phone_home_url_and_phone_home_json_url_and_uid_and_containerid[2]
                    containerid = phone_home_url_and_phone_home_json_url_and_uid_and_containerid[3]
                    print('-' * 40 + '| 该博主的微博号为: %s' % nick_name)
                    print('-' * 40 + '| 该博主手机版微博地址为: %s' % phone_home_url_and_phone_home_json_url_and_uid_and_containerid[0])
                    print('-' * 40 + '| 该博主的 uid 为: %s' % uid)
                    print('-' * 40 + '| 该博主的 containerid 为: %s' % containerid)
                    print('-' * 40 + '| 即将开始爬取该博主所有微博信息 ...... |')
                    new_containerid = self.get_right_containerid(uid, containerid)

                    # tmp_proxies = {
                    #     'http': self.proxies['http'][randint(1, 70)]
                    # }
                    #
                    mblog_list = self.mblog_list(new_containerid, containerid)

                    for item in mblog_list:
                        Articles_list = SinaWeiboArticlesItem()

                        # 先赋初值避免运行报错
                        Articles_list['text'] = ''
                        Articles_list['image_url_list'] = ''  # 先赋予初值避免报错

                        Articles_list['m_media_url'] = ''
                        Articles_list['retweeted_text'] = ''
                        Articles_list['retweeted_image_url_list'] = ''
                        Articles_list['media_url'] = ''
                        Articles_list['reposts_count'] = 0
                        Articles_list['comments_count'] = 0
                        Articles_list['attitudes_count'] = 0

                        Articles_list['id'] = item['id']
                        Articles_list['nick_name'] = nick_name
                        Articles_list['created_at'] = item['created_at']
                        Articles_list['text'] = filter_emoji_str(item['text'])

                        tmp_index = 1
                        for tmp_item in item['image_url_list']:
                            Articles_list['image_url_list'] += '第%d张图片url：' % tmp_index + tmp_item + ' '
                            tmp_index += 1
                        Articles_list['m_media_url'] = item['m_media_url']
                        Articles_list['retweeted_text'] = filter_emoji_str(item['retweeted_text'])

                        tmp_index = 1
                        for tmp_item in item['retweeted_image_url_list']:
                            Articles_list['retweeted_image_url_list'] += '第%d张图片url：' % tmp_index + tmp_item + ' '
                            tmp_index += 1
                        Articles_list['media_url'] = item['media_url']
                        Articles_list['reposts_count'] = item['reposts_count']
                        Articles_list['comments_count'] = item['comments_count']
                        Articles_list['attitudes_count'] = item['attitudes_count']

                        yield Articles_list
                    """
                    print('*' * 40 + '| 即将开始爬取该博主的近半年文章对应的所有评论信息 ... |')

                    for item in mblog_list:
                        wb_id = item['id']
                        print('-' * 40 + '| 开始爬取文章id为(%s)的所有评论信息 ... |' % wb_id)
                        comments_list = self.get_comments_list(wb_id, nick_name)

                        print('-' * 40 + '| 爬取文章id为(%s)的所有评论信息结束! |' % wb_id)
                        for item in comments_list:
                            Reviews_list = SinaWeiboReviewsItem()

                            # 先赋予初值避免报KeyError的错
                            Reviews_list['username'] = ''
                            Reviews_list['comment'] = ''
                            Reviews_list['review_created_at'] = ''
                            Reviews_list['is_reply_comment'] = 'False'
                            Reviews_list['like_counts'] = 0
                            Reviews_list['review_pics'] = ''

                            Reviews_list['review_id'] = item['review_id']
                            Reviews_list['wb_id'] = item['wb_id']
                            Reviews_list['username'] = item['username']
                            Reviews_list['comment'] = filter_emoji_str(item['comment'])
                            Reviews_list['review_created_at'] = item['review_created_at']
                            Reviews_list['is_reply_comment'] = item['is_reply_comment']
                            Reviews_list['like_counts'] = item['like_counts']
                            Reviews_list['by_review_name'] = item['by_review_name']

                            tmp_index = 1
                            for tmp_item in item['review_pics']:
                                Reviews_list['review_pics'] = '第%d张图片url：' % tmp_index + tmp_item + ' '
                                tmp_index += 1

                            # yield Reviews_list
                            tmp_review = MySinaWeiboReviewsItemPipeline()
                            tmp_review.process_item(dict(Reviews_list))
                        print('-' * 40 + '| 进入短暂休眠, 即将开始继续爬取 ... |')
                        time.sleep(2)
                    """
                self.index += 1

    def get_right_containerid(self, uid, containerid):
        '''
        得到动态的正确的containerid
        :param uid:
        :param containerid:
        :return: containerid
        '''
        tmp_proxies = {
            'http': self.proxies['http'][randint(1, 70)]
        }

        page = str(1)
        tmp_url = 'https://m.weibo.cn/api/container/getIndex?containerid={containerid}&type=uid&value={uid}&page={page}'
        tmp_url = tmp_url.format(containerid=containerid, uid=uid, page=page)
        response = requests.get(url=tmp_url, headers=self.headers, proxies=tmp_proxies).json()

        # 切记: 此处为索引到-1就能避免报IndexError的错
        new_containerid = response['cards'][-1]['scheme']

        new_containerid = re.compile(r'.*?\?containerid=(.*?)_-.*?').findall(new_containerid)[0]
        # pprint(new_containerid)
        return new_containerid

    def mblog_list(self, new_containerid, containerid):
        '''
        微博号半年所有未必信息的爬取，(此外测试说明获取单博主所有博文不需要登录, 即不需要cookies)
        :param new_containerid: 动态的new_containerid
        :param containerid: 原生的containerid
        :return: mblog_list(里面包含每条微博的字典信息)
        '''
        mblog_list = []

        lfid = containerid
        containerid = str(new_containerid) + '_-_WEIBO_SECOND_PROFILE_WEIBO'
        page = str(1)
        base_url = 'https://m.weibo.cn/api/container/getIndex?luicode=10000011&page_type=03&containerid={}&lfid={}&page={}'.format(
            containerid, lfid, page,
        )
        # print(base_url)

        tmp_proxies = {
            'http': self.proxies['http'][randint(1, 70)]
        }

        response = requests.get(base_url, headers=self.headers, proxies=tmp_proxies, timeout=4).json()

        # 设置3层判断, 避免出错退出
        if response.get('cardlistInfo') is None:
            tmp_proxies = {
                'http': self.proxies['http'][randint(1, 70)]
            }
            response = requests.get(base_url, headers=self.headers, proxies=tmp_proxies,  timeout=4).json()
            if response.get('cardlistInfo') is None:
                tmp_proxies = {
                    'http': self.proxies['http'][randint(1, 70)]
                }
                response = requests.get(base_url, headers=self.headers, proxies=tmp_proxies,  timeout=4).json()
                if response.get('cardlistInfo') is None:
                    tmp_proxies = {
                        'http': self.proxies['http'][randint(1, 70)]
                    }
                    response = requests.get(base_url, headers=self.headers, proxies=tmp_proxies,  timeout=4).json()

        # pprint(response)

        total = response['cardlistInfo']['total']
        page_num = int(int(total) / 10) + 1
        print('-' * 40 + '| 微博页面总数为: %d |' % page_num)

        page_url = 'https://m.weibo.cn/api/container/getIndex?luicode=10000011&page_type=03&containerid={containerid}&lfid={lfid}&page={page}'
        is_over = False
        for i in range(1, page_num + 1, 1):  # 一直爬取到最后一页
            p_url = page_url.format(
                containerid=containerid, lfid=lfid, page=i
            )

            # 代理ip随机获取一个
            tmp_proxies = {
                'http': self.proxies['http'][randint(1, 70)]
            }

            print('-' * 40 + '| 现在使用的代理ip的地址为: %s |' % tmp_proxies['http'])

            page_response = requests.get(p_url, headers=self.headers, proxies=tmp_proxies, timeout=4)
            # print(page_response)
            page_data = page_response.json()

            # 设置3层处理代理无响应，重新随机ip进行请求，避免由于代理无响应而退出
            if page_data.get('cards') is None:
                print('-' * 40 + '| 当前的代理ip无响应, 重新获取代理ip中 ... |')
                tmp_proxies = {
                    'http': self.proxies['http'][randint(1, 70)]
                }
                print('-' * 40 + '| 现在使用的代理ip的地址为: %s |' % tmp_proxies['http'])
                page_response = requests.get(p_url, headers=self.headers, proxies=tmp_proxies,
                                             timeout=4)
                page_data = page_response.json()
                if page_data.get('cards') is None:
                    print('-' * 40 + '| 当前的代理ip无响应, 重新获取代理ip中 ... |')
                    tmp_proxies = {
                        'http': self.proxies['http'][randint(1, 70)]
                    }
                    print('-' * 40 + '| 现在使用的代理ip的地址为: %s |' % tmp_proxies['http'])
                    page_response = requests.get(p_url, headers=self.headers, proxies=tmp_proxies,
                                                 timeout=4)
                    page_data = page_response.json()
                    if page_data.get('cards') is None:
                        print('-' * 40 + '| 当前的代理ip无响应, 重新获取代理ip中 ... |')
                        tmp_proxies = {
                            'http': self.proxies['http'][randint(1, 70)]
                        }
                        print('-' * 40 + '| 现在使用的代理ip的地址为: %s |' % tmp_proxies['http'])
                        page_response = requests.get(p_url, headers=self.headers,
                                                     proxies=tmp_proxies,
                                                     timeout=4)
                        page_data = page_response.json()

            cards = page_data['cards']
            # pprint(cards)
            for card in cards:
                if card.get('mblog') is None:
                    pass
                else:
                    mblog = card['mblog']  # 获取mblog

                    created_at = mblog['created_at']

                    is_hour_date = re.compile(r'.*?(小时).*?').findall(created_at)
                    is_another_date = re.compile(r'.*?(昨天).*?').findall(created_at)
                    is_another_date2 = re.compile(r'.*?(前天).*?').findall(created_at)
                    tmp_month = re.compile(r'(\d+).*?').findall(created_at)
                    tmp_day = re.compile(r'.*?-(\d+)').findall(created_at)
                    tmp_year = re.compile(r'20(\d+).*?').findall(created_at)  # 如果是2017是不显示年份的

                    '''
                    筛选近半年的全部微博
                    '''
                    if (is_hour_date != [] or is_another_date != [] or is_another_date2 != [] or (
                            tmp_month != [] and int(tmp_month[0]) >= self.month)) and tmp_year == []:
                        id = mblog['id']
                        text = mblog['text']
                        reposts_count = mblog['reposts_count']
                        comments_count = mblog['comments_count']
                        attitudes_count = mblog['attitudes_count']

                        '''
                        判断原创微博是否带有图片, 如果带有图片则存下图片地址
                        '''
                        image_url_list = []
                        if mblog.get('pics') is not None:
                            # 判断微博中是否有图片，如果有记录下每个图片地址
                            pics = mblog['pics']  # pics -> [{}, {}, ...] 最多9张图片(0->8)
                            for item in pics:
                                image_url_list.append(item['url'])

                        '''
                        判断原创微博是否带有视频地址, 如果有则存下视频地址
                        '''
                        m_medal_url = ''
                        if mblog.get('page_info') is not None:
                            page_info = mblog['page_info']
                            if page_info.get('media_info') is not None:
                                m_medal_url = page_info['page_url']
                        else:
                            m_medal_url = ''

                        '''
                        判断是否是转发的微博, 如果是, 则将转发微博的数据进行记录与存储
                        '''
                        retweeted_image_url_list = []
                        retweeted_text = ''
                        retweeted_medal_url = ''
                        if mblog.get('retweeted_status') is not None:
                            retweeted_status = mblog['retweeted_status']  # retweeted_status -> {}

                            if retweeted_status.get('text') is not None:
                                # 判断转发的微博是否带有文字内容, 如果存在则保存下来
                                retweeted_text = retweeted_status['text']
                            else:
                                retweeted_text = ''

                            if retweeted_status.get('pics') is not None:
                                # 判断转发的微博是否带有照片, 如果存在则保存下来
                                retweeted_pics = retweeted_status['pics']
                                for item in retweeted_pics:
                                    retweeted_image_url_list.append(item['url'])

                            if retweeted_status.get('pics') is None:
                                if retweeted_status.get('page_info'):
                                    page_info = retweeted_status['page_info']
                                    # 判断类型是否为带视频, 如果带视频就存下视频的地址
                                    if page_info.get('media_info') is not None:
                                        retweeted_medal_url = page_info['page_url']
                                    else:
                                        retweeted_medal_url = ''
                                else:
                                    retweeted_medal_url = ''
                            else:
                                retweeted_medal_url = ''

                        mblog_data = {
                            'created_at': created_at,           # 该微博文章创建时间
                            'id': id,                           # 该微博文章的id
                            'text': text,                       # 该微博的内容
                            'image_url_list': image_url_list,   # 原创微博的图片链接地址
                            'm_media_url': m_medal_url,         # 原创微博的视频url
                            'retweeted_text': retweeted_text,   # 该微博转发的内容
                            'retweeted_image_url_list': retweeted_image_url_list,  # 转发内容的图片链接(类型list)
                            'media_url': retweeted_medal_url,   # 转发内容的视频链接地址(类型str)
                            'reposts_count': reposts_count,     # 转载数
                            'comments_count': comments_count,   # 评论数
                            'attitudes_count': attitudes_count  # 赞数
                        }

                        mblog_list.append(mblog_data)
                        # print(' ' * 10, mblog_data)
                        # print('-' * 100)
                        # pprint(mblog_data)
                        print('----| 博文: |', mblog_data)
                        print('-' * 100)
                        # time.sleep(1)

                    else:
                        print('-' * 40 + '| 该微博号的近半年微博全部爬取完毕!! |')
                        print()
                        is_over = True
                        print('-' * 40 + '| 休眠4秒中..... |')
                        time.sleep(4)
                        break
                if is_over == True:
                    break
            if is_over == True:
                break
        return mblog_list

    def get_comments_list(self, wb_id, nick_name):
        '''
        根据给与博文的id获取该博文所有的评论信息(切记：此处也不需要登录, 即不需要cookies)
        :param wb_id:
        :param nick_name:
        :return:
        '''
        review_data_list = []
        url = 'https://m.weibo.cn/api/comments/show?id={id}'.format(id=wb_id)
        page_url = 'https://m.weibo.cn/api/comments/show?id={id}&page={page}'

        tmp_proxies = {
            'http': self.proxies['http'][randint(1, 70)]
        }
        print('-' * 40 + '| 现在使用的代理ip的地址为: %s |' % tmp_proxies['http'])

        response = requests.get(url, headers=self.headers, proxies=tmp_proxies, timeout=3).json()
        # 设置三层避免报错退出爬取
        if response.get('max') is None:
            tmp_proxies = {
                'http': self.proxies['http'][randint(1, 70)]
            }
            print('-' * 40 + '| 现在使用的代理ip的地址为: %s |' % tmp_proxies['http'])

            response = requests.get(url, headers=self.headers, proxies=tmp_proxies, timeout=3).json()
            if response.get('max') is None:
                tmp_proxies = {
                    'http': self.proxies['http'][randint(1, 70)]
                }
                print('-' * 40 + '| 现在使用的代理ip的地址为: %s |' % tmp_proxies['http'])

                response = requests.get(url, headers=self.headers, proxies=tmp_proxies,
                                        timeout=3).json()
                if response.get('max') is None:
                    tmp_proxies = {
                        'http': self.proxies['http'][randint(1, 70)]
                    }
                    print('-' * 40 + '| 现在使用的代理ip的地址为: %s |' % tmp_proxies['http'])

                    response = requests.get(url, headers=self.headers, proxies=tmp_proxies,
                                            timeout=3).json()

        page_max_num = response['max']  # 评论的页面总数
        print('-' * 40 + '| 该评论的页面总数为: %s |' % page_max_num)
        for i in range(1, page_max_num + 1, 1):
            p_url = page_url.format(id=wb_id, page=i)

            tmp_proxies = {
                'http': self.proxies['http'][randint(1, 70)]
            }
            print('-' * 40 + '| 现在使用的代理ip的地址为: %s |' % tmp_proxies['http'])

            response_data = requests.get(p_url, headers=self.headers, proxies=tmp_proxies, timeout=3).json()
            # 设置三层代理出错重新请求来避免报错退出爬取过程
            if response_data.get('data') is None:
                tmp_proxies = {
                    'http': self.proxies['http'][randint(1, 70)]
                }
                print('-' * 40 + '| 现在使用的代理ip的地址为: %s |' % tmp_proxies['http'])

                response_data = requests.get(p_url, headers=self.headers, proxies=tmp_proxies, timeout=3).json()
                if response_data.get('data') is None:
                    tmp_proxies = {
                        'http': self.proxies['http'][randint(1, 70)]
                    }
                    print('-' * 40 + '| 现在使用的代理ip的地址为: %s |' % tmp_proxies['http'])

                    response_data = requests.get(p_url, headers=self.headers, proxies=tmp_proxies, timeout=3).json()
                    if response_data.get('data') is None:
                        tmp_proxies = {
                            'http': self.proxies['http'][randint(1, 70)]
                        }
                        print('-' * 40 + '| 现在使用的代理ip的地址为: %s |' % tmp_proxies['http'])

                        response_data = requests.get(p_url, headers=self.headers, proxies=tmp_proxies, timeout=3).json()

            # print(response_data)
            data = response_data.get('data')
            for item in data:
                is_reply_comment = 'False'
                review_id = item['id']
                review_created_at = item['created_at']
                like_counts = item['like_counts']
                username = item['user']['screen_name']
                comment = item['text']
                if username == nick_name:
                    is_reply_comment = 'True'
                if item.get('pic') is not None:
                    review_pics = item['pic']['url']
                else:
                    review_pics = ''

                # 从评论内容中获取被评论者的微博名
                if re.compile(r'^回复').findall(comment) != []:
                    by_review_name = re.compile(r'^回复.*?@(.*?)</a>:.*?').findall(comment)[0]
                else:
                    by_review_name = ''

                review_data = {
                    'is_reply_comment': is_reply_comment,       # 判断是否为博主回复内容, 如果是则为True
                    'review_id': review_id,                     # 评论内容的id
                    'wb_id': wb_id,                             # 对应微博文章的id
                    'review_created_at': review_created_at,     # 评论内容的创建时间
                    'like_counts': like_counts,                 # 评论内容点赞数
                    'username': username,                       # 评论者微博号名
                    'comment': comment,                         # 评论的文字内容
                    'review_pics': review_pics,                 # 评论的图片内容
                    'by_review_name': by_review_name,           # 被评论者的微博名
                }

                review_data_list.append(review_data)
                # print('-' * 100)
                print('----| 评论: |', review_data)
                print('-' * 100)
        print('-' * 40 + '| 该博文的相关的所有评论爬取完毕！ |')
        # time.sleep(1)
        return review_data_list

    def get_right_phone_home_url_and_phone_home_json_url_and_uid_and_containerid(self, nick_name_url, personal_deal_info_url):
        '''
        得到不同主页类型的正确手机版主页url, 以及 uid 和 主页的containerid
        :param nick_name_url:
        :param personal_deal_info_url:
        :return: phone_home_url, phone_home_json_url, uid, containerid
        '''
        tmp_proxies = {
            'http': self.proxies['http'][randint(1, 70)]
        }

        # 第四种类型
        # https://weibo.com/2918003193/about
        is_about_url_personal_deal_info_url = re.compile('https://weibo.com/(.*?)/about').findall(str(personal_deal_info_url))
        if is_about_url_personal_deal_info_url != []:
            phone_home_url = 'https://m.weibo.cn/' + is_about_url_personal_deal_info_url[0]
            phone_home_json_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + \
                                  is_about_url_personal_deal_info_url[0]
            uid = is_about_url_personal_deal_info_url[0]
            containerid = requests.get(phone_home_json_url, headers=self.headers, proxies=tmp_proxies).json()['tabsInfo']['tabs'][0][
                'containerid']

            return phone_home_url, phone_home_json_url, uid, containerid

        # 第二种类型
        # https://weibo.com/u/3976064268?refer_flag=1028035010_
        is_u_url_nick_name_url = re.compile(r'https://weibo.com/u/(.*?)\?refer_flag=1028035010_').findall(nick_name_url)
        if is_u_url_nick_name_url != []:
            phone_home_url = 'https://m.weibo.cn/u/' + is_u_url_nick_name_url[0]
            phone_home_json_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + is_u_url_nick_name_url[
                0]
            uid = is_u_url_nick_name_url[0]
            containerid = requests.get(phone_home_json_url, headers=self.headers, proxies=tmp_proxies).json()['tabsInfo']['tabs'][0][
                'containerid']

            return phone_home_url, phone_home_json_url, uid, containerid

        # 第一种类型
        # https://weibo.com/273091100?refer_flag=1028035010_
        # 个人信息页：https://weibo.com/p/1005055416630439/info?mod=pedit_more
        is_number_url_nick_name_url = re.compile(r'https://weibo.com/(.*?)\?refer_flag=1028035010_').findall(
            nick_name_url)
        phone_home_json_url = ''
        if is_number_url_nick_name_url != []:
            phone_home_url = 'https://m.weibo.cn/' + is_number_url_nick_name_url[0]
            is_p_url_personal_deal_info_url = re.compile(r'https://weibo.com/p/(.*?)/info\?mod=pedit_more').findall(str(personal_deal_info_url))
            if is_p_url_personal_deal_info_url != []:
                get_uid_url = 'https://m.weibo.cn/api/container/getIndex?containerid=' + \
                              is_p_url_personal_deal_info_url[0]
                tmp_json_data = requests.get(get_uid_url, headers=self.headers, proxies=tmp_proxies).json()
                # pprint(tmp_json_data)
                uid = re.compile(r'.*?uid=(.*?)&.*?').findall(tmp_json_data['scheme'])[0]
                # print(uid)
                phone_home_url = 'https://m.weibo.cn/' + str(uid)
                phone_home_json_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + uid
                uid = is_number_url_nick_name_url[0]
                containerid = requests.get(phone_home_json_url, headers=self.headers, proxies=tmp_proxies).json()['tabsInfo']['tabs'][0][
                    'containerid']

                return phone_home_url, phone_home_json_url, uid, containerid

        # 第三种类型
        # https://weibo.com/p/1005053671188734/info?mod=pedit_more
        is_p_url_personal_deal_info_url = re.compile(r'https://weibo.com/p/(.*?)/info\?mod=pedit_more').findall(str(personal_deal_info_url))
        if is_p_url_personal_deal_info_url != []:
            get_uid_url = 'https://m.weibo.cn/api/container/getIndex?containerid=' + is_p_url_personal_deal_info_url[0]
            tmp_json_data = requests.get(get_uid_url, headers=self.headers, proxies=tmp_proxies).json()
            # pprint(tmp_json_data)
            uid = re.compile(r'.*?uid=(.*?)&.*?').findall(tmp_json_data['scheme'])[0]
            # print(uid)
            phone_home_url = 'https://m.weibo.cn/' + str(uid)
            # phone_home_json_url = get_uid_url
            phone_home_json_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + uid
            containerid = requests.get(phone_home_json_url, headers=self.headers, proxies=tmp_proxies).json()['tabsInfo']['tabs'][0][
                'containerid']
            return phone_home_url, phone_home_json_url, uid, containerid
        else:
            print('*' * 20 + '该nick_name_url 和 personal_deal_info_url无法被解析为对应手机版网址')
            return None

    def get_nick_name_and_and_nick_name_url_and_personal_deal_info_url(self):
        '''
        从给定的表中获取nick_name, nick_name_url, personal_deal url，从而进行相应的数据爬取工作
        :return:
        '''
        try:
            cs = self.conn.cursor()

            # sql = 'select nick_name, personal_deal_info_url from bozhu_user where bozhu_user.nick_name not in (select nick_name from personal_deal_info) and bozhu_user.nick_name not in (select nick_name from company_deal_info) and bozhu_user.nick_name != \"_可口可心\" and bozhu_user.nick_name != \"-_KEI_-\" and bozhu_user.nick_name != \"0511天蝎\";'
            # 下面的字段必须一一对应
            sql = 'select nick_name, nick_name_url, personal_deal_info_url from bozhu_user where sina_type = \"社会\" and nick_name != \"1018陕广新闻\" and bozhu_user.nick_name not in (select nick_name from sina_wb_article);'
            cs.execute(sql)

            result = cs.fetchall()  # return -> 一个 ((), (), ...)
            cs.close()

            print('=' * 12 + '| 成功获取数据库数据 |')
            return result
        except Exception as e:
            print('=' * 12 + '| 获取数据库数据失败 |')
            return None

    def get_proxy_ip_from_ip_pool(self):
        '''
        从代理ip池中获取到对应ip
        :return:
        '''
        base_url = 'http://127.0.0.1:8000'
        result = requests.get(base_url).json()

        result_ip_list = {}
        result_ip_list['http'] = []
        for item in result:
            tmp_url = 'http://' + str(item[0]) + ':' + str(item[1])
            result_ip_list['http'].append(tmp_url)
        # pprint(result_ip_list)

        return result_ip_list
