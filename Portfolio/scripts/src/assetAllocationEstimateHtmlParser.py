# -*- coding: utf-8 -*-
import os
import time
import json
from operator import itemgetter
# html template
import jinja2
from jinja2 import Environment, FileSystemLoader
# model
from model.assetModel import assetModel
# config
from config.assetCategoryConstants import assetCategoryConstants
from config.pathManager import pathManager

from estimateFundManager import estimateFundManager

class assetAllocationEstimateHtmlParser:

    def __init__(self, strategy='a'):
        if strategy == 'a':
            self.pm = pathManager(strategyName='康力泉')
        elif strategy == 'b':
            self.pm = pathManager(strategyName='父母')
        self.fundCategorys = self.getFundCategorys()
        categoryConstants = assetCategoryConstants()
        self.category1Array = categoryConstants.category1Array
        self.category2Array = categoryConstants.category2Array
        self.category3Array = categoryConstants.category3Array
        self.modelArray = []

    # 格式化浮点数
    def beautify(self,num):
        return round(float(num),2)

    # 不同 APP 配色
    def getFundColorByAppSourceName(self, name):
        # 色值转换 https://www.sioe.cn/yingyong/yanse-rgb-16/
        if name in [u'螺丝钉定投',u'李淑云螺丝钉',u'康世海螺丝钉']:
            # 242,195,0
            return '#F2C300'
        elif name in [u'且慢补充 150 份',u'且慢 S 定投']:
            # 0,176,204
            return '#00B1CC'
        elif u'天天基金' in name:
            # 233,80,26
            return '#E9501A'
        elif u'支付宝' in name:
            # 0,161,233
            return '#00A1E9'
        elif u'股票账户' in name:
            # 222,48,49
            return '#DE3031'
        elif u'现金账户' in name:
            # 0,161,233
            return '#F7A128'
        elif u'冻结资金' in name:
            # 222,48,49
            return '#8B8C90'
        else:
            return '#FFFFFF'

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
    def generateHtmlFile(self,fundModelArray, title, path=''):
        if len(fundModelArray) == 0:
            return
        # 先删除旧文件
        if os.path.exists(path):
            os.remove(path)
        # 天天基金获取估算净值
        manager = estimateFundManager()
        # 资产配置统计数据
        estimateTotalGainToday = 0.0            # 今日涨跌额估值
        outerFundEstimateTotalGainToday = 0.0   # 今日场外涨跌额估值
        gainByAppSource = {}                    # 分 APP 涨跌幅统计
        # esitmate 暂存区，如果一个代码查过了，就不要二次出现浪费时间了
        estimateCache = {}
        # 写入基金持仓数据
        data = []
        for fundModel in fundModelArray:
            # 现金，冻结资金，海外债券没什么可估值的。海外成熟市场因为是下午或晚上开盘，也没有估值的必要
            if fundModel.category1 in [u'现金',u'冻结资金',u'海外成熟'] or fundModel.category2 == u'海外债券':
                continue
            
            if fundModel.fundCode in estimateCache.keys():
                estimateValues = estimateCache[fundModel.fundCode]
            else:
                estimateValues = manager.estimate(fundModel.fundCode)
                estimateCache[fundModel.fundCode] = estimateValues
            #print(estimateValues)  # 元组数据
            time.sleep(0.1)
            if estimateValues:
                fundModel.currentNetValue = estimateValues[0]
                fundModel.currentNetValueDate = estimateValues[1]
                fundModel.estimateNetValue = estimateValues[2]
                fundModel.estimateRate = estimateValues[3]
                fundModel.estimateTime = estimateValues[4]
            else:
                print('{0}估值请求失败'.format(fund.fundCode))
            dict = fundModel.__dict__
            # 颜色
            color = self.getFundColorByAppSourceName(fundModel.appSource)
            # 格式化
            fundModel.currentNetValue = round(fundModel.currentNetValue,4)
            fundModel.estimateNetValue = round(fundModel.estimateNetValue,4)
            fundModel.estimateRate = str(round(fundModel.estimateRate * 100,4)) + u'%'
            dict['color'] = color
            # 红涨绿跌
            changeValue = round((fundModel.estimateNetValue - fundModel.currentNetValue)*fundModel.holdShareCount,2)
            dict['changeValue'] = changeValue
            dict['changeValueColor'] = self.getGainColor(changeValue)
            # 计入今日统计
            if fundModel.appSource != u'股票账户':
                # 仅计入场外基金部分（因为场内有情绪涨跌溢价，收盘价不能用净值估算代表）
                outerFundEstimateTotalGainToday = outerFundEstimateTotalGainToday + changeValue
            estimateTotalGainToday = estimateTotalGainToday + changeValue
            # 按 APP 来源统计收支
            if fundModel.appSource not in gainByAppSource.keys():
                gainByAppSource[fundModel.appSource] = round(changeValue,2)
            else:
                gainOfCurrentAppSource = gainByAppSource[fundModel.appSource]
                gainByAppSource[fundModel.appSource] = round(gainOfCurrentAppSource + changeValue,2)
            data.append(dict)
        # 按收益降序排序
        data.sort(key=itemgetter('changeValue'),reverse=True)
        # jinja2 框架输出 html
        env = Environment(loader=FileSystemLoader(os.path.join(self.pm.parentDir, u'template')))
        template = env.get_template(u'实时估值template.html')
        with open(path,'w+') as fout:
            htmlCode = template.render(name=title, \
                innerFundEstimateTotalGainToday = self.beautify(estimateTotalGainToday - outerFundEstimateTotalGainToday), \
                innerColor = self.getGainColor(self.beautify(estimateTotalGainToday - outerFundEstimateTotalGainToday)),\
                outerFundEstimateTotalGainToday = self.beautify(outerFundEstimateTotalGainToday), \
                outerColor = self.getGainColor(outerFundEstimateTotalGainToday),\
                estimateTotalGainToday = self.beautify(estimateTotalGainToday), \
                totalColor = self.getGainColor(estimateTotalGainToday),\
                data=data)
            fout.write(htmlCode)
        # 打开文件
        os.startfile(path)

if __name__ == "__main__":
    assetHtml = assetAllocationEstimateHtmlParser()
    # 读取文件
    assetModelArray = list
    assetJsonPath = os.path.join(assetHtml.pm.holdingOutputPath, u'{0}fund.json'.format(u'康力泉整体'))
    with open(assetJsonPath,'r',encoding=u'utf-8') as assetJsonFile:
        assetModelArray = json.loads(assetJsonFile.read(),object_hook=assetModel)
    
    assetHtml.generateHtmlFile(assetModelArray,title=u'康力泉整体收益估算',path=os.path.join(assetHtml.pm.holdingOutputPath, u'{0}收益估算.html'.format(u'康力泉整体')))