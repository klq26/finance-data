# -*- coding: utf-8 -*-
import os
import sys
import json
import shutil
from datetime import datetime
# for reduce method of lambda
from functools import reduce
# groupby & itemgetter
from itertools import groupby
from operator import itemgetter
import pandas as pd
# pretty table output
from prettytable import PrettyTable
# html template
import jinja2
from jinja2 import Environment, FileSystemLoader
# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
sys.path.append(srcDir)
# model
from model.assetModel import assetModel
from model.echartsModel import echartsModel
# config
from config.assetCategoryConstants import assetCategoryConstants
from config.indexValueInfo import indexValueInfo
from config.pathManager import pathManager
from config.historyProfitManager import  historyProfitManager
from config.colorConstants import colorConstants
# tools
from tools.dingtalk import dingtalk

class assetAllocationCategorySumParser:

    def __init__(self,path):
        self.pm = pathManager()
        self.colorConstants = colorConstants()
        categoryConstants = assetCategoryConstants()
        self.category1Array = categoryConstants.category1Array
        self.category2Array = categoryConstants.category2Array
        self.category3Array = categoryConstants.category3Array
        self.indexValueInfo = indexValueInfo()
        self.historyManager = historyProfitManager()
        self.dingtalk = dingtalk()
        self.outputPath = path
    
    # 格式化浮点数
    def beautify(self,num):
        return round(float(num),2)
    
    # 根据涨跌，返回颜色
    def getGainColor(self,value):
        # http://www.yuangongju.com/color
        changeValueColor = '#DD2200'
        if value >= 0:
            # 221,34,0
            changeValueColor = '#DD2200'
        else:
            # 0,153,51
            changeValueColor = '#009933'
        return changeValueColor
    
    def showInfo(self,modelArray, history_df):
        # jinja2
        category1Items = []
        category2Items = []
        category3Items = []
        # 总市值
        allMarketCaps = [x.holdMarketCap for x in modelArray]
        totalMarketCap = reduce(lambda x,y: x+y, allMarketCaps)
        # 总盈亏
        allTotalGains = [x.holdTotalGain for x in modelArray]
        totalGain = reduce(lambda x,y: x+y, allTotalGains)
        # 总投资额
        allInvest = self.beautify(totalMarketCap - totalGain)
        # 历史盈亏
        totalHistoryGain = self.beautify(self.historyManager.history_df.累计盈亏.sum())
        outStr0 = u'{0}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        outStr1 = u'\n总投入：{0}'.format(allInvest)
        outStr2 = u'持仓盈亏：{0}\n历史盈亏：{1}\n总盈亏：{2}'.format(self.beautify(totalGain),totalHistoryGain,self.beautify(totalHistoryGain + totalGain))
        outStr3 = u'总市值：{0}'.format(self.beautify(totalMarketCap))
        outStr4 = u'持仓收益率：{0}%\n累计收益率：{1}%'.format(self.beautify(totalGain/(totalMarketCap - totalGain) * 100),self.beautify(self.beautify(totalHistoryGain + totalGain)/(totalMarketCap - (totalHistoryGain + totalGain)) * 100))
        print(outStr0)
        print(outStr1)
        print(outStr2)
        print(outStr3)
        print(outStr4)
        # 给钉钉发消息
        self.dingtalk.sendMessage(f'{outStr0}\n当前市值情况：\n{outStr1}\n{outStr2}\n{outStr3}\n{outStr4}')
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

            # prettytable 输出
            gainRate = 0
            if marketCap - gain <= 0:
                gainRate = 0
            else:
                gainRate = gain/(marketCap - gain)* 100
            tb.add_row([category, self.beautify(marketCap), self.beautify(gain), u'{0}%'.format(self.beautify(gainRate)), u'{0}%'.format(self.beautify(marketCap / totalMarketCap * 100)), u'{0}%'.format(self.beautify(gain / totalGain * 100))])
            category1Item = {}
            category1Item['categoryName'] = str(category)
            category1Item['holdMarketCap'] = u'{0:.2f}'.format(self.beautify(marketCap))
            category1Item['holdTotalGain'] = u'{0:.2f}'.format(self.beautify(gain))
            category1Item['holdTotalGainRate'] = u'{0:.2f}%'.format(self.beautify(gainRate))
            category1Item['portfolioPercent'] = u'{0:.2f}%'.format(self.beautify(marketCap / totalMarketCap * 100))
            category1Item['portfolioGainContribute'] = u'{0:.2f}%'.format(self.beautify(gain / totalGain * 100))
            # color
            category1Item['color'] = self.colorConstants.colorForCategory1(category)
            category1Item['holdTotalGainColor'] = self.getGainColor(gain)
            category1Item['holdTotalGainRateColor'] = self.getGainColor(gainRate)
            category1Item['portfolioGainContributeColor'] = self.getGainColor(gain / totalGain * 100)
            category1Items.append(category1Item)
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
            
            category1 = [x.category1 for x in modelArray if x.category2 == category][0]

            #print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}\t占比：{4}%'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain), self.beautify(gain / totalGain * 100)))
            # prettytable 输出
            gainRate = 0
            if marketCap - gain <= 0:
                gainRate = 0
            else:
                gainRate = gain/(marketCap - gain)* 100
            tb.add_row([category, self.beautify(marketCap), self.beautify(gain),u'{0}%'.format(self.beautify(gainRate)), u'{0}%'.format(self.beautify(marketCap / totalMarketCap * 100)), u'{0}%'.format(self.beautify(gain / totalGain * 100))])
            category2Item = {}
            category2Item['categoryName'] = category
            category2Item['holdMarketCap'] = u'{0:.2f}'.format(self.beautify(marketCap))
            category2Item['holdTotalGain'] = u'{0:.2f}'.format(self.beautify(gain))
            category2Item['holdTotalGainRate'] = u'{0:.2f}%'.format(self.beautify(gainRate))
            category2Item['portfolioPercent'] = u'{0:.2f}%'.format(self.beautify(marketCap / totalMarketCap * 100))
            category2Item['portfolioGainContribute'] = u'{0:.2f}%'.format(self.beautify(gain / totalGain * 100))
            # color
            category2Item['color'] = self.colorConstants.colorForCategory1(category1)
            category2Item['holdTotalGainColor'] = self.getGainColor(gain)
            category2Item['holdTotalGainRateColor'] = self.getGainColor(gainRate)
            category2Item['portfolioGainContributeColor'] = self.getGainColor(gain / totalGain * 100)
            category2Items.append(category2Item)
        print(tb)
        print('\n三级分类：\n')
        tb = PrettyTable()
        tb.field_names = [u"名称", u'指数成本', u'指数点位',u'持仓 pe',u'持仓 pb',u'指数 roe', u"分类市值", u"持仓盈亏", u'历史盈亏', u'总盈亏', u"持仓收益率", u"组合占比", u"组合盈亏贡献"]
        # 三级分类同时负责更新 indexHoldingInfos.json
        indexHoldingInfos = list()
        with open(os.path.join(self.pm.configPath,'indexHoldingInfo.json'),u'r',encoding='utf-8') as f:
            indexHoldingInfos = json.loads(f.read())
        
        for category in self.category3Array:
            marketCaps = [x.holdMarketCap for x in modelArray if x.category3 == category]
            # 有些组合没有部分三级分类，应该忽略该级别的循环
            if len(marketCaps) == 0:
                continue
            marketCap = reduce(lambda x,y: x+y, marketCaps)
            for x in indexHoldingInfos:
                if x['name'] == category:
                    x['holding'] = round(marketCap,2)
            totalGains = [x.holdTotalGain for x in modelArray if x.category3 == category]
            gain = reduce(lambda x,y: x+y, totalGains)

            category1 = [x.category1 for x in modelArray if x.category3 == category][0]
            # 指数成本（三级分类持仓成本，换算成指数的点数）
            indexValue = 0.0
            holdingIndexValue = 0.0
            peValue = 0.0
            pbValue = 0.0
            roeValue = 0.0
            historyGain = 0.0
            for symbol in self.indexValueInfo.indexValueInfoList:
                if symbol['category3'] == category:
                    indexValue = float(symbol['result']['close'])
                    holdingIndexValue = float(symbol['result']['close']) / (1 + (gain/(marketCap - gain)))
                    peValue = float(symbol['result']['pe']) / (1 + (gain/(marketCap - gain)))
                    pbValue = float(symbol['result']['pb']) / (1 + (gain/(marketCap - gain)))
                    roeValue =  float(symbol['result']['roe']) * 100
            historyGain = history_df[history_df['三级分类'] == category].累计盈亏.sum()
            #print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}\t占比：{4}%'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain), self.beautify(gain / totalGain * 100)))
            # prettytable 输出
            gainRate = 0
            if marketCap - gain <= 0:
                gainRate = 0
            else:
                gainRate = gain/(marketCap - gain)* 100
            tb.add_row([category, u'{0:.2f}'.format(self.beautify(holdingIndexValue)), u'{0:.2f}'.format(self.beautify(indexValue)), u'{0:.2f}'.format(self.beautify(peValue)), u'{0:.2f}'.format(self.beautify(pbValue)), u'{0:.2f}%'.format(self.beautify(roeValue)), self.beautify(marketCap), u'{0:.2f}'.format(self.beautify(gain)), u'{0:.2f}'.format(self.beautify(historyGain)), u'{0:.2f}'.format(self.beautify(gain + historyGain)), u'{0}%'.format(self.beautify(gainRate)), u'{0}%'.format(self.beautify(marketCap / totalMarketCap * 100)), u'{0}%'.format(self.beautify(gain / totalGain * 100))])
            category3Item = {}
            category3Item['categoryName'] = str(category)
            
            category3Item['indexHoldingValue'] = u'{0:.2f}'.format(self.beautify(holdingIndexValue))
            category3Item['indexValue'] = u'{0:.2f}'.format(self.beautify(indexValue))
            category3Item['pe'] = u'{0:.2f}'.format(self.beautify(peValue))
            category3Item['pb'] = u'{0:.2f}'.format(self.beautify(pbValue))
            category3Item['roe'] = u'{0:.2f}%'.format(self.beautify(roeValue))
            category3Item['holdMarketCap'] =  u'{0:.2f}'.format(self.beautify(marketCap))
            category3Item['holdTotalGain'] =  u'{0:.2f}'.format(self.beautify(gain))
            category3Item['holdHistoryGain'] =  u'{0:.2f}'.format(self.beautify(historyGain))
            category3Item['holdEntireGain'] = u'{0:.2f}'.format(self.beautify(gain + historyGain))
            category3Item['holdTotalGainRate'] = u'{0:.2f}%'.format(self.beautify(gainRate))
            category3Item['portfolioPercent'] = u'{0:.2f}%'.format(self.beautify(marketCap / totalMarketCap * 100))
            category3Item['portfolioGainContribute'] = u'{0:.2f}%'.format(self.beautify(gain / totalGain * 100))
            # color
            category3Item['color'] = self.colorConstants.colorForCategory1(category1)
            category3Item['indexHoldingValueColor'] = self.getGainColor(indexValue - holdingIndexValue)
            category3Item['holdTotalGainColor'] = self.getGainColor(gain)
            category3Item['holdHistoryGainColor'] = self.getGainColor(historyGain)
            category3Item['holdEntireGainColor'] = self.getGainColor(gain + historyGain)
            category3Item['holdTotalGainRateColor'] = self.getGainColor(gainRate)
            category3Item['portfolioGainContributeColor'] = self.getGainColor(gain / totalGain * 100)
            category3Items.append(category3Item)
        print(tb)
        with open(os.path.join(self.pm.configPath,'indexHoldingInfo.json'),u'w',encoding='utf-8') as f:
            f.write(json.dumps(indexHoldingInfos, ensure_ascii=False, sort_keys = True, indent = 4, separators=(',', ':')))
        # jinja2 框架输出 html
        env = Environment(loader=FileSystemLoader(
            os.path.join(self.pm.parentDir, u'template')))
        template = env.get_template(u'资产分类template.html')
        with open(os.path.join(self.outputPath,u'资产配置分类情况.html'), 'w+', encoding=u'utf-8') as fout:
            htmlCode = template.render(category1Items = category1Items, category2Items = category2Items, category3Items = category3Items)
            fout.write(htmlCode)
        if sys.platform.startswith('win'):
            os.startfile(os.path.join(self.outputPath,u'资产配置分类情况.html'))
        elif sys.platform.startswith('linux'):
            shutil.copy(os.path.join(self.outputPath,u'资产配置分类情况.html'), '/var/www/html/assetCategory.html')
            self.dingtalk.sendMessage(f'账户：http://112.125.25.230/assetCategory.html')
            print('资产配置分类情况：http://112.125.25.230/assetCategory.html')

if __name__ == "__main__":
    print(__name__)
    historyManager = historyProfitManager()
    history_df = historyManager.history_df
    # 读取文件
    assetJsonPath = os.path.join(r'D:\github\finance-data\scripts\output\201912\全家', u'全家整体asset.json')
    with open(assetJsonPath,'r',encoding=u'utf-8') as assetJsonFile:
        contentList = json.loads(assetJsonFile.read(),object_hook=assetModel)
        assetModelArray = contentList
    t = assetAllocationCategorySumParser(path = os.getcwd())
    t.showInfo(assetModelArray, history_df)