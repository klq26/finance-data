# -*- coding: utf-8 -*-

import os
import sys
import ssl
import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

from config.requestHeaderManager import requestHeaderManager
from config.pathManager import pathManager

class indexInfo:

    def __init__(self):
        self.requestHeaderManager = requestHeaderManager()
        self.pm = pathManager()
        self.indexInfoList = []
        self.indexValues = []
        self.qiemanEvaluations = []
        self.danjuanEvaluations = []
        # 读取磁盘数据
        with open(os.path.join(self.pm.configPath,u'indexInfo.json'),u'r',encoding='utf-8') as f:
            self.indexInfoList = json.loads(f.read())
        #for index in self.indexInfoList:
        #    print(index)

    # 更新指数 和 估值数据，存入磁盘
    def update(self):
        print('更新指数信息...')
        # 查询指数点位
        self.updateIndexValues()
        print('50%...')
        # 查询指数估值
        self.updateIndexEvaluation()
        print('90%...')
        # 更新数组
        for index in self.indexInfoList:
            # 更新点数
            for value in self.indexValues:
                if index['valueSymbol'] == value['valueSymbol']:
                    index['result']['close'] = value['close']
                    break
            # 更新估值
            if index['EvaluationType'] == '':
                index['result']['pe'] = 0.0
                index['result']['pb'] = 0.0
                index['result']['roe'] = 0.0
            elif index['EvaluationType'] == 'qieman':
                for eval in self.qiemanEvaluations:
                    if index['EvaluationSymbol'] == eval['EvaluationSymbol']:
                        index['result']['pe'] = eval['pe']
                        index['result']['pb'] = eval['pb']
                        index['result']['roe'] = eval['roe']
                        break
            elif index['EvaluationType'] == 'danjuan':
                for eval in self.danjuanEvaluations:
                    if index['EvaluationSymbol'] == eval['EvaluationSymbol']:
                        index['result']['pe'] = eval['pe']
                        index['result']['pb'] = eval['pb']
                        index['result']['roe'] = eval['roe']
                        break
        # 写入磁盘
        with open(os.path.join(self.pm.configPath,u'indexInfo.json'),u'w+',encoding='utf-8') as f:
            f.write(json.dumps(self.indexInfoList, ensure_ascii = False, sort_keys = True, indent = 4, separators=(',', ':')))
        print('更新完毕')

    # 更新指数点数
    def updateIndexValues(self):
        # 读取雪球指数点位
        xueqiuSymbols = [x for x in self.indexInfoList if x['valueType'] == u'xueqiu']
        xueqiuUrlPrefix = u'https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol='
        url = xueqiuUrlPrefix
        for symbol in xueqiuSymbols:
            url = url + '{0},'.format(symbol['valueSymbol'])
        # 组成 URL
        xueqiuUrl = url[0:len(url)-1]
        response = self.requestUrl(xueqiuUrl, self.requestHeaderManager.getXueqiuKLQ())
        data = json.loads(response.text)
        items = data['data']['items']
        for item in items:
            data = {}
            data['valueSymbol'] = item['quote']['symbol']
            data['close'] = round(float(item['quote']['current']),2)
            self.indexValues.append(data)

        # 读取东方财富指数点位
        eastMoneySymbols = [x for x in self.indexInfoList if x['valueType'] == u'eastmoney']
        for symbol in eastMoneySymbols:
            url = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id={0}&TYPE=yk'.format(symbol['valueSymbol'])
            response = self.requestUrl(url, self.requestHeaderManager.getXueqiuKLQ())
            result = response.text.replace('(','').replace(')','')
            values = result.split('\n')
            latestYearValue = values[-2]
            data = {}
            data['valueSymbol'] = symbol['valueSymbol']
            data['close'] = round(float(latestYearValue.split(',')[2]),2)
            self.indexValues.append(data)
        
        # for d in self.indexValues:
        #     print(d)
    
    # 更新指数估值
    def updateIndexEvaluation(self):
        # 读取且慢估值
        qiemanUrl = u'https://qieman.com/pmdj/v2/idx-eval/latest'
        response = self.requestUrl(qiemanUrl, self.requestHeaderManager.getQiemanKLQ())
        jsonData = json.loads(response.text)
        evalList = jsonData['idxEvalList']
        for eval in evalList:
            data = {}
            if u'pe' in eval.keys():
                data['pe'] = eval['pe']
            else:
                data['pe'] = 0.0
            if u'pb' in eval.keys():
                data['pb'] = eval['pb']
            else:
                data['pb'] = 0.0
            if u'roe' in eval.keys():
                data['roe'] = eval['roe']
            else:
                data['roe'] = 0.0
            data['EvaluationSymbol'] = eval['indexName']
            self.qiemanEvaluations.append(data)
        # for d in self.qiemanEvaluations:
        #     print(d)

        # 读取蛋卷估值
        danjuanUrl = u'https://danjuanapp.com/djapi/fundx/activity/user/vip_valuation/show/detail?source=lsd'
        response = self.requestUrl(danjuanUrl, self.requestHeaderManager.getDanjuanKLQ())
        jsonData = json.loads(response.text)
        evalList = jsonData['data']['valuations']
        for eval in evalList:
            data = {}
            if u'pe' in eval.keys():
                data['pe'] = eval['pe']
            else:
                data['pe'] = 0.0
            if u'pb' in eval.keys():
                data['pb'] = eval['pb']
            else:
                data['pb'] = 0.0
            if u'roe' in eval.keys():
                data['roe'] = eval['roe']
            else:
                data['roe'] = 0.0
            data['EvaluationSymbol'] = eval['index_name']
            self.danjuanEvaluations.append(data)
        # for d in self.danjuanEvaluations:
        #     print(d)
    
    # 请求
    def requestUrl(self, url, header):
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url,headers = header, verify = False)
        return response

if __name__ == '__main__':
    info = indexInfo()
    info.update()