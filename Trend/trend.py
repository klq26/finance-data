#encoding = utf-8

from pandas import *
from enum import Enum
from datetime import *
import os

# 趋势枚举值
class trendType(Enum):
    unknown  = 1	# 未知
    rise   = 2 		# 上涨
    fall   = 3		# 下跌

def printTrend(name):
	# 返回结果集合
	result = []
	result.append('开始日期\t结束日期\t开始\t结束\t幅度\t持有期\n')
	# 加载数据
	dataname = name
	datapath = os.path.join(datadir,dataname)

	df = pandas.read_csv(datapath, sep=',', names=['date','value'],encoding='utf-8')

	# 初始化
	trend = trendType.unknown
	money = 10000	# 初始资金
	cash = money
	waveThreshold = 0.15	# ±15% 的变化标记为行情反转的阈值
	current = df.value.values[0]
	today = datetime.strptime(df.date.values[0],'%Y/%m/%d')
	start = df.value.values[0]
	startDate = datetime.strptime(df.date.values[0],'%Y/%m/%d')
	newHigh = df.value.values[0]
	newHighDate = datetime.strptime(df.date.values[0],'%Y/%m/%d')
	newLow = df.value.values[0]
	newLowDate = datetime.strptime(df.date.values[0],'%Y/%m/%d')

	for i in range(1,len(df.value.values)):
		# 取值
		current = df.value.values[i]
		today = datetime.strptime(df.date.values[i],'%Y/%m/%d')
		# 判断
		if current > newHigh:
			newHigh = current
			newHighDate = today
		if current < newLow:
			newLow = current
			newLowDate = today
		# 行情第一次确认趋势方向
		if newHigh / start >= 1 + waveThreshold:
			if trend == trendType.unknown or trend == trendType.fall:
				# 行情确认上涨
				trend = trendType.rise
				#print('{0} 行情上涨确认'.format(today))
		elif newLow / start <= 1 - waveThreshold:
			if trend == trendType.unknown or trend == trendType.rise:
				# 行情确认下跌
				#print('{0} 行情下跌确认'.format(today))
				trend = trendType.fall
		
		# 行情反转
		if trend == trendType.rise and current / newHigh <= 1 - waveThreshold:
			# 上涨趋势转型为下降趋势
			print('上涨区间: {0} ~ {1}\t开始:{2}\t结束:{3}\t幅度:{4}%\t持有期 {5} 天'.format(startDate.strftime('%Y/%m/%d'), newHighDate.strftime('%Y/%m/%d'),round(start,2),round(newHigh,2),round((newHigh/start-1)*100,2),(newHighDate - startDate).days))
			result.append('{0}\t{1}\t{2}\t{3}\t{4}%\t{5}\n'.format(startDate.strftime('%Y/%m/%d'), newHighDate.strftime('%Y/%m/%d'),round(start,2),round(newHigh,2),round((newHigh/start-1)*100,2),(newHighDate - startDate).days))
			#print('{0} 行情下跌确认'.format(newHighDate))
			cash = cash * (1+round((newHigh/start-1),2))
			start = newHigh
			startDate = newHighDate
			newHigh = current
			newHighDate = today
			newLow = current
			newLowDate = today
			trend = trendType.fall
		elif trend == trendType.fall and current / newLow >= 1 + waveThreshold:
			# 下降趋势转型为上涨趋势
			print('下跌区间: {0} ~ {1}\t开始:{2}\t结束:{3}\t幅度:{4}%\t持有期 {5} 天'.format(startDate.strftime('%Y/%m/%d'), newLowDate.strftime('%Y/%m/%d'),round(start,2),round(newLow,2),round((newLow/start-1)*100,2),(newLowDate - startDate).days))
			result.append('{0}\t{1}\t{2}\t{3}\t{4}%\t{5}\n'.format(startDate.strftime('%Y/%m/%d'), newLowDate.strftime('%Y/%m/%d'),round(start,2),round(newLow,2),round((newLow/start-1)*100,2),(newLowDate - startDate).days))
			#print('{0} 行情上涨确认'.format(newLowDate))
			cash = cash * (1+round((newLow/start-1),2))
			start = newLow
			startDate = newLowDate
			newHigh = current
			newHighDate = today
			newLow = current
			newLowDate = today
			trend = trendType.rise
		
	# 收尾判断最新一日的情况
	print('收盘区间: {0} ~ {1}\t开始:{2}\t结束:{3}\t幅度:{4}%\t持有期 {5} 天'.format(startDate.strftime('%Y/%m/%d'), today.strftime('%Y/%m/%d'), round(start,2),round(current,2),round((current/start-1)*100,2),(today - startDate).days))
	result.append('{0}\t{1}\t{2}\t{3}\t{4}%\t{5}\n'.format(startDate.strftime('%Y/%m/%d'), today.strftime('%Y/%m/%d'), round(start,2),round(current,2),round((current/start-1)*100,2),(today - startDate).days))
	cash = cash * (1+round((current/start-1),2))
	print('初始 {0} 元变为 {1}'.format(money, round(cash,2)))
	return result
	pass

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
		results = printTrend(datanames[choice])
		# 输出到文件
		outputfile = open(os.path.join(os.getcwd(),'{0}_result.txt'.format(datanames[choice])),'w+',encoding='utf-8')
		if results != None and len(results) > 0:
			#[print(x) for x in results]
			[outputfile.write(x) for x in results]
		#print('\n')
		outputfile.flush()
		outputfile.close()

		
		