# coding:utf-8

'''
@author = super_fazai
@File    : dict_utils.py
@connect : superonesfazai@gmail.com
'''

"""
dict utils
"""

__all__ = [
    'dict_obj_2_markdown_table',            # 字典对象转换为markdown table
]

def dict_obj_2_markdown_table(target) -> str:
    '''
    字典对象转换为markdown table
        eg: 
            data = [
                {
                    'pr': 291,
                    'status': 'closed',
                    'date': 'None',
                    'title': 'Adds new wiz bang feature'
                },
                {
                    'pr': 290,
                    'status': 'v1.0',
                    'date': 'None',
                    'title': 'Updates UI to be more awesome'
                }
            ]
            print(dict_obj_2_markdown_table(data))
            # | pr | status | date | title |
            # |-----|-----|-----|-----|
            # | 291 | closed | None | Adds new wiz bang feature |
            # | 290 | v1.0 | None | Updates UI to be more awesome |
    :param target: 
    :return: 
    '''
    markdown_table = ""
    # 表头部
    markdown_header = '| ' + ' | '.join(map(str, target[0].keys())) + ' |'
    # 值
    markdown_header_separator = '|-----' * len(target[0].keys()) + '|'
    # Add the header row and separator to the table
    markdown_table += markdown_header + '\n'
    markdown_table += markdown_header_separator + '\n'
    # Loop through the list of dictionaries outputting the rows
    for row in target:
        markdown_row = ""
        for key, col in row.items():
            markdown_row += '| ' + str(col) + ' '
        markdown_table += markdown_row + '|' + '\n'

    return markdown_table

