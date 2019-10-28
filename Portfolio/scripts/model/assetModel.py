# -*- coding: utf-8 -*-

class assetModel:   
    """
    资产配置统计对象模型
    """
    def __init__(self, data = None):
        self.fundCode = u'000000'
        self.fundName = u'默认名称'
        self.holdNetValue = 0.0000          # 持仓成本
        self.holdShareCount = 0.00          # 持仓份额
        self.holdMarketCap = 0.00           # 持仓市值
        self.holdTotalGain = 0.0            # 持仓盈亏
        self.category1 = ''
        self.category1 = ''
        self.category2 = ''
        self.category3 = ''
        self.category4 = ''
        # 支持了一个简易的 json 字符串转 fundModel 对象的逻辑
        if data:
            self.__dict__ = data

    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self,key,value)