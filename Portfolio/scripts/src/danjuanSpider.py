# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from config.pathManager import pathManager
from config.requestHeaderManager import requestHeaderManager

class danjuanSpider:
    
    # 初始化构造函数
    def __init__(self, strategy = 'a'):
        self.luosidingUrl = u'https://danjuanapp.com/djapi/holding/plan/CSI666'
        # 暂存，这是拿钉钉宝数据的，暂时不算很重要
        self.dingdingbaoUrl = u'https://danjuanapp.com/position/strategy/CSI1021'
        self.strategy = strategy
        if strategy == 'a':
            self.pm = pathManager(strategyName='康力泉')
        elif strategy == 'b':
            self.pm = pathManager(strategyName='父母')
        self.headerManager = requestHeaderManager()

    def getKLQ(self):
        self.requestWithName(self.luosidingUrl, '螺丝钉定投', self.headerManager.getDanjuanKLQ())
        self.requestWithName(self.dingdingbaoUrl, '钉钉宝', self.headerManager.getDanjuanKLQ())
    
    def getLSY(self):
        self.requestWithName(self.luosidingUrl, '李淑云',self.headerManager.getDanjuanLSY())
        
    def getKSH(self):
        self.requestWithName(self.luosidingUrl, '康世海',self.headerManager.getDanjuanKSH())
        
    def requestWithName(self, url, name, header):
        headers=header
        if url == None:
            url = self.luosidingUrl
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, headers = headers,verify=False)
        pm = pathManager()
        with open(os.path.join(self.pm.holdingOutputPath,u'danjuan_{}.txt'.format(name)),'w',encoding='utf-8') as f:
            data = json.loads(response.text)['data']
            titleLine = u'{0}\t总市值\t{1}\t累计收益\t{2}'.format(name,round(data['total_assets'],2),round(data['total_gain'],2))
            print(titleLine)
            f.write(titleLine + '\n')
            headerLine = u'基金名称\t基金代码\t持仓成本\t持仓份额\t持仓市值\t累计收益'
            print(headerLine)
            f.write(headerLine + '\n')
            for item in data['items']:
                # 名称，代码，持仓成本，持仓份额，持仓市值，累计收益
                seq = (item['fd_name'],item['fd_code'],str(round(item['holding_cost'],4)),\
                str(round(item['volume'],2)),str(round(item['market_value'],2)),str(round(item['total_gain'],2)))
                print(u'\t'.join(seq))
                f.write(u'\t'.join(seq) + '\n')
            print('\n')

if __name__ == '__main__':
    strategy = 'a'
    if len(sys.argv) >= 2:
        #print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：父母')
        strategy = sys.argv[1]
    if strategy == 'a':
        spider = danjuanSpider('a')
        spider.getKLQ()
        os.startfile(spider.pm.holdingOutputPath)
    elif strategy == 'b':
        spider = danjuanSpider('b')
        spider.getLSY()
        spider.getKSH()
        os.startfile(spider.pm.holdingOutputPath)
    elif strategy == 'debug':
        print('[DEBUG] {0}'.format(__file__))
    else:
        print('[ERROR] 无法识别的参数：{0}'.format(strategy))