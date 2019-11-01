# -*- coding: utf-8 -*-

import os
import sys
import shutil
import json
import requests
import subprocess

from config.pathManager import pathManager

from tiantianSpider import tiantianSpider
from guangfaSpider import guangfaSpider
from qiemanSpider import qiemanSpider
from huataiSpider import huataiSpider
from danjuanSpider import danjuanSpider

class allFundSpider:
    def __init__(self):
        self.strategy = ''

    def getKLQ(self):
        tt = tiantianSpider()
        tt.getKLQ()
        gf = guangfaSpider()
        gf.getKLQ()
        qm = qiemanSpider()
        qm.getKLQ()
        ht = huataiSpider()
        ht.dataFormat()
        dj = danjuanSpider()
        dj.getKLQ()
        # 拷贝文件
        fileNameExt = u'康力泉'
        self.pm = pathManager(strategyName=fileNameExt)
        fileName = u'cash_{0}.txt'.format(fileNameExt)
        shutil.copy(os.path.join(self.pm.inputPath,fileName),os.path.join(self.pm.holdingOutputPath,fileName))
        fileName = u'freeze_{0}.txt'.format(fileNameExt)
        shutil.copy(os.path.join(self.pm.inputPath,fileName),os.path.join(self.pm.holdingOutputPath,fileName))
    
    def getParent(self):
        fileNameExt = u'父母'
        self.pm = pathManager(strategyName=fileNameExt)
        tt = tiantianSpider('b')
        tt.getLSY()
        dj = danjuanSpider('b')
        dj.getLSY()
        dj.getKSH()
        
if __name__ == '__main__':
    strategy = 'a'
    if len(sys.argv) >= 2:
        #print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：父母')
        strategy = sys.argv[1]
    spider = allFundSpider()
    if strategy == 'a':
        spider.getKLQ()
        os.startfile(spider.pm.holdingOutputPath)
    elif strategy == 'b':
        spider.getParent()
        os.startfile(spider.pm.holdingOutputPath)
    elif strategy == 'debug':
        print('debug')
    else:
        print('[ERROR] 无法识别的参数：{0}'.format(strategy))