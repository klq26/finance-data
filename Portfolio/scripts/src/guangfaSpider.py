# -*- coding: utf-8 -*-

import os
import requests
import json

from config.cookieConfig import cookieConfig
from config.pathManager import pathManager

class guangfaSpider:
    
    # 初始化构造函数
    def __init__(self):
        # 注意；这些请求需要从未登录状态，一路点详情进入具体页面才会发送，否则追踪不到
        #self.url = u'https://trade.gffunds.com.cn/mapi/acco_hold_detail?fund_code=001064'
        #self.url = u'https://trade.gffunds.com.cn/mapi/account/assets/position-gains?tttt=0.7061572339183033'
        self.url = u'https://trade.gffunds.com.cn/mapi/account/assets/position-gains?tttt=0.5490600043154694'

    def fetchWithCookie(self,name,cookie):
        headers={
        'Cookie': cookie,
        'GFF-Charset': 'UTF-8', # 建议参数，否则字符不正确
        'GFF-NetNo': '9999',    # 必须参数，否则无法返回数据
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
        }
        response = requests.get(self.url, headers = headers)
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
                            f.write(u'\t'.join(seq) + '\n')
                            break
                    break
                print('\n')

if __name__ == '__main__':
    spider = guangfaSpider()
    cookie = cookieConfig()
    Cookies = {}

    # 复制 Chrome 的 UA 可用正则“^(.*?): (.*?)$” 替换成 “'\1': '\2',” 就可以
    # http://www.gffunds.com.cn/

    # 康力泉 Cookie
    Cookies['kangliquan'] = cookie.guangfaCookie

    spider.fetchWithCookie(name=u'支付宝', cookie=Cookies['kangliquan'])