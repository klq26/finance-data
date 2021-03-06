# -*- coding: utf-8 -*-
import os
import sys
import re
import requests
import json
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from bs4 import BeautifulSoup
# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
sys.path.append(srcDir)

from config.pathManager import pathManager
from config.requestHeaderManager import requestHeaderManager

class tiantianSpider:
    
    # 初始化构造函数
    def __init__(self, strategy = 'a'):
        
        self.totalMarketCap = 0.0
        self.totalGain = 0.0
        self.results = []
        self.strategy = strategy
        if strategy == 'a':
            self.pm = pathManager(strategyName=u'康力泉')
        elif strategy == 'b':
            self.pm = pathManager(strategyName=u'父母')
        self.headerManager = requestHeaderManager()

    def getKLQ(self):
        self.url = u'https://trade.1234567.com.cn/MyAssets/do.aspx/GetHoldAssetsNew?1571906547481'
        self.urlPrefix = u'https://trade.1234567.com.cn'
        self.requestWithName(u'康力泉',self.headerManager.getTiantianKLQ(),self.headerManager.getTiantianKLQ())
    
    def getLSY(self):
        self.url = u'https://trade7.1234567.com.cn/MyAssets/do.aspx/GetHoldAssetsNew?1574478714617'
        self.urlPrefix = u'https://trade7.1234567.com.cn'
        self.requestWithName(u'李淑云',self.headerManager.getTiantianLSY(),self.headerManager.getTiantianSingleLSY())
    
    def requestWithName(self,name,header,singleHeader):
        """
        天天基金的爬虫略麻烦：
        1）请求为 POST 记得附带参数
        2）持仓摊薄成本和持仓份额需要进行二次查询，去 detail 页面解析
        3）需要通过解析 html 标签取值，接口返回的是 html 代码
        """
        headers = header
        # 天天基金 Post 请求的配置参数
        postData = json.dumps({'type':'0','sorttype':'5','isNeedTotal':'true'})
        ssl._create_default_https_context = ssl._create_unverified_context
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(self.url, verify=False, headers = headers, data = postData)
        data = json.loads(response.text)
        
        html = json.loads(data['d'])['content']
        soup = BeautifulSoup(html, 'lxml')
        # 取出条目列表
        contentList = soup.find_all('tr')
        totalCount = len(contentList)
        current = 1
        pm = pathManager()
        with open(os.path.join(self.pm.holdingOutputPath,'tiantian_{}.txt'.format(name)),'w',encoding='utf-8') as f:
            for item in contentList:
                # 取出所有 td
                tds = item.find_all('td')            
                a = item.find(attrs={'class':u'btn-more f14'})
                # 拼接详情页 URL
                detailUrl = self.urlPrefix + a.get('href')
                # 从持仓详情页，取出品种的 摊薄单价 & 持仓份额
                ssl._create_default_https_context = ssl._create_unverified_context
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                # 老妈的天天基金详情需要独立的请求 header 无奈出此下策
                singleHeaders = singleHeader
                
                detailResponse = requests.get(detailUrl,headers = singleHeaders, verify=False)
                # e.g.
                # <span id="tanbaodanjia">摊薄单价(元)：<span class="number14">1.0193</span></span>
                # <div class="h20"><span class="ft w220">持仓份额(份)：<span class="numbergray14">65064.33</span></span></div>
                detailSoup = BeautifulSoup(detailResponse.text,'lxml')
                # 持仓成本
                price = detailSoup.find(id=u'tanbaodanjia').span.text
                h20s = detailSoup.find_all(attrs={'class':'h20'})
                # 持仓份额
                volume = h20s[0].span.span.text
                partent = re.compile(u'^(.*?)（(.*?)）$')
                re_get = re.findall(partent, tds[0].p.a.text)
                # 名称
                fundName = re_get[0][0]
                # 代码
                fundCode = re_get[0][1]
                # 持仓市值
                partent2 = re.compile(u'([0-9]+.[0-9]+)')   # 123.45 排除“有在途交易”
                re_get2 = re.findall(partent2, tds[1].text.replace(',',''))
                marketValue = re_get2[0]
                # 累计收益
                totalGain = tds[2].span.text.replace(',','')
                seq = (re_get[0][0],re_get[0][1],price,\
                volume,marketValue,totalGain)
                self.results.append(u'\t'.join(seq))
                # 计算整体情况
                self.totalMarketCap = self.totalMarketCap + round(float(marketValue),2)
                self.totalGain = self.totalGain + round(float(totalGain),2)
                print('\r天天基金进度：{0:.2f}% {1} / {2}'.format(float(current)/totalCount * 100, current,totalCount),end='',flush=True)
                if current == totalCount:
                    print('\n')
                current = current + 1
            # 开始写入整体情况
            titleLine = u'{0}\t总市值\t{1}\t累计收益\t{2}'.format(u'天天基金',round(self.totalMarketCap,2),round(self.totalGain,2))
            print(titleLine)
            f.write(titleLine + '\n')
            # 写入表头
            headerLine = u'基金名称\t基金代码\t持仓成本\t持仓份额\t持仓市值\t累计收益'
            print(headerLine)
            f.write(headerLine + '\n')
            for string in self.results:
                print(string)
                f.write(string + '\n')
            print('\n')

if __name__ == '__main__':
    strategy = 'a'
    if len(sys.argv) >= 2:
        #print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：父母')
        strategy = sys.argv[1]
        
    spider = tiantianSpider(strategy)
    if strategy == 'a':
        spider.getKLQ()
    elif strategy == 'b':
        spider.getLSY()
    elif strategy == 'debug':
        print('[DEBUG] {0}'.format(__file__))
    else:
        print(u'[ERROR] 参数错误，不支持的策略编号。')
        exit()