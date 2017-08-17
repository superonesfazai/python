# coding=utf-8

import os
import time

def auto_git():
    # os.popen('cd ~/myFiles/codeDoc/PythonDoc && ls')
    # time.sleep(0.5)
    os.popen('cd ~/myFiles/codeDoc/PythonDoc && git add --all')
    time.sleep(2)
    os.system('cd ~/myFiles/codeDoc/PythonDoc && git commit -m "{}"'.format(time.ctime()))
    time.sleep(2)
    os.system('cd ~/myFiles/codeDoc/PythonDoc && git push -u origin master')
    print('提交成功!!')

if __name__ == '__main__':
    auto_git()
