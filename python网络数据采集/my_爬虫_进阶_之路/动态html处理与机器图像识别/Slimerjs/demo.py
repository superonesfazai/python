# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2018/4/14 11:47
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
import time
from time import sleep, time

FIRFOX_DRIVER_PATH = '/Users/afa/myFiles/tools/geckodriver'
driver = webdriver.Firefox(executable_path=FIRFOX_DRIVER_PATH)

js = r'''
var page = require("webpage").create();
page.open("http://slimerjs.org")
    .then(function(status){
         if (status == "success") {
             console.log("The title of the page is: "+ page.title);
         }
         else {
             console.log("Sorry, the page is not loaded");
         }
         page.close();
         phantom.exit();
    })
'''

try:
    driver.execute_script(js)
except Exception as e:
    print('遇到错误:', e)
finally:
    driver.quit()