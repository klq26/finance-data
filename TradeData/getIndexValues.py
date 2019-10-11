﻿# coding=utf-8

import urllib.request
import json
import re

# 根据 code 转换汉字名称
def indexToName(index):
	data = {'000016':'上证50','000300':'沪深300','000905':'中证500','000852':'中证1000',\
	'399006':'创业板','000922':'中证红利','399812':'养老产业','000991':'全指医药','399971':'中证传媒',\
	'000827':'中证环保','000990':'中证消费','000992':'全指金融','399975':'证券公司','HSI5':'恒生指数','HSCEI5':'恒生国企指数','GDAXI_UI':'德国30',\
	'FTSE_UI':'英国富时100','FCHI_UI':'法国CAC40','DJIA_UI':'道琼斯工业','NDX_UI':'纳斯达克','SPX_UI':'标普500','UDI0':'美元指数'}
	return data[index] if index in data.keys() else None
	pass

def indexValue(code):
	# TYPE=mk 月线 wk 周线 k 日线
	url = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id={0}&TYPE=k'.format(code)	# eastmoney 接口有点意思，指数后面加了1 代表上证，加 2 代表深证
	response = urllib.request.urlopen(url)
	lines = response.readlines()
	index = code
	# 海外指数
	outer_code = ['HSI5','HSCEI5','GDAXI_UI','FTSE_UI','FCHI_UI','DJIA_UI','NDX_UI','SPX_UI','UDI0']
	if code not in outer_code:
		index = code[0:len(code)-1]
	name = indexToName(index)
	filename = '{0}.csv'.format(index)
	print('下载 {0}...'.format(filename))
	file = open(filename,'w+')
	for line in lines:
		raw = str(line).split(',')
		# for r in raw:
		# 	print(r)
		# break
		# 日期、开盘，收盘，最高，最低，成交量，成交额，变化率，换手率
		# 2018-10-23,2544.49,2464.81,2566.63,2344.98,342853317,4635亿,8.50%,2.13
		# print(raw)
		date = raw[0].replace('b\'','').replace('(','').replace('-','/')
		if len(raw) < 3:
			continue
		value = raw[2]
		file.write('{0}\t{1}\n'.format(date,value))
	file.flush()
	pass

def main():
	# 指数点数
	indexlist = ['0000161','0003001','0009051','0008521','3990062','0009221','3991062','3998122','0009911','3999712','0008271','0009901','0009921','3999752','HSI5',
	'HSCEI5','GDAXI_UI','FTSE_UI','FCHI_UI','DJIA_UI','NDX_UI','SPX_UI','UDI0'\
	]	# , 恒生和 DAX30
	[indexValue(x) for x in indexlist]
	pass

if __name__ == '__main__':
	main()
