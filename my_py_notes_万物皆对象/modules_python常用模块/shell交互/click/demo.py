# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from click import command as click_command
from click import option as click_option
from click import echo as click_echo

@click_command()
@click_option("-count", default=1, help="Number of greetings.")
@click_option("-name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    for _ in range(count):
        click_echo("Hello, %s!" % name)

spider_name = None

@click_command()
@click_option('-spider_name', type=str, default=None, help='spider_name!!')
def init_spider(c):
    global spider_name
    spider_name = c
    _ = Spider(spider_name=spider_name)

class Spider():
    def __init__(self, spider_name):
        print(spider_name)

if __name__ == '__main__':
    # hello()
    init_spider()

"""
$ python demo.py --count=3
Your name: Click
Hello, Click!
Hello, Click!
Hello, Click!
"""