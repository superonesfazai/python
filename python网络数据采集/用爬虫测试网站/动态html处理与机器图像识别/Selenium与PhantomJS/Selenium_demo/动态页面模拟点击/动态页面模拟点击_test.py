# coding = utf-8

'''
@author = super_fazai
@File    : 动态页面模拟点击_test.py
@Time    : 2017/8/31 12:03
@connect : superonesfazai@gmail.com
'''

import unittest     # python测试模块
from selenium import webdriver
from bs4 import BeautifulSoup

class DouYuSelenium(unittest.TestCase):
    def setUp(self):
        '''
        初始化方法
        :return:
        '''
        self.driver = webdriver.PhantomJS()

    def test_douyu(self):   # 具体的测试用例方法，一定要以test开头
        self.driver.get('http://www.douyu.com/directory/all')
        while True:
            # 指定xml解析
            soup = BeautifulSoup(self.driver.page_source, 'xml')
            # 返回当前页面所有房间标题list 和 观众人数
            titles = soup.find_all('h3', {'class': 'ellipsis'})
            nums = soup.find_all('span', {'class': 'dy-num fr'})

            # 使用zip()函数来可以把list合并, 并创建一个元组对[(1, 2),(3, 4)]
            for title, num in zip(nums, titles):
                print('观众人数:' + num.get_text().strip(), '\t房间标题:' + title.get_text().strip())
            # page_source.find()未找到内容则返回-1
            if self.driver.page_source.find('shark-pager-disable-next') != -1:
                break
            # 模拟下一页点击
            self.driver.find_element_by_class_name('shark-pager-next').click()
    def tearDown(self):
        print('加载完成...')
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()

