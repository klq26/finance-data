# -*- coding: utf-8 -*-
import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
sys.path.append(srcDir)
#for p in sys.path:
#    print(p)
from config.pathManager import pathManager
from config.cookieConfig import cookieConfig

class tianTianTradeInfosSpider:

    def __init__(self, strategy='a'):
        self.cookieConfig = cookieConfig()
        self.pm = pathManager()
        self.urlPrefix = u'https://query.1234567.com.cn/Query/DelegateList?'
        self.endYear = 2019
        self.endMonth = 11
        # 历史数据区间，后面不用更改，仅康力泉使用
        self.historyYear = 2016
        self.historyStartMonth = 5
        self.historyEndMonth = 10
        # strategy
        if strategy == 'a':
            # 2016年5月 创建账户
            self.hasHistory = True
            self.startYear = 2017
            self.startMonth = 1
            self.cookie = self.cookieConfig.tiantianCookieKLQ
            self.dataFolder = os.path.join(self.pm.outputPath,u'tiantianTradeInfos',u'htmls','康力泉')
        if strategy == 'b':
            # 2018年1月 创建账户
            self.hasHistory = False
            self.startYear = 2018
            self.startMonth = 1
            self.cookie = self.cookieConfig.tiantianCookieMother
            self.dataFolder = os.path.join(self.pm.outputPath,u'tiantianTradeInfos',u'htmls','李淑云')
        if strategy == 'c':
            # 2018年2月 创建账户
            self.hasHistory = False
            self.startYear = 2018
            self.startMonth = 2
            self.cookie = self.cookieConfig.tiantianCookieFather
            self.dataFolder = os.path.join(self.pm.outputPath,u'tiantianTradeInfos',u'htmls','康世海')
        if not os.path.exists(self.dataFolder):
            os.makedirs(self.dataFolder)
        # 请求数据
        self.getTradeInfosData()

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

    def getTradeInfosDataByUrl(self, url):
        headers = {'Cookie' : self.cookie}
        response = requests.post(url, headers = headers)
        if response.status_code == 200:
            return response.text
        else:
            return '[ERROR] CODE:{0} URL:{1}'.format(response.status_code,url)

    def getTradeInfosData(self):
        # 获取 2016 年 10 月之前的数据（注意：这个只有康力泉有）
        if self.hasHistory:
            dates = []
            months = [x for x in range(self.historyStartMonth,self.historyEndMonth)]
            year = self.historyYear
            for month in months:
                if month < 10:
                    mStr = u'0{0}'.format(month)
                else:
                    mStr = str(month)
                dates.append(u'{0}-{1}-01'.format(year,mStr))
            # 追加历史数据截止日期
            dates.append('2016-09-30')
            print(dates)
            for i in range(1,len(dates)):
                startDate = dates[i-1]
                endDate = dates[i]
                url = self.urlWithParams(isHistory='true',startDate=startDate, endDate=endDate)
                text = self.getTradeInfosDataByUrl(url)
                if 'ERROR' not in text:
                    with open(os.path.join(self.dataFolder, u'{0}_{1}.html'.format(startDate,endDate)),'w',encoding='utf-8') as htmlFile:
                        htmlFile.write(text)
                else:
                    print(htmlText)
        # 获取 2016 年 10 月之后的数据
        dates = []
        months = [x for x in range(1,13)]
        years = [x for x in range(self.startYear,self.endYear + 1)]
        for year in years:
            for month in months:
                if year < self.startYear or (year == self.startYear and month < self.startMonth):
                    print('跳过 {0}-{1}'.format(year,month))
                    continue
                if year == self.endYear and month > self.endMonth + 1:
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
                with open(os.path.join(self.dataFolder, u'{0}_{1}.html'.format(startDate,endDate)),'w',encoding='utf-8') as htmlFile:
                    htmlFile.write(text)
            else:
                print(htmlText)


if __name__ == "__main__":
    strategy = 'a'
    if len(sys.argv) >= 2:
        #
        strategy = sys.argv[1]
    else:
        print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：李淑云 c：康世海 debug：测试代码')
        exit()
    # 传入配置，开始流程
    if strategy == 'debug':
        # 测试代码
        spider = tianTianTradeInfosSpider('a')
        spider.getTradeInfosData()
    else:
        spider = tianTianTradeInfosSpider(strategy)