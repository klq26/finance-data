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
# output
from echartsJson import echartsJson

class calculateFundCategoryData:

    def __init__(self):
        print()
        self.category1Array = [u'A 股',u'海外新兴',u'海外成熟',u'债券',u'商品'] # ,u'现金类'
        self.category2Array = [u'大盘股',u'中小盘股',u'红利价值',u'行业股',u'香港',u'海外互联',u'海外成熟',u'国内债券',u'海外债券',u'商品'] # ,u'保本理财'
        self.category3Array = [u'上证50',u'50AH',u'沪深300',u'300价值',u'基本面60',u'基本面120',u'中小板',u'中证500',u'500低波动',u'中证1000',u'创业板',u'中证红利',u'标普红利',u'养老产业',u'全指医药',u'中证环保',u'中证传媒',u'证券公司',u'金融地产',u'恒生',u'香港中小',u'海外互联网',u'德国30',u'可转债',u'美元债',u'黄金',u'原油']
    
    # 格式化浮点数
    def beautify(self,num):
        return round(float(num),2)
    
    def calculate(self,modelArray):
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
            marketCaps = [x.marketCap for x in modelArray if x.category2 == category]
            marketCap = reduce(lambda x,y: x+y, marketCaps)
            
            totalGains = [x.totalGain for x in modelArray if x.category2 == category]
            gain = reduce(lambda x,y: x+y, totalGains)
            
            print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain)))
        print('\n三级分类：\n')
        for category in self.category3Array:
            marketCaps = [x.marketCap for x in modelArray if x.category3 == category]
            marketCap = reduce(lambda x,y: x+y, marketCaps)
            
            totalGains = [x.totalGain for x in modelArray if x.category3 == category]
            gain = reduce(lambda x,y: x+y, totalGains)
            
            print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain)))

    def colorForCategory1(self,category1):
        #self.category1Array = [u'A 股',u'海外新兴',u'海外成熟',u'债券',u'商品']
        
        # js code
        #var aStockColor = {color: '#0aa3b5'};			// A 股（大盘股，中小盘股，红利价值，行业股）
        #var outSideNewColor = {color: '#187a2f'};		// 海外新兴（香港，海外互联网）
        #var outSideMatureColor = {color: '#ebb40f'};	// 海外成熟（德国）
        #var universalGoodsColor = {color: '#dd4c51'};	// 商品（黄金，白银，原油）
        #var bondColor = {color: '#be8663'};				// 债券（可转债，美元债）
        #var cashColor = {color: '#f7a128'};				// 低风险理财（货币基金，地产项目）
        #var frozenCashColor = {color: '#8b8c90'};		// 冻结资金（公积金）
        
        if category1 == self.category1Array[0]:
            return '#0AA3B5'
        elif category1 == self.category1Array[1]:
            return '#187A2F'
        elif category1 == self.category1Array[2]:
            return '#EBB40F'
        elif category1 == self.category1Array[3]:
            return '#BE8663'
        elif category1 == self.category1Array[4]:
            return '#DD4C51'
        else:
            return 'FFFFFF'
            
    def generateEchartsJson(self,modelArray):
        # 内部排序函数，按 category id 升序排列
        #def fundModelSortFunc(item):
        #    return item.category4
        # 排序
        #modelArray.sort(key=fundModelSortFunc)
        # 按对象的 category4 字段升序排序
        modelArray.sort(key=itemgetter('category4'))
        # 资产配置总市值
        totalMarketCap = 0.0
        for item in modelArray:
            totalMarketCap = totalMarketCap + item.marketCap
            #print(item.__dict__)
        totalMarketCap = self.beautify(totalMarketCap)
        #print(totalMarketCap)
        
        echarts = []
        
        # 树形结构化
        for category in self.category1Array:
            category1Models = [x for x in modelArray if x.category1 == category]
            # 一级分类
            print(category)
            # echarts 模型
            echart1 = echartsModel()
            echart1.name = category
            echart1.value = 0.0
            echart1.itemStyle['color'] = self.colorForCategory1(category)
            for category2, category2Array in groupby(category1Models,key=itemgetter('category2')):
                # 二级分类
                #print('-',category2)
                # echarts 模型
                echart2 = echartsModel()
                echart2.name = category2
                echart2.value = 0.0
                echart2.itemStyle['color'] = echart1.itemStyle['color']
                for category3, category3Array in groupby(category2Array,key=itemgetter('category3')):
                    # 三级分类
                    #print('--',category3)
                    # echarts 模型
                    echart3 = echartsModel()
                    echart3.name = category3
                    echart3.value = 0.0
                    echart3.itemStyle['color'] = echart1.itemStyle['color']
                    for model in category3Array:
                        #print('----- {0}'.format(model.__dict__))
                        echart3.value = echart3.value + round(float(model.marketCap),2)
                    echart2.value = echart2.value + echart3.value   # 变成百分比之前，存入上级分类，下同
                    echart3.value = round(float(echart3.value / totalMarketCap * 100),2)
                    echart2.children.append(echart3.__dict__)
                echart1.value = echart1.value + echart2.value   # 变成百分比之前，存入上级分类
                print(echart1.value)
                echart2.value = round(float(echart2.value / totalMarketCap * 100),2)
                echart1.children.append(echart2.__dict__)
            echart1.value = round(float(echart1.value / totalMarketCap * 100),2)
            print(echart1.__dict__)
            echarts.append(echart1.__dict__)
        # 写入文件
        with open(os.path.join(os.getcwd(),'config','echarts.json'),'w',encoding='utf-8') as jsonFile:
            jsonFile.write(json.dumps(echarts))