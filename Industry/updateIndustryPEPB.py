from jqdatasdk import *
from pandas import *
import datetime
import numpy
import os

auth('13810650842','123456a')

df = DataFrame()

industry_codes = ['HY001','HY002','HY003','HY004','HY005','HY006','HY007','HY008','HY010']  # HY007 + HY010 = 金融地产，HY009 基本没有公司

for code in industry_codes:
    # os.getcwd() 可以打印当前路径，建议在 updateIndustryPEPB.py 所在的文件夹下运行脚本

    path = os.path.join(os.getcwd(),u'Industry', u'IndustryData', u'{0}.csv'.format(code))
    if os.path.exists(path):
        df = DataFrame.from_csv(path,sep='\t',encoding='utf-8')
        days = get_trade_days(start_date=df.date.values[-1].replace('/',''), end_date=datetime.date.today())
        days = list(days)
        days.remove(days[0])    # 去掉第一个交易日（因为来自 dataframe 说明有数据）
        days.remove(days[-1])   # 去掉最新一个交易日（因为数据库没更新）
        print(u'历史数据最新一天：{0}'.format(df.date.values[-1]))
        for day in days:
            stocks = get_industry_stocks(code, date=day)
            if code == 'HY007':
                dichan = get_industry_stocks('HY011', date=day)
                stocks.extend(dichan)
            is_industry = True
            count = len(stocks)
            q = query(
                valuation.pe_ratio,
                valuation.pb_ratio
            ).order_by(
                valuation.code.asc()
            ).filter(
                valuation.code.in_(stocks)
            )
            result = get_fundamentals(q,day)
            if len(result) == 0:
                print('无数据')
                continue

            pes = result.pe_ratio.astype(float)
            pbs = result.pb_ratio.astype(float)

            # 指数市盈率（公式：PE = n/Σ[1/个股PE]，n为PE个数）
            count_pe = 0
            sum = 0
            for i in range(0,len(pes.values)):
                if(pes.values[i] > 0):
                    sum += 1/pes.values[i]
                    count_pe+=1
            pe_index = count_pe / sum

            count_pb = 0
            sum = 0
            for i in range(0,len(pbs.values)):
                if(pbs.values[i] > 0):
                    sum += 1/pbs.values[i]
                    count_pb+=1
            pb_index = count_pb / sum

            value = 0

            if is_industry:
                value = count
            else:
                value = round(get_current_data()[index].last_price,2)

            series = pandas.Series([day.strftime('%Y/%m/%d'),value,round(pe_index,2),round(pb_index,2)], index=['date','value','pe','pb'])
            print(series)
            df = df.append(series,ignore_index=True)
    else:
        print('{0} 无数据'.format(path))
    if len(df) > 0:
        df.to_csv(path, sep='\t',columns=['date','value','pe','pb'],encoding='utf-8')
