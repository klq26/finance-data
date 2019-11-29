# -*- coding: utf-8 -*-

import os
import sys
import requests
import json
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning
 
from config.requestHeaderManager import requestHeaderManager
from config.pathManager import pathManager

class guangfaSpider:
    
    # 初始化构造函数
    def __init__(self):
        # 注意；这些请求需要从未登录状态，一路点详情进入具体页面才会发送，否则追踪不到
        self.url = u'https://trade.gffunds.com.cn/mapi/account/assets/position-gains?tttt=0.5490600043154694'
        self.headerManager = requestHeaderManager()
        
    def getKLQ(self):
        self.requestWithName(u'支付宝')
    
    def requestWithName(self,name):
        headers=self.headerManager.getGuangfaKLQ()
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(self.url, headers = headers, verify=False)
        pm = pathManager()
        with open(os.path.join(pm.holdingOutputPath,u'guangfa_{}.txt'.format(name)),'w',encoding='utf-8') as f:
            jsonData = json.loads(response.text)['data']
            contentList = jsonData['fundPositionGainList']
            for data in contentList:
                # 注意：我们只要广发基金中，来自于蚂蚁金服的份额。这一部分是支付宝买的
                if data['fundCode'] == '001064':
                    for buyInfo in data['fundAgencyPositionGains']:
                        if buyInfo[u'agencyName'] == u'蚂蚁杭州':
                            titleLine = u'{0}\t总市值\t{1}\t累计收益\t{2}'.format(name,round(float(buyInfo['totalBalance']),2),round(float(buyInfo['positionGain']),2))
                            print(titleLine)
                            f.write(titleLine + '\n')
                            headerLine = u'基金名称\t基金代码\t持仓成本\t持仓份额\t持仓市值\t累计收益'
                            print(headerLine)
                            f.write(headerLine + '\n')
                            # 名称，代码，持仓成本，持仓份额，持仓市值，累计收益
                            seq = (data['fundName'],data['fundCode'],str(round(float(buyInfo['purchasePrice']),4)),\
                            str(round(float(buyInfo['currentShares']),2)),str(round(float(buyInfo['totalBalance']),2)),str(round(float(buyInfo['positionGain']),2)))
                            print(u'\t'.join(seq))
                            print(u'\n\n')
                            f.write(u'\t'.join(seq) + '\n')
                            break
                    break
                print('\n')

if __name__ == '__main__':
    strategy = 'a'
    if len(sys.argv) >= 2:
        #print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：父母')
        strategy = sys.argv[1]
    if strategy == 'debug':
        print('[DEBUG] {0}'.format(__file__))
    else:
        spider = guangfaSpider()
        spider.getKLQ()