#!/usr/bin/python3.5
#coding: utf-8

#通过len(file.readlines())来返回一个文件的行数

#通常我们在读取文件的时候，会用到read(), readline(), readlines()
#通常的用法
#1.
def test1():
    with open('避免死锁.md.txt', "r") as f:
        print (f.read())
    f.close()
#2.
def test2():    
    f = open("避免死锁.md.txt", "r")
    for line in f.readlines(): 
        line = line.strip('\n')  #python按行读取文件，如何去掉换行符"\n"
        print (line)    
    f.close()

#python读取大文件的方法
#方法1：
#将文件切分成小段，每次处理完小段内容后，释放内存
#这里会使用yield生成自定义可迭代对象， 即generator， 每一个带有yield的函数就是一个generator

def read_in_block(file_path):    
    BLOCK_SIZE = 1024    
    with open(file_path, "r") as f:        
        while True:            
            block = f.read(BLOCK_SIZE)  # 每次读取固定长度到内存缓冲区            
            if block:                
                yield block            
            else:                
                return  # 如果读取到文件末尾，则退出

def test3():    
    file_path = "避免死锁.md.txt"
    for block in read_in_block(file_path):        
        print (block)

#方法2：
#利用open("", "")系统自带方法生成迭代对象
#for line in f这种用法是把文件对象f当作迭代对象,系统将自动处理IO缓冲和内存管理, 这种方法是更加pythonic的方法,比较简洁
def test4():
    with open('避免死锁.md.txt') as f:
        for line in f:
            line = line.strip('\n')
            print (line)

if __name__ == '__main__':
    test4()


