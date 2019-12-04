# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os
import sys
from os import path
import json
# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
sys.path.append(srcDir)
from config.pathManager import pathManager

# # pandas 配置
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 5000)


class historyProfitManager:

    def __init__(self):
        self.pm = pathManager()
        self.history_df = pd.read_excel(
            path.join(self.pm.configPath, '历史交易盈亏.xlsx'))
        # 把数字补 0 改成 字符串
        self.history_df['基金代码'] = self.history_df['基金代码'].apply(
            lambda x: str(x).zfill(6))
        self.allCodes = list(self.history_df.基金代码.unique())
        self.category1Array = list(self.history_df.一级分类.unique())
        self.category2Array = list(self.history_df.二级分类.unique())
        self.category3Array = list(self.history_df.三级分类.unique())

        self.parent_df = self.getParentsHistoryProfit()
        self.klq_df = self.getKLQHistoryProfit()

        # print(self.allCodes)
        # print(self.category1Array)
        # print(self.category2Array)
        # print(self.category3Array)
        # print(self.history_df)

    # 获取父母历史收益 df
    def getParentsHistoryProfit(self):
        # # 返回 bool 值集合
        # fatherSources = (self.history_df.来源.str.contains(r'父'))
        # # 根据行 bool 值决定是否进入筛选结果
        # father_df = self.history_df[fatherSources]
        parent_df = self.history_df[self.history_df['持有人'] == u'父母']
        parent_df = parent_df.reset_index(drop=True)
        # print(parent_df)
        return parent_df

    # 获取康力泉历史收益 df
    def getKLQHistoryProfit(self):
        klq_df = self.history_df[~(self.history_df['持有人'] == u'父母')]
        klq_df = klq_df.reset_index(drop=True)
        # print(klq_df)
        return klq_df

    def categoryHistorySumInfo(self, categoryLevel=1, isParent=False):
        uniqueCategory = []
        df = None
        categoryKey = ''
        role = ''
        if isParent:
            role = '父母'
            if categoryLevel == 1:
                uniqueCategory = list(self.parent_df.一级分类.unique())
                categoryKey = '一级分类'
            elif categoryLevel == 2:
                uniqueCategory = list(self.parent_df.二级分类.unique())
                categoryKey = '二级分类'
            elif categoryLevel == 3 or categoryLevel > 3 or categoryLevel < 1:
                uniqueCategory = list(self.parent_df.三级分类.unique())
                categoryKey = '三级分类'
            df = self.parent_df
        else:
            role = '康力泉'
            if categoryLevel == 1:
                uniqueCategory = list(self.klq_df.一级分类.unique())
                categoryKey = '一级分类'
            elif categoryLevel == 2:
                uniqueCategory = list(self.klq_df.二级分类.unique())
                categoryKey = '二级分类'
            elif categoryLevel == 3 or categoryLevel > 3 or categoryLevel < 1:
                uniqueCategory = list(self.klq_df.三级分类.unique())
                categoryKey = '三级分类'
            df = self.klq_df
        for category in uniqueCategory:
            sub_df = df[df[categoryKey] == category]
            print(role, categoryKey, category,round(sub_df.累计盈亏.sum(),2), sep='\t')
        print()

        pass

if __name__ == "__main__":
    manager = historyProfitManager()
