#coding: utf-8

# config.py版本是python2的
def test():
    """
    测试配置文件
    :return:
    """
    from config import db
    from config import proxy

    print(db)
    print(proxy)


if __name__ == '__main__':
    test()
