# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
sys.path.append(srcDir)

from config.requestHeaderManager import requestHeaderManager
from config.pathManager import pathManager

class qiemanSpider:
    
    # 初始化构造函数
    def __init__(self):
        # 补充 150 份
        self.urlForPlan150 = u'https://qieman.com/pmdj/v2/long-win/ca/assets-summary?capitalAccountId=CA8UKLYHA67WPK&useV2OrderApi=true&classify=true'
        # S 定投
        self.urlForPlanS = u'https://qieman.com/pmdj/v2/long-win/ca/assets-summary?capitalAccountId=CA8FCJKFPANTP2&useV2OrderApi=true&classify=true'
        # ★ 填写验证必须参数
        self.headerManager = requestHeaderManager()
    
    def getKLQ(self):
        self.requestWithName(name=u'10万补充ETF计划',url=self.urlForPlan150)
        self.requestWithName(name=u'我的S定投计划',url=self.urlForPlanS)
    
    def requestWithName(self, name, url):
        headers=self.headerManager.getQiemanKLQ()
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, headers = headers, verify=False)
        pm = pathManager()
        with open(os.path.join(pm.holdingOutputPath,'qieman_{}.txt'.format(name)),'w',encoding='utf-8') as f:
            #print(response.text)
            data = json.loads(response.text)
            # "totalAsset": 34074.8509,   # 总资产
            # "accumulatedProfit": 444.71,# 累计收益
            # list("planAssetList") 
            #   list("assetList")
            #       名称，代码
            #       "fund" 
            #           "fundCode": "000478", "fundName": "建信中证500指数增强A",   
            #       持仓成本，持仓份额，持仓市值，累计收益
            #       "custUnitValue": 1.9239, "totalShare": 3813.64, "totalAsset": 7501.4299, "accumulatedProfit": 164.43,
            titleLine = u'{0}\t总市值\t{1}\t累计收益\t{2}'.format(name,round(data['totalAsset'],2),round(data['accumulatedProfit'],2))
            print(titleLine)
            f.write(titleLine + '\n')
            headerLine = u'基金名称\t基金代码\t持仓成本\t持仓份额\t持仓市值\t累计收益'
            print(headerLine)
            f.write(headerLine + '\n')
            for assetCategory in data['planAssetList']:
                for item in assetCategory['assetList']:
                    # 名称，代码，持仓成本，持仓份额，持仓市值，累计收益
                    seq = (item['fund']['fundName'],item['fund']['fundCode'],str(round(item['custUnitValue'],4)),\
                    str(round(item['totalShare'],2)),str(round(item['totalAsset'],2)),str(round(item['accumulatedProfit'],2)))
                    print(u'\t'.join(seq))
                    f.write(u'\t'.join(seq) + '\n')
            print('\n')

if __name__ == '__main__':
    strategy = 'a'
    if len(sys.argv) >= 2:
        #print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：父母')
        strategy = sys.argv[1]
    if strategy == 'debug':
        print('[DEBUG] {0}'.format(__file__))
    else:
        spider = qiemanSpider()
        spider.getKLQ()
    