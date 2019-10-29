# -*- coding: utf-8 -*-

import os
import json
import requests
import subprocess

from config.cookieConfig import cookieConfig

from tiantianSpider import tiantianSpider
from guangfaSpider import guangfaSpider
from qiemanSpider import qiemanSpider
from huataiSpider import huataiSpider
from danjuanSpider import danjuanSpider

class allFundSpider:
    def __init__(self):
        print()
        
    def doFetch(self):
        cookie = cookieConfig()
        
        tt = tiantianSpider()
        tt.fetchWithCookie(name=u'康力泉', cookie=cookie.tiantianCookieKLQ)
        #print('tt')
        gf = guangfaSpider()
        gf.fetchWithCookie(name=u'支付宝', cookie=cookie.guangfaCookie)
        #print('gf')
        qm = qiemanSpider()
        qm.fetchWithCookie(name=u'10万补充ETF计划',url=qm.urlForPlan150)
        qm.fetchWithCookie(name=u'我的S定投计划',url=qm.urlForPlanS)
        #print('qm')
        ht = huataiSpider()
        ht.dataFormat()
        #print('ht')
        dj = danjuanSpider()
        dj.fetchWithCookie(name=u'螺丝钉定投', cookie=cookie.danjuanCookieKLQ)
        #print('dj')

if __name__ == '__main__':
    spider = allFundSpider()
    spider.doFetch()