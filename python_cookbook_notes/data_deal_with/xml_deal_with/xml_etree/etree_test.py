# coding: utf-8

import xml.etree.ElementTree as ET

xml_str_test = """
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
"""


def print_node(node):
    # print "attrib:%s" % node.attrib
    print("tag:%s" % node.tag)
    print("text:%s" % node.text)


def read_nodes(em):
    print(type(em), em)
    for child in em:
        print_node(child)
        read_nodes(child)


def xml_to_dict(xml_str):
    """
    将xml转为dict
    """
    dict_data = {}
    root = ET.fromstring(xml_str)
    dict_data[root.tag] = {}
    print_node(root)
    read_nodes(root)


def run():
    xml_to_dict(xml_str_test)


run()


'''
测试结果:
tag:data
text:
    
(<class 'xml.etree.ElementTree.Element'>, <Element 'data' at 0x7f7fd0b36750>)
tag:country
text:
        
(<class 'xml.etree.ElementTree.Element'>, <Element 'country' at 0x7f7fd0b36790>)
tag:rank
text:1
(<class 'xml.etree.ElementTree.Element'>, <Element 'rank' at 0x7f7fd0b367d0>)
tag:year
text:2008
(<class 'xml.etree.ElementTree.Element'>, <Element 'year' at 0x7f7fd0b36890>)
tag:gdppc
text:141100
(<class 'xml.etree.ElementTree.Element'>, <Element 'gdppc' at 0x7f7fd0b36950>)
tag:neighbor
text:None
(<class 'xml.etree.ElementTree.Element'>, <Element 'neighbor' at 0x7f7fd0b36ad0>)
tag:neighbor
text:None
(<class 'xml.etree.ElementTree.Element'>, <Element 'neighbor' at 0x7f7fd0b36b10>)
tag:country
text:
        
(<class 'xml.etree.ElementTree.Element'>, <Element 'country' at 0x7f7fd0b36b50>)
tag:rank
text:4
(<class 'xml.etree.ElementTree.Element'>, <Element 'rank' at 0x7f7fd0b36b90>)
tag:year
text:2011
(<class 'xml.etree.ElementTree.Element'>, <Element 'year' at 0x7f7fd0b36bd0>)
tag:gdppc
text:59900
(<class 'xml.etree.ElementTree.Element'>, <Element 'gdppc' at 0x7f7fd0b36c10>)
tag:neighbor
text:None
(<class 'xml.etree.ElementTree.Element'>, <Element 'neighbor' at 0x7f7fd0b36c50>)
tag:country
text:
        
(<class 'xml.etree.ElementTree.Element'>, <Element 'country' at 0x7f7fd0b36c90>)
tag:rank
text:68
(<class 'xml.etree.ElementTree.Element'>, <Element 'rank' at 0x7f7fd0b36cd0>)
tag:year
text:2011
(<class 'xml.etree.ElementTree.Element'>, <Element 'year' at 0x7f7fd0b36d10>)
tag:gdppc
text:13600
(<class 'xml.etree.ElementTree.Element'>, <Element 'gdppc' at 0x7f7fd0b36d50>)
tag:neighbor
text:None
(<class 'xml.etree.ElementTree.Element'>, <Element 'neighbor' at 0x7f7fd0b36d90>)
tag:neighbor
text:None
(<class 'xml.etree.ElementTree.Element'>, <Element 'neighbor' at 0x7f7fd0b36dd0>)
'''