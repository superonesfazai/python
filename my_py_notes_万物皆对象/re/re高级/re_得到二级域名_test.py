# coding = utf-8

'''
@author = super_fazai
@File    : re_得到二级域名_test.py
@Time    : 2017/8/18 16:52
@connect : superonesfazai@gmail.com
'''

import re

tmp_ = r'''
http://www.interoem.com/messageinfo.asp?id=35
http://3995503.com/class/class09/news_show.asp?id=14
http://lib.wzmc.edu.cn/news/onews.asp?id=769
http://www.zy-ls.com/alfx.asp?newsid=377&id=6
http://www.fincm.com/newslist.asp?id=415
'''

result = re.findall(r'(http://.*?.(com|cn))', tmp_)

for i in range(0, len(result)):
    print(result[i][0])