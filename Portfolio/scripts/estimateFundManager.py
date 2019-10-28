# -*- coding: utf-8 -*-

import os
import json
import requests
import datetime
import time

from config.cookieConfig import cookieConfig

class estimateFundManager:
    
    # 初始化构造函数
    def __init__(self):
        # 场内代码
        self.innerMarketCodes = [u'510050',u'510300',u'510500',u'512580',u'512880',u'512980',u'518880',u'159902',u'159915',u'159938']

    def estimate(self, code):
        if code == '' or code == u'000000':
            return(0,'NA',0,0.0000,'NA')
        if code in self.innerMarketCodes:
            # 场内基金
            return self.estimateInnerMarketETF(code)
        else:
            # 场外基金
            return self.estimateOuterMarketFund(code)
    
    # 获取场外基金的估值数据
    def estimateOuterMarketFund(self, code):
        url = u'http://fundgz.1234567.com.cn/js/{0}.js'
        headers={
        'User-Agent':'Mozilla/5.0(Macintosh;intel Mac OS 10_11_4)Applewebkit/537.36(KHTML,like Gecko)Chrome/52.0.2743.116 Safari/537.36'
        }
        response = requests.get(url.format(code), headers = headers)
        # 粗略去掉一些字符，因为简单所以没有使用正则表达式
        text = response.text.replace('jsonpgz(','').replace(';','').replace(')','')
        #print(u'[URL]:{0}'.format(self.url.format(code)))
        #print(u'[TEXT]:{0}'.format(text))
        # [TEXT]:{"fundcode":"000478","name":"建信中证500指数增强A","jzrq":"2019-10-25","dwjz":"1.9812","gsz":"2.0151","gszzl":"1.71","gztime":"2019-10-28 15:00"}
        if text == u'':
            # 华安德国 30 这样的 QDII 基金，可能没有估值，返回一个默认的
            return(0,'NA',0,0.0000,'NA')
        data = json.loads(text)
        # 当前净值，当前净值日期，估算净值，估算增长率，估算时间戳
        return (round(float(data['dwjz']),4),data['jzrq'],round(float(data['gsz']),4),round(float(data['gszzl'])/100,4),data['gztime'])

    # 获取场内 ETF 的实时数据
    def estimateInnerMarketETF(self,code):
        cookie = cookieConfig()
        url = 'https://stock.xueqiu.com/v5/stock/quote.json?symbol={0}{1}&extend=detail'
        headers={
        'User-Agent':'Mozilla/5.0(Macintosh;intel Mac OS 10_11_4)Applewebkit/537.36(KHTML,like Gecko)Chrome/52.0.2743.116 Safari/537.36',
        'Cookie' : cookie.xueqiuCookie
        }
        marketSign = ''
        if code.startswith(u'15'):
            marketSign = u'SZ'
        else:
            marketSign = u'SH'
        response = requests.get(url.format(marketSign,code), headers = headers)
        data = json.loads(response.text)
        # data.quote.last_close & data.quote.nav_date & data.quote.current & current/last_close & timestamp
        quote = data['data']['quote']
        netValueDateTimeStamp = int(int(quote['nav_date'])/1000)
        esitmateValueDateTimeStamp = int(int(quote['timestamp'])/1000)
        
        netValueDateArray = datetime.datetime.fromtimestamp(netValueDateTimeStamp)
        esitmateValueDateArray = datetime.datetime.fromtimestamp(esitmateValueDateTimeStamp)
        
        netValueDate = netValueDateArray.strftime("%Y-%m-%d %H:%M")
        esitmateValueDate = esitmateValueDateArray.strftime("%Y-%m-%d %H:%M")
        
        # 当前净值，当前净值日期，估算净值，估算增长率，估算时间戳
        return (round(float(quote['last_close']),4),netValueDate,round(float(quote['current']),4),round(float(quote['current'])/float(quote['last_close'])-1,4),esitmateValueDate)
        

#manager = estimateFundManager()
#print(manager.estimate(u'510500'))

