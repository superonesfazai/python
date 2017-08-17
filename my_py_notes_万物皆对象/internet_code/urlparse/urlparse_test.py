# encoding: utf-8

import sys
sys.path.append('...')
from 日常脚本.url import get_next_url

print(get_next_url('http://www.163.com/mail/index.htm', 'http://www.163.com/about.htm'))
print(get_next_url('http://www.163.com/mail/index.htm', '/about.htm'))
print(get_next_url('http://www.163.com/mail/index.htm', 'about.htm'))