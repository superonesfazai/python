# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-21 下午2:41
# @File    : juhe_data_box_office.py

from urllib.request import urlopen
from urllib.error import HTTPError

import os
import json

area = ['cn', 'us', 'hk']
data_type = ['json', 'xml']
my_key = '65db3f69cb847043fe48cf072bbf6f79'
msg = ''

def init_menu():

    menu_info = '''
              \t-1.获取内地电影票房榜
              \t-2.获取美国电影票房榜
              \t-3.获取香港电影票房榜
              \t-0.退出
    '''

    print('在线获取近期电影票房榜'.center(40, '*'))
    print(menu_info)
    print('*'.center(40, '*'))

class box_office(object):
    def get_box_office(msg):
        def print_info(json_obj):
            # print(json_obj.get('reason'))
            result = json_obj.get('result')

            print('本周统计时间: ', result[0]['wk'])
            for i in range(0, len(result)):
                # print(result[i])
                print('票房排名:', result[i]['rid'], end=' ')
                print('电影名:', result[i]['name'], end=' ')
                print('本周票房收入: ', result[i]['wboxoffice'], end=' ')
                print('总票房收入: ', result[i]['tboxoffice'])

        global area
        try:
            tmp_html = 'http://v.juhe.cn/boxoffice/rank?' \
                       'area=%s' \
                       '&dtype=%s' \
                       '&key=%s' % (area[msg], data_type[0], my_key)
            print(area[msg])
            json_data = urlopen(tmp_html).read().decode('utf-8')
            # print(json)
        except HTTPError as e:
            print('data 获取失败,网络连接异常...')
        else:
            if json == None:
                print('data 为空!无法解析!')
                return False
            else:
                json_obj = json.loads(json_data)
                print_info(json_obj)
                return True


def main():
    global msg
    while True:
        init_menu()
        msg = int(input('请输入您要在线获取的信息:'))
        if msg == 1:
            box_office.get_box_office(msg-1)
            print('获取成功！')
        elif msg == 2:
            box_office.get_box_office(msg-1)
            print('获取成功！')
        elif msg == 3:
            box_office.get_box_office(msg-1)
        elif msg == 0:
            os.system('clear')
            break
            pass
        else:
            print('输入有误!请重新输入')
            os.system('clear')
            continue

if __name__ == '__main__':
    main()