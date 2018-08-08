# coding:utf-8

'''
@author = super_fazai
@File    : tmp_pcbody.py
@Time    : 2016/12/3 14:30
@connect : superonesfazai@gmail.com
'''

import requests
import re
from scrapy.selector import Selector
import selenium.webdriver.support.ui as ui
from pprint import pprint
from selenium import webdriver
import gc
from time import sleep

# phantomjs驱动地址
EXECUTABLE_PATH = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'

def get_body():
    start_url = 'http://life.pcbaby.com.cn/xms/'
    all_ul_list = []
    for index in range(0, 100):
        if index == 0:
            next_url = start_url
        else:
            next_url = start_url +'index_{0}.html'.format(index)
        print('待处理的next_url为: ', next_url)
        response = requests.get(next_url)
        body = response.content.decode('gbk')
        # body = re.compile(r'\n').sub('', body)
        body = re.compile(r'\t').sub('', body)
        body = re.compile(r'  ').sub('', body)
        # print(body)

        tmp_ul_list = parse_1(body=body)
        print(tmp_ul_list)
        for item in tmp_ul_list:
            all_ul_list.append(item)
    print(all_ul_list)

def parse_1(body):
    # ul.mb30 li
    ul = Selector(text=body).css('ul.mb30').extract_first()
    if ul is None:
        print('ul为空值')
        return []

    # print(ul)
    # print(list(Selector(text=ul).css('li').extract()))
    my_ul = []
    for item in list(Selector(text=ul).css('li').extract()):
        li_url = 'http:' + Selector(text=item).css('dd.oh p a::attr("href")').extract_first()
        # print(li_url)
        title = Selector(text=item).css('dd.oh p a::text').extract_first()
        simple_intro = Selector(text=item).css('dd.oh p.aList-intro::text').extract_first()
        main_img_url = Selector(text=item).css('div.aList-img img::attr("src")').extract_first()
        if main_img_url is not None:
            main_img_url = 'http:' + main_img_url

        else:
            main_img_url = ''
        content = my_tmp.get_body(url=li_url)
        # print(content)
        my_li = {
            'li_url': li_url,               # 新闻的地址
            'title': title,                 # 新闻的标题
            'simple_intro': simple_intro,   # 新闻的简介
            'main_img_url': main_img_url,   # 新闻的主图
            'content': content,             # 新闻的内容
        }
        print(my_li)
        my_ul.append(my_li)
    # print(my_ul)
    return my_ul

class MyTmp():
    def init_phantomjs(self):
        print('--->>>初始化phantomjs驱动中<<<---')
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000  # 1秒
        cap['phantomjs.page.settings.loadImages'] = False
        cap['phantomjs.page.settings.disk-cache'] = True
        # cap['phantomjs.page.settings.userAgent'] = HEADERS[randint(0, 34)]  # 随机一个请求头
        # cap['phantomjs.page.customHeaders.Cookie'] = cookies

        self.driver = webdriver.PhantomJS(executable_path=EXECUTABLE_PATH, desired_capabilities=cap)

        wait = ui.WebDriverWait(self.driver, 15)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        print('------->>>初始化完毕<<<-------')

    def get_body(self, url):
        self.driver.set_page_load_timeout(10)  # 设置成10秒避免数据出错

        try:
            self.driver.get(url)
            self.driver.implicitly_wait(15)
            body = self.driver.page_source
            body = re.compile(r'\n').sub('', body)
            body = re.compile(r'\t').sub('', body)
            body = re.compile(r'  ').sub('', body)
            # print(body)

        except Exception as e:  # 如果超时, 终止加载并继续后续操作
            print('-->>time out after 10 seconds when loading page')
            self.driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            body = ''

        # tmp_body = Selector(text=body).css('div.artText').extract_first()
        tmp_body = re.compile(r'<div class="artText">(.*)<div class="artNav">').findall(body)
        if tmp_body != []:
            tmp_body = '<div class="artText">' + tmp_body[0]
            tmp_body = re.compile(r'src="//www1.pcbaby.com.cn/images/blank.gif" #').sub(r'', tmp_body)
            tmp_body = re.compile(r'图片来源：太平洋亲子网').sub(r'', tmp_body)
            tmp_body = re.compile(r'<p>　　打开淘宝APP，搜索“@太平洋亲子”，<em style="color: #f44">关注</em>后抽母婴大奖。</p>').sub('', tmp_body)
            tmp_body = re.compile(r'src=\"').sub('src=\"http:', tmp_body)
            # print(tmp_body)
            return tmp_body
        else:
            print('tmp_body为空值')
            return ''

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        gc.collect()

my_tmp = MyTmp()
my_tmp.init_phantomjs()

if __name__ == '__main__':
    get_body()
    try:
        del my_tmp
    except:
        pass
    gc.collect()

