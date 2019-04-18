#encoding=utf-8

from pandas import *
import numpy as np
from enum import Enum
from datetime import *
import os

def analysis_rise(datapath,name,code):
	df = pandas.read_csv(datapath,header=0,sep='\t',encoding='utf-8')
	# 改变数据格式
	df['幅度'] = df['幅度'].str.split('%').str[0].astype(float) * 0.01	# 33% 字符串变成 0.33
	df['持有期'] = df['持有期'].astype('int64')	# 字符串变整数

	df_rise = df.loc[(df['幅度'] > 0) & (df['持有期'] > 90)]
	df_fall = df.loc[(df['幅度'] < 0) & (df['持有期'] > 90)]
	str = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\n'.format(\
	name,code,round(df_rise.幅度.min(),4),round(df_rise.幅度.max(),4),round(df_rise.幅度.mean(),4),round(df_rise.幅度.median(),4)\
	,df_rise.持有期.min(),df_rise.持有期.max(),round(df_rise.持有期.mean(),2),round(df_rise.持有期.median(),2))
	return str
	pass

def analysis_fall(datapath,name,code):
	df = pandas.read_csv(datapath,header=0,sep='\t',encoding='utf-8')
	# 改变数据格式
	df['幅度'] = df['幅度'].str.split('%').str[0].astype(float) * 0.01	# 33% 字符串变成 0.33
	df['持有期'] = df['持有期'].astype('int64')	# 字符串变整数

	df_rise = df.loc[(df['幅度'] > 0) & (df['持有期'] > 90)]
	df_fall = df.loc[(df['幅度'] < 0) & (df['持有期'] > 90)]
	str = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\n'.format(\
	name,code,round(df_fall.幅度.max(),4),round(df_fall.幅度.min(),4),round(df_fall.幅度.mean(),4),round(df_fall.幅度.median(),4)\
	,df_fall.持有期.min(),df_fall.持有期.max(),round(df_fall.持有期.mean(),2),round(df_fall.持有期.median(),2))
	return str
	pass

# 数据目录选择
dirnames = []
for root, dirs, files in os.walk(os.getcwd(), topdown=True):
	for name in dirs:
		dirnames.append(name)
print('请选择：' + os.linesep)
for i in range(0,len(dirnames)):
	name = dirnames[i]
	print('{0}\t{1}'.format(i,name))
choice = int(input())
dirpath = dirnames[choice]
datadir = os.path.join(os.getcwd(),dirpath)
# 输出文件
risefile = open('analysis_rise.txt','w+',encoding='utf-8')
fallfile = open('analysis_fall.txt','w+',encoding='utf-8')
rise_title = '名称\t代码\t最小涨幅\t最大涨幅\t平均涨幅\t涨幅中位数\t最小持有期\t最大持有期\t平均持有期\t持有期中位数\n'
fall_title = '名称\t代码\t最小跌幅\t最大跌幅\t平均跌幅\t跌幅中位数\t最小持有期\t最大持有期\t平均持有期\t持有期中位数\n'
risefile.write(rise_title)
fallfile.write(fall_title)
# 遍历数据
for root, dirs, files in os.walk(datadir, topdown=True):
	for name in files:
		arr = name.split('_')
		indexName = arr[0]
		indexCode = arr[1].split('.txt')[0]
		datapath = os.path.join(root, name)
		riseStr = analysis_rise(datapath,indexName,indexCode)
		risefile.write(riseStr)
		fallStr = analysis_fall(datapath,indexName,indexCode)
		fallfile.write(fallStr)
risefile.flush()
risefile.close()
fallfile.flush()
fallfile.close()



