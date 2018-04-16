# coding:utf-8

'''
@author = super_fazai
@File    : 解析抖音接口数据.py
@Time    : 2018/4/7 17:11
@connect : superonesfazai@gmail.com
'''

from my_requests import MyRequests
import json, gc, time
from pprint import pprint
from time import sleep
from random import randint

PHONE_HEADERS = [
    'Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
    'Mozilla/5.0 (Linux; Android 7.0; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en',
    'Mozilla/5.0 (Linux; Android 5.1.1; vivo Xplay5A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.1.1)',
    'Mozilla/5.0 (Linux; Android 6.0; LEX626 Build/HEXCNFN5902606111S) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/7.4 baiduboxapp/8.3.1 (Baidu; P1 6.0)',
    'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; ZUK Z2121 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.8.952 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM-C7000 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.2.948 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
    'Mozilla/5.0 (Linux; Android 5.1; m3 note Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.1)',
    'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; SM-G9550 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.0.953 Mobile Safari/537.36',
]

class DouYinUserIdParse():
    '''
    根据抖音用户user_id抓取其所有视频并且解析
    '''
    def __init__(self):
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'upgrade-insecure-requests': '1',
            'user-agent': PHONE_HEADERS[randint(0, len(PHONE_HEADERS)-1)],
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'cache-control': 'max-age=0',
            'authority': 'www.douyin.com',
            # 'cookie': '_ba=BA0.2-20180330-5199e-OeUxtvwJvy5ElpWGFLId; _ga=GA1.2.390071767.1522391891; sso_login_status=1; tt_webid=6540458660484122126; __tea_sdk__user_unique_id=10_; __tea_sdk__ssid=e88eef4a-ec1f-497d-b2c7-301239bfdc67; login_flag=d6ee54ffebe3021c3fb67ff863970736; sessionid=7bdfd0e36df78f38c25abd13f0eff3cc; uid_tt=644e532b271dae498b62c659de17afdf; sid_tt=7bdfd0e36df78f38c25abd13f0eff3cc; sid_guard="7bdfd0e36df78f38c25abd13f0eff3cc|1522819290|2591999|Fri\\054 04-May-2018 05:21:29 GMT"',
        }

    def _get_aweme_api_videos_info(self, user_id):
        self.user_id = user_id
        params = (
            ('user_id', self.user_id),
            ('max_cursor', '0'),
            ('count', '20'),
        )

        url = 'https://www.douyin.com/aweme/v1/aweme/post/'
        body = MyRequests.get_url_body(url=url, headers=self.headers, params=params)
        # print(body)

        self.deal_with_data(body=body)

    def deal_with_data(self, body):
        try:
            data = json.loads(body)
            pprint(data)
        except:
            data = {}

        _video_list = []
        for item in data.get('aweme_list', []):
            try:
                # 用户id
                user_id = self.user_id
                # 用户头像
                head_img = item.get('author', {}).get('avatar_larger', {}).get('url_list', [])[0]
                # 用户昵称
                nick_name = item.get('author', {}).get('nickname', '')
                # 抖音号(即根据抖音搜索能直接找到用户id)
                unique_id = item.get('author', {}).get('unique_id', '')
                # 短id(即也可根据短id查找到该用户)
                short_id = item.get('author', {}).get('short_id', '')
                # 用户签名
                signature = item.get('author', {}).get('signature', '')

                '''music'''
                # 歌手名
                singer_name = item.get('music', {}).get('author_name', '')
                # 歌手头像
                singer_head_img = item.get('music', {}).get('cover_hd', {}).get('url_list', [])[0]
                # 歌曲名
                music_name = item.get('music', {}).get('music_name', '')
                # 歌曲play_url
                music_play_url = item.get('music', {}).get('play_url', {}).get('url_list', [])[0]

                '''video'''
                # 视频id
                video_id = item.get('aweme_id', '')
                # 视频描述
                video_desc = item.get('desc', '')
                # 视频创建时间
                create_time = str(self.timestamp_to_regulartime(item.get('create_time')))
                # 评论数
                comment_count = item.get('statistics', {}).get('comment_count', 0)
                # 点赞数
                like_count = item.get('statistics', {}).get('digg_count', 0)
                # 播放数
                play_count = item.get('statistics', {}).get('play_count', 0)
                # 分享数
                share_count = item.get('statistics', {}).get('share_count', 0)
                # video的高度 and 宽度
                video_height = item.get('video', {}).get('height')
                video_width = item.get('video', {}).get('width')
                # video 播放url
                video_play_url = item.get('video', {}).get('play_addr', {}).get('url_list', [])[0]

                # 是否删除
                _d = item.get('status', {}).get('is_delete')     # True or False
                is_delete = 1 if _d else 0

                _ = {
                    'user_id': user_id,                 # 用户id
                    'head_img': head_img,               # 用户头像
                    'nick_name': nick_name,             # 用户昵称
                    'unique_id': unique_id,             # 抖音号(即根据抖音搜索能直接找到用户id)
                    'short_id': short_id,               # 短id(即也可根据短id查找到该用户)
                    'signature': signature,             # 用户签名
                    'singer_name': singer_name,         # 歌手名
                    'singer_head_img': singer_head_img, # 歌手头像
                    'music_name': music_name,           # 歌曲名
                    'music_play_url': music_play_url,   # 歌曲play_url
                    'video_id': video_id,               # 视频id
                    'video_desc': video_desc,           # 视频描述
                    'create_time': create_time,         # 视频创建时间
                    'comment_count': comment_count,     # 评论数
                    'like_count': like_count,           # 点赞数
                    'play_count': play_count,           # 播放数
                    'share_count': share_count,         # 分享数
                    'video_height': video_height,       # video的高度
                    'video_width': video_width,         # video的宽度
                    'video_play_url': video_play_url,   # video 播放url
                    'is_delete': is_delete,             # 是否删除
                }
                _video_list.append(_)

            except Exception as e:
                print('遇到错误:', e)
                break

        pprint(_video_list)

    def timestamp_to_regulartime(self, timestamp):
        '''
        将时间戳转换成时间
        '''
        # 利用localtime()函数将时间戳转化成localtime的格式
        # 利用strftime()函数重新格式化时间

        # 转换成localtime
        time_local = time.localtime(int(timestamp))
        # print(time_local)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

        return dt

    def __del__(self):
        gc.collect()

def get_all_user_id(file_path):
    all_user_id_list = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            if line == '':
                continue
            all_user_id_list.append(int(line))

    all_user_id_list = sorted(list(set(all_user_id_list)))

    return all_user_id_list

def main():
    douyin_path = '/Users/afa/myFiles/my_spider_logs/抖音/user_id.txt'
    all_user_id_list = get_all_user_id(file_path=douyin_path)

    while True:
        try:
            _ = DouYinUserIdParse()
            # 3055049857
            # user_id = input('请输入待抓取的user_id(以";"结束): ').strip('\n').strip(';')
            for user_id in all_user_id_list:
                print(user_id)
                _._get_aweme_api_videos_info(user_id=user_id)
                sleep(1.2)
        except KeyboardInterrupt:
            print('KeyboardInterrupt')

if __name__ == '__main__':
    main()

