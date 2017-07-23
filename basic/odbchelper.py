#!/usr/bin/python3.5
#coding: utf-8

def buildConnectionString(params):
    '''
    Build a connection string from a dictionary of parameters.
    Returns string.
    '''
    return ';'.join(['%s=%s' % (k, v) for k, v in params.items()])

if __name__ == '__main__':
    myParams = {'server':'mpilgrim', \
                'database':'master', \
                'uid':'sa', \
                'pwd':'secret'}
    print(buildConnectionString(myParams))

    for i in '可迭代对象':
        pass