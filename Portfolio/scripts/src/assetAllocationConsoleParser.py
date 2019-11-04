# -*- coding: utf-8 -*-
import os
import json
# for reduce method of lambda
from functools import reduce
# groupby & itemgetter
from itertools import groupby
from operator import itemgetter
# pretty table output
from prettytable import PrettyTable
# model
from model.assetModel import assetModel
from model.echartsModel import echartsModel
# config
from config.assetCategoryConstants import assetCategoryConstants

class assetAllocationConsoleParser:

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
        allMarketCaps = [x.holdMarketCap for x in modelArray]
        totalMarketCap = reduce(lambda x,y: x+y, allMarketCaps)
        # 总盈亏
        allTotalGains = [x.holdTotalGain for x in modelArray]
        totalGain = reduce(lambda x,y: x+y, allTotalGains)
        # 总投资额
        allInvest = self.beautify(totalMarketCap - totalGain)
        print(u'\n总投入：{0}'.format(allInvest))
        print(u'总盈亏：{0}'.format(self.beautify(totalGain)))
        print(u'总市值：{0}'.format(self.beautify(totalMarketCap)))
        print(u'组合收益率：{0}%'.format(self.beautify(totalGain/allInvest * 100)))
        print('\n一级分类：\n')
        tb = PrettyTable()
        tb.field_names = [u"名称", u"分类市值", u"占比", u"盈亏（元）", u"盈亏占比"]
        for category in self.category1Array:
            marketCaps = [x.holdMarketCap for x in modelArray if x.category1 == category]
            # 有些组合没有部分一级分类，应该忽略该级别的循环
            if len(marketCaps) == 0:
                continue
            marketCap = reduce(lambda x,y: x+y, marketCaps)
            
            totalGains = [x.holdTotalGain for x in modelArray if x.category1 == category]
            gain = reduce(lambda x,y: x+y, totalGains)
            
            #print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}\t占比：{4}%'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain), self.beautify(gain / totalGain * 100)))
            # prettytable 输出
            tb.add_row([category, self.beautify(marketCap), u'{0}%'.format(self.beautify(marketCap / totalMarketCap * 100)), self.beautify(gain), u'{0}%'.format(self.beautify(gain / totalGain * 100))])
        print(tb)
        print('\n二级分类：\n')
        tb = PrettyTable()
        tb.field_names = [u"名称", u"分类市值", u"占比", u"盈亏（元）", u"盈亏占比"]
        for category in self.category2Array:
            #print(category)
            marketCaps = [x.holdMarketCap for x in modelArray if x.category2 == category]
            # 有些组合没有部分二级分类，应该忽略该级别的循环
            if len(marketCaps) == 0:
                continue
            marketCap = reduce(lambda x,y: x+y, marketCaps)
            
            totalGains = [x.holdTotalGain for x in modelArray if x.category2 == category]
            gain = reduce(lambda x,y: x+y, totalGains)
            
            #print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}\t占比：{4}%'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain), self.beautify(gain / totalGain * 100)))
            # prettytable 输出
            tb.add_row([category, self.beautify(marketCap), u'{0}%'.format(self.beautify(marketCap / totalMarketCap * 100)), self.beautify(gain), u'{0}%'.format(self.beautify(gain / totalGain * 100))])
        print(tb)
        print('\n三级分类：\n')
        tb = PrettyTable()
        tb.field_names = [u"名称", u"分类市值", u"占比", u"盈亏（元）", u"盈亏占比"]
        for category in self.category3Array:
            marketCaps = [x.holdMarketCap for x in modelArray if x.category3 == category]
            # 有些组合没有部分三级分类，应该忽略该级别的循环
            if len(marketCaps) == 0:
                continue
            marketCap = reduce(lambda x,y: x+y, marketCaps)
            
            totalGains = [x.holdTotalGain for x in modelArray if x.category3 == category]
            gain = reduce(lambda x,y: x+y, totalGains)
            
            #print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}\t占比：{4}%'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain), self.beautify(gain / totalGain * 100)))
            # prettytable 输出
            tb.add_row([category, self.beautify(marketCap), u'{0}%'.format(self.beautify(marketCap / totalMarketCap * 100)), self.beautify(gain), u'{0}%'.format(self.beautify(gain / totalGain * 100))])
        print(tb)
