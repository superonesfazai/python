# Create your views here.

"""
定义视图
"""

from django.http import HttpResponse
from django.template import loader, RequestContext

# def index(request):
#     # 1. 获取模板
#     template = loader.get_template('./booktest/index.html')
#     # 2. 定义上下文
#     context = RequestContext(request, {'title':'图书列表','list':range(10)})
#     # 3. 渲染模板
#     return HttpResponse(template.render(context))

# 视图调用模板简写
from django.shortcuts import render
from .models import BookInfo

# 首页展示所有图书
def index(request):
    # context={'title':'图书列表','list':range(10)}
    # 查询所有图书
    booklist = BookInfo.objects.all()
    # 将图书列表传递到模板中, 然后渲染模板
    return render(request, 'booktest/index.html', {'booklist': booklist})

# 详细页, 接收图书的编号, 根据编号查询
def detail(request, id):
    # 根据图书编号对应图书
    book = BookInfo.objects.get(pk=id)
    # 将图书信息传递到模板中, 然后渲染模板
    return render(request, 'booktest/detail.html', {'book': book})