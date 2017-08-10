# 实现具体功能

import sqlite3

conn = sqlite3.connect('cards')

def init_sqlite3_db():
    global conn
    conn = sqlite3.connect('cards')
    create_table_if_not = 'create table if not exists cards(name VARCHAR(20) not NULL, phone int(11), qq int(10), email VARCHAR(30))'
    conn.execute(create_table_if_not)
    conn.commit()

def new_card():
    global conn
    init_sqlite3_db()
    conn.isolation_level = None

    tmp_name = str(input('请输入您的姓名:'))
    tmp_phone = int(input('请输入您的手机号:'))
    tmp_qq = int(input('请输入您的qq:'))
    tmp_email = str(input('请输入您的常用邮箱:'))

    tmp_card_tuple = (tmp_name, tmp_phone, tmp_qq, tmp_email)

    tmp_new_card = "insert into cards(name, phone, qq, email) values (\'%s\', %d, %d, \'%s\')" % tmp_card_tuple
    cur = conn.cursor() # 游标
    cur.execute(tmp_new_card)
    conn.commit()
    print('恭喜,添加成功!')

    pass

def show_all_cards():
    global conn
    init_sqlite3_db()
    conn.isolation_level = None

    cur = conn.cursor()
    cur.execute("select * from cards")
    res = cur.fetchall()
    # print(res)
    col_name_list = [tuple[0] for tuple in cur.description]
    print('查询结果如下'.center(35, '-'))
    for line in res:
        tmp_num = 0
        for f in line:
            print(col_name_list[tmp_num] + ':', end='')
            print(f, end='\t')
            tmp_num += 1
        print('')
    print('-' * 40)
    pass

def index_card():
    global conn
    init_sqlite3_db()
    conn.isolation_level = None

    tmp_index_name = str(input('请输入要查询的用户姓名:'))
    index_name_sql = 'select * from cards where name = "%s"' % tmp_index_name
    cur = conn.cursor()
    cur.execute(index_name_sql)
    res = cur.fetchall()
    col_name_list = [tuple[0] for tuple in cur.description]
    if res:
        print('查询结果如下'.center(35, '-'))
        for line in res:
            tmp_num = 0
            for i in line:
                print(col_name_list[tmp_num] + ':', end='')
                print(i, end='\t')
                tmp_num += 1
            print('')
        print('-' * 40)
    else:
        print('查询失败,对不起用户不存在!!'.center(35, '-'))

def del_card():
    global conn
    init_sqlite3_db()
    conn.isolation_level = None

    tmp_del_name = str(input('请输入要删除的用户姓名:'))
    del_name_sql = 'delete from cards where name = "%s"' % tmp_del_name
    cur = conn.cursor()
    cur.execute(del_name_sql)
    conn.commit()
    print('删除成功!!')

def update_card():
    global conn
    init_sqlite3_db()


    update_card_sql = 'update from cards where '

    cur = conn.cursor()
    cur.execute()