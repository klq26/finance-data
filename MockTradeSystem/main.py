# coding=utf-8

import os
import sys
from datetime import datetime

from pandas import *
import numpy
import math

from portfolio import *
from strategy import *

def mockTradeSystem(datapath,dataname):
	# 声明一个 100w 的投资组合
	initCash = 1000000
	myPortfolio = portfolio(initCash)
	# 读取走势数据
	df = None
	strategy = None
	# 初始化投资组合 & 策略
	if dataname == '000300.csv':
		strategy = strategyHS300('沪深300','000300',1000 * 0.01)
		myPortfolio.initFund('沪深300','000300',1.0,0)
	if dataname == '399905.csv':
		strategy = strategyZZ500('中证500','399905',1000 * 0.01)
		myPortfolio.initFund('中证500','399905',1.0,0)
	if dataname == '10YEAR.csv':
		strategy = strategy10YEAR('10年期国债','180027',1000 * 0.01)
		myPortfolio.initFund('10年期国债','180027',1.0,0)		
	if strategy == None:
		print('{0} 暂无对应策略，需要更新 mockTradeSystem 函数'.format(dataname))
		return
	print()
	print('数据来源：' + datapath)
	if os.path.exists(datapath):
		df = pandas.read_csv(datapath, sep=',', names=['date','close'],encoding='utf-8')
	else:
		print('无数据')
		return
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
	pass

def main():
	
	# 遍历数据集合
	datadir = os.path.join(os.getcwd(),'..','TradeData')
	datanames = []
	datapaths = []
	for root, dirs, files in os.walk(datadir, topdown=True):
		for name in files:
			datanames.append(name)
			datapaths.append(os.path.join(root, name))

	# 用户交互
	shouldContinue = True
	while shouldContinue:
		# 输出数据集合
		print('请选择：' + os.linesep)
		for i in range(0,len(datanames)):
			name = datanames[i]
			print('{0}\t{1}'.format(i,name))
		print('{0}\t{1}'.format(-1,'退出'))
		# 等待用户操作
		choice = int(input())
		if (choice < 0 and choice != -1) or choice >= len(datanames):
			print('索引越界，请重新数据' + os.linesep)
		elif choice == -1:
			print('退出程序')
			shouldContinue = False
		else:
			print(datanames[choice] + os.linesep)
			mockTradeSystem(datapaths[choice],datanames[choice])
	
if __name__ == '__main__':
    main()