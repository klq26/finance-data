from jqdatasdk import *
from pandas import *
import numpy
import os

auth('13810650842','123456a')

index = '000905.XSHG'
date = '2018-10-12'

# 利润，市值
def pe_profit_marketcap(stocks, year=2018, quarter=1):
    q = query(
        # 只要动态市盈率字段
        valuation.market_cap,
        # valuation.pe_ratio,
        valuation.code,
        income.np_parent_company_owners
    ).order_by(
        # 按PE升序排列
        valuation.market_cap.desc()
    ).filter(
        valuation.code.in_(stocks),
    )
    # 获取所有股票的PE组合（剔除负数）
    df = get_fundamentals(q,statDate='{0}{1}'.format(year,quarter))

    if len(df.values) == 0:
        return pandas.DataFrame()
    return df
    pass


years = [x for x in range(2005,2019)]
quarters = ['Q{0}'.format(x) for x in range(1,5)]

for year in years:
    stocks = get_index_stocks(index,date='{0}-12-31'.format(year))
    # stocks = list(get_all_securities(['stock'],date='{0}-12-31'.format(year)).index)
    # print(len(stocks))
    year_profit = 0
    year_map_cap = 0
    for quarter in quarters:
        result = pe_profit_marketcap(stocks,year=year,quarter=quarter)
        if len(result) == 0:
            print('{0}{1} No Data'.format(year,quarter))
            continue
        dateString = str()
        if quarter == 'Q1':
            dateString = "/3/31"
        elif quarter == 'Q2':
            dateString = "/6/30"
        elif quarter == 'Q3':
            dateString = "/9/30"
        elif quarter == 'Q4':
            dateString = "/12/31"
        print('{0}{1}\t{2}\t{3}'.format(year,dateString,round(result.np_parent_company_owners.sum()/100000000/10000,4),round(result.market_cap.sum()/10000,4)))
        year_profit = year_profit + result.np_parent_company_owners.sum()
        year_map_cap = year_map_cap + result.market_cap.sum()
    # 利润单位：元，除以 1 万亿 / 市值单位：亿元，除以 1 万
    # print('{0}/12/31\t{1}\t{2}'.format(year,round(year_profit/100000000/10000,4),round(year_map_cap/10000,4)))


# # 获取指数权重（有缓存）
# def indexWeights(code,date):
#     path = 'indexWeights\code_{0}.txt'.format(code)
#     if os.path.exists(path):
#         print('weight for {0} from cache.'.format(code))
#         return DataFrame.from_csv(path,sep='\t',encoding='utf-8')
#     df = get_index_weights(code,date=date)
#     df.to_csv('indexWeights\code_{0}.txt'.format(code),sep='\t',columns=['display_name','date','weight'],encoding='utf-8')
#     return df
