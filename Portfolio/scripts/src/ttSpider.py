# -*- coding: utf-8 -*-

import os
import json
import requests
import re

class ttSpider:
    
    # 初始化构造函数
    def __init__(self, strategy = 'a'):
        # 历史持仓明细
        self.url = u'https://trade.1234567.com.cn/SearchHandler/bi.aspx?callback=jQuery&type=billhold&qkt=91b4e48755424a9bb0813eaaeac1895c&ttype=month&year=2019&data=9&_=1572521296738'
       # 历史交易明细
       # https://trade.1234567.com.cn/SearchHandler/bi.aspx?callback=jQuery&type=billtrade&qkt=91b4e48755424a9bb0813eaaeac1895c&ttype=month&year=2019&data=10&_=1572521296742
       # 历史分红明细
       # https://trade.1234567.com.cn/SearchHandler/bi.aspx?callback=jQuery&type=billdivid&qkt=91b4e48755424a9bb0813eaaeac1895c&ttype=month&year=2019&data=10&_=1572521296745
        headers=    \
        {   \
            u"Cookie": u"st_si=16011911173883; st_asi=delete; ASP.NET_SessionId=hrum14ihhpbovjfdoimkovkt; st_pvi=58108632980853; st_sp=2019-10-29%2016%3A44%3A03; st_inirUrl=http%3A%2F%2F1234567.com.cn%2F; st_sn=21; st_psi=2019103119250883-112200304021-9130734151; cp_token=aecf69d2ddac4b519747842c734d1f98; FundTradeLoginUser=XUtRAsGHSPA7Lw8NXRs3A49NTPYbWU7hK29AS8E1YDixUHhxXWRDXGDKnrmuDRuQSQBgvL1Z; fund_trade_cn=XcADDx92EzCREoPfXD4blNO59MIEsPp/nwxeWi2Wdlbu/Fx8TsLXOZPSSEa7FYTJi2n7ydHuvM3TqfKaQLdrDRde339tuBRkXdQRqcPpkBqo1Xfi8pM=; fund_trade_name=Xgnl49mOXPrDCDLLcIs3/v+XyiSb9ZVQfILwSADeSyVeKH15n1FesVDvuru2Gf1QuZxmDmO8; fund_trade_visitor=XJD6aZOHYPFS4GX9bPs3SMNGdcxb5ZCFsSfUSXhlAV8czHCIqPPqV6DJCDr/qBjQ3FIrJCub; fund_trade_risk=X8LOdYqu+P3RzkUj3hsvLwKvyR3bGv/fZe5+SAi+N3Cr8H4//LGu9KDtmhvDRuWQFivtbPEm; fund_trade_gps=6; VipLevel=1; TradeLoginToken=1fb6307062b94e0ca4f1ab30e3c5c973; UTOKEN=XcADDx92EzCREoPfXD4blNO59MIEsPp/nwxeWi2Wdlbu/Fx8TsLXOZPSSEa7FYTJi2n7yPHCF/npR6dvNRoeDlwJ4brkvoqVFmQpnzxNjtqCy6hMiYw=; LToken=14459a840a80453b92d3f4b778b0b927; fund_trade_trackid=S2J2HJWCgowuSym5Ce07E0Top0/CIwHeNElm+tRdRfCtD5UtWrbeJrgKBBhKVJzNT+K1c8tPcozw5GUgW4JDEg==; FundTradeLoginTab=0; FundTradeLoginCard=0; b_pl_bq=91b4e48755424a9bb0813eaaeac1895c", \
            u"Referer": u"https://trade.1234567.com.cn/Query/bill?spm=S", \
            u"User-Agent": u"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36", \
        }
        response = requests.get(self.url, headers = headers)
        regex = re.compile('jQuery\((.*?)\);')
        rawjsonData = regex.findall(response.text)
        print(rawjsonData[0])
        data = json.loads(rawjsonData[0])
        with open('data.json','w',encoding='utf-8') as file:
           file.write(json.dumps(data, ensure_ascii=False, sort_keys = True, indent = 4, separators=(',', ':')))
        
if __name__ == '__main__':
    s = ttSpider()