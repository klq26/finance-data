# -*- coding: utf-8 -*-

# class owner:
#     KLQ  = 1
#     PARENT     = 2
#     NA = -1

# class appSource:
#     HUATAI = 1
#     TIANTIAN = 2
#     QIEMAN = 3
#     DANJUAN = 4
#     ZHIFUBAO = 5
#     FREEZE = 6
#     CASH = 7
#     NA = -1


class accountModel:   
    """
    资产配置统计对象模型
    """
    def __init__(self, data = None):
        self.accountName = u'默认名称'
        self.sortId = 0
        self.owner = u'NA'
        self.appSource = u'NA'
        self.marketCap = 0.00
        self.gain = 0.00
        self.gainRate = 0.00
        self.recommendColor = ''
        # 支持了一个简易的 json 字符串转 model 对象的逻辑
        if data:
            self.__dict__ = data

    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self,key,value)