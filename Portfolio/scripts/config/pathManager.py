# -*- coding: utf-8 -*-
import os
import time

class pathManager:

    def __init__(self,strategyName=u'康力泉'):
        # 当前目录
        currentDir = os.path.abspath(os.path.dirname(__file__))
        # 父目录（.\scripts)
        parentDir = os.path.dirname(currentDir)
        # echarts 路径
        echartsDir = os.path.join(os.path.dirname(parentDir),'echarts')

        # 输入路径
        self.inputPath = os.path.join(parentDir, u'input')
        #if not os.path.exists(self.inputPath):
        #    os.makedirs(self.inputPath)
        # 输出路径
        self.outputPath = os.path.join(parentDir, u'output',time.strftime("%Y%m", time.localtime()), strategyName)
        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)
        # 配置文件路径
        self.configPath = os.path.join(parentDir, u'config')
        #if not os.path.exists(self.configPath):
        #    os.makedirs(self.configPath)
        # echarts 的 data.js 文件路径
        self.echartsPath = echartsDir
        #if not os.path.exists(self.echartsPath):
        #    os.makedirs(self.echartsPath)
        #print(self.inputPath)
        #print(self.outputPath)
        #print(self.configPath)
        #print(self.echartsPath)
        

if __name__ == "__main__":
    pathManager()