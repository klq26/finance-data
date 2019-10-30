# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup

from urllib.parse import urlencode

class tianTianTradeInfosSpider:

    def __init__(self):
        self.endYear = 2019
        self.endMonth = 11
        self.cookie = u'Cookie: st_si=48193464463530; st_asi=delete; b_p_log_key=UXRF8fAgsvU1SArYSDZb1vNi/JgRlELFdZEJcyP6AshghN+GTGQZhKJmUzB8WTAY5eYgy3QDKWSkjTh6709wxqrYbnqGW8s/gMglTQ0MCnP4PcCtIi4=; b_pl_bq=de9612a5f90c4a9bab2a853807e9822c; FundTradeLoginTab=0; FundTradeLoginCard=0; st_pvi=69416177127426; st_sp=2019-08-25%2008%3A06%3A30; st_inirUrl=https%3A%2F%2Ftrade7.1234567.com.cn%2FQuery%2Fbill; st_sn=36; st_psi=20191030163723516-112200304021-0615596360; cp_token=037bb6d4002c4f4cacb9d9dea671bc93; FundTradeLoginUser=Y0aJHHQxhKGx5+sZUxu7v5i1tMPtnu3fyAKvCqZ9ONP1lCrvNWNc0xWGQMF0O8IU6wul6rBu; fund_trade_cn=Yu9occN+NBmPD0KGMY4Rb1EepzvmuhhVv50mTfm2lotj/fVEW03adqR5CkD9IJFIcKMIvGCMj1PcLZ+IW/vQWt24PyyCuJJRheUAh2g/Oya3uf6L/iM=; fund_trade_name=Yqf8Zv5PGKQoD2XwIEuglB7B7vZtRgTYx/gRCxjB0bXCACOV2gfGbNWaGBWegE+U5NktRjWz; fund_trade_visitor=YE4ZLbkxHKAnxl7eUxuhdRwU1GittX7TjCKRCvMvHky6oC70yaYhMtWWouiFrsCUotOKjaxc; fund_trade_risk=YsPOpTEiaKP1wBtidQufmxnYS0at/xzHL3caCWG2pRIC/C6lra5G49W5o2u3OTTUAxsIvPFV; fund_trade_gps=6; VipLevel=1; TradeLoginToken=b4307c2912244f71b752c497a1c10cb4; UTOKEN=Yu9occN+NBmPD0KGMY4Rb1EepzvmuhhVv50mTfm2lotj/fVEW03adqR5CkD9IJFIcKMIviCp1dvsvspCYdRIWjA0g4W3EwtaOBUPH+hf+uiKuT4Q8UQ=; LToken=55a907064ec4425290e55a79ec2e2238; fund_trade_trackid=exlaI1s/9a4ElDO1SerZiGln5+wVJJBNEn5AQW3OfG1wFIf52h+hx+buUDrKBDTqv1XkDMeEkO1iM42SlRFQVQ=='
        self.urlPrefix = u'https://query.1234567.com.cn/Query/DelegateList?'
        self.dataFolder = u'htmls'
        if not os.path.exists(self.dataFolder):
            os.makedirs(self.dataFolder)

    def urlWithParams(self, isHistory='false',startDate='', endDate=''):
        # 参数
        params = {}
        params[u'DataType'] = 1
        params[u'StartDate'] = startDate # '2019-09-30'
        params[u'EndDate'] = endDate # '2019-10-30' 
        params[u'BusType'] = 0
        params[u'Statu'] = 2    # 状态 == 成功
        params[u'FundType'] = 0
        params[u'PageSize'] = 240
        params[u'PageIndex'] = 1
        params[u'Container'] = u'tb_delegate'
        params[u'IsHistory'] = isHistory # 2016年10月之前，这里是 'true'
        # DataType=1&StartDate=2019-09-30&EndDate=2019-10-30&BusType=0&Statu=2&FundType=0&PageSize=20&PageIndex=1&Container=tb_delegate&IsHistory=false
        encodedParams = urlencode(params)
        return self.urlPrefix + encodedParams

    def getHistoryTradeInfosData(self,startDate='', endDate=''):
        # 2016 年 10 月之前的数据天天基金是历史数据，IsHistory = true
        # 10月 ~ 12月没有交易
        url = self.urlWithParams(isHistory='true',startDate=startDate, endDate=endDate)
        headers = {'Cookie' : self.cookie}
        response = requests.post(url, headers = headers)
        if response.status_code == 200:
            return response.text
        else:
            return '[ERROR] CODE:{0} URL:{1}'.format(response.status_code,url)

    def getTradeInfosDataByUrl(self, url):
        headers = {'Cookie' : self.cookie}
        response = requests.post(url, headers = headers)
        if response.status_code == 200:
            return response.text
        else:
            return '[ERROR] CODE:{0} URL:{1}'.format(response.status_code,url)

    def getTradeInfosData(self):
        # 获取 2016 年 10 月之前的数据
        startDate = '2016-09-01'
        endDate='2016-09-30'
        text = self.getHistoryTradeInfosData(startDate=startDate, endDate=endDate)
        if 'ERROR' not in text:
            with open(os.path.join(u'htmls', u'{0}_{1}.html'.format(startDate,endDate)),'w',encoding='utf-8') as htmlFile:
                htmlFile.write(text)
        else:
            print(htmlText)
        # 获取 2016 年 10 月之后的数据
        dates = []
        months = [x for x in range(1,13)]
        years = [x for x in range(2017,self.endYear + 1)]
        for year in years:
            for month in months:
                if year == 2019 and month > self.endMonth + 1:
                    break
                if month < 10:
                    mStr = u'0{0}'.format(month)
                else:
                    mStr = str(month)
                dates.append(u'{0}-{1}-01'.format(year,mStr))

        for i in range(1,len(dates)):
            startDate = dates[i-1]
            endDate = dates[i]
            url = self.urlWithParams(isHistory='false',startDate=startDate, endDate=endDate)
            text = self.getTradeInfosDataByUrl(url)
            if 'ERROR' not in text:
                with open(os.path.join(u'htmls', u'{0}_{1}.html'.format(startDate,endDate)),'w',encoding='utf-8') as htmlFile:
                    htmlFile.write(text)
            else:
                print(htmlText)


if __name__ == "__main__":
    spider = tianTianTradeInfosSpider()
    spider.getTradeInfosData()