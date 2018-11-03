# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@connect : superonesfazai@gmail.com
'''

"""
curl命令 转成原生的python requests代码
"""

from fzutils.curl_utils import curl_cmd_2_py_code

curl_cmd = r'''
curl 'https://item.m.jd.com/ware/view.action?wareId=5089253' -H 'authority: item.m.jd.com' -H 'cache-control: max-age=0' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9' -H 'cookie: shshshfpa=190d22bf-c657-9adf-7ed0-5231583371a5-1540431960; __jdv=122270672|direct|-|none|-|1540431960925; shshshfpb=06a4d86b086a7f8906e5568293f314080816ad1953614db365bd120596; __jdu=1540431960925947619357; __jda=122270672.1540431960925947619357.1540431961.1540973528.1541226872.3; __jdc=122270672; PCSYCityID=1213; 3AB9D23F7A4B3C9B=VPTRMAJLYNCCOBDCWN4WIXBXMHFSLMAUXAEDILFUILKYURR2LK6JT4HQAT7I2A2ROS73HDVPIHLJSRARZUQ3HLZ6FQ; _gcl_au=1.1.1309968266.1541226881; SERVERID=829967b5466bfedb97552b970fb8e158; wxa_level=1; cid=9; webp=1; mba_muid=1540431960925947619357; autoOpenApp_downCloseDate_auto=1541227023062_21600000; sc_width=414; wq_area=15_1213_0%7C; retina=0; visitkey=46448432169960106; ipLoc-djd=1-72-4137-0; areaId=1; warehistory="5089253,100000822981,"; wq_logid=1541227231.1523346430; __jdb=122270672.9.1540431960925947619357|3.1541226872; mba_sid=15412270217292328127344821122.3; __wga=1541227234286.1541227025126.1541227025126.1541227025126.3.1; PPRD_P=UUID.1540431960925947619357-LOGID.1541227234306.677776343; shshshfp=8b9dc4f8d614a6a42b69cf7d1607a8ac; shshshsID=cef18e5ba9d31fbf3b4e0158c6436749_6_1541227235080' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)