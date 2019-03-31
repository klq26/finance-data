#coding=utf-8

from jqdatasdk import *
from pandas import *
from datetime import datetime
import numpy
import os

auth('13810650842','123456a')

index = '000016.XSHG'

def indexWeightsAndMarketCap(index):
    # 取出成分股
    stocks = get_index_stocks(index)
    # 获取成分股名称
    names = []
    for code in stocks:
        names.append(get_security_info(code).display_name)
    # 获取成分股权重
    weights = get_index_weights(index)
    weights = weights.sort_values(by="code",ascending= True)
    # 获取成分股市值
    q = query(
        valuation.market_cap,
        valuation.code
    ).filter(
        valuation.code.in_(stocks),
    )
    df = get_fundamentals(q,statDate=datetime.now())
    df = df.sort_values(by="code",ascending= True)
    # 合并
    df['name'] = names
    df['weight'] = weights.weight.values

    order = ['code','name','market_cap','weight']
    df = df[order]
    print(df)
    path = os.getcwd() + '{0}.csv'.format(index)
    df.to_csv(path,columns=['code','name','market_cap','weight'], sep='\t',encoding='utf-8')

def allUniqueStocks(indexs,indexnames):
    total = 0
    count = 0
    # 整理股票池（排除多指数之间的共有股票）
    stocks_pool = []
    for code in indexs:
        stocks = get_index_stocks(code)
        for stock in stocks:
            if stock not in stocks_pool:
                stocks_pool.append(stock)
                total += 1
        print(code + ' ' + indexnames[count] + ' 入池股票数：' + str(total))
        count = count + 1
        total = 0
    print('入池股票总数:\t{0}'.format(len(stocks_pool)))
    # 股票代码排序
    stocks_pool = sorted(stocks_pool) 
    # 市值
    q = query(
        valuation.market_cap,
        valuation.code
    ).order_by(
        valuation.code.asc()
    ).filter(
        valuation.code.in_(stocks_pool),
    )
    marketcap = get_fundamentals(q,statDate=datetime.now())
    marketcap = marketcap.sort_values(by="code",ascending= True)
    # 名字
    names = []
    for code in stocks_pool:
        names.append(get_security_info(code).display_name)
    # 组成 DataFrame
    df = DataFrame()
    df['code'] = stocks_pool
    df['name'] = names
    df['market_cap'] = marketcap.market_cap.values
    df = df.sort_values(by="code",ascending= True)
    path = os.getcwd() + 'holdingStocks.csv'
    df.to_csv(path, sep='\t',encoding='utf-8')
    
    
# run
indexnames = ['上证50','沪深300','中证500','中证1000','创业板','中证红利','养老产业','全指医药','中证传媒','中证环保','全指消费','金融地产','证券公司']
indexs = ['000016.XSHG','000300.XSHG','000905.XSHG','000852.XSHG','399006.XSHE','000922.XSHG', \
        '399812.XSHE','000991.XSHG','399971.XSHE','000827.XSHG','000990.XSHG','000992.XSHG','399975.XSHE']

allUniqueStocks(indexs,indexnames)

for index in indexs:
    indexWeightsAndMarketCap(index)
