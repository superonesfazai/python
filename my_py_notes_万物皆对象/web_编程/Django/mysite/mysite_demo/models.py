# coding = utf-8

'''
@author = super_fazai
@File    : models.py
@Time    : 2017/8/21 22:57
@connect : superonesfazai@gmail.com
'''

"""
一旦你的models被定义, django就能自动地创建一个管理接口-一个网站让用户去增加, 修改, 删除项目
这是容易的在admin site中去注册你的models
"""

from django.db import models

class Reporter(models.Model):
    full_name = models.CharField(max_length=70)
    def __str__(self):
        return self.full_name

class Article(models.Model):
    pub_date = models.DateField()
    headline = models.CharField()
    content = models.TextField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline