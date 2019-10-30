# -*- coding: utf-8 -*-

import os
import sys
import json
import time

from config.pathManager import pathManager
# 多种统计输出
from assetAllocationExcelParser import assetAllocationExcelParser               # 输出资产配置信息到 Excel 表
from assetAllocationConsoleParser import assetAllocationConsoleParser           # 输出资产配置信息到控制台
from assetAllocationJSObjectParser import assetAllocationJSObjectParser         # 输出资产配置信息到 echarts 专用 data.js 对象
from assetAllocationEstimateExcelParser import assetAllocationEstimateExcelParser   # 输出当日收盘后的估算净值及预测涨跌金额
# model
from model.fundModel import fundModel
from model.assetModel import assetModel

class assetAllocationCombine:
    """
    把天天基金，且慢，螺丝钉计划的数据整合到一张 Excel 表
    """
    def __init__(self, strategy='a'):
        self.strategy = strategy # 默认 A 策略，即康力泉（不含现金和冻结资金）
        # 根据策略生成对于的变量配置参数
        if self.strategy == 'a':
            self.filenames = [u'danjuan_螺丝钉定投.txt',u'qieman_10万补充ETF计划.txt',u'qieman_我的S定投计划.txt', u'tiantian_康力泉.txt',u'huatai_康力泉.txt',u'guangfa_支付宝.txt']
            self.excelFilePathExt = u'康力泉权益类'
            self.echartsJSFilePathExt = u'康力泉'
            self.echartsFile = u'KLQPortfolio.html'
        elif self.strategy == 'b':
            self.filenames = [u'danjuan_李淑云.txt',u'danjuan_康世海.txt',u'tiantian_李淑云.txt']
            self.excelFilePathExt = u'父母'
            self.echartsJSFilePathExt = u'父母'
            self.echartsFile = u'ParentPortfolio.html'
        elif self.strategy == 'c':
            self.filenames = [u'danjuan_螺丝钉定投.txt',u'qieman_10万补充ETF计划.txt',u'qieman_我的S定投计划.txt', u'tiantian_康力泉.txt',u'huatai_康力泉.txt',u'guangfa_支付宝.txt',u'cash_康力泉.txt',u'freeze_康力泉.txt']
            self.excelFilePathExt = u'康力泉整体'
            self.echartsJSFilePathExt = u'康力泉'
            self.echartsFile = u'KLQPortfolio.html'
        # 持仓基金数据的本地保存路径标识
        self.fundJsonFilePathExt = self.excelFilePathExt
        self.pm = pathManager()
        self.fundCategorys = self.getFundCategorys()
        self.filepaths = []
        for root, dirs, files in os.walk(os.getcwd(), topdown=False):
            for name in files:
                if name in self.filenames:
                    self.filepaths.append(os.path.join(root,name))
        
        # 基金数据模型集合
        self.fundModelArray = []
        # 资产配置对象模型集合
        self.assetModelArray = []
        # 开始生成
        self.generateJsonFiles()

    # 根据 txt 文件集合，生成基金模型数组 fundModelArray 以及资产配置模型数组 assetModelArray
    def generateJsonFiles(self):
        for filepath in self.filepaths:
            with open(filepath,'r',encoding='utf-8') as file:
                lines = file.readlines()
                # 一行，二行过滤
                for i in range(2,len(lines)):
                    values = lines[i].replace('\n','').split('\t')
                    # 生成 fundModel
                    fund = fundModel()
                    fund.fundName = values[0]                                   # 基金名称
                    fund.fundCode = values[1]                                   # 基金净值
                    fund.holdNetValue = round(float(values[2]),4)               # 持仓成本
                    fund.holdShareCount = round(float(values[3]),2)             # 持仓份额
                    fund.holdMarketCap = round(float(values[4]),2)              # 持仓市值
                    fund.holdTotalGain = round(float(values[5]),2)              # 持仓盈亏
                    fund.estimateNetValue = 0.0000                              # 估算净值
                    fund.estimateTime = u'估算时间'                             # 估算时间
                    fund.estimateRate = 0.0000                                  # 估算涨跌幅
                    category = self.getFundCategoryByCode(fund.fundCode)
                    fund.category1 = category[u'category1']                    # 一级分类
                    fund.category2 = category[u'category2']                    # 二级分类
                    fund.category3 = category[u'category3']                    # 三级分类
                    fund.category4 = category[u'category4']                    # 分类 ID
                    fund.appSource = self.getFundAppSourceByFilePath(filepath)  # APP 来源
                    # 生成 assetModel
                    asset = assetModel()
                    asset.fundName = values[0]                                  # 基金名称
                    asset.fundCode = values[1]                                  # 基金净值
                    asset.holdNetValue = round(float(values[2]),4)              # 持仓成本
                    asset.holdShareCount = round(float(values[3]),2)            # 持仓份额
                    asset.holdMarketCap = round(float(values[4]),2)             # 持仓市值
                    asset.holdTotalGain = round(float(values[5]),2)             # 持仓盈亏
                    asset.category1 = category[u'category1']                    # 一级分类
                    asset.category2 = category[u'category2']                    # 二级分类
                    asset.category3 = category[u'category3']                    # 三级分类
                    asset.category4 = category[u'category4']                    # 分类 ID
                    asset.appSource = fund.appSource
                    
                    self.fundModelArray.append(fund.__dict__)
                    self.assetModelArray.append(asset.__dict__)
        # 输出文件
        fundJsonPath = os.path.join(self.pm.outputPath, u'{0}fund.json'.format(self.fundJsonFilePathExt))
        with open(fundJsonPath,'w',encoding=u'utf-8') as fundJsonFile:
            fundJsonFile.write(json.dumps(self.fundModelArray, ensure_ascii=False, sort_keys = True, indent = 4, separators=(',', ':')))
        assetJsonPath = os.path.join(self.pm.outputPath, u'{0}asset.json'.format(self.fundJsonFilePathExt))
        with open(assetJsonPath,'w',encoding=u'utf-8') as assetJsonFile:
            assetJsonFile.write(json.dumps(self.assetModelArray, ensure_ascii=False, sort_keys = True, indent = 4, separators=(',', ':')))

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
    
    # 根据基金文件，获取 APP 持仓来源
    def getFundAppSourceByFilePath(self,filepath):
        if u'螺丝钉定投' in filepath:
            return u'螺丝钉定投'
        elif u'danjuan_李淑云' in filepath:
            return u'李淑云螺丝钉'
        elif u'danjuan_康世海' in filepath:
            return u'康世海螺丝钉'
        elif u'10万补充ETF计划' in filepath:
            return u'且慢补充 150 份'
        elif u'我的S定投计划' in filepath:
            return u'且慢 S 定投'       
        elif u'tiantian_康力泉' in filepath:
            return u'天天基金'
        elif u'tiantian_李淑云' in filepath:
            return u'天天基金'
        elif u'guangfa' in filepath:
            return u'支付宝'
        elif u'huatai_康力泉' in filepath:
            return u'股票账户'
        elif u'cash_康力泉' in filepath:
            return u'现金账户'
        elif u'freeze_康力泉' in filepath:
            return u'冻结资金'
        return '未知'

    # 读取本地 fundModel 数据
    def loadFundModelArrayFromJson(self):
        # 读取文件
        fundJsonPath = os.path.join(self.pm.outputPath, u'{0}fund.json'.format(self.fundJsonFilePathExt))
        with open(fundJsonPath,'r',encoding=u'utf-8') as fundJsonFile:
            # object_hook 配合 init 传入 self.__dict__ = dictData 实现 json 字符串转 python 自定义对象
            contentList = json.loads(fundJsonFile.read(),object_hook=fundModel)
            return contentList
   
    # 读取本地 assetModel 数据
    def loadAssetModelArrayFromJson(self):
        # 读取文件
        assetJsonPath = os.path.join(self.pm.outputPath, u'{0}asset.json'.format(self.fundJsonFilePathExt))
        with open(assetJsonPath,'r',encoding=u'utf-8') as assetJsonFile:
            # object_hook 配合 init 传入 self.__dict__ = dictData 实现 json 字符串转 python 自定义对象
            contentList = json.loads(assetJsonFile.read(),object_hook=assetModel)
            return contentList
    


if len(sys.argv) <= 1:
    print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉股票情况 b：父母 c：康力泉整体资产配置情况')
    exit()
strategy = sys.argv[1]
combine = None
if strategy == 'a':
    combine = assetAllocationCombine('a')
elif strategy == 'b':
    combine = assetAllocationCombine('b')
elif strategy == 'c':
    combine = assetAllocationCombine('c')
else:
    print(u'[ERROR] 参数错误，不支持的策略编号。')
    exit()

# 从 json 文件读取数据
assetModelArray = combine.loadAssetModelArrayFromJson()
fundModelArray = combine.loadFundModelArrayFromJson()

# 输出 Excel 资产配置
assetExcel = assetAllocationExcelParser()
assetExcel.generateExcelFile(assetModelArray,path=os.path.join(self.pm.outputPath, u'{0}资产配置.xlsx'.format(combine.excelFilePathExt)))

# 输出 控制台 统计信息
console = assetAllocationConsoleParser()
console.showInfo(assetModelArray)

# 输出 echarts.json 和 data.json
jsObject = assetAllocationJSObjectParser()
jsObject.generateEchartsJsonFile(assetModelArray)
jsObject.generateJSObjectFile(assetModelArray,combine.echartsJSFilePathExt)

# 生成实时估值信息
estimateExcel = assetAllocationEstimateExcelParser()
estimateExcel.generateEstimateExcelFile(fundModelArray, path=os.path.join(self.pm.outputPath, u'{0}收益估算.xlsx'.format(combine.excelFilePathExt)))

# 打开资产配置旭日图
os.startfile(os.path.join(self.pm.echartsPath,combine.echartsFile))