#coding:utf-8

'''
了解了马尔可夫概念之后，让我们再回到本节的主题，研究一个具体的例子：文本分析与写作。
还用前面例子里分析的威廉·亨利·哈里森的就职演讲内容， 我们可以写出下面的代码，
通过演讲内容的结构生成任意长度的（下面示例中链长为 100）马尔可夫链组成的句子：
'''

from urllib.request import urlopen
from random import randint

def word_list_sum(word_list):
    sum = 0
    for word, value in word_list.items():
        sum += value
    return sum

def retrieve_random_word(word_list):
    rand_index = randint(1, word_list_sum(word_list))
    for word, value in word_list.items():
        rand_index -= value
        if rand_index <= 0:
            return word

def build_word_dict(text):
    # 剔除换行符和引号
    text = text.replace("\n", " ");
    text = text.replace("\"", "");
    # 保证每个标点符号都和前面的单词在一起
    # 这样不会被剔除，保留在马尔可夫链中
    punctuation = [',', '.', ';',':']
    for symbol in punctuation:
        text = text.replace(symbol, " "+symbol+" ")

    words = text.split(" ")
    # 过滤空单词
    words = [word for word in words if word != '']

    word_dict = {}
    for i in range(1, len(words)):
        if words[i-1] not in word_dict:
            # 为单词新建一个词典
            word_dict[words[i-1]] = {}
        if words[i] not in word_dict[words[i-1]]:
            word_dict[words[i-1]][words[i]] = 0
        word_dict[words[i-1]][words[i]] = word_dict[words[i-1]][words[i]] + 1
    return word_dict

text = str(urlopen('http://pythonscraping.com/files/inaugurationSpeech.txt').read(), 'utf-8')
wordDict = build_word_dict(text)
# 生成链长为100的马尔可夫链
length = 100
chain = ''
currentWord = 'I'
for i in range(0, length):
    chain += currentWord+' '
    currentWord = retrieve_random_word(wordDict[currentWord])
print(chain)

'''
那么代码是怎么实现的呢？
buildWordDict 函数把网上获取的演讲文本的字符串作为参数，然后对字符串做一些清理
和格式化处理， 去掉引号，把其他标点符号两端加上空格，这样就可以对每一个单词进行
有效的处理。最后，再建立如下所示的一个二维字典——字典里有字典：
    {word_a : {word_b : 2, word_c : 1, word_d : 1},
    word_e : {word_b : 5, word_d : 2},...}
在这个字典示例中，“ word_a”出现了四次，有两次后面跟的单词是“ word_b”，一次是
“ word_c”，一次是“ word_d”。“ word_e”出现了七次，有五次后面跟的单词是“ word_b”，
两次是“ word_d”。
如果我们要画出这个结果的节点模型， 那么“ word_a”可能就有带 50% 概率的箭头指向
“ word_b”（四次中的两次），带 25% 概率的箭头指向“ word_c”，还有带 25% 概率的箭头
指向“ word_d”。
一旦字典建成， 不管你现在看到了文章的哪个词，都可以用这个字典作为查询表来选择下
一个节点。 3 这个字典的字典是这么使用的，如果我们现在位于“ word_e”节点，那么下一
步就要把字典 {word_b : 5, word_d : 2} 传递到 retrieveRandomWord 函数。这个函数会按
照字典中单词频次的权重随机获取一个单词。
先确定一个随机的开始词（ 示例中用的是经常使用的“ I”），我们可以通过马尔可夫链随意
地重复，生成我们需要的任意长度的句子。
'''

# 最后一个单词的考虑： 因为可能一个单词的后面没有单词