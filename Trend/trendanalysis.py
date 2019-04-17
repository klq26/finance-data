#encoding=utf-8

from pandas import *
import numpy as np
from enum import Enum
from datetime import *
import os

datapath = os.path.join(os.getcwd(),'trend_上证指数_000001.txt')
print(datapath)

df = pandas.read_csv(datapath,header=0,sep='\t',encoding='utf-8')
# 改变数据格式
df['幅度'] = df['幅度'].str.split('%').str[0].astype(float) * 0.01	# 33% 字符串变成 0.33
df['持有期'] = df['持有期'].astype('int64')	# 字符串变整数

df_rise = df.loc[(df['幅度'] > 0) & (df['持有期'] > 90)]
df_fall = df.loc[(df['幅度'] < 0) & (df['持有期'] > 90)]

print(df_rise)
print(df_rise.幅度.median())	# 中位数
print(df_rise.持有期.mean())	# 平均数

count = len(df_rise.loc[df_rise['持有期'] > 150])/len(df_rise)
df.to_html('test.html')
