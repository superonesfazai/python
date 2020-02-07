# coding:utf-8

'''
@author = super_fazai
@File    : association_analysis_pro.py
@connect : superonesfazai@gmail.com
'''

"""
升级版关联分析的计算，适合大数据

文件准备的类型为列表：
['html', 'redirect', 'seo', 'google-search']
['prolog', 'swi-prolog']
['javascript', 'math', 'colors', 'html5-canvas']
['c#', 'asp.net-mvc']
"""

from collections import defaultdict


def write_(s, c, l):
    """把0，1，2，3，... 等字母代表的feature，转换成实体
    """
    print('=' * 50)
    print('Start writing...')

    support_sample_li = [[i[0][0], i[0][1], round(i[1], 3)] for i in s]
    confidence_sample_li = [[i[0][0], i[0][1], round(i[1], 3)] for i in c]
    lift_sample_li = [[i[0][0], i[0][1], round(i[1], 3)] for i in l]

    # 写入文件
    with open('./data/output_data/support_pro.data', 'w', encoding='utf-8') as fs, \
            open('./data/output_data/confidence_pro.data', 'w', encoding='utf-8') as fc, \
            open('./data/output_data/lift_pro.data', 'w', encoding='utf-8') as fl:
        for s in support_sample_li:
            fs.write(str(s) + '\n')
        print('The file support.data is written...')

        for c in confidence_sample_li:
            fc.write(str(c) + '\n')
        print('The file confidence.data is written...')

        for l in lift_sample_li:
            fl.write(str(l) + '\n')
        print('The file lift.data is written...')


def calculate(file):
    support_dict = defaultdict(float)
    confidence_dict = defaultdict(float)
    lift_dict = defaultdict(float)

    with open(file, 'r', encoding='utf-8') as f:
        with open('./data/feature_times_di.sql', 'w', encoding='utf-8') as f2:
            together_appear_dict = defaultdict(int)
            feature_num_dict = defaultdict(int)
            content_li = f.readlines()
            n_samples = len(content_li)
            for ind, item in enumerate(content_li):
                if ind % 10000 == 0:
                    print('Currently processed====', ind/10000, '万====line data...')
                line_li = eval(item.strip())
                for i in line_li:
                    feature_num_dict[i] += 1
                    for j in line_li:
                        if i == j:
                            continue
                        else:
                            tp = (i, j)
                        # print(tp)
                        together_appear_dict[tp] += 1
            # print(together_appear_dict)
            # print(feature_num_dict)
            print('Two dict is evaluated...')

            # 通过遍历together_appear_dict，计算出两两特征的支持度，置信度，提升度
            print('Start calculating...')

            num = 0
            for k, v in together_appear_dict.items():
                if num % 10000 == 0:
                    print('Calculated====', num/10000, '万==== data...')
                support_dict[k] = v / n_samples
                confidence_dict[k] = v / feature_num_dict[k[0]]
                lift_dict[k] = v * n_samples / (feature_num_dict[k[0]] * feature_num_dict[k[1]])
                num += 1

            print('Data calculated...')
            return support_dict, confidence_dict, lift_dict

if __name__ == '__main__':
    # 配置路径，如果数据没有经过处理，就配置origin_data_file
    # 如果数据已经经过处理，为0，1数据，就可以直接配置ready_data_file
    origin_data_file = './data/input_data/origin_pro.txt'
    ready_data_file = './data/input_data/sample.txt'

    support_di, confidence_di, lift_di = calculate(origin_data_file)

    # print('support_di: ', support_di)
    # print('confidence_di: ', confidence_di)
    # print('lift_di: ', lift_di)

    support = sorted(support_di.items(), key=lambda x: x[1], reverse=True)
    confidence = sorted(confidence_di.items(), key=lambda x: x[1], reverse=True)
    lift = sorted(lift_di.items(), key=lambda x: x[1], reverse=True)
    # print('support_li: ', support)
    # print('confidence_li: ', confidence)
    # print('lift_li: ', lift)

    write_(support, confidence, lift)