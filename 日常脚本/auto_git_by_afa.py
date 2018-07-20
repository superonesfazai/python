# coding=utf-8

from fzutils.linux_utils import auto_git

def main():
    python_path = '/home/afa/myFiles/codeDoc/pythonDoc/python'

    auto_git(python_path)
    print(' Money is on the way! '.center(100, '*'))

if __name__ == '__main__':
    main()