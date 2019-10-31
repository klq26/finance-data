# -*- coding: utf-8 -*-

import os
import sys
import shutil
import json
import requests
import subprocess

from config.cookieConfig import cookieConfig
from config.pathManager import pathManager

from tiantianSpider import tiantianSpider
from guangfaSpider import guangfaSpider
from qiemanSpider import qiemanSpider
from huataiSpider import huataiSpider
from danjuanSpider import danjuanSpider

class allFundSpider:
    def __init__(self):
        self.strategy = ''

    def doFetchKLQ(self):
        cookie = cookieConfig()
        
        tt = tiantianSpider()
        tt.fetchWithCookie(name=u'康力泉', cookie=cookie.tiantianCookieKLQ)
        gf = guangfaSpider()
        gf.fetchWithCookie(name=u'支付宝', cookie=cookie.guangfaCookie)
        qm = qiemanSpider()
        qm.fetchWithCookie(name=u'10万补充ETF计划',url=qm.urlForPlan150)
        qm.fetchWithCookie(name=u'我的S定投计划',url=qm.urlForPlanS)
        ht = huataiSpider()
        ht.dataFormat()
        dj = danjuanSpider()
        dj.fetchWithCookie(name=u'螺丝钉定投', cookie=cookie.danjuanCookieKLQ)
        # 拷贝文件
        fileNameExt = u'康力泉'
        self.pm = pathManager(strategyName=fileNameExt)
        fileName = u'cash_{0}.txt'.format(fileNameExt)
        shutil.copy(os.path.join(self.pm.inputPath,fileName),os.path.join(self.pm.holdingOutputPath,fileName))
        fileName = u'freeze_{0}.txt'.format(fileNameExt)
        shutil.copy(os.path.join(self.pm.inputPath,fileName),os.path.join(self.pm.holdingOutputPath,fileName))
    
    def doFetchParent(self):
        cookie = cookieConfig()
        
        tt = tiantianSpider('b')
        tt.fetchWithCookie(name=u'李淑云', cookie=cookie.tiantianCookieMother)
        dj = danjuanSpider('b')
        dj.fetchWithCookie(name=u'李淑云', cookie=cookie.danjuanCookieMother)
        dj.fetchWithCookie(name=u'康世海', cookie=cookie.danjuanCookieFather)
        
if __name__ == '__main__':
    strategy = 'a'
    if len(sys.argv) >= 2:
        #print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：父母')
        strategy = sys.argv[1]
    spider = allFundSpider()
    if strategy == 'a':
        spider.doFetchKLQ()
        os.startfile(spider.pm.holdingOutputPath)
    elif strategy == 'b':
        spider.doFetchParent()
        os.startfile(spider.pm.holdingOutputPath)
    elif strategy == 'debug':
        print('debug')
    else:
        print('[ERROR] 无法识别的参数：{0}'.format(strategy))