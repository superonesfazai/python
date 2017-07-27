# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-26 下午7:28
# @File    : gettext_test.py

import gettext

# gettext.bindtextdomain('GoldenDict', '/media/afa/新加卷/dicts/English2Ch/goldendict_for_ubuntu/Golden_Offline_dict_without_pic_sounds/02_En-Zh-New_Oxford_English_Chinese_dict_17M_BGL')
# gettext.textdomain('GoldenDict')
# _ = gettext.gettext

t = gettext.translation('GoldenDict', '')

print(_('This is a translatable string.'))