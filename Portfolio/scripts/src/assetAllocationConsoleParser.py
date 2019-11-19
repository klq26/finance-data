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
from config.xueqiuIndexValue import xueqiuIndexValue
# tools
from tools.dingtalk import dingtalk

class assetAllocationConsoleParser:

    def __init__(self):
        categoryConstants = assetCategoryConstants()
        self.category1Array = categoryConstants.category1Array
        self.category2Array = categoryConstants.category2Array
        self.category3Array = categoryConstants.category3Array
        self.xueqiuIndexValue = xueqiuIndexValue()
        self.dingtalk = dingtalk()
    
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
        outStr1 = u'\n总投入：{0}'.format(allInvest)
        outStr2 = u'总盈亏：{0}'.format(self.beautify(totalGain))
        outStr3 = u'总市值：{0}'.format(self.beautify(totalMarketCap))
        outStr4 = u'组合收益率：{0}%'.format(self.beautify(totalGain/allInvest * 100))
        print(outStr1)
        print(outStr2)
        print(outStr3)
        print(outStr4)
        # 给钉钉发消息
        self.dingtalk.sendMessage(f'当前市值情况：\n{outStr1}\n{outStr2}\n{outStr3}\n{outStr4}\n')
        print('\n一级分类：\n')
        tb = PrettyTable()
        tb.field_names = [u"名称", u"分类市值", u"盈亏（元）", u"分类盈亏率", u"组合占比", u"组合盈亏贡献"]
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
            tb.add_row([category, self.beautify(marketCap), self.beautify(gain), u'{0}%'.format(self.beautify(gain/(marketCap - gain)* 100)), u'{0}%'.format(self.beautify(marketCap / totalMarketCap * 100)), u'{0}%'.format(self.beautify(gain / totalGain * 100))])
        print(tb)
        print('\n二级分类：\n')
        tb = PrettyTable()
        tb.field_names = [u"名称", u"分类市值", u"盈亏（元）", u"分类盈亏率", u"组合占比", u"组合盈亏贡献"]
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
            tb.add_row([category, self.beautify(marketCap), self.beautify(gain),u'{0}%'.format(self.beautify(gain/(marketCap - gain) * 100)), u'{0}%'.format(self.beautify(marketCap / totalMarketCap * 100)), u'{0}%'.format(self.beautify(gain / totalGain * 100))])
        print(tb)
        print('\n三级分类：\n')
        tb = PrettyTable()
        tb.field_names = [u"名称", u"分类市值", u"盈亏（元）", u"分类盈亏率", u"组合占比", u"组合盈亏贡献",u'指数成本']
        for category in self.category3Array:
            marketCaps = [x.holdMarketCap for x in modelArray if x.category3 == category]
            # 有些组合没有部分三级分类，应该忽略该级别的循环
            if len(marketCaps) == 0:
                continue
            marketCap = reduce(lambda x,y: x+y, marketCaps)
            
            totalGains = [x.holdTotalGain for x in modelArray if x.category3 == category]
            gain = reduce(lambda x,y: x+y, totalGains)
            # 指数成本（三级分类持仓成本，换算成指数的点数）
            indexValue = 0.0
            for symbol in self.xueqiuIndexValue.indexSymbols:
                if symbol['category3'] == category:
                    indexValue = float(symbol['close']) / (1 + (gain/(marketCap - gain)))
            #print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}\t占比：{4}%'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain), self.beautify(gain / totalGain * 100)))
            # prettytable 输出
            tb.add_row([category, self.beautify(marketCap), self.beautify(gain),u'{0}%'.format(self.beautify(gain/(marketCap - gain) * 100)), u'{0}%'.format(self.beautify(marketCap / totalMarketCap * 100)), u'{0}%'.format(self.beautify(gain / totalGain * 100)),self.beautify(indexValue)])
        print(tb)
