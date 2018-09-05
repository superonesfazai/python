# coding = utf-8

'''
@author = super_fazai
@File    : shandong_envir.py
@Time    : 2017/9/22 09:10
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from pprint import pprint
from urllib.request import urlopen
import re

class ShanDongEnvir(object):
    def __init__(self):
        self.driver = webdriver.Chrome('/Users/afa/myFiles/tools/chromedriver')

    def run(self):
        self.driver.get('http://58.56.98.78:8801/AirDeploy.Web/AirQuality/MapMain.aspx?type=kqzl')

        # self.driver.save_screenshot('12.png')
        js = 'document.getElementById("div_FirstText").style.display="none";'

        self.driver.execute_script(js)

        # self.driver.save_screenshot('2.png')

        tmp_soup = BeautifulSoup(self.driver.page_source, 'lxml')

        time_now = tmp_soup.select('.shuoming_fra .date')[0].get_text()
        city_name = tmp_soup.select('#divList tbody tr td')[0].get_text()
        city_focus = tmp_soup.select('#divList tbody tr td')[1].get_text()

        print(time_now)
        print(city_name)
        print(city_focus)

        # self.driver.find_element('#divList tbody tr td a').click()

        self.driver.find_element_by_css_selector('#divList tbody tr td a').click()

        sleep(3)

        # self.driver.save_screenshot('3.png')
        # pprint(self.driver.switch_to.frame(0))

        deal_info_link = self.driver.find_element_by_css_selector('#contents .contentPane iframe').get_property('src')
        print(deal_info_link)
        # city_focus_number = re.compile('')


if __name__ == '__main__':
    envir = ShanDongEnvir()
    envir.run()
