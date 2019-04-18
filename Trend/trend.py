#encoding=utf-8

from pandas import *
from enum import Enum
from datetime import *
import os

# 趋势枚举值
class trendType(Enum):
    unknown  = 1	# 未知
    rise   = 2 		# 上涨
    fall   = 3		# 下跌

# 根据 code 转换汉字名称
def indexToName(index):
	data = {'000001':'上证指数','399106':'深证综指','000016':'上证50','000300':'沪深300','399905':'中证500','000852':'中证1000',\
	'399006':'创业板','000922':'中证红利','399812':'养老产业','000991':'全指医药','399971':'中证传媒',\
	'000827':'中证环保','000990':'中证消费','000992':'全指金融','399975':'证券公司','HSI':'恒生指数','HSCEI':'恒生国企指数','DAX30':'德国30',\
	'FTSE100':'英国富时100','CAC40':'法国CAC40','DJI':'道琼斯工业','NASDAQ':'纳斯达克','SPX500':'标普500','USDI':'美元指数','10YEAR':'10年期国债','SPSIOPTR':'英为标普油气TR'}
	return data[index] if index in data.keys() else '未知'
	pass

def printTrend(name,rate):
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
	waveThreshold = rate * 0.01
	if waveThreshold == 0:
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
	print('{0}\t{1}'.format('q','退出'))
	print('{0}\t{1}'.format('all','全部'))
	# 等待用户操作
	str = input()
	choice = 0
	if str.isdigit(): # 是否为数字
		choice = int(str)
	elif str == 'all':
		choice = 99999
	elif str == 'q':
		exit()
	print('预期幅度是？例如 15 表示 ±15%')
	rate = float(input())
	if choice == 99999:
		# 文件夹
		dirpath = os.path.join(os.getcwd(),'{0}'.format(round(rate,0)))
		if not os.path.exists(dirpath):
			os.mkdir(dirpath)
		for name in datanames:
			results = printTrend(name, rate)
			# 输出到文件
			code = name.split('.')[0]
			name = indexToName(code)
			outputfile = open(os.path.join(dirpath,'{0}_{1}.txt'.format(name,code,rate)),'w+',encoding='utf-8')
			if results != None and len(results) > 0:
				#[print(x) for x in results]
				[outputfile.write(x) for x in results]
			#print('\n')
			outputfile.flush()
			outputfile.close()
		# 全部刷新之后退出
		exit()
	elif choice < 0 or choice >= len(datanames):
		print('索引越界，请重新数据' + os.linesep)
	elif choice == -1:
		print('退出程序')
		shouldContinue = False
	else:
		print(datanames[choice] + os.linesep)
		results = printTrend(datanames[choice],rate)
		# 输出到文件
		code = datanames[choice].split('.')[0]
		name = indexToName(code)
		# 文件夹
		dirpath = os.path.join(os.getcwd(),'{0}'.format(round(rate,0)))
		if not os.path.exists(dirpath):
			os.mkdir(dirpath)
		outputfile = open(os.path.join(dirpath,'{0}_{1}.txt'.format(name,code,rate)),'w+',encoding='utf-8')
		if results != None and len(results) > 0:
			#[print(x) for x in results]
			[outputfile.write(x) for x in results]
		#print('\n')
		outputfile.flush()
		outputfile.close()

