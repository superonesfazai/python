# coding = utf-8

'''
@author = super_fazai
@File    : select_处理下拉框.py
@connect : superonesfazai@gmail.com
'''

from selenium.webdriver.support.ui import Select    # 导入Select类
from selenium import webdriver

driver = webdriver.PhantomJS()

# 找到name 的选项卡
select = Select(driver.find_element_by_name('status'))

select.select_by_index(1)
select.select_by_value(0)
select.select_by_visible_text('未审核')

'''
以上是三种选择下拉框的方式，它可以根据索引来选择，
可以根据值来选择，可以根据文字来选择。
注意：
    index 索引从 0 开始
    value是option标签的一个属性值，并不是显示在下拉框中的值
    visible_text是在option标签文本的值，是显示在下拉框的值

全部取消选择怎么办？很简单
'''
select.deselect_all()