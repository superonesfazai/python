# coding = utf-8

'''
@author = super_fazai
@File    : 模拟滚动条滚动到底部.py
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
import time
from time import sleep, time

driver = webdriver.PhantomJS(executable_path='/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs')
# driver.get('https://movie.douban.com/typerank?type_name=剧情&type=11&interval_id=100:90&action=')
# driver.get('https://d.weibo.com')
# url  = 'https://weibo.com/tupiandingjian?refer_flag=0000015010_/info?mod&is_all=1'
# url = 'https://item.taobao.com/item.htm?id=542022399141&ali_trackid=2:mm_55678658_12502097_47308190:1508679867_237_2040095806&spm=a21bo.7925826.192013.3.64336a46QXTShg'
# url = 'https://h5.m.taobao.com/app/detail/desc.html?_isH5Des=true#!id=546756179626&type=0&f=TB1aJRLQXXXXXXyXFXX8qtpFXlX&sellerType=C'
url = 'https://m.1688.com/page/offerRemark.htm?offerId=534158857177'

start_time = time()
driver.get(url)
print(time()-start_time)

# 向下滚动10000像素
js = 'document.body.scrollTop=10000'
# js="var q=document.documentElement.scrollTop=10000"
# js = r'''
# function scrollToBottom() {
#     var Height = document.body.clientHeight,  //文本高度
#         screenHeight = window.innerHeight,  //屏幕高度
#         INTERVAL = 100,  // 滚动动作之间的间隔时间
#         delta = 500,  //每次滚动距离
#         curScrollTop = 0;    //当前window.scrollTop 值
#
#     var scroll = function () {
#         curScrollTop = document.body.scrollTop;
#         window.scrollTo(0,curScrollTop + delta);
#     };
#
#     var timer = setInterval(function () {
#         var curHeight = curScrollTop + screenHeight;
#         if (curHeight >= Height){   //滚动到页面底部时，结束滚动
#             clearInterval(timer);
#         }
#         scroll();
#     }, INTERVAL)
# }
# scrollToBottom()
# '''
sleep(4)
# driver.implicitly_wait(20)

# exec_code = compile('''
# driver.find_element_by_css_selector('div.tab-item.filter:nth-child(2)').click()
# ''', '', 'exec')
# exec(exec_code)
# 查看页面快照
driver.save_screenshot('douban.png')

# 执行js语句
driver.execute_script(js)
sleep(4)

# 查看页面快照
driver.save_screenshot('newdouban.png')
# print(driver.page_source)
driver.quit()