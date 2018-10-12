# coding=utf-8

import urllib.request
import json
import re

# 获取基金的单位净值和累积净值
def fundValue(code):
	url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={0}&page=1&per=1'.format(code)
	response = urllib.request.urlopen(url)
	string = response.read().decode("utf-8")

	leftTag1 = "<td>"
	leftTag2 = "<td class='tor bold'>"
	rightTag = "</td>"

	raw_date = re.findall("{0}.*?{1}".format(leftTag1,rightTag),string)	# 首次筛选标签，第一个为日期
	raw_value = re.findall("{0}.*?{1}".format(leftTag2,rightTag),string)	# 首次筛选数据列，第一第二分别为单位、累计净值
	date = raw_date[0].replace(leftTag1,'').replace(rightTag,'') if len(raw_date) > 0 else 'NA'
	value1 = raw_value[0].replace(leftTag2,'').replace(rightTag,'') if len(raw_value) > 0 else 'NA'
	value2 = raw_value[1].replace(leftTag2,'').replace(rightTag,'') if len(raw_value) > 1 else 'NA'

	value = value1 if fundUseUnitValueScope(code) else value2
	print('{0}\t{1}\t{2}\t{3}'.format(date,codeToName(code),code,value))
	pass

# 根据 code 转换汉字名称
def codeToName(code):
	data = {'100032':'红利场外','510050':'50ETF','510300':'300ETF','510500':'500ETF','512100':'1000ETF',\
	'159915':'创业板','159938':'医药ETF','001180':'医药场外','000968':'养老场外','512880':'证券ETF','512580':'环保ETF',\
	'001064':'环保场外','512980':'传媒ETF','001469':'金融场外','000614':'德国30','000071':'恒生','003376':'7-10国债',\
	'001061':'海外债','340001':'可转债','518880':'黄金ETF','001051':'华夏50场外','000478':'建信500场外','001052':'华夏500场外',\
	'161017':'富国500场外','002903':'广发500场外C','100038':'富国300场外','000051':'华夏300场外','004752':'广发传媒场外'}
	return data[code] if code in data.keys() else None
	pass

# 使用单位净值的基金数组
def fundUseUnitValueScope(code):
	scope = ['510050','510300','510500','512100','159915','159938','512880','512580','512980']
	return code in scope

# 且慢估值，需要先 Charles 抓包查到 x-sign 放入请求 header 否则无数据
def fundEval(xsign = '1539312519715F56A31741DE42773BF6CA3A2A7AB00D1'):
	"""
	# 指导格式
	"date": 1535385600000,
	    "idxEvalList": [
	        {
	            "indexCode": "CSPSADRP.CI",
	            "indexName": "标普红利",
	            "date": 1535385600000,
	            "pe": 9.46,
	            "pePercentile": 0.1031,
	            "peHigh": 25.57,
	            "peLow": 7.96,
	            "pb": 1.41,
	            "pbLow": 1.16,
	            "pbHigh": 6.8,
	            "pbPercentile": 0.1649,
	            "roe": 0.1489,
	            "scoreBy": 0,
	            "source": 1,
	            "group": "LOW"
	        },
	"""
	url = 'https://qieman.com/pmdj/v2/idx-eval/latest'
	# user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
	# content_type = 'application/json'
	headers = {'x-sign':xsign}	# 且慢请求防盗链参数，没有这个拿不到数据，去浏览器查一下，更新之后，即可自动化
	req = urllib.request.Request(url, headers = headers)
	response = urllib.request.urlopen(req)
	string = response.read().decode("utf-8")
	json_data = json.loads(string)
	"""
	{'indexCode': 'CSPSADRP.CI', 'indexName': '标普红利', 'date': 1535385600000, 'pe': 9.46, 'pePercentile': 0.1031, 'peHigh': 25.57, 'peLow': 7.96, 'pb': 1.41, 'pbLow': 1.16, 'pbHigh': 6.8, 'pbPercentile': 0.1649, 'roe': 0.1489, 'scoreBy': 0, 'source': 1, 'group': 'LOW'}
	"""
	if len(json_data) > 0:
		results = []
		scopes = fundEvalScope()
		for item in scopes:
			for x in json_data['idxEvalList']:
				if item in x['indexName']:
					results.append('{0}\t{1}\t{2}'.format(x['indexName'],x['pe'],x['pb']))
					break
		if len(results) > 0:
			return results
	pass

# 且慢估值的提取范围和顺序范围
def fundEvalScope():
	return ['中证红利','上证50','沪深300','中证500','中证1000','创业板指','全指医药','全指医药','养老产业','证券公司','中证环保','中证环保','中证传媒','上证50','中证500','中证500','中证500','中证500','沪深300','沪深300','中证传媒']
	pass

# 恒生估值
def HKEval():
	url = 'https://www.legulegu.com/stockdata/market/hsi'
	response = urllib.request.urlopen(url)
	htmls = response.readlines()
	pe = [x.decode('utf-8') for x in htmls if 'current-data' in str(x)]	#current-data 是乐咕乐股网站 html 代码中给 pe 的 class name
	pe = re.findall(":.*?<",str(pe))[0]
	return str(pe).replace(":","").replace("<","")
	pass

def main():
	# # 自由基金
	fundlist = ['100032','510050','510300','510500','512100','159915','159938','001180','000968','512880','512580','001064','512980'\
	,'001051','000478','001052','161017','002903','100038','000051','004752'\
	,'001469','000614','000071','003376','001061','340001','518880']
	[fundValue(x) for x in fundlist]
	print('\n')
	# # 且慢估值
	results = fundEval()
	if results != None and len(results) > 0:
		print('名称\tPE\tPB')
		[print(x) for x in results]
	print('\n')
	# # ETF 计划基金
	# etfPlanList = ['001051','000478','001052','161017','002903','100038','000051','004752']
	# [fundValue(x) for x in etfPlanList]
	# 恒生估值
	HKEval()
	pass

if __name__ == '__main__':
	main()