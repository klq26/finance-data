# -*- coding: utf-8 -*-
import os
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

class assetAllocationHtmlParser:

    def __init__(self):
        self.pm = pathManager()
        self.fundCategorys = self.getFundCategorys()
        categoryConstants = assetCategoryConstants()
        self.category1Array = categoryConstants.category1Array
        self.category2Array = categoryConstants.category2Array
        self.category3Array = categoryConstants.category3Array
        self.modelArray = []

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
        # 色值转换 https://www.sioe.cn/yingyong/yanse-rgb-16/
        if name in [u'螺丝钉定投',u'李淑云螺丝钉',u'康世海螺丝钉']:
            # 242,195,0
            return 'F2C300'
        elif name in [u'且慢补充 150 份',u'且慢 S 定投']:
            # 0,176,204
            return '00B1CC'
        elif u'天天基金' in name:
            # 233,80,26
            return 'E9501A'
        elif u'支付宝' in name:
            # 0,161,233
            return '00A1E9'
        elif u'股票账户' in name:
            # 222,48,49
            return 'DE3031'
        elif u'现金账户' in name:
            # 0,161,233
            return 'F7A128'
        elif u'冻结资金' in name:
            # 222,48,49
            return '8B8C90'
        else:
            return 'FFFFFF'

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
    def generateHtmlFile(self,assetModelArray, title, path=''):
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
            dict = assetModel.__dict__
            dict['color'] = color
            data.append(dict)
            
        totalMarketCap = self.beautify(totalMarketCap)
        totalCashMarketCap = self.beautify(totalCashMarketCap)
        totalStockMarketCap = self.beautify(totalMarketCap - totalCashMarketCap)
        totalGain = self.beautify(totalGain)
        totalStockGain = self.beautify(totalGain - totalCashGain)
        totalCashGain = self.beautify(totalCashGain)
        
        # jinja2 框架输出 html
        env = Environment(loader=FileSystemLoader(os.path.join(self.pm.parentDir, u'template')))
        template = env.get_template(u'资产配置template.html')
        with open(path,'w+') as fout:
            htmlCode = template.render(name=title, \
                totalMarketCap=totalMarketCap, \
                totalStockMarketCap=totalStockMarketCap, \
                totalCashMarketCap=totalCashMarketCap, \
                totalGain=totalGain, \
                totalGainColor = self.getGainColor(totalGain), \
                totalStockGain=totalStockGain, \
                totalStockGainColor = self.getGainColor(totalStockGain), \
                totalCashGain=totalCashGain, \
                totalCashGainColor = self.getGainColor(totalCashGain), \
                data=data)
            fout.write(htmlCode)
        # 打开文件
        os.startfile(path)

if __name__ == "__main__":
    assetHtml = assetAllocationHtmlParser()
    # 读取文件
    assetModelArray = list
    assetJsonPath = os.path.join(assetHtml.pm.holdingOutputPath, u'{0}asset.json'.format(u'康力泉整体'))
    with open(assetJsonPath,'r',encoding=u'utf-8') as assetJsonFile:
        assetModelArray = json.loads(assetJsonFile.read(),object_hook=assetModel)
    
    assetHtml.generateHtmlFile(assetModelArray,title=u'康力泉整体资产配置',path=os.path.join(assetHtml.pm.holdingOutputPath, u'{0}资产配置.html'.format(u'康力泉整体')))
    
    assetModelArray.sort(key=itemgetter('category4'))
    assetHtml.generateHtmlFile(assetModelArray,title=u'康力泉整体资产配置（分类ID升序）',path=os.path.join(assetHtml.pm.holdingOutputPath, u'{0}资产配置（分类ID升序）.html'.format(u'康力泉整体')))