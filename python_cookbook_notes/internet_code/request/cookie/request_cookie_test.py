#!/usr/bin/env python
# encoding: utf-8

import requests

def test_cookie():
    """
    测试cookies
    :return:
    """
    url = 'http://www.baixing.com'
    r = requests.get(url)
    print(r.cookies.items())  # [('__city', 'shanghai'), ('__s', '2hpl4if6jromtarou0vcvvtnm4')]
    # 清除会话 cookie
    r.cookies.clear_session_cookies()
    print(r.cookies.items())  # [('__city', 'shanghai')]



test_cookie()
