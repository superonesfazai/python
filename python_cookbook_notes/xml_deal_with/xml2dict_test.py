#!/usr/bin/env python
# encoding: utf-8

import xmltodict
import json
from copy import deepcopy


xml_str_test = """
<data>
    <country>
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
    </country>
    <country>
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
    </country>
    <country>
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <items>
            <i>1</i>
            <i>2</i>
            <i></i>
        </items>
    </country>
</data>
"""


def xml_to_dict(xml_str):
    """
    将xml转为dict
    :param xml_str:
    :return:
    """
    xml_dict = xmltodict.parse(xml_str)
    print(json.dumps(xml_dict, indent=4))
    # print(type(xml_dict))       # type: <class 'collections.OrderedDict'>
    # print(json.loads(json.dumps(xml_dict)))
    # print(json.dumps(xml_dict))       # json.dumps(xml_dict) 把dict类型转化为json类型
    # print(type(json.loads(json.dumps(xml_dict))))   # json.loads(json对象) 将其转换为标准编码的dict类型
    output(json.loads(json.dumps(xml_dict)))


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
    if isinstance(data, str) or data is None:  #python3默认编码就是unicode所以无序判断是否为unicode 编码
        row_list.append(':')
        row_list.append(data if data else '')
        print(' '.join(row_list))


def run():
    xml_to_dict(xml_str_test)


if __name__ == '__main__':
    run()


# pip install xmltodict

"""

{
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
                        "2"
                    ]
                }
            }
        ]
    }
}
data > country > [0] > gdppc : 141100
data > country > [0] > rank : 1
data > country > [0] > year : 2008
data > country > [1] > gdppc : 59900
data > country > [1] > rank : 4
data > country > [1] > year : 2011
data > country > [2] > items > i > [0] : 1
data > country > [2] > items > i > [1] : 2
data > country > [2] > items > i > [2] :
data > country > [2] > gdppc : 13600
data > country > [2] > rank : 68
data > country > [2] > year : 2011

"""