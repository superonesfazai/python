# 处理app的主要业务逻辑
# coding: utf-8

import os
import cards_utils

def init_menu():
    while True:
        print('欢迎使用<名片系统> v0.1beta'.center(35, '*'))
        print('1.新建名片'.center(35, ' '))
        print('2.显示全部'.center(35, ' '))
        print('3.查询名片'.center(35, ' '))
        print('4.删除名片'.center(35, ' '))
        print('5.更改名片'.center(35, ' '))
        print('0.退出'.center(35, ' '))
        print(''.center(40, '*'))
        msg = int(input('请输入功能编号:'))

        if msg == 1:
            cards_utils.new_card()
        elif msg == 2:
            os.system('clear')
            cards_utils.show_all_cards()
            input('请输入任意值继续')
            os.system('clear')
        elif msg == 3:
            os.system('clear')
            cards_utils.index_card()
            input('请输入任意值继续')
        elif msg == 4:
            os.system('clear')
            cards_utils.del_card()
            input('请输入任意值继续')
        elif msg == 5:
            os.system('clear')
        elif msg == 0:
            # os.system('clear')
            print('欢迎再次使用!')
            break
        else:
            print('输入错误,请重新输入!!')
            input('请输入任意值继续')
            os.system('clear')

init_menu()