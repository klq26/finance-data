# -*- coding: utf-8 -*-

class indexModel:
    """
    指数
    """
    def __init__(self,data = None):
        self.indexCode = u'000000'
        self.indexName = u'默认名称'
        self.indexArea = u'亚洲'
        self.sequence = 0
        self.current = 0.00
        self.lastClose = 0.00
        self.dealMoney = 0.00
        self.dailyChangValue = 0.00
        self.dailyChangRate = 0.00
        
        # 支持了一个简易的 json 字符串转 indexModel 对象的逻辑
        if data:
            self.__dict__ = data
    
    def __str__(self):
        """
        输出对象
        """
        seq = (self.indexName,self.indexCode,self.indexArea,self.current,self.lastClose,self.dailyChangRate,self.dailyChangValue)
        return u'\t'.join(seq)
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self,key,value)