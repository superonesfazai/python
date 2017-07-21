#coding:utf-8

import csv

csv_file = open('tmp_py_files.csv', 'w+')
try:
    writer = csv.writer(csv_file)
    writer.writerow(('number', 'number plus2', 'number time2'))
    for i in range(10):
        writer.writerow((i, i+2, i*2))
finally:
    csv_file.close()