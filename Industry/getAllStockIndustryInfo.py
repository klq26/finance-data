from jqdatasdk import *
from pandas import *
import numpy
import os
import sys

auth('13810650842','123456a')

index = '000016.XSHG'   # 注意：如果算上证指数，需要传入 000002.XSHG。因为 000001 包含 B 股，如 900923，900929 等

today = '2019-01-30'

industry_codes = ['HY001','HY002','HY003','HY004','HY005','HY006','HY007','HY008','HY009','HY010','HY011']
industry_names = ['能源','材料','工业','可选消费','必选消费','医药卫生','金融','信息技术','电信服务','公用事业','地产']

# 用来复制粘贴到命令行去使用的 code 值参考
indexs_list = ['000002.XSHG','000016.XSHG','000300.XSHG','000905.XSHG','000827.XSHG','000852.XSHG','000922.XSHG','000991.XSHG','000992.XSHG','399006.XSHE','399812.XSHE','399971.XSHE','399975.XSHE']

# 初始化行业信息（有缓存）
def initIndustryData(date=today):
    path = os.getcwd()+ '/IndustryData/JoinQuaintIndustry.txt'
    if os.path.exists(path):
        print('A股行业信息缓存文件存在..')
        return DataFrame.from_csv(path,sep='\t',encoding='utf-8')
    df = DataFrame(data=None,columns=['code','name','HY_CODE','HY_NAME'])
    totalCount = 0
    for i in range(0,len(industry_codes)):
        hycode = industry_codes[i]
        hyname = industry_names[i]
        print('整理行业：' + hyname)
        stockcodes = get_industry_stocks(hycode, date=date)
        stocknames = []
        print('成分股个数：{0}'.format(len(stockcodes)))
        totalCount += len(stockcodes)
        count = 0
        for code in stockcodes:
            count += 1
            print('{0} 进度：{1}%'.format(hyname,round(count/len(stockcodes)*100,2)))
            stocknames.append(get_security_info(code).display_name)
        indexs = range(0,len(stockcodes))
        hy = DataFrame(data=None,index=indexs,columns=['code','name','HY_CODE','HY_NAME'])
        hy['code'] = stockcodes
        hy['name'] = stocknames
        hy['HY_CODE'] = hycode
        hy['HY_NAME'] = hyname
        df = df.append(hy,ignore_index=True)
    df.to_csv(path, sep='\t',columns=['code','name','HY_CODE','HY_NAME'],encoding='utf-8')
    print('A股行业信息整理完毕，总数：{0}'.format(totalCount))
    return df

# 获取指数权重（有缓存）
def indexWeights(code,date=today):
    path = os.getcwd()+'/indexWeights/weight_{0}.txt'.format(code)
    if os.path.exists(path):
        print('{0} 权重信息缓存文件存在..'.format(code))
        return DataFrame.from_csv(path,sep='\t',encoding='utf-8')
    df = get_index_weights(code,date=date)
    df.to_csv(path, sep='\t',columns=['display_name','date','weight'],encoding='utf-8')
    return df

# ★运行★

if len(sys.argv) > 1:
    index = sys.argv[1]
    print(index)

industrys = initIndustryData(date=today)
print(index)
weights = indexWeights(index,date=today)  # https://www.joinquant.com/help/api/help?name=index 查询指数
#
hycodes = []    # 按指数顺序，取股票行业分类
hynames = []    # 按指数顺序，取股票行业分类
for code in weights.index.values:
    hy_info = industrys.loc[industrys['code'] == code]   # Series
    if len(hy_info) == 0:
        print('{0} 未找到行业数据'.format(code))
        hycodes.append('NA')
        hynames.append('NA')
        continue
    else:
        hycodes.append(hy_info.HY_CODE.values[0])
        hynames.append(hy_info.HY_NAME.values[0])
# 补充行业信息
weights['HY_CODE'] = hycodes
weights['HY_NAME'] = hynames
weights = weights.sort_values(by=['HY_CODE'])
#
for name in industry_names:
    hy_group = weights.loc[weights['HY_NAME'] == name]
    if len(hy_group) > 0:
        print('{0}\t{1}'.format(name,round(hy_group.weight.sum()/100,4)))
    else:
        print('{0}\t0'.format(name))
