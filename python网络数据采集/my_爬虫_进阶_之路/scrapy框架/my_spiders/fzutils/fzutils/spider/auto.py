# coding:utf-8

import codecs
from requests import get

# import sys
# from templates.config import config
# sys.path.append('..')
# from time_utils import get_shanghai_time

# from os.path import dirname
# from fzutils import spider
from ..time_utils import get_shanghai_time
from .templates.config import config

__all__ = [
    'auto_generate_crawler_code',           # 爬虫代码自动生成器
]

def auto_generate_crawler_code():
    '''
    爬虫代码自动生成器
    :return:
    '''
    def get_template_str():
        # 读取模板文件
        # 本地读取
        # template = dirname(spider.__file__) + '/templates/' + config.get('template_file')
        # with codecs.open(template, 'rb', 'utf-8') as f:
        #     s = f.read()
        # return s

        # 网址读取
        template_url = 'http://pdfs3i7nf.bkt.clouddn.com/base_spider_template.txt'
        s = get(url=template_url).content.decode('utf-8')
        # print(s)

        return s

    s = get_template_str()
    # return
    if not s:
        return False

    # print(s)
    print('#--------------------------------')
    print('# 爬虫模板自动生成器 by super_fazai')
    print('#--------------------------------')
    print('@@ 下面是备选参数, 无输入则取默认值!!')
    author = input('请输入author:')
    connect = input('请输入email:')
    file_name = input('请输入创建的文件名(不含.py):')
    class_name = input('请输入class_name:')

    try:
        s = s.format(
            author=config.get('author') if author == '' else author,
            file_name=config.get('file_name') if file_name == '' else file_name,
            create_time=str(get_shanghai_time()),
            connect=config.get('connect') if connect == '' else connect,
            class_name=config.get('class_name') if class_name == '' else class_name,
        )
        # print(s)
    except Exception as e:
        print('遇到错误:', e)
        return False

    # 保存文件
    file_name = config['file_name'] + '.py' if file_name == '' else file_name+'.py'
    with codecs.open(file_name, 'wb', 'utf-8') as f:
        f.write(s)
        f.flush()

    print('\n创建爬虫文件{0}完毕!\nenjoy!🍺'.format(file_name))

    return True
