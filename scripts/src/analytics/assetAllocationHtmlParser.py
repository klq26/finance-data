# -*- coding: utf-8 -*-
import os
import sys
import json
import shutil
from operator import itemgetter
import pandas as pd
# html template
import jinja2
from jinja2 import Environment, FileSystemLoader
# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
sys.path.append(srcDir)
# model
from model.assetModel import assetModel
# config
from config.assetCategoryConstants import assetCategoryConstants
from config.pathManager import pathManager
from config.colorConstants import colorConstants
from config.historyProfitManager import  historyProfitManager
from tools.dingtalk import dingtalk

class assetAllocationHtmlParser:

    def __init__(self):
        self.pm = pathManager()
        self.fundCategorys = self.getFundCategorys()
        self.historyManager = historyProfitManager()
        categoryConstants = assetCategoryConstants()
        self.category1Array = categoryConstants.category1Array
        self.category2Array = categoryConstants.category2Array
        self.category3Array = categoryConstants.category3Array
        self.modelArray = []
        self.colorConstants = colorConstants()
        self.dingtalk = dingtalk()

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

    # 不同 APP 配色
    def getFundColorByAppSourceName(self, name):
        return self.colorConstants.getFundColorByAppSourceName(name)

    # 获取资产旭日图分类配置文件
    def getFundCategorys(self):
        path = os.path.join(self.pm.configPath,u'fundCategory.json')
        if not os.path.exists(path):
            print(u'[ERROR] 缺少资产配置分类文件：{0}'.format(path))
            exit()
        with open(path,'r',encoding='utf-8') as jsonFile:
            data = json.loads(jsonFile.read())
            fundCategorys = data['data']
            return fundCategorys

    # 根据基金代码，获取资产旭日图分类数据
    def getFundCategoryByCode(self,code):
        for fundCategory in self.fundCategorys:
            if code == fundCategory['code']:
                return fundCategory
        return ''

    # 读取 txt，生成 assetModel 基金数据集合，输出到 xlsx 文件
    def generateHtmlFile(self,assetModelArray, history_df, title, path=''):
        # 先删除旧文件
        if os.path.exists(path):
            os.remove(path)
        
        # 资产配置统计数据
        totalMarketCap = 0.0
        totalStockMarketCap = 0.0
        totalCashMarketCap = 0.0
        totalGain = 0.0
        totalCashGain = 0.0
        totalStockGain = 0.0
        data = []
        for assetModel in assetModelArray:
            if assetModel.category1 in [u'现金',u'冻结资金']:
                totalCashGain = totalCashGain + assetModel.holdTotalGain
                totalCashMarketCap = totalCashMarketCap + assetModel.holdMarketCap
            totalMarketCap = totalMarketCap + assetModel.holdMarketCap
            totalGain = totalGain + assetModel.holdTotalGain
            # 增加色值
            color = self.getFundColorByAppSourceName(assetModel.appSource)
            assetDict = assetModel.__dict__
            assetDict['color'] = color
            # 计算收益率特殊处理已经平仓的品种
            if assetModel.holdMarketCap == 0:
                assetDict['holdTotalGainRate'] = '0.00%'
            else:
                assetDict['holdTotalGainRate'] = '{:.2f}%'.format(self.beautify(assetModel.holdTotalGain / (assetModel.holdMarketCap - assetModel.holdTotalGain) * 100))
            assetDict['changeValueColor'] = self.getGainColor(assetModel.holdTotalGain)
            # 输出格式化（保留小数点后 4 或 2 位）
            assetDict['holdNetValue'] = '{:.4f}'.format(assetDict['holdNetValue'])
            assetDict['holdShareCount'] = '{:.2f}'.format(assetDict['holdShareCount'])
            assetDict['holdMarketCap'] = '{:.2f}'.format(assetDict['holdMarketCap'])
            assetDict['holdTotalGain'] = '{:.2f}'.format(assetDict['holdTotalGain'])
            data.append(assetDict)
        
        # 第一行统计信息
        totalMarketCap = self.beautify(totalMarketCap)
        totalCashMarketCap = self.beautify(totalCashMarketCap)
        totalStockMarketCap = self.beautify(totalMarketCap - totalCashMarketCap)
        # 第二行统计信息
        totalGain = self.beautify(totalGain)
        totalStockGain = self.beautify(totalGain - totalCashGain)
        totalCashGain = self.beautify(totalCashGain)
        # 第三行统计信息
        totalGainRate = round(totalGain/(totalMarketCap-totalGain),4)
        totalStockGainRate = round(totalStockGain/(totalStockMarketCap - totalStockGain),4)
        if totalCashMarketCap > 0:
            totalCashGainRate = round(totalCashGain/(totalCashMarketCap-totalCashGain),4)
        else:
            totalCashGainRate = 0
        # 第四行统计信息
        totalHistoryGain = self.beautify(history_df.累计盈亏.sum())
        totalHistoryStockGain = self.beautify(history_df[~(history_df['一级分类'].isin([u'现金',u'冻结资金']))].累计盈亏.sum())
        totalHistoryCashGain = self.beautify(history_df[(history_df['一级分类'].isin([u'现金',u'冻结资金']))].累计盈亏.sum())
        # 第五行统计信息
        entireGain = self.beautify(totalHistoryGain + totalGain)
        entireStockGain = self.beautify(totalHistoryStockGain + totalStockGain)
        entireCashGain = self.beautify(totalHistoryCashGain + totalCashGain)
        # 第六行统计信息
        entireGainRate = round(entireGain/(totalMarketCap-entireGain),4)
        entireStockGainRate = round(entireStockGain/(totalStockMarketCap-entireStockGain),4)
        if totalCashMarketCap > 0:
            entireCashGainRate = round(entireCashGain/(totalCashMarketCap-entireCashGain),4)
        else:
            entireCashGainRate = 0
        # 生产 summary
        summary = list()
        rowTitles = ['当前市值', '持仓盈亏', '持仓收益率', '历史盈亏', '整体盈亏', '整体收益率']
        keys = list()
        keys += [u'property{0}'.format(x) for x in range(1,5)]
        keys += [u'property{0}Color'.format(x) for x in range(2,5)]
        keys.sort()
        # print('keys',keys)
        # keys ['property1', 'property2', 'property2Color', 'property3', 'property3Color', 'property4', 'property4Color']
        def getRowDataByIndex(rowTitle, index):
            if index == 0:
                return [rowTitles[index], totalStockMarketCap,u'#333333', totalCashMarketCap, u'#333333', totalMarketCap, u'#333333']
            if index == 1:
                return [rowTitles[index], totalStockGain,u'#333333', totalCashGain, u'#333333', totalGain, u'#333333']
            if index == 2:
                return [rowTitles[index], u'{:.2f}%'.format(totalStockGainRate * 100),self.getGainColor(totalStockGainRate), u'{:.2f}%'.format(totalCashGainRate * 100), self.getGainColor(totalCashGainRate), u'{:.2f}%'.format(totalGainRate * 100), self.getGainColor(totalGainRate)]
            if index == 3:
                return [rowTitles[index], totalHistoryStockGain,u'#333333', totalHistoryCashGain, u'#333333', totalHistoryGain, u'#333333']
            if index == 4:
                return [rowTitles[index], entireStockGain,u'#333333', entireCashGain, u'#333333', entireGain, u'#333333']
            if index == 5:
                return [rowTitles[index], u'{:.2f}%'.format(entireStockGainRate * 100),self.getGainColor(entireStockGainRate), u'{:.2f}%'.format(entireCashGainRate * 100), self.getGainColor(entireCashGainRate), u'{:.2f}%'.format(entireGainRate * 100), self.getGainColor(entireGainRate)]
        
        for i in range(len(rowTitles)):
            values = getRowDataByIndex(rowTitles, i)
            result = dict(zip(keys,values))
            summary.append(result)

        # jinja2 框架输出 html
        env = Environment(loader=FileSystemLoader(os.path.join(self.pm.parentDir, u'template')))
        template = env.get_template(u'资产配置template.html')
        with open(path,'w+',encoding='utf-8') as fout:
            htmlCode = template.render(name=title, \
                summary=summary, \
                data=data)
            fout.write(htmlCode)
        # 打开文件
        if sys.platform.startswith('win'):
            os.startfile(path)
        elif sys.platform.startswith('linux'):
            shutil.copy(path, '/var/www/html/assetAllocation.html')
            self.dingtalk.sendMessage(f'市值：http://112.125.25.230/assetAllocation.html')

if __name__ == "__main__":
    assetHtml = assetAllocationHtmlParser()
    # 读取文件
    assetModelArray = list
    assetJsonPath = os.path.join(assetHtml.pm.holdingOutputPath, u'{0}asset.json'.format(u'康力泉整体'))
    with open(assetJsonPath,'r',encoding=u'utf-8') as assetJsonFile:
        assetModelArray = json.loads(assetJsonFile.read(),object_hook=assetModel)
    
    assetHtml.generateHtmlFile(assetModelArray, assetHtml.historyManager.getKLQHistoryProfit(), title=u'康力泉整体资产配置',path=os.path.join(assetHtml.pm.holdingOutputPath, u'{0}资产配置.html'.format(u'康力泉整体')))

    #assetModelArray.sort(key=itemgetter('category4'))
    #assetHtml.generateHtmlFile(assetModelArray,title=u'康力泉整体资产配置（分类ID升序）',path=os.path.join(assetHtml.pm.holdingOutputPath, u'{0}资产配置（分类ID升序）.html'.format(u'康力泉整体')))