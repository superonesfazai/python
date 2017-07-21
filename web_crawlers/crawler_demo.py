#!/usr/bin/python3.5
#coding: utf-8

import urllib
import urllib.request
import re  #正则表达式

#下载静态html网页
url = 'http://www.csdn.net'
with urllib.request.urlopen(url) as url1:
    content = url1.read()
#content = urllib.urlopen(url.read())  #python2.7
open('csdn.html', 'wb').write(content)
#获取标题
title_pat = r'(?<=<title>).*?(?=</title>)'
title_ex = re.compile(title_pat, re.M|re.S)
title_obj = re.search(title_ex, content)
title = title_obj.group()
print(title)
#获取超链接内容
href = r'<a href=.*?>(.*?)</a>'
m = re.findall(href, content, re.S|re.M)
for text in m:
    print (unicode(text, 'utf-8'))
    break
