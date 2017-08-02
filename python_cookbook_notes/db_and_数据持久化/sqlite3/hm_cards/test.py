# test

tmp_name = str(input('请输入您的姓名:'))
tmp_phone = int(input('请输入您的手机号:'))
tmp_qq = int(input('请输入您的qq:'))
tmp_email = str(input('请输入您的常用邮箱:'))

tmp_card_tuple = (tmp_name, tmp_phone, tmp_qq, tmp_email)

tmp_new_card = "insert into cards(name, phone, qq, email) " \
               "values (\'%s\', %d, %d, \'%s\')" % tmp_card_tuple

print(type(tmp_new_card))
print(tmp_new_card)