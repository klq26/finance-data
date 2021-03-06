# -*- coding: utf-8 -*-
import os
import time

class pathManager:

    def __init__(self,strategyName=u'康力泉'):
        # 当前目录
        currentDir = os.path.abspath(os.path.dirname(__file__))
        
        # 父目录（.\src)
        self.parentDir = os.path.dirname(currentDir)
        # 输入路径
        self.inputPath = os.path.join(os.path.dirname(self.parentDir), u'input')
        # 工具路径
        self.toolsPath = os.path.join(self.parentDir, u'tools')
        # 爬虫路径
        self.spiderPath = os.path.join(self.parentDir, u'spider')
        #if not os.path.exists(self.inputPath):
        #    os.makedirs(self.inputPath)
        # 持仓数据输出路径
        self.holdingOutputPath = os.path.join(os.path.dirname(self.parentDir), u'output',time.strftime("%Y%m", time.localtime()), strategyName)
        if not os.path.exists(self.holdingOutputPath):
            os.makedirs(self.holdingOutputPath)
        # 公共输出路径
        self.outputPath = os.path.join(os.path.dirname(self.parentDir), u'output')
        # 公共输出路径
        # 配置文件路径
        self.configPath = os.path.join(self.parentDir, u'config')
        #if not os.path.exists(self.configPath):
        #    os.makedirs(self.configPath)
        # echarts 的 data.js 文件路径
        self.echartsPath = os.path.join(self.parentDir,'echarts')
        # 测试路径
        #print(currentDir, self.parentDir,self.inputPath, self.toolsPath, self.spiderPath,self.outputPath,self.echartsPath, sep='\n')

if __name__ == "__main__":
    pathManager()