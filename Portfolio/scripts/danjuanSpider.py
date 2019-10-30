# -*- coding: utf-8 -*-

import os
import json
import requests

from config.cookieConfig import cookieConfig
from config.pathManager import pathManager

class danjuanSpider:
    
    # 初始化构造函数
    def __init__(self, strategy = 'a'):
        self.url = u'https://danjuanapp.com/djapi/holding/plan/CSI666'
        self.strategy = strategy
        if strategy == 'a':
            self.pm = pathManager(strategyName='康力泉')
        elif strategy == 'b':
            self.pm = pathManager(strategyName='父母')

    def fetchWithCookie(self,name,cookie):
        headers={
        'Cookie': cookie,
        'User-Agent':'Mozilla/5.0(Macintosh;intel Mac OS 10_11_4)Applewebkit/537.36(KHTML,like Gecko)Chrome/52.0.2743.116 Safari/537.36'
        }
        response = requests.get(self.url, headers = headers)
        pm = pathManager()
        with open(os.path.join(self.pm.outputPath,u'danjuan_{}.txt'.format(name)),'w',encoding='utf-8') as f:
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
    spider = danjuanSpider()
    cookie = cookieConfig()
    Cookies = {}
    # 康力泉 Cookie
    Cookies['kangliquan'] = cookie.danjuanCookieKLQ
    # 老妈 Cookie
    Cookies['mother'] = cookie.danjuanCookieMother
    # 老爸 Cookie
    Cookies['father'] = cookie.danjuanCookieFather

    spider.fetchWithCookie(name=u'螺丝钉定投', cookie=Cookies['kangliquan'])
    spider.fetchWithCookie(name=u'李淑云', cookie=Cookies['mother'])
    spider.fetchWithCookie(name=u'康世海', cookie=Cookies['father'])