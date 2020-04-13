# -*- coding: utf-8 -*-

import os
import sys
from os import path
import json
# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
sys.path.append(srcDir)

import pandas as pd
import numpy as np

from config.pathManager import pathManager

# # pandas 配置
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 5000)


class assetCategoryManager:

    def __init__(self):
        self.pm = pathManager()
        self.category_df = pd.read_excel(
            path.join(self.pm.configPath, '资产配置分类表.xlsx'))
        # 把数字补 0 改成 字符串
        self.category_df['基金代码'] = self.category_df['基金代码'].apply(
            lambda x: str(x).zfill(6))
        self.allCodes = list(self.category_df.基金代码.unique())
        self.category1Array = list(self.category_df.一级分类.unique())
        self.category2Array = list(self.category_df.二级分类.unique())
        self.category3Array = list(self.category_df.三级分类.unique())
        # print(self.allCodes)
        # print(self.category1Array)
        # print(self.category2Array)
        # print(self.category3Array)

    # 生成 fundCategory.json 文件
    def generateFundCategoryJsonFile(self):
        outputPath = path.join(self.pm.configPath, 'fundCategory.json')
        funds = []
        for i in range(len(self.category_df)):
            fundDict = {}
            fundDict['name'] = self.category_df.基金名称.values[i]
            fundDict['code'] = str(self.category_df.基金代码.values[i]).zfill(6)
            fundDict['category1'] = self.category_df.一级分类.values[i]
            fundDict['category2'] = self.category_df.二级分类.values[i]
            fundDict['category3'] = self.category_df.三级分类.values[i]
            fundDict['category4'] = str(self.category_df.分类ID.values[i])
            funds.append(fundDict)
        with open(outputPath, 'w+', encoding=u'utf-8') as f:
            f.write(json.dumps({'data': funds}, indent=4,
                               ensure_ascii=False, separators=(',', ':')))

    # 从库中生成一个支持在线查询实时估值的代码集合（支持区分场内或场外）
    def getEstimableFunds(self, isInnerMarket = True):
        unEstimableCodes = ['股票', '海外互联网', '房地产', '纯债', '美元债',
                            '白银', '无息外借款', '住房公积金', '民间借贷', '企业借贷', '货币基金']
        # unEstimable_df = self.category_df[self.category_df['三级分类'].isin(unEstimableCodes)]
        # unEstimable_df = unEstimable_df.reset_index(drop=True)
        marketStr = u'场外'
        if not isInnerMarket:
            # & 指定多条件时，多个条件之间的 () 不能省略，即：() & ()
            estimableCodes_df = self.category_df[(~self.category_df['三级分类'].isin(unEstimableCodes)) & (self.category_df['市场'] == marketStr)]
        else:
            estimableCodes_df = self.category_df[(~self.category_df['三级分类'].isin(unEstimableCodes)) & (self.category_df['市场'].isin([u'沪市', u'深市']))]
        estimableCodes_df = estimableCodes_df.reset_index(drop=True)
        results = dict(zip(list(estimableCodes_df.基金名称.unique()), list(estimableCodes_df.基金代码.unique())))
        return results

    def getCanUpdateNavFunds(self):
        canUpdateNavCodes_df = self.category_df[(self.category_df['市场'] == "场外")]
        canUpdateNavCodes_df = canUpdateNavCodes_df.append(self.category_df[self.category_df['市场'] == '场内'])
        canUpdateNavCodes_df = canUpdateNavCodes_df.reset_index(drop=True)
        results = dict(zip(list(canUpdateNavCodes_df.基金名称.unique()), list(canUpdateNavCodes_df.基金代码.unique())))
        return results

if __name__ == "__main__":
    manager = assetCategoryManager()
    manager.generateFundCategoryJsonFile()
    print(manager.getEstimableFunds(isInnerMarket = True))
    print(manager.getEstimableFunds(isInnerMarket = False))
