# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@connect : superonesfazai@gmail.com
'''

import re
from celery.utils.log import get_task_logger
from fzutils.celery_utils import init_celery_app
from fzutils.spider.fz_driver import BaseDriver
from fzutils.common_utils import json_2_dict

PHANTOMJS_DRIVER_PATH = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'

tasks_name = 'driver_tasks'
app = init_celery_app(
    name=tasks_name,
)
lg = get_task_logger(tasks_name)

@app.task(name=tasks_name + '._test', bind=True)
def _test(self):
    driver = BaseDriver(executable_path=PHANTOMJS_DRIVER_PATH)
    url = 'https://httpbin.org/get'
    body = driver.get_url_body(url=url)
    # lg.info(str(body))
    try:
        data = json_2_dict(re.compile('<pre.*?>(.*)</pre>').findall(body)[0], default_res={})
    except IndexError:
        return {}
    del driver

    return data