# coding:utf-8

'''
@author = super_fazai
@File    : tomato_rich_film.py
@Time    : 2018/7/31 14:31
@connect : superonesfazai@gmail.com
'''

import pandas as pd
import jieba
from skimage.io import imread
from wordcloud.wordcloud import WordCloud
from wordcloud.wordcloud import STOPWORDS
from wordcloud import ImageColorGenerator
from collections import Counter
import matplotlib.pyplot as plt

tomato_com = pd.read_excel('/Users/afa/myFiles/tmp/西虹市首富.xlsx')

def plot_thermodynamic_diagram():
    '''热力图'''
    grouped = tomato_com.groupby(['city'])
    grouped_pct = grouped['score'] #tip_pct列
    city_com = grouped_pct.agg(['mean', 'count'])
    city_com.reset_index(inplace=True)
    city_com['mean'] = round(city_com['mean'], 2)

    data=[(city_com['city'][i],city_com['count'][i]) for i in range(0, city_com.shape[0])]

    geo = Geo(
        '《西虹市首富》全国热力图',
        title_color="#fff",
        title_pos="center",
        width=1200,
        height=600,
        background_color='#404a59')

    attr, value = geo.cast(data)

    geo.add(
        "",
        attr,
        value,
        type="heatmap",
        visual_range=[0, 200],
        visual_text_color="#fff",
        symbol_size=10,
        is_visualmap=True,
        is_roam=False)

    geo.render('西虹市首富全国热力图.html')

    return

def plot_words_cloud():
    '''
    词云
    :return:
    '''
    tomato_str = ' '.join(tomato_com['comment'])

    words_list = []

    word_generator = jieba.cut_for_search(tomato_str)

    for word in word_generator:
        words_list.append(word)

    words_list = [k for k in words_list if len(k) > 1]

    back_color = imread('/Users/afa/myFiles/tmp/灰姑娘.png')  # 解析该图片
    wc = WordCloud(
        background_color='white',           # 背景颜色
        max_words=200,                      # 最大词数
        mask=back_color,                    # 以该参数值作图绘制词云[设置词云形状]，这个参数不为空时，width和height会被忽略
        max_font_size=300,                  # 显示字体的最大值
        stopwords=STOPWORDS.add('苟利国'),   # 使用内置的屏蔽词，再添加'苟利国'
        font_path="/Library/Fonts/Songti.ttc",
        random_state=42,                    # 为每个词返回一个PIL颜色
        # width=1000,                       # 图片的宽
        # height=860                        #图片的长
    )

    tomato_count = Counter(words_list)

    wc.generate_from_frequencies(tomato_count)
    # 基于彩色图像生成相应彩色
    image_colors = ImageColorGenerator(back_color)

    # 绘制词云
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis('off')
    plt.show()
    return

# plot_thermodynamic_diagram()
plot_words_cloud()