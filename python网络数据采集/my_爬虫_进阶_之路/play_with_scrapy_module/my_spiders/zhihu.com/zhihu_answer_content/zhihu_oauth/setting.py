# coding=utf-8

from __future__ import unicode_literals

import requests.adapters

ADAPTER_WITH_RETRY = requests.adapters.HTTPAdapter(
    max_retries=requests.adapters.Retry(
        total=10,
        status_forcelist=[403, 408, 500, 502]
    )
)

DEFAULT_CAPTCHA_FILENAME = 'captcha.gif'
"""
请求验证码后储存文件名的默认值，现在的值是当前目录下的 captcha.gif。

仅在 :meth:`.ZhihuClient.login_in_terminal` 中被使用。
"""
