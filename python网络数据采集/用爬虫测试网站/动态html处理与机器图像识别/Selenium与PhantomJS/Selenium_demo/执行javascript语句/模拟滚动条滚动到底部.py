# coding = utf-8

'''
@author = super_fazai
@File    : 模拟滚动条滚动到底部.py
@Time    : 2017/8/31 12:29
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
import time

driver = webdriver.PhantomJS(executable_path='/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs')
# driver.get('https://movie.douban.com/typerank?type_name=剧情&type=11&interval_id=100:90&action=')
# driver.get('https://d.weibo.com')
driver.get('https://weibo.com/tupiandingjian?refer_flag=0000015010_/info?mod&is_all=1')
# 向下滚动10000像素
# js = 'document.body.scrollTop=10000'
# js="var q=document.documentElement.scrollTop=10000"
js = r'''
function scrollToBottom() {
    var Height = document.body.clientHeight,  //文本高度
        screenHeight = window.innerHeight,  //屏幕高度
        INTERVAL = 100,  // 滚动动作之间的间隔时间
        delta = 500,  //每次滚动距离
        curScrollTop = 0;    //当前window.scrollTop 值

    var scroll = function () {
        curScrollTop = document.body.scrollTop;
        window.scrollTo(0,curScrollTop + delta);
    };

    var timer = setInterval(function () {
        var curHeight = curScrollTop + screenHeight;
        if (curHeight >= Height){   //滚动到页面底部时，结束滚动
            clearInterval(timer);
        }
        scroll();
    }, INTERVAL)
}
scrollToBottom()
'''
time.sleep(5)
# driver.implicitly_wait(20)
# 查看页面快照
driver.save_screenshot('douban.png')

# 执行js语句
driver.execute_script(js)
time.sleep(5)

# 查看页面快照
driver.save_screenshot('newdouban.png')

driver.quit()