# -*- coding: utf-8 -*-
import os
import json
# for reduce method of lambda
from functools import reduce
# groupby & itemgetter
from itertools import groupby
from operator import itemgetter
# model
from model.fundModel import fundModel
from model.echartsModel import echartsModel
# config
from config.assetCategoryConstants import assetCategoryConstants

class assetAllocationInfoCalculator:

    def __init__(self):
        categoryConstants = assetCategoryConstants()
        self.category1Array = categoryConstants.category1Array
        self.category2Array = categoryConstants.category2Array
        self.category3Array = categoryConstants.category3Array
    
    # 格式化浮点数
    def beautify(self,num):
        return round(float(num),2)
    
    def showInfo(self,modelArray):
        # 总市值
        allMarketCaps = [x.marketCap for x in modelArray]
        totalMarketCap = reduce(lambda x,y: x+y, allMarketCaps)
        print(u'总市值：{0}'.format(self.beautify(totalMarketCap)))
        # 总盈亏
        allTotalGains = [x.totalGain for x in modelArray]
        totalGain = reduce(lambda x,y: x+y, allTotalGains)
        print(u'总盈亏：{0}'.format(self.beautify(totalGain)))
        print(u'组合收益率：{0}%'.format(self.beautify(totalGain/totalMarketCap * 100)))
        print('\n一级分类：\n')
        for category in self.category1Array:
            marketCaps = [x.marketCap for x in modelArray if x.category1 == category]
            marketCap = reduce(lambda x,y: x+y, marketCaps)
            
            totalGains = [x.totalGain for x in modelArray if x.category1 == category]
            gain = reduce(lambda x,y: x+y, totalGains)
            
            print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain)))
        print('\n二级分类：\n')
        for category in self.category2Array:
            #print(category)
            marketCaps = [x.marketCap for x in modelArray if x.category2 == category]
            # 有些组合没有部分二级分类，应该忽略该级别的循环
            if len(marketCaps) == 0:
                continue
            marketCap = reduce(lambda x,y: x+y, marketCaps)
            
            totalGains = [x.totalGain for x in modelArray if x.category2 == category]
            gain = reduce(lambda x,y: x+y, totalGains)
            
            print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain)))
        print('\n三级分类：\n')
        for category in self.category3Array:
            marketCaps = [x.marketCap for x in modelArray if x.category3 == category]
            # 有些组合没有部分三级分类，应该忽略该级别的循环
            if len(marketCaps) == 0:
                continue
            marketCap = reduce(lambda x,y: x+y, marketCaps)
            
            totalGains = [x.totalGain for x in modelArray if x.category3 == category]
            gain = reduce(lambda x,y: x+y, totalGains)
            
            print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain)))

