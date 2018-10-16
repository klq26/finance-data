from jqdatasdk import *
from pandas import *
import datetime
import numpy
import os

auth('13810650842','123456a')



df = DataFrame()

if os.path.exists('IndustryData\HY001.csv'):
    df = DataFrame.from_csv('IndustryData\HY001.csv',sep='\t',encoding='utf-8')
days = get_trade_days(start_date=df.date.values[-1].replace('/',''), end_date=datetime.date.today())
# days.remove(days[0])  # 去掉上次最后一个交易日（因为有数据）
# days.remove(days[-1])
days = list(days)
days.remove(days[0])    # 去掉第一个交易日（因为来自 dataframe 说明有数据）
days.remove(days[-1])   # 去掉最新一个交易日（因为数据库没更新）

for day in days:
#
#
# q = query(
#         # 只要动态市盈率字段
#         valuation.code,
#         valuation.pe_ratio,
#         valuation.pb_ratio
#     ).order_by(
#         valuation.code.asc()
#     ).filter(
#         valuation.code.in_(stocks)
#     )
#
#     df = get_fundamentals(q,context.current_dt)
#
#     if len(df) == 0:
#         return
#
#     pes = df.pe_ratio.astype(float)
#     pbs = df.pb_ratio.astype(float)
#
#     # 指数市盈率（公式：PE = n/Σ[1/个股PE]，n为PE个数）
#     count_pe = 0
#     sum = 0
#     for i in range(0,len(pes.values)):
#         if(pes.values[i] > 0):
#             sum += 1/pes.values[i]
#             count_pe+=1
#     pe_index = count_pe / sum
#
#     count_pb = 0
#     sum = 0
#     for i in range(0,len(pbs.values)):
#         if(pbs.values[i] > 0):
#             sum += 1/pbs.values[i]
#             count_pb+=1
#     pb_index = count_pb / sum
#
#     value = 0
#
#     if is_industry:
#         value = count
#     else:
#         value = round(get_current_data()[index].last_price,2)
#
#     series = pd.Series([context.current_dt.strftime('%Y/%m/%d'),value,round(pe_index,2),round(pb_index,2)], index=['date','value','pe','pb'])
#     print(series)
#     g.results = g.results.append(series,ignore_index=True)
