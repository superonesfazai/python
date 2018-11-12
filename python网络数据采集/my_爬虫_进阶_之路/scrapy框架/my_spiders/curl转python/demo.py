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
curl 'https://item.jd.com/4857727.html' -H 'authority: item.jd.com' -H 'cache-control: max-age=0' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9' -H 'cookie: shshshfpa=190d22bf-c657-9adf-7ed0-5231583371a5-1540431960; shshshfpb=06a4d86b086a7f8906e5568293f314080816ad1953614db365bd120596; __jdu=1540431960925947619357; PCSYCityID=1213; ipLoc-djd=1-72-4137-0; areaId=1; __jdc=122270672; __jdv=122270672|direct|-|none|-|1541986604770; __jda=122270672.1540431960925947619357.1540431961.1542001715.1542010948.9; shshshfp=20209411dd610d79a14a289de473b73d; shshshsID=6723f66314ae61c86d2ef4e42ef98985_15_1542016992511; __jdb=122270672.17.1540431960925947619357|9.1542010948; _gcl_au=1.1.36857904.1542016993; 3AB9D23F7A4B3C9B=VPTRMAJLYNCCOBDCWN4WIXBXMHFSLMAUXAEDILFUILKYURR2LK6JT4HQAT7I2A2ROS73HDVPIHLJSRARZUQ3HLZ6FQ' -H 'if-modified-since: Mon, 12 Nov 2018 09:56:40 GMT' --compressed
'''
res = curl_cmd_2_py_code(curl_cmd)
print(res)