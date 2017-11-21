# coding=utf-8

import os
import time
import datetime
import re

def auto_git(path):
    # os.popen('cd ~/myFiles/codeDoc/PythonDoc && ls')
    # time.sleep(0.5)
    print((path+'  正在提交').center(100, '*'))
    os.popen('cd {0} && git add --all'.format(path))
    time.sleep(2)
    now_time = str(datetime.datetime.now())
    now_time = str(re.compile(r'\..*').sub('', now_time))
    print(now_time)
    os.system('cd {0} && git commit -m "{1}"'.format(path, now_time))
    time.sleep(2)
    os.system('cd {0} && git push -u origin master'.format(path))
    print((path + ' 提交成功!!').center(100, '*') + '\n')

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