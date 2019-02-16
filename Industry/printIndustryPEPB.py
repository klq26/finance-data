from jqdatasdk import *
from pandas import *
import datetime
import numpy
import os

auth('13810650842','123456a')

start_date = '2018-01-30'
end_date = '2019-02-16'

df = DataFrame()

industry_codes = ['HY001','HY002','HY003','HY004','HY005','HY006','HY007','HY008','HY010']  # HY007 + HY010 = 金融地产，HY009 基本没有公司

days = get_trade_days(start_date=start_date, end_date=end_date)
count = len(days)

array = list()

for code in industry_codes:
    path = os.getcwd() + '/IndustryData/{0}.csv'.format(code)
    if os.path.exists(path):
        df = DataFrame.from_csv(path, sep='\t',encoding='utf-8')
        array.append(df.tail(count))

file = open('result.txt','a+')

for i in range(0,count):
    string = ''
    for df in array:
        if string == '':
            string = string + df.date.values[i] + '\t'
        string = string + str(df.value.values[i]) + '\t'
        string = string + str(df.pe.values[i]) + '\t'
        string = string + str(df.pb.values[i]) + '\t'
    print(string)
    file.write(string + '\n')
file.close()
