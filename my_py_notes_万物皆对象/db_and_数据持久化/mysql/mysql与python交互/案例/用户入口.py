# coding = utf-8

'''
@author = super_fazai
@File    : 用户入口.py
@Time    : 2017/9/12 15:56
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('.')

from tests import tests

t1= tests(
    host='localhost',
    port=3306,
    db='python',
    user='root',
    passwd='lrf654321',
)

while True:
    txt=input("请输入要进行的操作：1查询，2增加，3修改，4删除，5退出：")
    if txt=="1":
        result=t1.select()
        if result==None:
            print('表中无数据')
        else:
            for item in result:
                print('%s__%s'%(item[0], item[1]))
    elif txt=="2":
        title=input('请输入标题：')
        if t1.insert(title):
            print('添加成功')
        else:
            print('添加失败')
    elif txt=="3":
        tid=input('请输入编号：')
        title=input('请输入新标题：')
        if t1.update(title,tid):
            print('修改成功')
        else:
            print('修改失败')
    elif txt=="4":
        tid=input('请输入编号：')
        if t1.delete(tid):
            print('删除成功')
        else:
            print('删除失败')
    elif txt=="5":
        break