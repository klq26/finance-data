import json
import os
import sys
import time
from datetime import datetime

import pandas as pd
import numpy as np

from jqdatasdk import *

from config.pathManager import pathManager
from config.colorConstants import colorConstants

class indexIndustryWeight:

    def __init__(self):
        auth('13810650842', '123456a')
        print(u'聚宽数据API：{0}'.format(get_query_count()))
        self.pm = pathManager('全家')
        self.colorConstants = colorConstants()
        self.result_df = pd.read_csv(os.path.join(self.pm.holdingOutputPath,u'indexHoldingInfo.csv'), sep='\t')
        self.outputRenameColumns = {'name': '名称', 'code': '代码', 'market_cap': '市值（亿元）', 'pe_ratio': 'pe', 'pb_ratio': 'pb', 'daily_change': '涨跌幅',
                                    'holding': '持有市值（元）', 'daily_gain': '日盈亏', 'hy_code1': '一级行业代码', 'hy_name1': '一级行业名称', 'hy_code2': '二级行业代码', 'hy_name2': '二级行业名称', 'relate_index': '相关指数'}
        # 转置列名的 key-value，作为读入内存后的列名
        self.inputRenameColumns = dict(
            [(value, key) for key, value in self.outputRenameColumns.items()])
        self.result_df = self.result_df.rename(columns=self.inputRenameColumns)

        with open(os.path.join(self.pm.configPath,u'indexIndustryInfo.json'),'r',encoding='utf-8') as f:
            self.swIndexInfos = json.loads(f.read())

    def analytics(self):
        indexList = ['000016.XSHG', '000300.XSHG', '000919.XSHG', '399701.XSHE', '399702.XSHE', '000905.XSHG', '000852.XSHG',
                     '399006.XSHE', '000922.XSHG', '399812.XSHE', '000991.XSHG', '000827.XSHG', '399971.XSHE', '399975.XSHE', '000992.XSHG']
        indexNames = ['上证50', '沪深300', '300价值', '基本面60', '基本面120', '中证500', '中证1000',
                     '创业板', '中证红利', '养老产业', '全指医药', '中证环保', '中证传媒', '证券公司', '金融地产']
        industrys = []
        result_df = pd.DataFrame()
        for swIndexInfo in self.swIndexInfos:
            industrys.append(swIndexInfo['name'].replace('I',''))
        result_df['申万一级行业'] = industrys

        for i in range(0,len(indexList)):
            index = indexList[i]
            indexName = indexNames[i]
            # 指数成分股权重
            # keys: code weight display_name date
            df = get_index_weights(index)
            df = df.drop(['date'], axis=1)
            df = df[['display_name','weight']]
            hy_name1s = []
            for code in df.index.values:
                item = self.result_df[self.result_df['code'] == code]
                hy_name1s.append(item.hy_name1.values[0])
            df['hy_name1'] = hy_name1s
            #print(df)

            industrys = []
            rates = []
            counts = []
            
            for swIndexInfo in self.swIndexInfos:
                item = df[df['hy_name1'] == swIndexInfo['name']]
                # industrys.append(swIndexInfo['name'])
                #originColor = self.colorConstants.getIndustryColorByName(swIndexInfo['name'])
                swIndexInfo['count'] = len(item)
                counts.append(swIndexInfo['count'])
                swIndexInfo['rate'] = '{0}%'.format(round(item.weight.sum(), 2))
                rates.append(swIndexInfo['rate'])
                # swIndexInfo['originColor'] = originColor
                # swIndexInfo['color'] = '#{0}'.format(self.colorConstants.hexColorStringByPercent(origin = originColor, zero = '#FFFFFF', rate = 1.0))
                # colors.append(swIndexInfo['color'])
            
            result_df['{0}_1'.format(indexName)] = counts
            result_df['{0}_2'.format(indexName)] = rates
           
            #result_df['color'] = colors
        print(result_df)
        result_df.to_csv(os.path.join(self.pm.configPath, 'indexWeightInfo.csv'), sep='\t')



if __name__ == "__main__":
    indexWeight = indexIndustryWeight()
    indexWeight.analytics()
    #print(indexWeight.colorConstants.rgbTupleFromHexString('#FFAA15'))
