# -*- coding: utf-8 -*-

import sys
import os
import json
import requests
from datetime import datetime
import time
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning
 
from model.fundModel import fundModel
from config.requestHeaderManager import requestHeaderManager
from config.assetCategoryManager import assetCategoryManager
from config.pathManager import pathManager


class estimateFundManager:

    # 初始化构造函数
    def __init__(self):
        # 场内代码
        self.innerMarketCodes = assetCategoryManager().getEstimableFunds(isInnerMarket = True).values()
        self.headerManager = requestHeaderManager()
        self.dateFormat = u'%Y-%m-%d %H:%M:%S'
        self.pm = pathManager()
        self.cacheTimeStamp = 0
        self.cacheFundModelArray = []
        # 尝试查询缓存
        timeStamp, cacheFundModelArray = self.loadCache()
        if timeStamp > 0 and len(cacheFundModelArray) > 0:
            self.cacheTimeStamp = timeStamp
            self.cacheFundModelArray = cacheFundModelArray

    def estimate(self, code):
        if code == '' or code == u'000000':
            return(0, 'NA', 0, 0.0000, 'NA')
        # 命中缓存
        if len(self.cacheFundModelArray) > 0:
            for fundModel in self.cacheFundModelArray:
                if fundModel['fundCode'] == code:
                    #print(' {0} 命中缓存。估值：{1}'.format(code, fundModel['estimateNetValue']))
                    return (fundModel['currentNetValue'], fundModel['currentNetValueDate'], fundModel['estimateNetValue'], fundModel['estimateRate'], fundModel['estimateTime'])
        if code in self.innerMarketCodes:
            # 场内基金
            return self.estimateInnerMarketETF(code)
        else:
            # 场外基金
            return self.estimateOuterMarketFund(code)

    # 获取场外基金的估值数据
    def estimateOuterMarketFund(self, code):
        url = u'http://fundgz.1234567.com.cn/js/{0}.js'
        response = requests.get(url.format(code))
        # 粗略去掉一些字符，因为简单所以没有使用正则表达式
        text = response.text.replace(
            'jsonpgz(', '').replace(';', '').replace(')', '')
        # print(u'[URL]:{0}'.format(self.url.format(code)))
        # print(u'[TEXT]:{0}'.format(text))
        # [TEXT]:{"fundcode":"000478","name":"建信中证500指数增强A","jzrq":"2019-10-25","dwjz":"1.9812","gsz":"2.0151","gszzl":"1.71","gztime":"2019-10-28 15:00"}
        if text == u'':
            # 华安德国 30 这样的 QDII 基金，可能没有估值，返回一个默认的
            return(0, 'NA', 0, 0.0000, 'NA')
        data = json.loads(text)
        # 当前净值，当前净值日期，估算净值，估算增长率，估算时间戳
        return (round(float(data['dwjz']), 4), data['jzrq'], round(float(data['gsz']), 4), round(float(data['gszzl'])/100, 4), data['gztime'])

    # 获取场内 ETF 的实时数据
    def estimateInnerMarketETF(self, code):

        url = 'https://stock.xueqiu.com/v5/stock/quote.json?symbol={0}{1}&extend=detail'
        headers = self.headerManager.getXueqiuKLQ()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        ssl._create_default_https_context = ssl._create_unverified_context
        marketSign = ''
        if code.startswith(u'15') or code == '162411':
            marketSign = u'SZ'
        else:
            marketSign = u'SH'
        response = requests.get(url.format(
            marketSign, code), headers=headers, verify=False)
        data = json.loads(response.text)
        # data.quote.last_close & data.quote.nav_date & data.quote.current & current/last_close & timestamp
        quote = data['data']['quote']
        # DEBUG
        # print('\n', code, url.format(marketSign, code), data,sep='\n')
        netValueDateTimeStamp = int(int(quote['nav_date'])/1000)
        esitmateValueDateTimeStamp = int(int(quote['timestamp'])/1000)

        netValueDateArray = datetime.fromtimestamp(netValueDateTimeStamp)
        esitmateValueDateArray = datetime.fromtimestamp(
            esitmateValueDateTimeStamp)

        netValueDate = netValueDateArray.strftime("%Y-%m-%d")
        esitmateValueDate = esitmateValueDateArray.strftime("%Y-%m-%d %H:%M")

        # 当前净值，当前净值日期，估算净值，估算增长率，估算时间戳
        return (round(float(quote['last_close']), 4), netValueDate, round(float(quote['current']), 4), round(float(quote['current'])/float(quote['last_close'])-1, 4), esitmateValueDate)

    # 存入缓存文件
    def saveCache(self, fundModelArray):
        # 判断是否需要更新缓存
        nowTimeStamp = datetime.now().timestamp()
        # 缓存文件是 30 分钟之前的，才需要更新。另外如果需要缓存的基金数目发生变化，比如变多了，也要更新
        if nowTimeStamp - self.cacheTimeStamp <= 30 * 60 and len(fundModelArray) <= len(self.cacheFundModelArray):
            print('\n缓存文件为 30 分钟之内的。无需更新。当前缓存库条目数：{0}'.format(len(self.cacheFundModelArray)))
            return
        else:
            print('\n更新缓存库，条目数：{0}'.format(len(fundModelArray)))
        estimateValues = []
        for fundModel in fundModelArray:
            estimateValue = {}
            estimateValue['fundName'] = fundModel.fundName
            estimateValue['fundCode'] = fundModel.fundCode
            estimateValue['currentNetValue'] = fundModel.currentNetValue
            estimateValue['currentNetValueDate'] = fundModel.currentNetValueDate
            estimateValue['estimateNetValue'] = fundModel.estimateNetValue
            estimateValue['estimateRate'] = fundModel.estimateRate
            estimateValue['estimateTime'] = fundModel.estimateTime
            estimateValues.append(estimateValue)
        updateTime = datetime.now().strftime(self.dateFormat)
        cacheDict = {'updateTime': updateTime, 'data': estimateValues}
        with open(os.path.join(self.pm.configPath, 'fundEstimateCache.json'), 'w+', encoding=u'utf-8') as f:
            f.write(json.dumps(cacheDict, ensure_ascii=False, sort_keys = True, indent = 4, separators=(',', ':')))

    # 尝试加载缓存文件
    def loadCache(self):
        cacheFilePath = os.path.join(self.pm.configPath, 'fundEstimateCache.json')
        if os.path.exists(cacheFilePath):
            with open(os.path.join(self.pm.configPath, 'fundEstimateCache.json'), 'r', encoding=u'utf-8') as f:
                jsonData = json.loads(f.read())
                cacheTimeStamp = datetime.strptime(jsonData['updateTime'], self.dateFormat).timestamp()
                nowTimeStamp = datetime.now().timestamp()
                # 30 分钟以内的话，估值还是走缓存效率比较高
                if nowTimeStamp - cacheTimeStamp <= 30 * 60:
                    return (cacheTimeStamp, jsonData['data'])
        print('estimate 缓存失效，重新获取...')
        return (0,[])

if __name__ == '__main__':
    manager = estimateFundManager()
    print(manager.estimate(u'510500'))
