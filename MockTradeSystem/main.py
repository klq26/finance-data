# coding=utf-8

import os
import sys
from datetime import datetime

from pandas import *
import numpy
import math

from portfolio import *
from strategy import *

def main():
	# 声明一个 100w 的投资组合
	initCash = 1000000
	myPortfolio = portfolio(initCash)
	# 读取走势数据
	df = None
	#path = 'D:/000300.csv'	# 000300 2200 ~ 4000
	#strategy = strategyHS300('沪深300','000300',1000 * 0.01)
	#path = 'D:/399905.csv'	# 399905 4100 ~ 10000
	#strategy = strategyZZ500('中证500','399905',1000 * 0.01)
	path = 'D:/10YEAR.csv'	# 100YEAR 4.0 ~ 3.2
	strategy = strategy10YEAR('10年期国债','180027',1000 * 0.01)
	print()
	print('数据来源：' + path)
	if os.path.exists(path):
		print('数据存在..')
		df = pandas.read_csv(path,sep=',', names=['date','close'],encoding='utf-8')
	else:
		print('无数据')
		return
	# 初始化投资组合
	myPortfolio.initFund('沪深300','000300',1.0,0)
	print()
	index = 0
	isHolding = False	# 是否持仓
	startDate = datetime.strptime(df.date.values[index], '%Y/%m/%d')	# 开始日期（通常取第一个数据）
	lastDate = None	# 结束日期（最后一次交易日期）
	position = 0
	# 模拟交易
	for close in df.close.values:
		# 策略函数，后续封装
		recommendPosition = strategy.getRecommendPositions(close)
		recommendPrice = strategy.getRecommendPrice(close)
		if position != recommendPosition:
			print(df.date.values[index])
			lastDate = datetime.strptime(df.date.values[index], '%Y/%m/%d')
			myPortfolio.printFund()
			myPortfolio.updateFund(recommendPrice, recommendPosition)
			position = recommendPosition
			myPortfolio.printFund()
			print()
		index = index + 1
	# 循环结束后，计算最新市值	
	myPortfolio.updatePortfolio(1 / df.close.values[-1])	# 用最后一天的成交价更新投资组合最新市值
	print(df.date.values[-1])
	close = df.close.values[-1]
	recommendPosition = strategy.getRecommendPositions(close)
	recommendPrice = strategy.getRecommendPrice(close)
	myPortfolio.updatePortfolio(recommendPrice)
	myPortfolio.printFund()
	
	# 计算年化收益率
	days = (lastDate - startDate).days
	years = round(days / 365,2)
	rate = math.pow(myPortfolio.marketCap / initCash, 1.0/years) - 1
	print()
	print('年限：{:.2f}'.format(years))
	print('年化收益率：{:.2f}%'.format(rate * 100))

if __name__ == '__main__':
    main()