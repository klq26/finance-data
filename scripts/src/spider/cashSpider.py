# -*- coding: utf-8 -*-

import os
import sys
import ssl
import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
print(srcDir)
sys.path.append(srcDir)
from config.requestHeaderManager import requestHeaderManager
from config.pathManager import pathManager

class cashSpider:

    def __init__(self, strategy, strategyName):
        self.strategyName = strategyName
        if strategy == 'a':
            self.pm = pathManager(u'康力泉')
        elif strategy == 'b':
            self.pm = pathManager(u'父母')
        self.requestHeaderManager = requestHeaderManager()
        
    # 获取随手记的现金部分数据
    def getSuiShouJi(self):
        # 请求
        url = u'https://www.sui.com/account/account.do'
        headers = requestHeaderManager().getSuiKLQ()
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url,headers = headers, verify=False)
        # 解析
        accountKeys = {\
        u'acc-val-amount-156469181835':u'钱包',\
        u'acc-val-amount-156469181837':u'招商银行卡',\
        u'acc-val-amount-156469181839':u'工商银行卡',\
        u'acc-val-amount-1632793665':u'北京银行卡',\
        u'acc-val-amount-1632796112':u'中国银行卡',\
        u'acc-val-amount-1632797656':u'支付宝',\
        u'acc-val-amount-156469181859':u'招行信用卡'}
        soup = BeautifulSoup(response.text, 'lxml')
        totalCash = 0
        for key in accountKeys.keys():
            inputTag = soup.find(attrs={'id':key})
            if u'信用卡' in accountKeys[key]:
                totalCash = totalCash - float(inputTag['value'])
            else:
                totalCash = totalCash + float(inputTag['value'])
            #print(accountKeys[key],inputTag['value'])
        print(u'银行卡+支付宝+现金-信用卡：{0} 元，累计收益：{1} 元'.format(round(totalCash,2),round(0,2)))
        return (round(totalCash,2),round(0,2))

    # 获取且慢盈米宝
    def getQieManYingMiBao(self,headers):
        # 请求
        url = u'https://qieman.com/pmdj/v2/asset/summary'
        headers = headers
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url,headers = headers, verify=False)
        # 解析
        data = json.loads(response.text)
        wallets = data['walletAssets']
        totalCash = wallets[0]['totalAsset']
        totalGain = wallets[0]['accumulatedProfit']
        print(u'且慢盈米宝：{0} 元，累计收益：{1} 元'.format(round(totalCash,2),round(totalGain,2)))
        return (round(totalCash,2),round(totalGain,2))

    # 获取蛋卷钉钉宝短期债券
    def getDanjuanDingDingBao(self, headers):
        # 请求
        url = u'https://danjuanapp.com/djapi/holding/plan/CSI1021'
        # https://danjuanapp.com/djapi/holding/fund/003474 南方天天利
        # CSI1021 CSI1019 CSI666
        headers = headers
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url,headers = headers, verify=False)
        # 解析
        data = json.loads(response.text)['data']
        #titleLine = u'{0}\t总市值\t{1}\t累计收益\t{2}'.format(name,round(data['total_assets'],2),round(data['total_gain'],2))
        #print(titleLine)
        #f.write(titleLine + '\n')
        headerLine = u'基金名称\t基金代码\t持仓成本\t持仓份额\t持仓市值\t累计收益'
        #print(headerLine)
        #f.write(headerLine + '\n')
        totalCash = 0
        totalGain = 0
        for item in data['items']:
            # 名称，代码，持仓成本，持仓份额，持仓市值，累计收益
            seq = (item['fd_name'],item['fd_code'],str(round(item['holding_cost'],4)),\
            str(round(item['volume'],2)),str(round(item['market_value'],2)),str(round(item['total_gain'],2)))
            #print(u'\t'.join(seq))
            #f.write(u'\t'.join(seq) + '\n')
            totalCash = totalCash + round(item['market_value'],2)
            totalGain = totalGain + round(item['total_gain'],2)
        # print('\n')
        print(u'蛋卷钉钉宝：{0} 元，累计收益：{1} 元'.format(round(totalCash,2),round(totalGain,2)))
        return (round(totalCash,2),round(totalGain,2))

    def getDanjuan(self, isCash, code, headers):
        url = u'https://danjuanapp.com/djapi/holding/'
        if isCash:
            url = url + 'fund/' + code
        else:
            url = url + 'plan/' + code
        headers = headers
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url,headers = headers, verify=False)
        # 解析
        data = json.loads(response.text)['data']
        #titleLine = u'{0}\t总市值\t{1}\t累计收益\t{2}'.format(name,round(data['total_assets'],2),round(data['total_gain'],2))
        #print(titleLine)
        #f.write(titleLine + '\n')
        headerLine = u'基金名称\t基金代码\t持仓成本\t持仓份额\t持仓市值\t累计收益'
        #print(headerLine)
        #f.write(headerLine + '\n')
        totalCash = 0
        totalGain = 0
        # 名称，代码，持仓成本，持仓份额，持仓市值，累计收益
        seq = (data['fd_name'],data['fd_code'],str(round(data['holding_cost'],4)),\
        str(round(data['volume'],2)),str(round(data['market_value'],2)),str(round(data['total_gain'],2)))
        #print(u'\t'.join(seq))
        #f.write(u'\t'.join(seq) + '\n')
        totalCash = totalCash + round(data['market_value'],2)
        totalGain = totalGain + round(data['total_gain'],2)
        print(u'蛋卷货币基金：{0} 元，累计收益：{1} 元'.format(round(totalCash,2),round(totalGain,2)))
        return (round(totalCash,2),round(totalGain,2))


    # 获取天天基金活期宝
    def getTianTianHuoQiBao(self, url, header = None):
        # 请求
        url = url
        headers = header
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url,headers = headers, verify=False)
        # 解析
        #<span id="ctl00_body_lblTotalBalance" class="f24 c3">32,151.19</span>&nbsp;元</span>
        #<span id="ctl00_body_lblSumBenefit" class="red bold f14">5,653.13</span>
        soup = BeautifulSoup(response.text, 'lxml')
        totalCash = 0
        totalGain = 0
        spanTag = soup.find(attrs={'id':'ctl00_body_lblTotalBalance'})
        totalCash = float(spanTag.text.replace(',',''))
        spanTag = soup.find(attrs={'id':'ctl00_body_lblSumBenefit'})
        totalGain = float(spanTag.text.replace(',',''))
        print(u'天天现金宝：{0} 元，累计收益：{1} 元'.format(round(totalCash,2),round(totalGain,2)))
        return (round(totalCash,2),round(totalGain,2))

        # 获取且慢盈米宝
    
    

    def getKLQ(self):
        totalCash = 0
        totalGain = 0
        print(u'全部资金情况：')
        result = self.getSuiShouJi()
        totalCash = totalCash + result[0]
        totalGain = totalGain + result[1]
        # 且慢盈米宝之后不会在存现金，历史收益已收录
        # result = self.getQieManYingMiBao(headers=requestHeaderManager().getQiemanKLQ())
        # totalCash = totalCash + result[0]
        # totalGain = totalGain + result[1]

        # 蛋卷
        result = self.getDanjuan(True, '003474',headers=requestHeaderManager().getDanjuanKLQ())
        totalCash = totalCash + result[0]
        totalGain = totalGain + result[1]

        # 天天现金
        result = self.getTianTianHuoQiBao(u'https://trade.1234567.com.cn/xjb/index', self.requestHeaderManager.getTiantianKLQ())
        totalCash = totalCash + result[0]
        totalGain = totalGain + result[1]

        # 华宝证券，现在是手动更新
        totalCash = totalCash + 7561.53
        totalGain = totalGain + 20.71
        print(u'华宝证券：7561.53 元，累计收益：20.71 元')

        totalCash = round(totalCash,2)
        totalGain = round(totalGain,2)
        print(u'\n总现金：{0} 元，总累计收益：{1} 元'.format(totalCash,totalGain))
        cashPath = os.path.join(self.pm.inputPath, u'cash_{0}.txt'.format(self.strategyName))
        cash_lines = []
        # 读入内存
        with open(cashPath,u'r',encoding='utf-8') as f:
            for line in f.readlines():
                cash_lines.append(line)
        #print(cash_lines)
        # 写入磁盘
        with open(cashPath,u'w',encoding='utf-8') as f:
            for line in cash_lines:
                if u'货币基金综合' in line:
                    values = line.split('\t')
                    values[3] = str(totalCash)
                    values[4] = str(totalCash)
                    values[5] = str(totalGain)
                    f.write(u'\t'.join(values)+'\n')
                else:
                    f.write(line)

    def getParent(self):
        totalCash = 0
        totalGain = 0
        print(u'全部资金情况：')
        # result = self.getDanjuanDingDingBao(headers=requestHeaderManager().getDanjuanLSY())
        # totalCash = totalCash + result[0]
        # totalGain = totalGain + result[1]
        result = self.getDanjuan(True, '003474', headers=requestHeaderManager().getDanjuanKSH())
        totalCash = totalCash + result[0]
        totalGain = totalGain + result[1]
        totalCash = round(totalCash,2)
        totalGain = round(totalGain,2)
        print(u'\n总现金：{0} 元，总累计收益：{1} 元'.format(totalCash,totalGain))
        cashPath = os.path.join(self.pm.inputPath, u'cash_{0}.txt'.format(self.strategyName))
        cash_lines = []
        # 读入内存
        with open(cashPath,u'r',encoding='utf-8') as f:
            for line in f.readlines():
                cash_lines.append(line)
        #print(cash_lines)
        # 写入磁盘
        with open(cashPath,u'w',encoding='utf-8') as f:
            for line in cash_lines:
                if u'货币基金综合' in line:
                    values = line.split('\t')
                    values[3] = str(totalCash)
                    values[4] = str(totalCash)
                    values[5] = str(totalGain)
                    f.write(u'\t'.join(values)+'\n')
                else:
                    f.write(line)
        

if __name__ == '__main__':
    strategy = 'a'
    if len(sys.argv) >= 2:
        #print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：父母')
        strategy = sys.argv[1]
    if strategy == 'debug':
        print('[DEBUG] {0}'.format(__file__))
    elif strategy == 'a':
        spider = cashSpider(strategy, u'康力泉')
        spider.getKLQ()
    elif strategy == 'b':
        spider1 = cashSpider(strategy, u'父母')
        spider1.getParent()
        #https://qieman.com/pmdj/v2/asset/ca/detail?capitalAccountId=CA942R8128PFE7