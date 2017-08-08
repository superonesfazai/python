# -*- coding:utf-8 -*-
# file: PySqlite.py
#
import sqlite3											# ����sqlite3ģ��
con = sqlite3.connect('python')									# ���ӵ����ݿ�
cur = con.cursor()										# ������ݿ��α�
cur.execute('insert into people (name,age,sex) values (\'Jee\',21,\'F\')')			# ִ��SQL���
r = cur.execute('delete from people where age=20')						# ִ��SQL���
con.commit()											# �ύ����
cur.execute('select * from people')								# ִ��SQL���
s = cur.fetchall()										# �������
print(s)												# ��ӡ����
cur.close()											# �ر��α�
con.close()											# �ر����ݿ�����
