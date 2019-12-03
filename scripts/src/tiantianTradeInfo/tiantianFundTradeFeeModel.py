# -*- coding: utf-8 -*-

class tiantianFundTradeFeeModel:

    def __init__(self, data=None):
        self.name = ''
        self.code = ''
        self.buyFee = ''
        self.sellFee = {}
        if data:
            self.__dict__ = data

    def __str__(self):
        seq = u'\t'.join((self.name, self.code, self.buyFee, self.sellFee))
        return seq
        
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self,key,value)