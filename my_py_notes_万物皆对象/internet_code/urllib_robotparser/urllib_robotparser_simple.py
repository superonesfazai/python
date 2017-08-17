# coding = utf-8

'''
@author = super_fazai
@File    : urllib_robotparser_simple.py
@Time    : 2017/8/17 12:07
@connect : superonesfazai@gmail.com
'''

"""
一个网络爬虫能通过使用RobotFileParser.can_fetch()来测试一个网站是否允许去下载界面
"""

from urllib import parse, robotparser

AGENT_NAME = 'PyMOTW'
URL_BASE = 'http://pymotw.com/'
parser = robotparser.RobotFileParser()
parser.set_url(parse.urljoin(URL_BASE, 'robots.txt'))
parser.read()

PATHS = [
    '/',
    '/PyMOTW/',
    '/admin/',
    '/downloads/PyMOTW-1.92.tar.gz',
]

for path in PATHS:
    print('{!r:>6} : {}'.format(
        parser.can_fetch(AGENT_NAME, path), path))
    url = parse.urljoin(URL_BASE, path)
    print('{!r:>6} : {}'.format(
        parser.can_fetch(AGENT_NAME, url), url))
    print()

'''
测试结果:
True : /
  True : http://pymotw.com/

  True : /PyMOTW/
  True : http://pymotw.com/PyMOTW/

 False : /admin/
 False : http://pymotw.com/admin/

 False : /downloads/PyMOTW-1.92.tar.gz
 False : http://pymotw.com/downloads/PyMOTW-1.92.tar.gz
'''