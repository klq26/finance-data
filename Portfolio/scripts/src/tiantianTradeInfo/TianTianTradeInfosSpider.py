# -*- coding: utf-8 -*-
import os
import json
import requests
from bs4 import BeautifulSoup

from urllib.parse import urlencode

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

cookie = u'Cookie: st_si=48193464463530; st_asi=delete; b_p_log_key=UXRF8fAgsvU1SArYSDZb1vNi/JgRlELFdZEJcyP6AshghN+GTGQZhKJmUzB8WTAY5eYgy3QDKWSkjTh6709wxqrYbnqGW8s/gMglTQ0MCnP4PcCtIi4=; b_pl_bq=de9612a5f90c4a9bab2a853807e9822c; FundTradeLoginTab=0; FundTradeLoginCard=0; st_pvi=69416177127426; st_sp=2019-08-25%2008%3A06%3A30; st_inirUrl=https%3A%2F%2Ftrade7.1234567.com.cn%2FQuery%2Fbill; st_sn=36; st_psi=20191030163723516-112200304021-0615596360; cp_token=037bb6d4002c4f4cacb9d9dea671bc93; FundTradeLoginUser=Y0aJHHQxhKGx5+sZUxu7v5i1tMPtnu3fyAKvCqZ9ONP1lCrvNWNc0xWGQMF0O8IU6wul6rBu; fund_trade_cn=Yu9occN+NBmPD0KGMY4Rb1EepzvmuhhVv50mTfm2lotj/fVEW03adqR5CkD9IJFIcKMIvGCMj1PcLZ+IW/vQWt24PyyCuJJRheUAh2g/Oya3uf6L/iM=; fund_trade_name=Yqf8Zv5PGKQoD2XwIEuglB7B7vZtRgTYx/gRCxjB0bXCACOV2gfGbNWaGBWegE+U5NktRjWz; fund_trade_visitor=YE4ZLbkxHKAnxl7eUxuhdRwU1GittX7TjCKRCvMvHky6oC70yaYhMtWWouiFrsCUotOKjaxc; fund_trade_risk=YsPOpTEiaKP1wBtidQufmxnYS0at/xzHL3caCWG2pRIC/C6lra5G49W5o2u3OTTUAxsIvPFV; fund_trade_gps=6; VipLevel=1; TradeLoginToken=b4307c2912244f71b752c497a1c10cb4; UTOKEN=Yu9occN+NBmPD0KGMY4Rb1EepzvmuhhVv50mTfm2lotj/fVEW03adqR5CkD9IJFIcKMIviCp1dvsvspCYdRIWjA0g4W3EwtaOBUPH+hf+uiKuT4Q8UQ=; LToken=55a907064ec4425290e55a79ec2e2238; fund_trade_trackid=exlaI1s/9a4ElDO1SerZiGln5+wVJJBNEn5AQW3OfG1wFIf52h+hx+buUDrKBDTqv1XkDMeEkO1iM42SlRFQVQ=='

urlPrefix = u'https://query.1234567.com.cn/Query/DelegateList?'

# 参数举例
# DataType=1&StartDate=2019-09-30&EndDate=2019-10-30&BusType=0&Statu=2&FundType=0&PageSize=20&PageIndex=1&Container=tb_delegate&IsHistory=false

# 参数
params = {}
params[u'DataType'] = 1
#params[u'StartDate'] = '2019-09-30'
#params[u'EndDate'] = '2019-10-30' 
params[u'BusType'] = 0
params[u'Statu'] = 2    # 状态 == 成功
params[u'FundType'] = 0
params[u'PageSize'] = 240
params[u'PageIndex'] = 1
params[u'Container'] = u'tb_delegate'
params[u'IsHistory'] = 'false'  # 2016年10月之前，这里是 'true'
#result = urlencode(params)

headers = {'Cookie' : cookie}

for i in range(1,len(dates)):
    StartDate = dates[i-1]
    EndDate = dates[i]
    params[u'StartDate'] = StartDate    # '2019-09-30'
    params[u'EndDate'] = EndDate        # '2019-10-30' 
    urlParams = urlencode(params)
    url = urlPrefix + urlParams
    response = requests.post(url, headers = headers)
    if response.status_code == 200:
        with open(os.path.join(u'htmls', u'{0}_{1}.html'.format(StartDate,EndDate)),'w',encoding='utf-8') as htmlFile:
            htmlFile.write(response.text)
    else:
        print('[ERROR] 请求失败：{0} URL = {1}'.format(response.status_code,url))
