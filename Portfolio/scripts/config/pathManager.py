# -*- coding: utf-8 -*-
import os
import time

class pathManager:

    def __init__(self):
        # 输入路径
        self.inputPath = os.path.join(os.getcwd(),'..',u'input')
        if not os.path.exists(self.inputPath):
            os.makedirs(self.inputPath)
        # 输出路径
        self.outputPath = os.path.join(os.getcwd(),'..',u'output',time.strftime("%Y%m", time.localtime()))
        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)
        # 配置文件路径
        self.configPath = os.path.join(os.getcwd(),'..',u'config')
        if not os.path.exists(self.configPath):
            os.makedirs(self.configPath)
        # echarts 的 data.js 文件路径
        self.echartsPath = os.path.join(os.getcwd(),'..','..',u'echarts')
        if not os.path.exists(self.echartsPath):
            os.makedirs(self.echartsPath)

if __name__ == "__main__":
    pathManager()