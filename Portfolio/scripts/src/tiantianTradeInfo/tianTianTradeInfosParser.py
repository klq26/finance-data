# -*- coding: utf-8 -*-
import os
import json
from bs4 import BeautifulSoup

months = [x for x in range(1,13)]
years = [x for x in range(2017,2020)]
dates = []
for year in years:
    for month in months:
        if year == 2019 and month > 11:
            break
        if month < 10:
            mStr = u'0{0}'.format(month)
        else:
            mStr = str(month)
        dates.append(u'{0}-{1}-01'.format(year,mStr))


if os.path.exists(os.path.join(u'tiantianTradeInfo.txt')):
    os.remove(os.path.join(u'tiantianTradeInfo.txt'))

with open(os.path.join(u'tiantianTradeInfo.txt'),'a',encoding='utf-8') as outputFile:
    outputFile.write(u'交易发起日期\t产品名称\t产品代码\t业务类型\t申请数额\t申请单位\t确认数额\t确认单位\t链接\n')

    for i in range(1,len(dates)):
        StartDate = dates[i-1]
        EndDate = dates[i]
        with open(os.path.join(u'htmls', u'{0}_{1}.html'.format(StartDate,EndDate)),'r',encoding='utf-8') as htmlFile:
            soup = BeautifulSoup(htmlFile.read(),'lxml')

            dataList = soup.select('tr')
            # <tr class="" data-count="120">
            dataCount = soup.select('tr')[0].get('data-count')
            # 这里需要 dataCount 是因为如果用 select('tr')，为 0 的数据不会加入到 tr 数组，导致输出文件应该使用的命名错误
            if int(dataCount) > 0:
                for data in dataList:
                    date = data.select('td')[0].select('span')[0].text
                    name = data.select('td')[1].select('span')[0].text
                    code = data.select('td')[1].select('span')[1].text
                    operate = data.select('td')[2].text
                    cost = data.select('td')[3].text   # 申请数额
                    costUnit = data.select('td')[3].text[-1:len(cost)]    # 取最后一个字符，即单位（买入为元，卖出为份）
                    cost = cost[0:len(cost)-1]
                    gain = data.select('td')[4].text  # 确认数额
                    gainUnit = data.select('td')[4].text[-1:len(gain)]    # 取最后一个字符，即单位（买入为份，卖出为元）
                    gain = gain[0:len(gain)-1]
                    # 格式化数据
                    if code == '':
                        code = '------'
                    #if cost == '-':
                    #    cost = '0'
                    #if '-' in costUnit:
                    #    costUnit = '元'
                    #if gainUnit == '':
                    #    gainUnit = '-'
                    #state = data.select('td')[6].text
                    url = u'https://query.1234567.com.cn' + data.select('td')[7].select('a')[0].get('href')
                    #print(date,name,code,operate,cost,gain,state,url)
                    seq = u'\t'.join((date,name,code,operate,cost,costUnit,gain,gainUnit,url))
                    #print(seq)
                    outputFile.write(seq + '\n')
