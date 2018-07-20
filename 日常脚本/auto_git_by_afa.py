# coding=utf-8

import os

from fzutils.linux_utils import auto_git

def main():
    # home_linux
    python_path = '/home/afa/myFiles/codeDoc/pythonDoc/python'
    # cp_mac

    if os.path.exists(python_path):
        auto_git(python_path)
        print(' Money is on the way! '.center(100, '*'))
    else:
        print('{0} 路径有误! 无法进行git操作!'.format(python_path))

if __name__ == '__main__':
    main()