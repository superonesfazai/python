# coding = utf-8

'''
@author = super_fazai
@File    : d3py_demo.py
@Time    : 2017/8/14 13:16
@connect : superonesfazai@gmail.com
'''

import d3py
import pandas
import numpy as np

# some test data
T = 100
# this is a data frame with three columns (we only use 2)
df = pandas.DataFrame({
    "time": range(T),
    "pressure": np.random.rand(T),
    "temp": np.random.rand(T)
})
## build up a figure, ggplot2 style
# instantiate the figure object
fig = d3py.PandasFigure(df, name="basic_example", width=300, height=300)
# add some red points
fig += d3py.geoms.Point(x="pressure", y="temp", fill="red")
# writes 3 files, starts up a server, then draws some beautiful points in Chrome
fig.show()
