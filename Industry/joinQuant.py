from jqdatasdk import *
from pandas import *
import numpy
import os

auth('13810650842','123456a')

index = '000905.XSHG'

date = '2018-09-30'
industry_codes = ['HY001','HY002','HY003','HY004','HY005','HY006','HY007','HY008','HY009','HY010','HY011']
industry_names = ['能源','材料','工业','可选消费','必选消费','医药卫生','金融','信息技术','电信服务','公用事业','地产']
# chuangyeban = get_index_weights('399006.XSHE',date=date)

# 初始化行业信息（有缓存）
def initIndustryData(data):
    if os.path.exists('IndustryData\JoinQuaintIndustry.txt'):
        return DataFrame.from_csv('IndustryData\JoinQuaintIndustry.txt',sep='\t',encoding='utf-8')
    df = DataFrame(data=None,columns=['code','name','HY_CODE','HY_NAME'])
    for i in range(0,len(industry_codes)):
        hycode = industry_codes[i]
        hyname = industry_names[i]
        print('整理行业：' + hyname)
        stockcodes = get_industry_stocks(hycode, date=date)
        stocknames = []
        for code in stockcodes:
            stocknames.append(get_security_info(code).display_name)
        indexs = range(0,len(stockcodes))
        hy = DataFrame(data=None,index=indexs,columns=['code','name','HY_CODE','HY_NAME'])
        hy['code'] = stockcodes
        hy['name'] = stocknames
        hy['HY_CODE'] = hycode
        hy['HY_NAME'] = hyname
        df = df.append(hy,ignore_index=True)
    df.to_csv('IndustryData\JoinQuaintIndustry.txt',sep='\t',columns=['code','name','HY_CODE','HY_NAME'],encoding='utf-8')
    return df

# 获取指数权重（有缓存）
def indexWeights(code,date):
    path = 'indexWeights\code_{0}.txt'.format(code)
    if os.path.exists(path):
        print('weight for {0} from cache.'.format(code))
        return DataFrame.from_csv(path,sep='\t',encoding='utf-8')
    df = get_index_weights(code,date=date)
    df.to_csv('indexWeights\code_{0}.txt'.format(code),sep='\t',columns=['display_name','date','weight'],encoding='utf-8')
    return df

# ★运行★
industrys = initIndustryData(date)
print(index)
weights = indexWeights(index)  # https://www.joinquant.com/help/api/help?name=index 查询指数

hycodes = []    # 按指数顺序，取股票行业分类
hynames = []    # 按指数顺序，取股票行业分类
for code in weights.index.values:
    hy_info = industrys.loc[industrys['code'] == code]   # Series
    hycodes.append(hy_info.HY_CODE.values[0])
    hynames.append(hy_info.HY_NAME.values[0])
# 补充行业信息
weights['HY_CODE'] = hycodes
weights['HY_NAME'] = hynames
weights = weights.sort_values(by=['HY_CODE'])

for name in industry_names:
    hy_group = weights.loc[weights['HY_NAME'] == name]
    print('{0}\t{1}'.format(name,round(hy_group.weight.sum()/100,4)))
