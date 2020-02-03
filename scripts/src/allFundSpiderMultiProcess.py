# -*- coding: utf-8 -*-

import os
import sys
import shutil
import json
import requests
import subprocess

from config.pathManager import pathManager

class allFundSpiderMultiProcess:
    def __init__(self):
        self.strategy = ''
        self.klqSpiderArray = ['tiantianSpider.py','guangfaSpider.py','qiemanSpider.py','danjuanSpider.py','huataiSpider.py']
        self.parentSpidersArray = ['tiantianSpider.py','danjuanSpider.py']

    def getKLQ(self):
        fileNameExt = u'康力泉'
        self.pm = pathManager(strategyName=fileNameExt)
        # 多线程并发（都传策略 a）
        for pyFile in self.klqSpiderArray:
            args = [r"powershell","python",os.path.join(self.pm.spiderPath, pyFile),"a"]
            print('[Executing] {0} a...'.format(os.path.join(self.pm.spiderPath, pyFile)))
            p = subprocess.Popen(args)
        # 拷贝文件
        fileName = u'huabao_{0}.txt'.format(fileNameExt)
        shutil.copy(os.path.join(self.pm.inputPath,fileName),os.path.join(self.pm.holdingOutputPath,fileName))
        with open(os.path.join(self.pm.holdingOutputPath,fileName), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                print(line, end='')
        fileName = u'cash_{0}.txt'.format(fileNameExt)
        shutil.copy(os.path.join(self.pm.inputPath,fileName),os.path.join(self.pm.holdingOutputPath,fileName))
        with open(os.path.join(self.pm.holdingOutputPath,fileName), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                print(line, end='')
        fileName = u'freeze_{0}.txt'.format(fileNameExt)
        shutil.copy(os.path.join(self.pm.inputPath,fileName),os.path.join(self.pm.holdingOutputPath,fileName))
        with open(os.path.join(self.pm.holdingOutputPath,fileName), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                print(line, end='')
    
    def getParent(self):
        fileNameExt = u'父母'
        self.pm = pathManager(strategyName=fileNameExt)
        # 多线程并发（都传策略 b）
        for pyFile in self.parentSpidersArray:
            args = [r"powershell","python",os.path.join(self.pm.spiderPath, pyFile),"b"]
            print('[Executing] {0} b...'.format(os.path.join(self.pm.spiderPath, pyFile)))
            p = subprocess.Popen(args)
        # 拷贝文件
        fileName = u'cash_{0}.txt'.format(u'父母')
        shutil.copy(os.path.join(self.pm.inputPath,fileName),os.path.join(self.pm.holdingOutputPath,fileName))
        with open(os.path.join(self.pm.holdingOutputPath,fileName), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                print(line, end='')
        
if __name__ == '__main__':
    strategy = 'a'
    if len(sys.argv) >= 2:
        #print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：父母')
        strategy = sys.argv[1]
    spider = allFundSpiderMultiProcess()
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