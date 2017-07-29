# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-29 上午10:08
# @File    : 易面试点.py

# 1. 切记不要边遍历, 边增删, 否则会遗漏
a = [11, 22, 33, 44, 55, 66]

for i in a:     # 丢失元素44
    print(i)
    if i == 33:
        a.remove(i)
print(a)
print('')

a = [11, 22, 33, 44, 55, 66]
# 边遍历边删除列表元素的一般步骤
# 解决方案: 先创建临时列表,用于记录要删除的元素,再遍历临时列表删除,并在原列表中删除
tmp = []
for i in a:
    if i == 33:
        tmp.append(i)
i = 0
for j in tmp:
    if i >0 and i < len(a)-1:
        print(a[i])
    else:
        break
    i += 1
    a.remove(j)

print(a)