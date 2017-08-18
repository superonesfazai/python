# coding = utf-8

'''
@author = super_fazai
@File    : re_html_文本提取_test.py
@Time    : 2017/8/18 16:36
@connect : superonesfazai@gmail.com
'''

tmp_html = r'''
<div>
        <p>岗位职责：</p>
<p>完成推荐算法、数据统计、接口、后台等服务器端相关工作</p>
<p><br></p>
<p>必备要求：</p>
<p>良好的自我驱动力和职业素养，工作积极主动、结果导向</p>
<p>&nbsp;<br></p>
<p>技术要求：</p>
<p>1、一年以上 Python 开发经验，掌握面向对象分析和设计，了解设计模式</p>
<p>2、掌握HTTP协议，熟悉MVC、MVVM等概念以及相关WEB开发框架</p>
<p>3、掌握关系数据库开发设计，掌握 SQL，熟练使用 MySQL/PostgreSQL 中的一种<br></p>
<p>4、掌握NoSQL、MQ，熟练使用对应技术解决方案</p>
<p>5、熟悉 Javascript/CSS/HTML5，JQuery、React、Vue.js</p>
<p>&nbsp;<br></p>
<p>加分项：</p>
<p>大数据，数理统计，机器学习，sklearn，高性能，大并发。</p>

</div>
'''

import re
from pprint import pprint

regex = r'<p>(.*?)</p>'

regex = re.compile(regex)

result = re.findall(regex, tmp_html)
# result = ' '.join(result).replace('&nbsp', '').replace('<br>', '')

for item in result:
    if item == '&nbsp;<br>' or item == '<br>':
        result.remove(item)

for item in result:
    pprint(item)

pprint(result)
