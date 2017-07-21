#coding:utf-8

# 我们将用他的总统就职演说(http://pythonscraping.com/files/inaugurationSpeech.txt)的全文作为这一章许多示例代码的数据源

'''
从最基本的功能上说，这个集合可以用来确定这段文字中最常用的单词和短语。另
外，还可以提取原文中那些最常用的短语周围的句子，对原文进行看似合理的概括
'''

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
import operator

def clean_input(_input):
    _input = re.sub('\n+', ' ', _input).lower()     #把一个或多个'\n'替换成' '
    _input = re.sub('\[[0-9]*\]', '', _input)
    _input = re.sub(' +', ' ', _input)      #把多个空格替换成一个空格
    _input = bytes(_input, 'utf-8')
    _input = _input.decode('ascii', 'ignore')
    clean_input = []
    _input = _input.split(' ')
    for item in _input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            clean_input.append(item)
    return clean_input

def ngrams(_input, n):
    _input = clean_input(_input)
    output = {}
    for i in range(len(_input)-n+1):
        ngram_temp = ' '.join(_input[i:i+n])
        if ngram_temp not in output:
            output[ngram_temp] = 0
        output[ngram_temp] += 1
    return output

def isCommon(_ngram):        #过滤普通单词
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have", "it",
        "i", "that", "for", "you", "he", "with", "on", "do", "say", "this",
        "they", "is", "an", "at", "but","we", "his", "from", "that", "not",
        "by", "she", "or", "as", "what", "go", "their","can", "who", "get",
        "if", "would", "her", "all", "my", "make", "about", "know", "will",
        "as", "up", "one", "time", "has", "been", "there", "year", "so",
        "think", "when", "which", "them", "some", "me", "people", "take",
        "out", "into", "just", "see", "him", "your", "come", "could", "now",
        "than", "like", "other", "how", "then", "its", "our", "two", "more",
        "these", "want", "way", "look", "first", "also", "new", "because",
        "day", "more", "use", "no", "man", "find", "here", "thing", "give",
        "many", "well", 'may', 'has', 'must']
    for word in commonWords:
        if _ngram == word:
            return True
    return False

content = str(urlopen('http://pythonscraping.com/files/inaugurationSpeech.txt').read(), 'utf-8')
_ngrams = ngrams(content, 2)
# isCommon(_ngrams)
# print(type(_ngrams))
sorted_ngrams = sorted(_ngrams.items(), key = operator.itemgetter(1), reverse=True)
# print(type(sorted_ngrams))
print(sorted_ngrams)
new_ngrams = []
for tmp_tuple in sorted_ngrams:
    tmp_list = re.split(r'(\s+)', tmp_tuple[0])     #将一个字符串转化为一个由单词和空格组成的list
    # print(tmp_list)
    if isCommon(tmp_list[0]) and isCommon(tmp_list[2]):
        # print(tmp_tuple[0])
        # print('True')
        continue
    # print(tmp_tuple)
    new_ngrams.append(tmp_tuple)

print(new_ngrams)

'''
要过滤没意义的单词
'''

'''
最常用的 5000 个单词列表可以免费获取，作为一个基本的过滤器来过滤最常用的 2-gram
序列绰绰有余。 其实只用前 100 个单词就可以大幅改善分析结果，我们增加一个 isCommon
函数来实现
'''

'''
现在一些核心的主题词已经从文本中抽取出来了， 它们怎么帮助我们归纳这段文字呢？一
种方法是搜索包含每个核心 n-gram 序列的第一句话， 这个方法的理论是英语中段落的首句
往往是对后面内容的概述。前五个 2-gram 序列的搜索结果是:
    • The Constitution of the United States is the instrument containing this grant of power to the
    several departments composing the government.
    • Such a one was afforded by the executive department constituted by the Constitution.
    • The general government has seized upon none of the reserved rights of the states.
    • Called from a retirement which I had supposed was to continue for the residue of my life
    to fill the chief executive office of this great and free nation, I appear before you, fellowcitizens, to take the oaths which the constitution prescribes as a necessary qualification for
    the performance of its duties; and in obedience to a custom coeval with our government
    and what I believe to be your expectations I proceed to present to you a summary of the
    principles which will govern me in the discharge of the duties which I shall be called upon
    to perform.
    • The presses in the necessary employment of the government should never be used to clear
    the guilty or to varnish crime.
当然， 这些估计还不能马上发布到 CliffsNotes 上面， 但是考虑到全文原来一共有 217 句
话，而这里的第四句话（ “ Called from a retirement...”）已经把主题总结得很好了，作为初
稿应该能凑合。
'''

