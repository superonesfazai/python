# coding:utf-8

'''
@author = super_fazai
@File    : 今日热门推荐.py
@Time    : 2018/4/4 15:13
@connect : superonesfazai@gmail.com
'''

file_path = './tmp_user_id.txt'

user_id_list = []
with open(file_path, 'r') as f:
    for line in f.readlines():
        line = line.replace('\n', '')
        user_id_list.append(int(line))

user_id_list = sorted(list(set(user_id_list)))

with open(file_path, 'w+') as f:
    for item in user_id_list:
        f.write(str(item)+'\n')

print('排序写入完毕!')