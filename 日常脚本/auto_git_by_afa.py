# coding=utf-8

import os

from fzutils.auto_ops_utils import auto_git

def main():
    # home_linux
    # python_path = '/home/afa/myFiles/codeDoc/pythonDoc/python'
    # cp_mac
    python_path = '/Users/afa/myFiles/codeDoc/pythonDoc/python'
    fzutils_path = '/Users/afa/myFiles/codeDoc/pythonDoc/python/python网络数据采集/my_爬虫_进阶_之路/scrapy框架/my_spiders/fzutils'

    if os.path.exists(python_path):
        auto_git(python_path)
    else:
        print('{0} 路径有误! 无法进行git操作!'.format(python_path))

    if os.path.exists(fzutils_path):
        auto_git(fzutils_path)
    else:
        print('{0} 路径有误! 无法进行git操作!'.format(fzutils_path))

    print(' Money is on the way! '.center(100, '*'))

if __name__ == '__main__':
    main()