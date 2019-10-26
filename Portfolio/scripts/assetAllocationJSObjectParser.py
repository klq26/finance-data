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

class assetAllocationJSObjectParser:

    def __init__(self):
        categoryConstants = assetCategoryConstants()
        self.category1Array = categoryConstants.category1Array
        self.category2Array = categoryConstants.category2Array
        self.category3Array = categoryConstants.category3Array
        self.modelArray = []
        self.jsonStr = u''
        self.echarts = []
    
    # 格式化浮点数
    def beautify(self,num):
        return round(float(num),2)
        
    # 资产分类的 echarts 背景色
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

    def generateEchartsJsonFile(self,modelArray):
        self.modelArray = modelArray
        # 按对象的 category4 字段升序排序
        modelArray.sort(key=itemgetter('category4'))
        # 资产配置总市值
        totalMarketCap = 0.0
        for item in modelArray:
            totalMarketCap = totalMarketCap + item.marketCap
            #print(item.__dict__)
        totalMarketCap = self.beautify(totalMarketCap)
        #print(totalMarketCap)
        
        # 树形结构化
        for category in self.category1Array:
            category1Models = [x for x in modelArray if x.category1 == category]
            # 一级分类
            #print(category)
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
                    echart3.name = u'{0} , {1}%'.format(echart3.name,echart3.value)
                    echart2.children.append(echart3.__dict__)
                echart1.value = echart1.value + echart2.value   # 变成百分比之前，存入上级分类
                #print(echart1.value)
                echart2.value = round(float(echart2.value / totalMarketCap * 100),2)
                echart2.name = u'{0} , {1}%'.format(echart2.name,echart2.value)
                echart1.children.append(echart2.__dict__)
            echart1.value = round(float(echart1.value / totalMarketCap * 100),2)
            echart1.name = u'{0} , {1}%'.format(echart1.name,echart1.value)
            #print(echart1.__dict__)
            self.echarts.append(echart1.__dict__)
        # 写入文件
        with open(os.path.join(os.getcwd(),'config','echarts.json'),'w',encoding='utf-8') as jsonFile:
            jsonFile.write(json.dumps(self.echarts))
    
    # 生成直接可用的 data.js 文件
    def generateJSObjectFile(self,modelArray,name):
        jsPath = os.path.join(os.getcwd(),'..','echarts',u'data_{0}.js'.format(name))
        with open(jsPath,'w',encoding='utf-8') as jsFile:
            # print(jsPath)
            jsFile.write('function getData()\n')
            jsFile.write('{\n')
            jsFile.write('\t' + r'return {0}'.format(json.dumps(self.echarts)))
            jsFile.write('\n}')
        