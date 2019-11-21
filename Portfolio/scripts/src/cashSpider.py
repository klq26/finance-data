# -*- coding: utf-8 -*-

import os
import sys
import ssl

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

from config.requestHeaderManager import requestHeaderManager
from config.pathManager import pathManager

class cashSpider:

    def __init__(self,strategy):
        print()
        
    # 获取随手记的现金部分数据
    def getSuiShouJi(self):
        # 请求
        url = u'https://www.sui.com/account/account.do'
        headers = requestHeaderManager().getSuiKLQ()
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url,headers = headers, verify=False)
        # 解析 key
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
        print(u'其他现金：{0} 元'.format(totalCash))

    def getQieManCash(self):
        # 请求
        url = u'https://qieman.com/assets/wallet'
        headers = requestHeaderManager().getQiemanKLQ()
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url,headers = headers, verify=False)
        print(response.text)
        
if __name__ == '__main__':
    strategy = 'a'
    if len(sys.argv) >= 2:
        #print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：父母')
        strategy = sys.argv[1]
    if strategy == 'debug':
        print('[DEBUG] {0}'.format(__file__))
    else:
        spider = cashSpider(strategy)
        #spider.getSuiShouJi()
        spider.getQieManCash()