from jqdatasdk import *
from pandas import *
import numpy
import os

auth('13810650842','123456a')

index = '000300.XSHG'
date = '2018-10-19'

columns=['code,dividend,dividend_date,market_cap']
result = DataFrame(columns=columns)
stocks = get_index_stocks(index,date=date)

# 获取现金分红数据
# limit = 5 是取最新的 5 个报告期，因为从 2016-01-01 开始算，刚好到 2018-6-30 是每只股 5 个报告期
q1 = query(
    finance.STK_XR_XD.bonus_amount_rmb,
    finance.STK_XR_XD.report_date,
    finance.STK_XR_XD.code
).filter(
    finance.STK_XR_XD.code.in_(stocks),
    finance.STK_XR_XD.report_date>='2016-01-01'
).order_by(
    finance.STK_XR_XD.code
).limit(4 * len(stocks))
dividend_df = finance.run_query(q1)
dividend_df.to_csv('dividend_{0}.txt'.format(index),sep='\t',encoding='utf-8')
# dividend_df = DataFrame.from_csv('dividend_{0}.txt'.format(index),sep='\t',encoding='utf-8')

for stock in stocks:
    # 取出每只股票的最近 5 条记录
    temp = dividend_df.loc[stock == dividend_df.code]
    # 按报告期，逆序排列临时数组
    temp = temp.sort_values(by=['report_date'],ascending=False)
    for record in temp.values:
        # record 参考格式：[293520.804 '2017-12-31' '600000.XSHG']
        if not numpy.isnan(record[0]):
            # 判断 nan，打印数据
            print('{0}\t{1}'.format(record[2],record[0]))
            break

print('\n')

# 获取市值信息
q2 = query(
    # 只要动态市盈率字段
    valuation.market_cap,
    valuation.code,
).order_by(
    # 按PE升序排列
    valuation.code
).filter(
    valuation.code.in_(stocks),
)
marketcap_df = get_fundamentals(q2,date=date)
marketcap_df.to_csv('marketcap_{0}.txt'.format(index),sep='\t',encoding='utf-8')
# marketcap_df = DataFrame.from_csv('dividend_{0}.txt'.format(index),sep='\t',encoding='utf-8')

for record in marketcap_df.values:
    # 市值数据单位是 万亿，需要乘以 10000 才能转换为 万
    print('{0}\t{1}'.format(record[1],float(record[0]) * 10000))
