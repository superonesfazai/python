# coding = utf-8

'''
@author = super_fazai
@File    : difflib_differ.py
@Time    : 2017/8/17 08:18
@connect : superonesfazai@gmail.com
'''

# text1 = """Lorem ipsum dolor sit amet, consectetuer adipiscing
# elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
# pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis
# pharetra tortor.  In nec mauris eget magna consequat
# convalis. Nam sed sem vitae odio pellentesque interdum. Sed
# consequat viverra nisl. Suspendisse arcu metus, blandit quis,
# rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
# molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
# tristique vel, mauris. Curabitur vel lorem id nisl porta
# adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
# tristique enim. Donec quis lectus a justo imperdiet tempus."""

text1 = r'''
import cmath

print(cmath.exp(2))     # return the exponential value e**x

print(cmath.sqrt(4))    # 开方

print(cmath.asin(0.5))

print('%.20f' % cmath.pi)
'''

text1_lines = text1.splitlines()

text2 = r'''
import cmath
import sys

print(cmath.exp(2))     # return the exponential value e**x

print(cmath.sqrt(4))    # 开方

print(cmath.asin(0.5))

print('%.20f' % cmath.pi)
'''

# text2 = """Lorem ipsum dolor sit amet, consectetuer adipiscing
# elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
# pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis
# pharetra tortor. In nec mauris eget magna consequat
# convalis. Nam cras vitae mi vitae odio pellentesque interdum. Sed
# consequat viverra nisl. Suspendisse arcu metus, blandit quis,
# rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
# molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
# tristique vel, mauris. Curabitur vel lorem id nisl porta
# adipiscing. Duis vulputate tristique enim. Donec quis lectus a
# justo imperdiet tempus.  Suspendisse eu lectus. In nunc."""

text2_lines = text2.splitlines()

import difflib

d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)
print('\n'.join(diff))

# 段落中的最后一句话发生了重大变化，因此删除旧版本并添加新的版本来表示差异

'''
测试结果:
  Lorem ipsum dolor sit amet, consectetuer adipiscing
  elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
- pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis
+ pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis
?         +

- pharetra tortor.  In nec mauris eget magna consequat
?                 -

+ pharetra tortor. In nec mauris eget magna consequat
- convalis. Nam sed sem vitae odio pellentesque interdum. Sed
?                 - --

+ convalis. Nam cras vitae mi vitae odio pellentesque interdum. Sed
?               +++ +++++   +

  consequat viverra nisl. Suspendisse arcu metus, blandit quis,
  rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
  molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
  tristique vel, mauris. Curabitur vel lorem id nisl porta
- adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
- tristique enim. Donec quis lectus a justo imperdiet tempus.
+ adipiscing. Duis vulputate tristique enim. Donec quis lectus a
+ justo imperdiet tempus.  Suspendisse eu lectus. In nunc.
'''