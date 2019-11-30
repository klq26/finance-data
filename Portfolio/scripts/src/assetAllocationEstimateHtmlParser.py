# -*- coding: utf-8 -*-
import os
import sys
import time
import json
from operator import itemgetter
# html template
import jinja2
from jinja2 import Environment, FileSystemLoader
# model
from model.fundModel import fundModel
# config
from config.assetCategoryConstants import assetCategoryConstants
from config.colorConstants import colorConstants
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
        self.colorConstants = colorConstants()
        self.fundJsonFilePathExt = ''

    # 格式化浮点数
    def beautify(self,num):
        return round(float(num),2)

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

    # 读取 txt，生成 fundModel 基金数据集合，输出到 xlsx 文件
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
        # 进度标识
        current = 0
        totalCount = len(fundModelArray)
        for fundModel in fundModelArray:
            # 现金，冻结资金，海外债券没什么可估值的。海外成熟市场因为是下午或晚上开盘，也没有估值的必要
            if fundModel.category1 in [u'现金',u'冻结资金',u'海外成熟'] or fundModel.category2 == u'海外债券':
                current = current + 1
                print('\rExcel estimate 进度：{0:.2f}% {1} / {2}'.format(float(current)/totalCount * 100, current,totalCount),end='',flush=True)
                continue
            
            if fundModel.fundCode in estimateCache.keys():
                estimateValues = estimateCache[fundModel.fundCode]
            else:
                estimateValues = manager.estimate(fundModel.fundCode)
                estimateCache[fundModel.fundCode] = estimateValues
            #print(estimateValues)  # 元组数据
            time.sleep(0.1)
            current = current + 1
            print('\rHtml estimate 进度：{0:.2f}% {1} / {2}'.format(float(current)/totalCount * 100, current,totalCount),end='',flush=True)
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
            fundModel.estimateRate = '{:.2f}%'.format(round(fundModel.estimateRate * 100,4))
            dict['color'] = color
            # 红涨绿跌
            changeValue = round((fundModel.estimateNetValue - fundModel.currentNetValue)*fundModel.holdShareCount,2)
            dict['changeValue'] = changeValue
            dict['changeValueColor'] = self.colorConstants.getGainColor(changeValue)
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
            # 输出格式化（保留小数点后 4 或 2 位）
            dict['holdNetValue'] = '{:.4f}'.format(dict['holdNetValue'])
            dict['holdShareCount'] = '{:.2f}'.format(dict['holdShareCount'])
            dict['holdMarketCap'] = '{:.2f}'.format(dict['holdMarketCap'])
            dict['holdTotalGain'] = '{:.2f}'.format(dict['holdTotalGain'])
            dict['currentNetValue'] = '{:.4f}'.format(dict['currentNetValue'])
            dict['estimateNetValue'] = '{:.4f}'.format(dict['estimateNetValue'])
            dict['changeValue'] = '{:.2f}'.format(dict['changeValue'])
            data.append(dict)
        # 将估值数据写入缓存，30 分钟之内都有效
        manager.saveCache(fundModelArray)
        # 按收益降序排序
        data.sort(key=itemgetter('changeValue'),reverse=True)
        # jinja2 框架输出 html
        env = Environment(loader=FileSystemLoader(os.path.join(self.pm.parentDir, u'template')))
        template = env.get_template(u'实时估值template.html')
        with open(path,'w+',encoding=u'utf-8') as fout:
            htmlCode = template.render(name=title, \
                innerFundEstimateTotalGainToday = self.beautify(estimateTotalGainToday - outerFundEstimateTotalGainToday), \
                innerColor = self.colorConstants.getGainColor(self.beautify(estimateTotalGainToday - outerFundEstimateTotalGainToday)),\
                outerFundEstimateTotalGainToday = self.beautify(outerFundEstimateTotalGainToday), \
                outerColor = self.colorConstants.getGainColor(outerFundEstimateTotalGainToday),\
                estimateTotalGainToday = self.beautify(estimateTotalGainToday), \
                totalColor = self.colorConstants.getGainColor(estimateTotalGainToday),\
                data=data)
            fout.write(htmlCode)
        # 打开文件
        os.startfile(path)

    # 读取本地 fundModel 数据
    def loadFundModelArrayFromJson(self):
        # 读取文件
        fundJsonPath = os.path.join(self.pm.holdingOutputPath, u'{0}fund.json'.format(self.fundJsonFilePathExt))
        with open(fundJsonPath,'r',encoding=u'utf-8') as fundJsonFile:
            # object_hook 配合 init 传入 self.__dict__ = dictData 实现 json 字符串转 python 自定义对象
            contentList = json.loads(fundJsonFile.read(),object_hook=fundModel)
            return contentList

if __name__ == "__main__":
    strategy = 'a'
    if len(sys.argv) >= 2:
        #print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：父母')
        strategy = sys.argv[1]
    assetHtml = assetAllocationEstimateHtmlParser(strategy)
    if strategy == 'a':
        assetHtml.fundJsonFilePathExt = u'康力泉整体'
    elif strategy == 'b':
        assetHtml.fundJsonFilePathExt = u'父母'
    # 读取文件
    path=os.path.join(assetHtml.pm.holdingOutputPath, u'{0}收益估算.xlsx'.format(assetHtml.fundJsonFilePathExt))
    assetHtml.generateHtmlFile(assetHtml.loadFundModelArrayFromJson(),title=u'{0}收益估算'.format(assetHtml.fundJsonFilePathExt),path=os.path.join(assetHtml.pm.holdingOutputPath, u'{0}收益估算.html'.format(assetHtml.fundJsonFilePathExt)))