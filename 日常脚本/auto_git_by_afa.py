# coding=utf-8

import os
import time
import pytz
import datetime
import re

def auto_git(path):
    # os.popen('cd ~/myFiles/codeDoc/PythonDoc && ls')
    # time.sleep(0.5)
    print((path+'  正在提交').center(100, '*'))
    os.popen('cd {} && git add --all'.format(path))
    time.sleep(2)
    os.system('cd {} && git commit -m "{}"'.format(path, get_shanghai_time()))
    time.sleep(2)
    os.system('cd {} && git push -u origin master'.format(path))
    print((path + ' 提交成功!!').center(100, '*') + '\n')

def get_shanghai_time():
    '''
    时区处理，时间处理到上海时间
    '''
    tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
    now_time = datetime.datetime.now(tz)

    # 处理为精确到秒位，删除时区信息
    now_time = re.compile(r'\..*').sub('', str(now_time))
    # 将字符串类型转换为datetime类型
    now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

    return str(now_time)

def main():
    python_path = '~/myFiles/codeDoc/PythonDoc'
    js_path = '~/myFiles/codeDoc/js_doc'
    jquery_path = '~/myFiles/codeDoc/jquery'
    html_path = '~/myFiles/codeDoc/html_doc'
 
    auto_git(python_path)
    auto_git(html_path)
    auto_git(js_path)
    auto_git(jquery_path)
    print(' Money is on the way! '.center(100, '*'))

if __name__ == '__main__':
    main()