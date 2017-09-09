# coding=utf-8

import os
import time

def auto_git(path):
    # os.popen('cd ~/myFiles/codeDoc/PythonDoc && ls')
    # time.sleep(0.5)
    print((path+'  正在提交').center(200, '-'))
    os.popen('cd {} && git add --all'.format(path))
    time.sleep(2)
    os.system('cd {} && git commit -m "{}"'.format(path, time.ctime()))
    time.sleep(2)
    os.system('cd {} && git push -u origin master'.format(path))
    print((path + ' 提交成功!!').center(200, '-') + '\n')

def main():
    python_path = '~/myFiles/codeDoc/PythonDoc'
    js_path = '~/myFiles/codeDoc/js_doc'
    jquery = '~/myFiles/codeDoc/jquery'

    auto_git(python_path)
    auto_git(js_path)
    auto_git(jquery)
    print('\n' + '再接再厉哦!'.center(250, '*'))

if __name__ == '__main__':
    main()