# coding=utf-8

import os
import time

def auto_git():
    # os.popen('cd ~/myFiles/codeDoc/PythonDoc && ls')
    # time.sleep(0.5)
    path = '~/myFiles/codeDoc/PythonDoc'
    os.popen('cd {} && git add --all'.format(path))
    time.sleep(2)
    os.system('cd {} && git commit -m "{}"'.format(path, time.ctime()))
    time.sleep(2)
    os.system('cd {} && git push -u origin master'.format(path))
    print('提交成功!!')

if __name__ == '__main__':
    auto_git()
