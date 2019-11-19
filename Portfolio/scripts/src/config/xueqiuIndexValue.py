# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from config.pathManager import pathManager
from config.requestHeaderManager import requestHeaderManager

class xueqiuIndexValue:
    
    def __init__(self):
        self.urlPrefix = u'https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol='
        self.headerManager = requestHeaderManager()
        self.pm = pathManager()
        #组成雪球 URL
        with open(os.path.join(self.pm.configPath,u'xueqiuIndexSymbol.json'),u'r',encoding='utf-8') as f:
            self.indexSymbols = json.loads(f.read())
            url = self.urlPrefix
            for symbol in self.indexSymbols:
                url = url + '{0},'.format(symbol['xueqiuSymbol'])
            # 组成 URL
            self.url = url[0:len(url)-1]
        # 查询指数最新值
        self.fetchIndexValues(self.headerManager.getXueqiuKLQ())
        
    # 查询指数
    def fetchIndexValues(self,header):
        headers=header
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(self.url, headers = headers,verify=False)
        data = json.loads(response.text)
        items = data['data']['items']
        for symbol in self.indexSymbols:
            for item in items:
                #print(item['quote']['symbol'],item['quote']['name'],item['quote']['current'])
                if item['quote']['symbol'] == symbol['xueqiuSymbol']:
                    symbol['close'] = item['quote']['current']
                    break
        # 写回 json 文件
        self.udpateIndexValues()
    
    # 写入磁盘
    def udpateIndexValues(self):
        with open(os.path.join(self.pm.configPath,u'xueqiuIndexSymbol.json'),u'w+',encoding='utf-8') as f:
            f.write(json.dumps(self.indexSymbols, ensure_ascii = False, sort_keys = True, indent = 4, separators=(',', ':')))

if __name__ == '__main__':
    xueqiu = xueqiuIndexValue()