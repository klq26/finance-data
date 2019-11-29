import json
import os
import sys
import time
from datetime import datetime

import pandas as pd
import numpy as np

from jqdatasdk import *

from model.echartsModel import echartsModel
from config.pathManager import pathManager
from config.colorConstants import colorConstants

# pandas 配置
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 5000)


class assetAllocationIndustryParser:

    def __init__(self, strategyName, forceUpdate=False):
        self.strategyName = strategyName
        self.pm = pathManager(self.strategyName)
        self.colorConstants = colorConstants()
        self.echarts = []
        # 市值情况
        with open(os.path.join(self.pm.configPath, 'indexHoldingInfo.json'), u'r', encoding=u'utf-8') as f:
            self.holdingInfos = json.loads(f.read())
        # print(self.holdingInfos)
        # 输出时切换到中文列名
        self.outputRenameColumns = {'name': '名称', 'code': '代码', 'market_cap': '市值（亿元）', 'pe_ratio': 'pe', 'pb_ratio': 'pb', 'daily_change': '涨跌幅',
                                    'holding': '持有市值（元）', 'daily_gain': '日盈亏', 'hy_code1': '一级行业代码', 'hy_name1': '一级行业名称', 'hy_code2': '二级行业代码', 'hy_name2': '二级行业名称', 'relate_index': '相关指数'}
        # 转置列名的 key-value，作为读入内存后的列名
        self.inputRenameColumns = dict(
            [(value, key) for key, value in self.outputRenameColumns.items()])
        # print(self.inputRenameColumns)
        # 个股持仓明细表
        cachFile = os.path.join(
            self.pm.holdingOutputPath, 'indexHoldingInfo.csv')
        shouldUpdate = True
        if not forceUpdate and os.path.exists(cachFile):
            print('indexHoldingInfo.csv 存在... 是否需要在线更新？[Y/N]')
            choice = str(input()).upper()
            # 这里只要不是 Y 都不更新了，防止过多查询聚宽
            if choice != 'Y':
                shouldUpdate = False
                self.result_df = pd.read_csv(cachFile, sep='\t')
                self.result_df = self.result_df.rename(
                    columns=self.inputRenameColumns)
                print('日盈亏：{0} 元'.format(
                    round(self.result_df.daily_gain.sum(), 2)))
        if shouldUpdate:
            # 登录
            auth('13810650842', '123456a')
            print(u'聚宽数据API：{0}'.format(get_query_count()))
            self.result_df = self.generateDataFrameCSVFile()
        # 申万指数 json
        with open(os.path.join(
            self.pm.configPath,u'indexIndustryInfo.json'),'r',encoding='utf-8') as f:
            self.swIndexInfos = json.loads(f.read())
        self.generateEchartsModels(self.result_df)
        self.generateJSObjectFile('全家') # 这里暂时没有使用 strategyName 作为输出标识符，后面应该想想更好的办法
        # 打开
        os.startfile(os.path.join(self.pm.echartsPath,u'FamilyStockIndustry.html'))

    # 生成持仓所有个股的行业情况的 DataFrame 本地 csv 文件
    def generateDataFrameCSVFile(self):
        # 今天的日期（用于拿最新的日涨跌额）
        todayStr = time.strftime("%Y-%m-%d", time.localtime())
        self.totalHolding = 0.0
        # 聚宽支持的 A 股指数（包含权重）
        indexList = ['000016.XSHG', '000300.XSHG', '000919.XSHG', '399701.XSHE', '399702.XSHE', '000905.XSHG', '000852.XSHG',
                     '399006.XSHE', '000922.XSHG', '399812.XSHE', '000991.XSHG', '000827.XSHG', '399971.XSHE', '399975.XSHE', '000992.XSHG']
        # 计算用 df header
        dfHeaders = ['name', 'code', 'market_cap', 'daily_change', 'pe_ratio', 'pb_ratio',
                     'hy_code1', 'hy_name1', 'hy_code2', 'hy_name2', 'holding', 'daily_gain', 'relate_index']
        # 输出用 df header
        outputDfHeaders = ['名称', '代码', '市值（亿元）', '涨跌幅', 'pe', 'pb',
                           '一级行业代码', '一级行业名称', '二级行业代码', '二级行业名称', '持有市值（元）', '日盈亏', '相关指数']
        # 初始化
        result_df = pd.DataFrame(columns=dfHeaders)
        # 股票池
        uniqueStockPool = []
        # 分指数请求数据，添加不重复的个股到 result_df
        for index in indexList:
            # 指数成分股
            stocks = get_index_stocks(index)
            # 指数成分股权重
            # keys: code weight display_name
            weights = get_index_weights(index)
            # 股票行业集合
            # keys: sw_l1 sw_l2 industry_code industry_name
            industrys = get_industry(stocks)
            # 当前指数持有总金额
            indexHolding = 0
            for holdingInfo in self.holdingInfos:
                if holdingInfo['code'] == index[0:6]:
                    indexName = holdingInfo['name']
                    indexHolding = float(holdingInfo['holding'])
                    self.totalHolding = self.totalHolding + indexHolding
                    #print('self.totalHolding',round(self.totalHolding,2), 'indexHolding', indexHolding)
            q = query(
                valuation.code,
                valuation.pe_ratio,
                valuation.pb_ratio,
                valuation.market_cap    # 单位：亿元
            ).order_by(
                valuation.code.asc()
            ).filter(
                valuation.code.in_(stocks)
            )
            df = get_fundamentals(q)
            # result_df 下的各列数据
            names = []
            daily_changes = []
            holdings = []
            hy_code1s = []
            hy_name1s = []
            hy_code2s = []
            hy_name2s = []
            for code in df.code.values:
                # 权重接口会返回 display_name，省略二次查询
                item = weights[weights.index == code]
                name = item.display_name.values[0]
                weight = item.weight.values[0]
                industry = industrys[code]
                # print(name,round(weight/100,4))
                names.append(name)
                # print(code,current_data[code].last_price,current_data[code].day_open)
                holdings.append(round((indexHolding * weight / 100), 2))
                if 'sw_l1' in industry.keys():
                    hy_code1s.append(industry['sw_l1']['industry_code'])
                    # 之后拿申万行业，不拿聚宽了。聚宽有些是错误的，比如 '600733.XSHG' 是汽车行业，他归类到金融地产了
                    hy_name1s.append(industry['sw_l1']['industry_name'])
                else:
                    hy_code1s.append('未知')
                    hy_name1s.append('未知')
                if 'sw_l2' in industry.keys():
                    hy_code2s.append(industry['sw_l2']['industry_code'])
                    # 去掉所有聚宽二级行业中的“指数”字样
                    hy_name2s.append(industry['sw_l2']['industry_name'])
                else:
                    hy_code2s.append('未知')
                    hy_name2s.append('未知')
            df['name'] = names
            df['holding'] = holdings
            df['hy_code1'] = hy_code1s
            df['hy_name1'] = hy_name1s
            df['hy_code2'] = hy_code2s
            df['hy_name2'] = hy_name2s
            # 以下三个先占位，后续会统一补充
            df['relate_index'] = 'NA'
            df['daily_gain'] = 0
            df['daily_change'] = 0
            # 列先后顺序排序
            df = df[dfHeaders]
            # 添加不在池中的股票
            uniqueStocks = df[~df['code'].isin(uniqueStockPool)]
            # 把已经在股票池中的持仓金额更新到总表
            duplicateStocks = df[df['code'].isin(uniqueStockPool)]
            #print('index', index[0:6], 'index uniqueStocks count', len(uniqueStocks),'index total count',len(df))
            for i in range(0, len(uniqueStocks)):
                code = uniqueStocks.code.values[i]
                uniqueStockPool.append(code)
                uniqueStocks['relate_index'].values[i] = indexName
            result_df = result_df.append(
                uniqueStocks, ignore_index=True, verify_integrity=False)
            for i in range(0, len(duplicateStocks)):
                code = duplicateStocks.code.values[i]
                newHolding = duplicateStocks.holding.values[i]
                index = result_df[result_df['code'] == code].index.values[0]
                #print('duplicate: {0}'.format(code), index, float(result_df.loc[index,'holding']),round(newHolding,2))
                # 股票已经包含在其他指数的情况，求和各指数下的投资，连接所有的指数名称，便于分析
                result_df.loc[index, 'holding'] = round(
                    result_df.loc[index, 'holding'], 2) + round(newHolding, 2)
                result_df.loc[index, 'relate_index'] = result_df.loc[index,
                                                                     'relate_index'] + ',{0}'.format(indexName)
            #print('pool stock count', len(result_df), 'index total cash',round(result_df.holding.sum(),2))
        # 一次性拿回所有持仓个股的日涨跌幅
        prices_df = get_price(list(result_df.code.values), count=2, end_date=todayStr,
                              frequency='daily', fields=['open', 'close'], panel=False)
        for code in result_df.code.values:
            sub_df = prices_df[prices_df['code'] == code]
            pre_close = sub_df.close.values[0]
            current = sub_df.close.values[1]
            rate = round((current - pre_close)/pre_close, 4)
            # 计算所有股票的日盈亏率
            daily_changes.append(rate)
        # 所有股票的日涨跌幅更新
        result_df['daily_change'] = daily_changes
        # 持仓市值倒叙排列
        result_df = result_df.sort_values('holding', ascending=False)
        # print('total holding', round(result_df.holding.sum(),2))
        # 重置 index 索引号
        result_df.reset_index(drop=True, inplace=True)
        # 算一下今日收益
        result_df['daily_gain'] = result_df.apply(
            lambda x: round(x['holding'] * x['daily_change'], 2), axis=1)
        # 输出前的最后格式化
        result_df['holding'] = result_df['holding'].apply(
            lambda x: round(x, 2))
        result_df['daily_change'] = result_df['daily_change'].apply(
            lambda x: '{0}%'.format(round(x * 100, 2)))
        result_df['pe_ratio'] = result_df['pe_ratio'].apply(
            lambda x: round(x, 2))
        result_df['pb_ratio'] = result_df['pb_ratio'].apply(
            lambda x: round(x, 2))
        print('日盈亏：{0} 元'.format(round(result_df.daily_gain.sum(), 2)))
        # 输出之前的重命名
        result_df = result_df.rename(columns=self.outputRenameColumns)
        result_df = result_df[outputDfHeaders]
        # print(result_df)
        result_df.to_csv(os.path.join(self.pm.holdingOutputPath,
                                      'indexHoldingInfo.csv'), sep='\t')
        return result_df
    
    # float 保留两位小数
    def beautify(self,num):
        return round(float(num),2)
    
    # 申万指数颜色
    def colorWithHyName1(self,hy_name1):
        return self.colorConstants.getIndustryColorByName(hy_name1)

    # 申万指数排序算法
    def indexWithHyName1(self,hy_name1):
        for swIndex in self.swIndexInfos:
            if hy_name1 == swIndex['name']:
                return swIndex['index']
        return 0

    # 用申万指数排序索引对输出结果进行排序
    def swIndexSortFunc(self, echartModel):
        return echartModel['index']

    # 生成绘制行业分类所需的 echarts data.js 文件
    def generateEchartsModels(self,df):
        self.totalHolding = self.beautify(df.holding.sum())
        all_industry = {}
        # 唯一一级分类
        #all_hy_name1 = list(df.hy_name1.unique())
        # 唯一二级分类
        #all_hy_name2 = list(df.hy_name2.unique())
        
        for i in range(0,len(df)):
            # 一级行业
            industary1 = df.hy_name1.values[i]
            if industary1 not in all_industry.keys():
                all_industry[industary1] = {}
            # 二级行业
            industary2 = df.hy_name2.values[i]
            if industary2 not in all_industry[industary1].keys():
                # 二级行业持仓市值求和
                #industry2Holding = round(df[df['hy_name2'] == industary2].holding.sum(),2)
                # 百分比
                industry2Holding = round((round(df[df['hy_name2'] == industary2].holding.sum(),2))/self.totalHolding * 100,2)
                # 二维字典
                all_industry[industary1][industary2] = industry2Holding
        # 遍历生成 echarts 对象
        for key in all_industry.keys():
            # 一级行业市值求和
            industry1_sum = round(sum(list(all_industry[key].values())),2)
            color = self.colorWithHyName1(key)
            echart1 = echartsModel()
            echart1.value = industry1_sum
            # 防止图太乱
            if echart1.value >= 1.5:
                echart1.name = '{0},{1}%'.format(key,industry1_sum)
            echart1.itemStyle = {'color':color}
            print(echart1.name)
            for subIndustryKey in all_industry[key].keys():
                echart2 = echartsModel()
                echart2.value = all_industry[key][subIndustryKey]
                # 防止图太乱
                if echart2.value >= 0.5:
                    echart2.name = '{0},{1}%'.format(subIndustryKey,all_industry[key][subIndustryKey])
                echart2.itemStyle = {'color':color}
                echart1.children.append(echart2.__dict__)
                print('\t{0},{1}%'.format(subIndustryKey,all_industry[key][subIndustryKey]))
                # 在对象字典上，加上指数的 index，用于后续排序
                echart1['index'] = self.indexWithHyName1(key)
            self.echarts.append(echart1.__dict__)
        # 用申万指数排序索引对输出结果进行排序
        self.echarts.sort(key = self.swIndexSortFunc)

    # 生成直接可用的 data.js 文件
    def generateJSObjectFile(self,name):
        fileName = u'stockIndustry_{0}.js'.format(name)
        jsPath = os.path.join(self.pm.echartsPath,fileName)
        with open(jsPath,'w',encoding='utf-8') as jsFile:
            # print(jsPath)
            jsFile.write('function getData()\n')
            jsFile.write('{\n')
            jsFile.write('\t' + r'return {0}'.format(json.dumps(self.echarts, ensure_ascii=False, sort_keys = True, indent = 4, separators=(',', ':'))))
            jsFile.write('\n}')

if __name__ == "__main__":
    strategy = 'a'
    if len(sys.argv) >= 2:
        #print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：父母')
        strategy = sys.argv[1]
    strategyName = ''
    if strategy == 'a':
        strategyName = u'康力泉'
    elif strategy == 'b':
        strategyName = u'父母'
    elif strategy == 'c':
        strategyName = u'全家'
    industryParser = assetAllocationIndustryParser(strategyName,forceUpdate=False)
