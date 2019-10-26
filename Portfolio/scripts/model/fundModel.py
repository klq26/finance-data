# -*- coding: utf-8 -*-

class fundModel:   
    """
    资产配置统计对象模型
    """
    def __init__(self):
        self.marketCap = 0.0
        self.totalGain = 0.0
        self.category1 = ''
        self.category1 = ''
        self.category2 = ''
        self.category3 = ''
        self.category4 = ''
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    # 不覆盖这个函数无法通过 setattr(object, key, value) 的 key-value 方式为对象赋值
    def __setitem__(self, key, value):
        setattr(self,key,value)