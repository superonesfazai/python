# coding = utf-8

'''
@author = super_fazai
@File    : duanzi_spider.py
@Time    : 2017/8/29 11:29
@connect : superonesfazai@gmail.com
'''

import urllib.request
import re
from urllib.error import URLError

class Spider:
    """
    内涵段子爬虫类
    """
    def __init__(self, page):
        self.page = page
        self.enable = True

    def load_page(self):
        '''
        定义一个请求url网页的方法, 来获取数据
        :return: 返回页面的html
        '''
        url =  'http://www.neihan8.com/article/list_5_' + str(self.page) + '.html'
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
        headers = {
            'user-agent': user_agent,
        }
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        html = response.read()
        # 注意 ：对于每个网站对中文的编码各自不同，
        # 所以html.decode(‘gbk’)的写法并不是通用写法，根据网站的编码而异
        gbk_html = html.decode('gbk').encode('utf-8')   # 解决中文乱码问题

        # 找到所有的段子内容<div class = "f18 mb20"></div>
        # re.S 如果没有re.S 则是只匹配一行有没有符合规则的字符串，如果没有则下一行重新匹配
        # 如果加上re.S 则是将所有的字符串将一个整体进行匹配
        pattern = re.compile(r'<div.*?class="f18 mb20">(.*?)</div>', re.S)
        self.item_list = pattern.findall(gbk_html.decode())
        # print(self.item_list)

        return self.item_list

    def print_one_page(self):
        '''
        处理得到的段子列表
        :param item_list: 得到的段子list
        :param page: 处理第几页
        :return:
        '''
        print("第 {} 页 开始爬取".format(self.page).center(50, '-'))
        for item in self.load_page():
            print("-" * 20)
            # 清洗数据
            item = item.replace('<p>', '').replace('</p>', '').replace('<br />', '')
            # print(item)
            self.write_2_file(item)
        print("第 {} 页 爬取完毕...".format(self.page).center(50, '-'))

    def write_2_file(self, text):
        '''
        将文件追加写进文件中
        :param text: 文件内容
        :return:
        '''
        my_file = open('./duanzi.txt', 'a+', encoding='utf-8')  # 这样打开能解决报错:UnicodeEncodeError: 'ascii' codec can't encode characters in position 2-5: ordinal not in range(128)
        my_file.write(text)
        my_file.write('-' * 100)
        my_file.close()

    def do_work(self):
        '''
        让crawler working
        :return:
        '''
        # 接下来我就通过参数的传递对page进行叠加来遍历 内涵段子吧的全部段子内容
        while self.enable:
            try:
                self.item_list = self.load_page()
            except URLError as e:
                print(e.reason)
                continue
            # 对得到的段子item_list进行处理
            self.print_one_page()
            self.page += 1


if __name__ == "__main__":
    """
        ======================
            内涵段子小爬虫
        ======================
    """
    title = r'''
    ======================
            内涵段子小爬虫
    ======================
    '''
    print(title)
    print('请输入enter继续...')
    input()
    my_spider = Spider(1)
    my_spider.do_work()