# coding:utf-8

'''
@author = super_fazai
@File    : app.py
@connect : superonesfazai@gmail.com
'''

"""
启动:
    1. rq worker
    2. python3 app.py
"""

from jobs import get_q, count_words

def run():
    q = get_q()
    j = q.enqueue(f=count_words, args=('https://httpin.org',))
    print(j.result)

if __name__ == '__main__':
    run()