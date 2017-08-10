# coding:utf-8

__author__ = 'afa'

from copy import deepcopy

tmp_info = {
    "data": {
        "country": [
            {
                "rank": "1",
                "year": "2008",
                "gdppc": "141100"
            },
            {
                "rank": "4",
                "year": "2011",
                "gdppc": "59900"
            },
            {
                "rank": "68",
                "year": "2011",
                "gdppc": "13600",
                "items": {
                    "i": [
                        "1",
                        "2",
                        ''
                    ]
                }
            }
        ]
    }
}

def output(data, row=None):
    """
    ** 递归所有分支
    :param data:
    :param row:
    :return:
    """
    row_list = row if row else []
    if isinstance(data, list):
        for index, item in enumerate(data):
            list1 = deepcopy(row_list)
            list1.append('>')
            list1.append('[%s]' % index)
            output(item, list1)
    if isinstance(data, dict):
        for key, value in data.items():
            list2 = deepcopy(row_list)
            if list2:
                list2.append('>')
            list2.append(key)
            output(value, list2)
    if isinstance(data, str) or data is None:  #python3默认编码就是unicode所以无需判断是否为unicode 编码
        row_list.append(':')
        row_list.append(data if data else '')
        print(' '.join(row_list))

output(tmp_info)