# -*- coding: utf-8 -*-

class fundModel:   
    """
    基金对象模型
    """
    def __init__(self,data = None):
        self.fundCode = u'000000'
        self.fundName = u'默认名称'
        self.holdNetValue = 0.0000          # 持仓成本
        self.holdShareCount = 0.00          # 持仓份额
        self.holdMarketCap = 0.00           # 持仓市值
        self.holdTotalGain = 0.0            # 持仓盈亏
        self.currentNetValue = 0.0000       # 当前净值
        self.currentNetValueDate = ''       # 当前净值日期
        self.estimateNetValue = 0.0000      # 估算净值
        self.estimateRate = 0.0000          # 估算涨跌幅
        self.estimateTime = u'估算时间'     # 估算时间
        self.category1 = ''
        self.category1 = ''
        self.category2 = ''
        self.category3 = ''
        self.category4 = ''
        self.appSource = u'默认来源'
        # 支持了一个简易的 json 字符串转 fundModel 对象的逻辑
        if data:
            self.__dict__ = data
    
    def __str__(self):
        """
        输出对象
        """
        seq = (self.fundName,self.fundCode,str(self.holdNetValue),str(self.holdShareCount),str(self.holdMarketCap),str(self.holdTotalGain),str(self.currentNetValue),str(self.estimateNetValue),u'{0}%'.format(round(self.estimateRate * 100,2)),str(round((self.estimateNetValue - self.currentNetValue)*self.holdShareCount,2)),str(self.estimateTime))
        return u'\t'.join(seq)
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self,key,value)