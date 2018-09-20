# coding:utf-8

'''
@author = super_fazai
@File    : 每日幸运大转盘.py
@Time    : 2017/9/29 13:12
@connect : superonesfazai@gmail.com
'''

import re
from pprint import pprint
import requests
from pprint import pprint
import time

headers = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept': 'application/json, text/plain, */*',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'm.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}

cookies = {
    'cookie': 'SINAGLOBAL=1920862274319.4636.1502628639473; __utma=15428400.1070391683.1506563351.1506563351.1506563351.1; __utmz=15428400.1506563351.1.1.utmcsr=verified.weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/verify; YF-Ugrow-G0=ea90f703b7694b74b62d38420b5273df; YF-V5-G0=3d0866500b190395de868745b0875841; _s_tentry=login.sina.com.cn; Apache=5535716871036.658.1506825662817; ULV=1506825662957:9:1:1:5535716871036.658.1506825662817:1506609903208; YF-Page-G0=b35da6f93109faa87e8c89e98abf1260; TC-V5-G0=ac3bb62966dad84dafa780689a4f7fc3; TC-Page-G0=4c4b51307dd4a2e262171871fe64f295; TC-Ugrow-G0=5e22903358df63c5e3fd2c757419b456; login_sid_t=7512e659ecf2f4cf12080ce37d716b1d; WBtopGlobal_register_version=1844f177002b1566; cross_origin_proto=SSL; UOR=developer.51cto.com,widget.weibo.com,login.sina.com.cn; SSOLoginState=1506955740; un=rlzeam07@163.com; wvr=6; SCF=AluwsnVuuVb8f4iOGi5k7zRy-IBKAxmfDFs-_RbHERcH6ekYMJ_9vkzZLyueJJVbFUqFhKX4gpugo1IA7lkBlYI.; SUB=_2A25019iaDeThGeBP7VYY8SzNwzmIHXVXpU1SrDV8PUJbmtAKLXngkW-eciawg0sKAweobhKHAe08nyUGiw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFqTWuN4lGrED1Loh_Jr2Gs5JpX5K-hUgL.FoqpSoB4eKzp1h-2dJLoIEQLxKqL1h5L1-BLxK.L1h5LBonLxKqL1h5L1-BLxKnLB.qL1-Sk1hMceKet; SUHB=0eb98WoRtKCUkR; ALF=1538579524; wb_cusLike_6164912185=N',
}

def tmp(nick_name_url, personal_deal_info_url):
    # 第四种类型
    # https://weibo.com/2918003193/about
    is_about_url_personal_deal_info_url = re.compile('https://weibo.com/(.*?)/about').findall(personal_deal_info_url)
    if is_about_url_personal_deal_info_url != []:
        phone_home_url = 'https://m.weibo.cn/' + is_about_url_personal_deal_info_url[0]
        phone_home_json_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + \
                              is_about_url_personal_deal_info_url[0]
        uid = is_about_url_personal_deal_info_url[0]
        containerid = requests.get(phone_home_json_url, headers=headers).json()['tabsInfo']['tabs'][0]['containerid']

        return phone_home_url, phone_home_json_url, uid, containerid

    # 第二种类型
    # https://weibo.com/u/3976064268?refer_flag=1028035010_
    is_u_url_nick_name_url = re.compile(r'https://weibo.com/u/(.*?)\?refer_flag=1028035010_').findall(nick_name_url)
    if is_u_url_nick_name_url != []:
        phone_home_url = 'https://m.weibo.cn/u/' + is_u_url_nick_name_url[0]
        phone_home_json_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + is_u_url_nick_name_url[0]
        uid = is_u_url_nick_name_url[0]
        containerid = requests.get(phone_home_json_url, headers=headers).json()['tabsInfo']['tabs'][0]['containerid']

        return phone_home_url, phone_home_json_url, uid, containerid

    # 第一种类型
    # https://weibo.com/273091100?refer_flag=1028035010_
    # 个人信息页：https://weibo.com/p/1005055416630439/info?mod=pedit_more
    is_number_url_nick_name_url = re.compile(r'https://weibo.com/(.*?)\?refer_flag=1028035010_').findall(nick_name_url)
    phone_home_json_url = ''
    if is_number_url_nick_name_url != []:
        phone_home_url = 'https://m.weibo.cn/' + is_number_url_nick_name_url[0]
        is_p_url_personal_deal_info_url = re.compile(r'https://weibo.com/p/(.*?)/info\?mod=pedit_more').findall(personal_deal_info_url)
        if is_p_url_personal_deal_info_url != []:
            get_uid_url = 'https://m.weibo.cn/api/container/getIndex?containerid=' + is_p_url_personal_deal_info_url[0]
            tmp_json_data = requests.get(get_uid_url, headers=headers).json()
            # pprint(tmp_json_data)
            uid = re.compile(r'.*?uid=(.*?)&.*?').findall(tmp_json_data['scheme'])[0]
            # print(uid)
            phone_home_url = 'https://m.weibo.cn/' + str(uid)
            phone_home_json_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + uid
            uid = is_number_url_nick_name_url[0]
            containerid = requests.get(phone_home_json_url, headers=headers).json()['tabsInfo']['tabs'][0]['containerid']

            return phone_home_url, phone_home_json_url, uid, containerid

    # 第三种类型
    # https://weibo.com/p/1005053671188734/info?mod=pedit_more
    is_p_url_personal_deal_info_url = re.compile(r'https://weibo.com/p/(.*?)/info\?mod=pedit_more').findall(personal_deal_info_url)
    if is_p_url_personal_deal_info_url != []:
        get_uid_url = 'https://m.weibo.cn/api/container/getIndex?containerid=' + is_p_url_personal_deal_info_url[0]
        tmp_json_data = requests.get(get_uid_url, headers=headers).json()
        # pprint(tmp_json_data)
        uid = re.compile(r'.*?uid=(.*?)&.*?').findall(tmp_json_data['scheme'])[0]
        # print(uid)
        phone_home_url = 'https://m.weibo.cn/' + str(uid)
        # phone_home_json_url = get_uid_url
        phone_home_json_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + uid
        containerid = requests.get(phone_home_json_url, headers=headers).json()['tabsInfo']['tabs'][0]['containerid']
        return phone_home_url, phone_home_json_url, uid, containerid
    else:
        print('*' * 20 + '该nick_name_url 和 personal_deal_info_url无法被解析为对应手机版网址')
        return None

nick_name_url = 'https://weibo.com/u/3976064268?refer_flag=1028035010_'
personal_deal_info_url = ''
xxx = tmp(nick_name_url, personal_deal_info_url)
print(xxx)
# json_data = requests.get(xxx[1], headers=headers).json()
# pprint(json_data)

# tmp_url = 'https://m.weibo.cn/api/container/getIndex?containerid=2302832918003193&type=uid&value=2918003193&page=2'
'''
containerid:2304132918003193_-_WEIBO_SECOND_PROFILE_WEIBO
luicode:10000011
lfid:2302832918003193
page_type:03
page:2
'''
containerid = str(2304132918003193)

lfid = containerid
containerid = str(containerid) + '_-_WEIBO_SECOND_PROFILE_WEIBO'
# page_type = str('03')
page = str(1)       # 页码数 = (微博总数(total)-9)/10 + 1

card_list_info_url = 'https://m.weibo.cn/api/container/getIndex?luicode=10000011&page_type=03&containerid={}&lfid={}&page={}'.format(
    containerid, lfid, page
)

# tmp = requests.get(card_list_info_url, headers=headers, cookies=cookies).json()
# pprint(tmp)

def get_right_containerid(uid, containerid):
    '''
    得到动态的正确的containerid
    :param uid:
    :param containerid:
    :return: containerid
    '''
    # https://m.weibo.cn/api/container/getIndex?containerid={oid}&type=uid&value={uid}&page={page}
    page = str(1)
    tmp_url = 'https://m.weibo.cn/api/container/getIndex?containerid={containerid}&type=uid&value={uid}&page={page}'
    tmp_url = tmp_url.format(containerid=containerid, uid=uid, page=page)
    response = requests.get(url=tmp_url, headers=headers).json()
    # pprint(response)
    # 切记: 此处为索引到-1就能避免报IndexError的错
    new_containerid = response['cards'][-1]['scheme']
    new_containerid = re.compile(r'.*?\?containerid=(.*?)_-.*?').findall(new_containerid)[0]
    # pprint(new_containerid)
    return new_containerid

def mblog_list(new_containerid, containerid):
    '''
    微博号半年所有未必信息的爬取
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
    response = requests.get(base_url, headers=headers).json()
    # pprint(response)

    total = response['cardlistInfo']['total']
    page_num = int(int(total) / 10) + 1
    print('-' * 30 + '| 微博页面总数为: %d' % page_num)

    page_url = 'https://m.weibo.cn/api/container/getIndex?luicode=10000011&page_type=03&containerid={containerid}&lfid={lfid}&page={page}'
    is_over = False
    for i in range(1, page_num + 1, 1):     # 一直爬取到最后一页
        p_url = page_url.format(
            containerid=containerid, lfid=lfid, page=i
        )
        page_response = requests.get(p_url, headers=headers)
        # print(page_response)
        page_data = page_response.json()
        cards = page_data['cards']
        # pprint(cards)
        for card in cards:
            if card.get('mblog') is None:
                pass
            else:
                mblog = card['mblog']       # 获取mblog

                created_at = mblog['created_at']

                is_hour_date = re.compile(r'.*?(小时).*?').findall(created_at)
                is_another_date = re.compile(r'.*?(昨天).*?').findall(created_at)
                is_another_date2 = re.compile(r'.*?(前天).*?').findall(created_at)
                tmp_month = re.compile(r'(\d+).*?').findall(created_at)
                tmp_day = re.compile(r'.*?-(\d+)').findall(created_at)
                tmp_year = re.compile(r'20(\d+).*?').findall(created_at)    # 如果是2017是不显示年份的

                '''
                筛选近半年的全部微博
                '''
                if (is_hour_date != [] or is_another_date != [] or is_another_date2 != [] or (tmp_month != [] and int(tmp_month[0]) >= 4)) and tmp_year == []:
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
                        pics = mblog['pics']    # pics -> [{}, {}, ...] 最多9张图片(0->8)
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
                        retweeted_status = mblog['retweeted_status']    # retweeted_status -> {}

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
                        'created_at': created_at,                               # 该微博文章创建时间
                        'id': id,                                               # 该微博文章的id
                        'text': text,                                           # 该微博的内容
                        'image_url_list': image_url_list,                       # 原创微博的图片链接地址
                        'm_media_url': m_medal_url,                             # 原创微博的视频url
                        'retweeted_text': retweeted_text,                       # 该微博转发的内容
                        'retweeted_image_url_list': retweeted_image_url_list,   # 转发内容的图片链接(类型list)
                        'media_url': retweeted_medal_url,                       # 转发内容的视频链接地址(类型str)
                        'reposts_count': reposts_count,                         # 转载数
                        'comments_count': comments_count,                       # 评论数
                        'attitudes_count': attitudes_count                      # 点赞数
                    }
                    mblog_list.append(mblog_data)
                    # print(' ' * 10, mblog_data)
                    print('-' * 100)
                    pprint(mblog_data)
                    print('-' * 100)
                    # time.sleep(1)

                else:
                    print('-' * 40 + '该微博号的近半年微博全部爬取完毕!!')
                    is_over = True
                    break
            if is_over == True:
                break
        if is_over == True:
            break
    return mblog_list

# containerid = str(2304132918003193)
uid = str(3915752126)
containerid = str(2302833915752126)
# new_containerid = get_right_containerid(uid, containerid)
# print(mblog_list(new_containerid=new_containerid, containerid=containerid))

def get_comments(wb_id, nick_name):
    review_data_list = []
    url = 'https://m.weibo.cn/api/comments/show?id={id}'.format(id=wb_id)
    page_url = 'https://m.weibo.cn/api/comments/show?id={id}&page={page}'
    response = requests.get(url, headers=headers, timeout=3).json()
    if response.get('max') is None:
        print('-' * 40 + '| 未能成功获取评论信息内容 |')
        time.sleep(1)
        response = requests.get(url, headers=headers, timeout=3).json()
    page_max_num = response['max']      # 评论的页面总数
    print('-' * 40 + '| 该评论的页面总数为: %s |' % page_max_num)
    for i in range(1, page_max_num + 1, 1):
        p_url = page_url.format(id=wb_id, page=i)
        response_data = requests.get(p_url, headers=headers, timeout=3).json()
        # print(response_data)
        data = response_data.get('data')
        for item in data:
            is_reply_comment = False                       # 判断是否为博主回复内容
            review_id = item['id']
            review_created_at = item['created_at']
            like_counts = item['like_counts']
            username = item['user']['screen_name']
            comment = item['text']
            if username == nick_name:
                is_reply_comment = True
            if item.get('data') is not None:
                review_pics = item['pic']['url']
            else:
                review_pics = ''

            review_data = {
                'is_reply_comment': is_reply_comment,       # 判断是否为博主回复内容, 如果是则为True
                'review_id': review_id,                     # 评论内容的id
                'review_created_at': review_created_at,     # 评论内容的创建时间
                'like_counts': like_counts,                 # 评论内容点赞数
                'username': username,                       # 评论者微博号名
                'comment': comment,                         # 评论的文字内容
                'review_pics': review_pics,                 # 评论的图片内容
            }

            review_data_list.append(review_data)
            print('-' * 100)
            pprint(review_data)
            print('-' * 100)
    print('-' * 40 + '| 该微博的所有评论爬取完毕！ |')
    time.sleep(1)
    return review_data_list

# wb_id = '4151636518123999'  # 评论数页数较多
# nick_name = '_EchoLee_'

wb_id = '4158326294414867'    # 评论页数只有一页的处理
nick_name = '_aaayuko'
review_data_list = get_comments(wb_id, nick_name)
print(review_data_list)

# ----------------------------------------| 该博主的微博号为: _EchoLee_
# ----------------------------------------| 该博主手机版微博地址为: https://m.weibo.cn/2820457935
# ----------------------------------------| 即将开始爬取该博主所有微博信息 ...... |
# 错误内容: new_containerid = response['cards'][9]['scheme']
# IndexError: list index out of range

# 说明获取单博主所有文章，不需要cookies
# tmp_url = 'https://m.weibo.cn/api/container/getIndex?containerid=2304132918003193_-_WEIBO_SECOND_PROFILE_WEIBO&luicode=10000011&lfid=2302832918003193'
# response = requests.get(tmp_url, headers=headers).json()
# pprint(response)

# https://m.weibo.cn/api/comments/show?id=4158326294414867

# 从评论内容中获取被评论者的微博名
# comment = r"回复<a href='https://m.weibo.cn/n/一闪一闪亮今今丶'>@一闪一闪亮今今丶</a>:今天应该可以的"
comment = '把上期条纹卫衣的货赶紧先发发掉，都已经20多天了<span class="url-icon"><img src="//h5.sinaimg.cn/m/emoticon/icon/default/d_han-4ce3c6bac3.png" style="width:1em;height:1em;" alt="[汗]"></span>'
if re.compile(r'^回复').findall(comment) != []:
    by_review_name = re.compile(r'^回复.*?@(.*?)</a>:.*?').findall(comment)
else:
    by_review_name = ''
print(by_review_name)