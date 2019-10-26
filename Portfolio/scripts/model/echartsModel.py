# -*- coding: utf-8 -*-

import json



class echartsModel:   
    """
    echarts 库资产旭日图对象模型
    """
    def __init__(self):
        self.name = ''		# A股 , 48.34%
        self.value = ''		# 48.34 注意不是 0.4834
        self.itemStyle = {}	# "color": "#0aa3b5"
        self.children = []	# list(echartModel)
        
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self,key,value)

