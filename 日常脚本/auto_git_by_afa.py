# coding=utf-8

from os.path import exists

from fzutils.auto_ops_utils import auto_git

def main():
    # home_linux
    # python_path = '/home/afa/myFiles/codeDoc/pythonDoc/python'
    # cp_mac
    python_path = '/Users/afa/myFiles/codeDoc/pythonDoc/python'
    fzutils_path = '/Users/afa/myFiles/codeDoc/pythonDoc/python/python网络数据采集/my_爬虫_进阶_之路/scrapy框架/my_spiders/fzutils'
    fz_ip_pools_path = '/Users/afa/myFiles/codeDoc/pythonDoc/python/python网络数据采集/my_爬虫_进阶_之路/scrapy框架/my_spiders/fz_ip_pool'
    blog_path = '/Users/afa/myFiles/superonesfazai.github.io'

    if exists(python_path):
        auto_git(python_path)
    else:
        print('{0} 路径有误! 无法进行git操作!'.format(python_path))

    if exists(fzutils_path):
        auto_git(fzutils_path)
    else:
        print('{0} 路径有误! 无法进行git操作!'.format(fzutils_path))

    if exists(fz_ip_pools_path):
        auto_git(fz_ip_pools_path)
    else:
        print('{0} 路径有误! 无法进行git操作!'.format(fz_ip_pools_path))

    if exists(blog_path):
        auto_git(blog_path)
    else:
        print('{0} 路径有误! 无法进行git操作!'.format(blog_path))

    print(' Money is on the way! '.center(100, '*'))

if __name__ == '__main__':
    main()