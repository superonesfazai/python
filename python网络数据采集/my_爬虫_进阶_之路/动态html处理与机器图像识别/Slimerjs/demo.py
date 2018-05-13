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
import gc


SLIMERJS_DRIVER_PATH = '/Users/afa/myFiles/tools/slimerjs-1.0.0/slimerjs'

driver = webdriver.PhantomJS(executable_path=SLIMERJS_DRIVER_PATH)
# driver.get('https://slimerjs.org')
# sleep(3)
# driver.save_screenshot('screenie.png')

js = r'''
var page = require('webpage').create();
 var videoUrl = phantom.args[0];
 var page.open(videoUrl, function (){
      window.setTimeout(function(){
            phantom.exit();
      },10);
});
'''

driver.execute_script(js)

try:
    del driver
    driver.quit()
except:
    print('driver释放失败')
gc.collect()