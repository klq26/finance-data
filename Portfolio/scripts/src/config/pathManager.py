# -*- coding: utf-8 -*-
import os
import time

class pathManager:

    def __init__(self,strategyName=u'康力泉'):
        # 当前目录
        currentDir = os.path.abspath(os.path.dirname(__file__))
        # 父目录（.\src)
        parentDir = os.path.dirname(currentDir)
        # 输入路径
        self.inputPath = os.path.join(os.path.dirname(parentDir), u'input')
        #if not os.path.exists(self.inputPath):
        #    os.makedirs(self.inputPath)
        # 持仓数据输出路径
        self.holdingOutputPath = os.path.join(os.path.dirname(parentDir), u'output',time.strftime("%Y%m", time.localtime()), strategyName)
        if not os.path.exists(self.holdingOutputPath):
            os.makedirs(self.holdingOutputPath)
        # 公共输出路径
        self.outputPath = os.path.join(os.path.dirname(parentDir), u'output')
        # 公共输出路径
        # 配置文件路径
        self.configPath = os.path.join(parentDir, u'config')
        #if not os.path.exists(self.configPath):
        #    os.makedirs(self.configPath)
        # echarts 的 data.js 文件路径
        self.echartsPath = os.path.join(parentDir,'echarts')
        #if not os.path.exists(self.echartsPath):
        #    os.makedirs(self.echartsPath)
        #print(self.inputPath)
        #print(self.holdingOutputPath)
        #print(self.configPath)
        #print(self.echartsPath)
        

if __name__ == "__main__":
    pathManager()