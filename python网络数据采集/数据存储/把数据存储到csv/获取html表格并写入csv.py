#coding:utf-8

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
bs_obj = BeautifulSoup(html)
# 主对比表格是当前页面上的第一个表格
table = bs_obj.findAll("table", {"class": "wikitable"})[0]
rows = table.findAll("tr")
csv_file = open("editors.csv", 'wt', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
try:
    for row in rows:
        csv_row = []
        for cell in row.findAll(['td', 'th']):
            csv_row.append(cell.get_text())
            writer.writerow(csv_row)
finally:
    csv_file.close()

# 实际工作中写此程序之前的注意事项
'''
如果你有很多 HTML 表格,且每个都要转换成 CSV 文件系统,或者许多 HTML 表格都要
汇总到一个 CSV 文件系统,那么把这个程序整合到爬虫里以解决问题非常好。但是,如果
你只需要做一次这种事情,那么更好的办法就是:复制粘贴。选择 HTML 表格内容然
后粘贴到 Excel 文件里,可以另存为 CSV 格式,不需要写代码就能搞定!
'''