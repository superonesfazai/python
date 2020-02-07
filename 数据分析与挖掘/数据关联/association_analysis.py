# coding:utf-8

'''
@author = super_fazai
@File    : association_analysis.py
@connect : superonesfazai@gmail.com
'''

"""
# 关联分析

例子
根据水果商店的每个人的购买清单, 进行关联分析，类似于啤酒纸尿裤的挖掘，分别计算水果之间的支持度，置信度，提升度
其中，I表示总事务集。num()表示求事务集里特定项集出现的次数;

比如，num(I)表示总事务集的个数;

num(X∪Y)表示含有{X,Y}的事务集的个数（个数也叫次数）。

1.支持度（Support）
    - 支持度表示项集{X,Y}在总项集里出现的概率。公式为：
    - Support(X→Y) = P(X,Y) / P(I) = P(X∪Y) / P(I) = num(XUY) / num(I)
2.置信度 （Confidence）
    - 置信度表示在先决条件X发生的情况下，由关联规则”X→Y“推出Y的概率。即在含有X的项集中，含有Y的可能性，公式为：
    - Confidence(X→Y) = P(Y|X) = P(X,Y) / P(X) = P(XUY) / P(X)
3.提升度（Lift）
    - 提升度表示含有X的条件下，同时含有Y的概率，与不含X的条件下却含Y的概率之比。
    - Lift(X→Y) = P(Y|X) / P(Y)
    
表头的水果顺序
{'桃子': 0, '桔子': 1, '榴莲': 2, '甘蔗': 3, '芒果': 4, '苹果': 5, '草莓': 6, '香蕉': 7}

每行代表一个人的消费记录，1代表购买了该水果，0代表未购买该水果
[[0 1 0 0 0 1 0 1]
 [0 1 0 1 1 0 0 0]
 [0 0 0 0 1 0 0 1]
 [0 0 1 0 1 1 1 0]
 [1 1 0 0 0 1 0 1]
 [0 1 1 0 0 1 0 1]]
 
原始数据类型可以是：
苹果,桔子,香蕉
桔子,芒果,甘蔗
香蕉,芒果
苹果,芒果,榴莲,草莓
桔子,桃子,苹果,香蕉
桔子,香蕉,苹果,榴莲
"""

import numpy as np
from collections import defaultdict
import pandas as pd

def calculate(data_vector) -> tuple:
    """
    计算支持度，置信度，提升度
    :param data_vector:
    :return:
    """
    print('=' * 50)
    print('Calculating...')

    n_samples, n_features = data_vector.shape
    print('特征数: ', n_features)
    print('样本数: ', n_samples)

    support_dict = defaultdict(float)
    confidence_dict = defaultdict(float)
    lift_dict = defaultdict(float)

    # together_appear: {(0, 1): 3, (0, 3): 2, (0, 4): 1, (1, 0): 3, (1, 3): 2,...}
    # together_appear: 元组里的元素是特征的序号，后面的数字，是这两个特征同时出现的总次数
    together_appear_dict = defaultdict(int)

    # feature_num_dict: {0: 3, 1: 4, 2: 3,...}
    # feature_num_dict: key是特征的序号，后面的数字是这个特征出现的总次数
    feature_num_dict = defaultdict(int)

    # 通过两层的for循环计算特征单独出现的次数，以及两两特征共同出现的次数
    for line in data_vector:
        for i in range(n_features):
            if line[i] == 0:
                continue

            feature_num_dict[i] += 1
            for j in range(n_features):
                if i == j:
                    continue

                if line[j] == 1:
                    together_appear_dict[(i, j)] += 1

    # print(together_appear_dict)
    # print(feature_num_dict)

    # 通过遍历together_appear_dict，计算出两两特征的支持度，置信度，提升度
    for k, v in together_appear_dict.items():
        support_dict[k] = v / n_samples
        confidence_dict[k] = v / feature_num_dict[k[0]]
        lift_dict[k] = v * n_samples / (feature_num_dict[k[0]] * feature_num_dict[k[1]])

    return support_dict, confidence_dict, lift_dict

def create_one_hot(file) -> tuple:
    """
    将实体数据转换成：0，1数据类型(独热编码)，类似于词袋模型
    :param file:
    :return:
    """
    print('=' * 50)
    print('Start converting raw data into onehot data...')

    with open(file, 'r', encoding='utf-8') as f:
        all_feature_li = []
        line_split_li = [i.strip().split(',') for i in f]
        for i in line_split_li:
            for feature in i:
                all_feature_li.append(feature)

        all_feature_set_li = list(set(all_feature_li))
        all_feature_set_li.sort()
        # print(all_feature_set_li)

        feature_dict = defaultdict(int)
        for n, feat in enumerate(all_feature_set_li):
            feature_dict[feat] = n
        # print(feature_dict)

        out_li = []
        for j in line_split_li:
            feature_num_li = [feature_dict[i] for i in j]
            # print(feature_num_li)
            inner_li = [1 if num in feature_num_li else 0 for num in range(len(all_feature_set_li))]

            out_li.append(inner_li)

        out_array = np.array(out_li)
        # print(out_array)

        return out_array, feature_dict

def convert_to_sample(feature_dict, s, c, l) -> tuple:
    """
    把0，1，2，3，... 等字母代表的feature，转换成实体
    :param feature_dict:
    :param s:
    :param c:
    :param l:
    :return:
    """
    print('=' * 50)
    print('Start converting to the required sample format...')
    # print(feature_dict)
    feature_mirror_dict = dict()
    for k, v in feature_dict.items():
        feature_mirror_dict[v] = k
    # print(feature_mirror_dict)

    support_sample_li = [[feature_mirror_dict[i[0][0]], feature_mirror_dict[i[0][1]], round(i[1], 3)] for i in s]
    confidence_sample_li = [[feature_mirror_dict[i[0][0]], feature_mirror_dict[i[0][1]], round(i[1], 3)] for i in c]
    lift_sample_li = [[feature_mirror_dict[i[0][0]], feature_mirror_dict[i[0][1]], round(i[1], 3)] for i in l]

    # 写入文件
    with open('./data/output_data/support.data', 'w', encoding='utf-8') as fs, \
            open('./data/output_data/confidence.data', 'w', encoding='utf-8') as fc, \
            open('./data/output_data/lift.data', 'w', encoding='utf-8') as fl:
        for s in support_sample_li:
            fs.write(str(s) + '\n')

        for c in confidence_sample_li:
            fc.write(str(c) + '\n')

        for l in lift_sample_li:
            fl.write(str(l) + '\n')

    return support_sample_li, confidence_sample_li, lift_sample_li

if __name__ == '__main__':
    # 配置路径，如果数据没有经过处理，就配置origin_data_file
    # 如果数据已经经过处理，为0，1数据，就可以直接配置ready_data_file
    origin_data_file = './data/input_data/origin.txt'
    ready_data_file = './data/input_data/sample.txt'

    # 如果数据已经构建好了，可以直接读取数组进行计算
    # data = pd.read_csv(ready_data_file)
    # data_array = np.array(data)

    data_array, feature_di = create_one_hot(origin_data_file)
    # print(data_array)
    # 支持度, 置信度, 提升度
    support_di, confidence_di, lift_di = calculate(data_array)
    # print('support_di: ', support_di)
    # print('confidence_di: ', confidence_di)
    # print('lift_di: ', lift_di)

    support = sorted(support_di.items(), key=lambda x: x[1], reverse=True)
    confidence = sorted(confidence_di.items(), key=lambda x: x[1], reverse=True)
    lift = sorted(lift_di.items(), key=lambda x: x[1], reverse=True)
    # print('support_li: ', support)
    # print('confidence_li: ', confidence)
    # print('lift_li: ', lift)

    support_li, confidence_li, lift_li = convert_to_sample(feature_di, support, confidence, lift)
    # print('support_li: ', support_li)
    # print('confidence_li: ', confidence_li)
    # print('lift_li: ', lift_li)