# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2017/4/25 14:15
@connect : superonesfazai@gmail.com
'''

# 帮小小学妹简单处理xls

import pyexcel, re
from pprint import pprint

def deal_with_data_by_course_name(file_path, course_name):
    data = pyexcel.iget_records(file_name=file_path)

    for row in data:   # row a OrderedDict object
        # print(row)
        # break
        row = dict(row)
        class_name = row.get('课程名', '')
        if class_name == '':
            print('无该课程!')
            return None

        if class_name == course_name\
                and re.compile(r'软').findall(row.get('班级', '')) != []:
            try:
                row.pop('课程号')
                row.pop('星期')
            except: pass
            pprint(row)

    return None

def deal_with_data_by_stu_name(file_path, stu_name):
    data = pyexcel.iget_records(file_name=file_path)

    for row in data:   # row a OrderedDict object
        # print(row)
        # break
        row = dict(row)
        name = row.get('姓名', '')
        if stu_name == '':
            print('无该stu!')
            return None

        if name == stu_name\
                and re.compile(r'软').findall(row.get('班级', '')) != []:
            try:
                row.pop('课程号')
                row.pop('星期')
            except: pass
            pprint(row)

    return None

deal_with_data_by_course_name(
    file_path='/Users/afa/Downloads/exam_stu_table.xls',
    course_name='电路与模拟电子技术'
    # course_name='概率论与数理统计'
    # course_name='离散数学'
    # course_name='大学物理（1）'
)
#
# deal_with_data_by_stu_name(
#     file_path='/Users/afa/Downloads/exam_stu_table.xls',
#     stu_name='小姐姐'
# )