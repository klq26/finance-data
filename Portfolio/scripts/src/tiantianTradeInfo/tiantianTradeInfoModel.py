# -*- coding: utf-8 -*-

class tiantianTradeInfoModel:

    def __init__(self, data=None):
        self.date = ''
        self.name = ''
        self.code = ''
        self.operate = ''
        self.cost = ''
        self.costUnit = ''
        self.gain = ''
        self.gainUnit = ''
        self.url = ''
        if data:
            self.__dict__ = data

    def __str__(self):
        seq = u'\t'.join((self.date, self.name, self.code, self.operate, self.cost, self.costUnit, self.gain, self.gainUnit, self.url))
        return seq
        
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self,key,value)