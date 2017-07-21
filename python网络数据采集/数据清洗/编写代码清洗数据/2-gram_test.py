#coding: utf-8

#下面的代码将返回维基百科词条 "Python programming language"的 2-gram 列表

from urllib.request import urlopen
from bs4 import BeautifulSoup
# from collections import OrderedDict
import re
import string

# # test_1
# def ngrams(input, n):
#     input = input.split(' ')
#     output = []
#     for i in range(len(input)-n+1):
#         output.append(input[i:i+n])
#     return output

# # test_2
# # 让我们首先用一些正则表达式来移除转义字符( \n ),再把 Unicode 字符过滤掉。我们可以通过下面的函数对之前输出的结果进行清理
# def ngrams(input, n):
#     content = re.sub('\n+', ' ', content1)     #首先把内容中的换行符(或者多个换行符)替换成空格
#     content = re.sub(' +', ' ', content)      #然后把连续的多个空格替换成一个空格,确保所有单词之间只有一个空格
#     content = bytes(content, "UTF-8")
#     content = content.decode("ascii", "ignore")
#     print(content)
#     input = input.split(' ')
#     output = []
#     for i in range(len(input) - n + 1):
#         output.append(input[i:i + n])
#     return output

# test_3
# 现在“清洗任务”列表变得越来越长,让我们把规则都移出来,单独建一个函数,就叫clean_input

def clean_input(_input):
    _input = re.sub('\n+', " ", _input)
    _input = re.sub('\[[0-9]*\]', "", _input)
    _input = re.sub(' +', " ", _input)
    _input = bytes(_input, "UTF-8")
    _input = _input.decode("ascii", "ignore")
    # 仔细观察结果发现还有大小写的影响, eg: "Python Software"有两次是"Python software"的形式。同样"van Rossum"和" Van Rossum"也是作为两个序列统计的
    # 因此来增加一行代码使得到的数据更加标准化
    # _input = _input.upper()
    clean_input = []
    _input = _input.split(' ')
    for item in _input:
        # 这里用 import string 和 string.punctuation 来获取 Python 所有的标点符号
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            clean_input.append(item)
    return clean_input

def ngrams(_input, n):
    _input = clean_input(_input)
    output = []
    for i in range(len(_input)-n+1):
        output.append(_input[i:i + n])
    return output

html = urlopen('http://en.wikipedia.org/wiki/Python_(programming_language)')
bs_obj = BeautifulSoup(html)
content1 = bs_obj.find('div', {'id':'mw-content-text'}).get_text()
ngrams = ngrams(content1, 2)
# print(type(ngrams))
# ngrams = OrderedDict(sorted(ngrams.items(), key=lambda t: t[1], reverse=True))
print(ngrams)
print('2-grams count is: ' + str(len(ngrams)))

'''
由于pythona字典是无序的,不能像数组一样直接对n-grams序列的频率进行排序
字典内部元素的位置不是固定的,排序之后再次使用是还是会变化,
除非把排序过的字典里的值赋值给其他类型进行排序
在python的collections库里的OrdereDict可以解决这个问题
'''


'''
test_1:
ngrams 函数把一个待处理的字符串分成单词序列(假设所有单词按照空格分开),然后增
加到 n-gram 模型(本例中是 2-gram)里形成以每个单词开始的二元数组。
这段程序会从文字中返回一些有意思同时也很有用的 2-gram 序列:
['of', 'free'], ['free', 'and'], ['and', 'open-source'], ['open-source', 'software']
不过,同时也会出现一些零乱的数据:
['software\nOutline\nSPDX\n\n\n\n\n\n\n\n\nOperating', 'system\nfamilies\n\n\n\n
AROS\nBSD\nDarwin\neCos\nFreeDOS\nGNU\nHaiku\nInferno\nLinux\nMach\nMINIX\nOpenS
olaris\nPlan'], ['system\nfamilies\n\n\n\nAROS\nBSD\nDarwin\neCos\nFreeDOS\nGNU\
nHaiku\nInferno\nLinux\nMach\nMINIX\nOpenSolaris\nPlan', '9\nReactOS\nTUD:OS\n\n
\n\n\n\n\n\n\nDevelopment\n\n\n\nBasic'], ['9\nReactOS\nTUD:OS\n\n\n\n\n\n\n\n\n
Development\n\n\n\nBasic', 'For']
另外,因为每个单词(除了最后一个单词)都要创建一个 2-gram 序列,所以这个词条里共
有 7411 个 2-gram 序列。这并不是一个非常便于管理的数据集!

test_2:
这几步已经可以大大改善输出结果了,但是还有一些问题:
['Pythoneers.[43][44]', 'Syntax'], ['7', '/'], ['/', '3'], ['3', '=='], ['==', '
2']
因此,需要再增加一些规则来处理数据。我们还可以制定一些规则让数据变得更规范:
• 剔除单字符的“单词”,除非这个字符是“i”或“a”;
• 剔除维基百科的引用标记(方括号包裹的数字,如 [1]);
• 剔除标点符号(注意:这个规则有点儿矫枉过正,在第 9 章我们将详细介绍,本例暂时
这样处理)。

test_3:
这里用 import string 和 string.punctuation 来获取 Python 所有的标点符号。你可以在
Python 命令行看看标点符号有哪些:
>>> import string
>>> print(string.punctuation)
!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
在循环体中用 item.strip(string.punctuation) 对内容中的所有单词进行清洗,单词两端
的任何标点符号都会被去掉,但带连字符的单词(连字符在单词内部)仍然会保留。
这样输出的 2-gram 结果就更干净了:
['Linux', 'Foundation'], ['Foundation', 'Mozilla'], ['Mozilla', 'Foundation'], [
'Foundation', 'Open'], ['Open', 'Knowledge'], ['Knowledge', 'Foundation'], ['Fou
ndation', 'Open'], ['Open', 'Source']
'''

'''
除了这些，还需要再考虑一下，自己计划为数据标准化的进一步深入再投入多少计算能
力。 很多单词在不同的环境里会使用不同的拼写形式， 其实都是等价的，但是为了解决这
种等价关系，你需要对每个单词进行检查，判断是否和其他单词有等价关系。
比如，“ Python 1st” 和“ Python first”都出现在 2-gram 序列列表里。但是，如果增加一条
规则：“让所有‘ first’‘ second’‘ third’……与 1st， 2nd， 3rd……等价”，那么每个单词
都要额外增加十几次检查。
同理，连字符使用不一致（像“ co-ordinated” 和“ coordinated”）、单词拼写错误以及其他
语病（ incongruities）， 都可能对 n-gram 序列的分组结果造成影响，如果语病很严重的话，
还可能彻底打乱输出结果。
对带连字符单词的一个处理方法是， 先把连字符去掉，然后把单词当作一个字符串，这可
能需要在程序中增加一步操作。 但是，这样做也可能把带连字符的短语（这是很常见的，
比如“ just-in-time”“ object-oriented” 等）处理成一个字符串。要是换一种做法，把连字符
替换成空格可能更好一点儿。但是就得准备见到“ co ordinated”和“ ordinated attack”之类
的 2-gram 序列了！
'''