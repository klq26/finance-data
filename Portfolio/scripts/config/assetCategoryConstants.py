# -*- coding: utf-8 -*-

class assetCategoryConstants:   

    def __init__(self):
        """
        从 Excel 贴到 notepad++ 后通过正则表达式替换，可以得到 json 数组
        From：
        ^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$
        To：
        {"code":"\1","category1":"\2","category2":"\3","category3":"\4","category4":"\5"},
        """
        self.category1Array = [u'A 股',u'海外新兴',u'海外成熟',u'债券',u'商品',u'现金',u'冻结资金']
        self.category2Array = [u'大盘股',u'中小盘股',u'红利价值',u'行业股',u'香港',u'海外互联',u'海外成熟',u'国内债券',u'海外债券',u'商品',u'保本理财',u'中等风险理财',u'冻结资金']
        self.category3Array = [u'上证50',u'50AH',u'沪深300',u'300价值',u'基本面60',u'基本面120',u'中小板',u'中证500',u'500低波动',u'中证1000',u'创业板',u'中证红利',u'标普红利',u'养老产业',u'全指医药',u'中证环保',u'中证传媒',u'证券公司',u'金融地产',u'恒生',u'香港中小',u'海外互联网',u'德国30',u'可转债',u'美元债',u'黄金',u'原油',u'货币基金',u'房地产P2P',u'住房公积金',u'无息外借款']