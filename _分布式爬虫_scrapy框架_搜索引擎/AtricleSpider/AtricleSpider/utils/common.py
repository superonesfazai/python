#coding: utf-8

import hashlib

def get_md5(url):  #完成md5的摘要生成
    #if isinstance(url, str):  #python3中的判断方法,因为python3中没有unicode这个说法了,而python2中还有
    if isinstance(url, unicode):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()  #抽取摘要

if __name__ == '__main__':
    print(get_md5('http://jobbole.com'))  #python2中的写法,python2直接能处理unicode的编码
    #print(get_md5('http://jobbole.com'.encode('utf-8')))  #python3中的写法,python3不能直接处理unicode的编码