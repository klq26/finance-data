# -*- coding: utf-8 -*-

import re
import json
import time

from flask import Flask
from flask import request
from flask import Response

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import ssl

from indexModel import indexModel

app = Flask(__name__)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求指数数据 china asian euro america
# ////////////////////////////////////////////////////////////////////////////////////////
@app.route('/api/indexs', methods=['GET'])
def getIndexInfos():
    # 开始请求时间戳
    startTS = time.time()
    timeFormat = '%Y/%m/%d %H:%M:%S'
    startTime = time.strftime(timeFormat, time.localtime(startTS))
    print(startTime)
    area = request.args.get("area")
    # 可选区域
    areaGroup = ['china', 'asian', 'euro', 'america']
    if area == '' or area.lower() not in ['china', 'asian', 'euro', 'america']:
        # 结束时间
        endTS = time.time()
        endTime = time.strftime(timeFormat, time.localtime(endTS))
        duration = round(endTS - startTS, 4)
        result = {'code': -1, 'msg': '缺少 area 参数或参数无效。area 取值范围：{0}'.format(",".join(
            str(i) for i in areaGroup)), 'aliyun_date': endTime, 'duration': duration}
        return Response(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True), status=200, mimetype='application/json')
    else:
        # 结果
        result = ''
        response = ''
        if area.lower() == 'china':
            # 请求中国数据
            response = requestChinaIndexs()
        elif area.lower() == 'asian':
            # 请求亚洲数据
            response = requestAsianIndexs()
        elif area.lower() == 'euro':
            # 请求欧洲数据
            response = requestEuroIndexs()
        elif area.lower() == 'america':
            # 请求美洲数据
            response = requestAmericaIndexs()
        # 结束时间
        endTS = time.time()
        endTime = time.strftime(timeFormat, time.localtime(endTS))
        duration = round(endTS - startTS, 4)
        result = {'code': 0, 'msg': 'success', 'data': response,
            'aliyun_date': endTime, 'duration': duration}
        return Response(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True), status=200, mimetype='application/json')
    pass

# 请求中国
def requestChinaIndexs():
    url = "http://10.push2.eastmoney.com/api/qt/clist/get?cb=updateIndexInfos&pn=1&pz=30&fs=i:1.000832,i:1.000001,i:0.399001,i:0.399006,i:1.000015,i:1.000922,i:1.000016,i:1.000300,i:0.399905,i:1.000842,i:1.000852,i:0.399005,i:1.000991,i:1.000992,i:0.399975,i:0.399986,i:0.399812,i:0.399971,i:1.000827,i:100.HSI,i:100.HSCEI,i:124.HSCCI&fields=f14,f12,f2,f4,f3,f18,f6"
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        print(response.text)
        result = response.text.replace(
            'updateIndexInfos(', '').replace(');', '')
        # 清洗&重组数据
        return purgeChinaIndexs(json.loads(result))
    else:
        print('error')
        return 'error: {0}'.format(response.status_code)
    pass

# # 清洗&重组中国数据
def purgeChinaIndexs(jsonData):
    return purgeEastmoney100Data(jsonData,u'中国')

# 请求亚洲
def requestAsianIndexs():
    url = "http://87.push2.eastmoney.com/api/qt/ulist.np/get?cb=updateIndexInfos&np=1&pi=0&pz=40&po=1&secids=100.TWII%2C100.N225%2C100.KS11%2C100.STI%2C100.SENSEX&fields=f14,f12,f2,f4,f3,f18,f6"
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        print(response.text)
        result = response.text.replace('updateIndexInfos(','').replace(');','')
        # 清洗&重组数据
        return purgeAsianIndexs(json.loads(result))
    else:
        print('error')
        return 'error: {0}'.format(response.status_code)
    pass

# # 清洗&重组亚洲数据
def purgeAsianIndexs(jsonData):
    return purgeEastmoney87Data(jsonData,u'亚洲')

# 请求欧洲
def requestEuroIndexs():
    url = "http://87.push2.eastmoney.com/api/qt/ulist.np/get?cb=updateIndexInfos&np=1&pi=0&pz=40&po=1&secids=100.FTSE%2C100.FCHI%2C100.GDAXI%2C100.RTS&fields=f14,f12,f2,f4,f3,f18,f6"
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        print(response.text)
        result = response.text.replace('updateIndexInfos(','').replace(');','')
        # 清洗&重组数据
        return purgeEuroIndexs(json.loads(result))
    else:
        print('error')
        return 'error: {0}'.format(response.status_code)
    pass

# # 清洗&重组中国数据
def purgeEuroIndexs(jsonData):
    return purgeEastmoney87Data(jsonData,u'欧洲')

# 请求美洲
def requestAmericaIndexs():
    url = "http://87.push2.eastmoney.com/api/qt/ulist.np/get?cb=updateIndexInfos&np=1&pi=0&pz=40&po=1&secids=100.DJIA%2C100.NDX%2C100.SPX%2C107.XOP&fields=f14,f12,f2,f4,f3,f18,f6"
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        print(response.text)
        result = response.text.replace('updateIndexInfos(','').replace(');','')
        # 清洗&重组数据
        return purgeAmericaIndexs(json.loads(result))
    else:
        print('error')
        return 'error: {0}'.format(response.status_code)
    pass

# 清洗&重组美洲数据
def purgeAmericaIndexs(jsonData):
    return purgeEastmoney87Data(jsonData,u'美洲')

# 清洗东方财富亚洲数据（100.eastmoney）
def purgeEastmoney100Data(jsonData, indexArea):
    datalist = jsonData['data']['diff']
    print(datalist)
    result = []
    for key in datalist.keys():
        item = datalist[key]
        index = indexModel()
        index.indexCode = item['f12']
        index.indexName = item['f14'].replace(' ','')
        index.indexArea = indexArea
        index.sequence = int(key)
        index.current = round(float(item['f2'])/100, 2)
        index.lastClose = round(float(item['f18'])/100, 2)
        index.dailyChangRate = '{0:.2f}%'.format(
            round(float(item['f3'])/100, 2))
        index.dailyChangValue = round(float(item['f4'])/100, 2)
        index.dealMoney = round(float(item['f6']), 2)
        result.append(index.__dict__)
    return result

# 清洗东方财富欧美数据（87.eastmoney）
def purgeEastmoney87Data(jsonData, indexArea):
    datalist = jsonData['data']['diff']
    print(datalist)
    result = []
    count = 0
    # {"f2":1129217,"f3":-124,"f4":-14145,"f6":0.0,"f12":"TWII","f14":"台湾加权","f18":1143362}
    for item in datalist:
        index = indexModel()
        index.indexCode = item['f12']
        index.indexName = item['f14']
        if index.indexName.find(u'新加坡') > 0:
            index.indexName = '新加坡STI'
        if index.indexName == "印度孟买SENSEX":
            index.indexName = '印度SENSEX'
        if index.indexName.find(u'S&P') > 0:
            index.indexName = '油气XOP'
        if index.indexName.find(u'离岸') > 0:
            index.indexName = u'离岸人民币'
        index.indexArea = indexArea
        index.sequence = count
        if index.indexName == u'离岸人民币':
            index.current = round(float(item['f2'])/10000,4)
            index.lastClose = round(float(item['f18'])/10000,4)
            index.dailyChangValue = round(float(item['f4'])/10000,4)
        else:
            index.current = round(float(item['f2'])/100,2)
            index.lastClose = round(float(item['f18'])/100,2)
            index.dailyChangValue = round(float(item['f4'])/100,2)           
        index.dailyChangRate = '{0:.2f}%'.format(round(float(item['f3'])/100,2))
        index.dealMoney = round(float(item['f6']),2)
        result.append(index.__dict__)
        count = count + 1
    return result

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求期货&外汇数据
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/goods_and_exchanges', methods=['GET'])
def getGoodsAndExchangeInfo():
    # 开始请求时间戳
    startTS = time.time()
    timeFormat = '%Y/%m/%d %H:%M:%S'
    startTime = time.strftime(timeFormat, time.localtime(startTS))
    print(startTime)
    # 离岸人民币 url
    url_USDCNH = "http://87.push2.eastmoney.com/api/qt/ulist.np/get?cb=updateIndexInfos&np=1&pi=0&pz=40&po=1&secids=133.USDCNH&fields=f14,f12,f2,f4,f3,f18,f6"
    # 离岸人民币
    USDCNH = ''
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url_USDCNH, headers=headers, verify=False)
    if response.status_code == 200:
        # print(response.text)
        result = response.text.replace('updateIndexInfos(', '').replace(');', '')
        # 清洗&重组数据
        USDCNH = purgeEastmoney87Data(json.loads(result),'外汇')[0]
        # print(USDCNH)
    # 期货及其他外汇
    url = "https://hq.sinajs.cn/?list=hf_CHA50CFD,hf_GC,hf_SI,hf_CL,USDCNY,CADCNY,GBPCNY,EURCNY,AUDCNY,HKDCNY,TWDCNY,fx_sjpycny,fx_skrwcny"
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        # print(response.text)
        results = purgeGoodsAndExchanges(response.text)
        # 插入离岸人民币
        results.insert(4,USDCNH)
        # 分组（goods & exchanges）
        goods = results[0:4]
        for i in range(0,len(goods)):
            goods[i]['sequence'] = i
        exchanges = results[4:len(results)]
        for i in range(0,len(exchanges)):
            exchanges[i]['sequence'] = i
        # 结束时间
        endTS = time.time()
        endTime = time.strftime(timeFormat, time.localtime(endTS))
        duration = round(endTS - startTS, 4)
        result = {'code': 0, 'msg': 'success', 'data': {'goods': goods, 'exchanges':exchanges},
            'aliyun_date': endTime, 'duration': duration}
        return Response(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True), status=200, mimetype='application/json')
    else:
        result = {'code': -1, 'msg': '请求错误，该请求不带任何参数', 'aliyun_date': endTime, 'duration': duration}
        # 结束时间
        endTS = time.time()
        endTime = time.strftime(timeFormat, time.localtime(endTS))
        duration = round(endTS - startTS, 4)
        return Response(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True), status=200, mimetype='application/json')
    pass

# 清洗&重组期货和外汇数据
def purgeGoodsAndExchanges(data):
    exchanges = data.split(';')
    # 接口返回的最后一项是个 '\n'
    exchanges.pop(-1)
    # 期货
    # goodKeys = ['hf_CHA50CFD', 'hf_GC', 'hf_SI', 'hf_CL']
    # 外汇
    exchangeKeys = ['USDCNY', 'CADCNY', 'GBPCNY', 'EURCNY', 'AUDCNY', 'HKDCNY', 'TWDCNY','fx_sjpycny', 'fx_skrwcny']
    # 结果
    results = []
    # 正则匹配集
    rawlist = []
    # 正则匹配
    pattern = re.compile('var hq_str_(.*?)="(.*?)"')
    for item in exchanges:
        # print(item)
        result = re.findall(pattern, item)
        if len(result) > 0:
            rawlist.append(result[0])
    # 清洗正则匹配集，产出最终数据
    count = 0
    for item in rawlist:
        index = indexModel()
        # 数据集合
        values = item[1].split(',')
        # 代码
        indexCode = item[0].replace('hf_', '')
        if indexCode in exchangeKeys:
            # 外汇
            # 日元人民币
            if indexCode == 'fx_sjpycny':
                indexCode = 'JPYCNY'
                indexName = '日元人民币'
            # 韩元人民币
            elif indexCode == 'fx_skrwcny':
                indexCode = 'KRWCNY'
                indexName = '韩元人民币'
            else:
                indexCode = item[0].replace('hf_', '')
                indexName = values[9]
            index.indexCode = indexCode
            index.indexName = indexName
            index.indexArea = '外汇'

            index.current = round(float(values[2]), 4)
            index.lastClose = round(float(values[3]), 4)
            index.dailyChangRate = '{0:.2f}%'.format(
                round(float((index.current / index.lastClose - 1) * 100), 2))
            index.dailyChangValue = round(float(index.current - index.lastClose), 4)
            index.dealMoney = 0.0
            index.sequence = count
            count = count + 1
        else:
            # 期货
            index.indexCode = item[0].replace('hf_', '')
            if item[0] == 'hf_CHA50CFD':
                index.indexName = '富时A50'
            else:
                index.indexName = values[-1]
            index.indexArea = '期货'
            index.current = round(float(values[0]), 3)
            index.lastClose = round(float(values[7]), 3)
            index.dailyChangRate = '{0:.2f}%'.format(
                round(float((index.current / index.lastClose - 1) * 100), 2))
            index.dailyChangValue = round(float(index.current - index.lastClose), 3)
            index.dealMoney = 0.0
            index.sequence = count
            count = count + 1
        results.append(index.__dict__)
    return results

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求资金数据（两市成交额，融资融券，两市资金净流入，沪港通，沪深通净流入）
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/moneyinfo', methods=['GET'])
def getMoneyInfo():
    # 开始请求时间戳
    startTS = time.time()
    timeFormat = '%Y/%m/%d %H:%M:%S'
    startTime = time.strftime(timeFormat, time.localtime(startTS))
    # 请求中国沪深两市日成交额
    inlandDealMoney_url = "https://hq.sinajs.cn/?list=sh000002,sz399107"
    # 融资融券数据
    rzrq_url = "http://api.dataide.eastmoney.com/data/get_rzrq_lshj?orderby=dim_date&order=desc&pageindex=1&pagesize=240"
    # 沪深两市资金情况. http://data.eastmoney.com/zjlx/
    inlandMoneyFlow_url = "http://push2.eastmoney.com/api/qt/stock/fflow/kline/get?lmt=0&klt=1&secid=1.000001&secid2=0.399001&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&cb=updateMoneyFlow"
    # 沪港通，深港通南北向资金情况 http://data.eastmoney.com/hsgt/index.html
    hongkongMoneyFlow_url = "http://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55,f56&cb=updateHKMoneyFlow"

    # 各部分数据
    inlandDealMoneyData = []
    rzrqData = []
    inlandMoneyFlowData = []
    hongkongS2NFlowData = []
    hongkongN2SFlowData = []
    # 最终结果
    finalResult = []

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
    # 沪深两市成交额（亿）【Finish】
    response = requests.get(inlandDealMoney_url, headers=headers, verify=False)
    if response.status_code == 200:
        # print(response.text)
        # purge
        indexInfos = response.text.split(';')
        # 接口返回的最后一项是个 '\n'
        indexInfos.pop(-1)
        shanghaiDealMoney = 0
        shenzhenDealMoney = 0
        pattern = re.compile('var hq_str_(.*?)="(.*?)"')
        for item in indexInfos:
            # print(item)
            result = re.findall(pattern, item)
            if len(result) > 0:
                if result[0][0] == 'sh000002':
                    values = result[0][1].split(',')
                    shanghaiDealMoney = round(float(result[0][1].split(',')[9]) / 100000000,1)
                elif result[0][0] == 'sz399107':
                    shenzhenDealMoney = round(float(result[0][1].split(',')[9]) / 100000000,1)
        totalDealMoney = shanghaiDealMoney + shenzhenDealMoney
        # 结果
        inlandDealMoneyData = [{'name' : '沪', 'value' : shanghaiDealMoney},{'name' : '深', 'value' : shenzhenDealMoney},{'name' : '总', 'value' : totalDealMoney}]
        # print(inlandDealMoneyData)
        finalResult.append({'name':'沪深两市成交额（亿）','symbol':'hslscje', 'value':inlandDealMoneyData})

    # 融资融券余额（亿）
    response = requests.get(rzrq_url, headers=headers, verify=False)
    if response.status_code == 200:
        # print(response.text)
        jsonData = json.loads(response.text)
        if jsonData['data'] and len(jsonData['data']) > 0:
            lastestData = jsonData['data'][0]
            ts = int(lastestData['dim_date'])/1000  # python 只处理秒
            timeTuple = time.localtime(ts)
            rzrqyeDate = time.strftime("%Y-%m-%d", timeTuple)
            rzrqyeValue = round(lastestData['rzrqye']/(10000 * 10000), 1)
            rzyeValue = round(lastestData['rzye']/(10000 * 10000), 1)
            rqyeValue = round(lastestData['rqye']/(10000 * 10000), 1)
            
            rzrqData.append({'name' : '资', 'value' : rzyeValue})
            rzrqData.append({'name' : '券', 'value' : rqyeValue})
            rzrqData.append({'name' : '总', 'value' : rzrqyeValue})
            # print(rzrqData)
        finalResult.append({'name':'融资融券余额（亿）','symbol':'rzrqye', 'value':rzrqData})
    # 沪深资金净流入（亿）【Finish】
    response = requests.get(inlandMoneyFlow_url, headers=headers, verify=False)
    if response.status_code == 200:
        # print(response.text)
        data = response.text.replace('updateMoneyFlow(','').replace(');','')
        jsonData = json.loads(data)
        klines = jsonData["data"]["klines"]
        lastestData = klines[-1].split(',')
        # print(lastestData)
        # 取值
        # ["2020-02-21 15:00", "-25845607550.0", "27224361803.0", "-1378753893.0", "-18919648215.0", "-6925959335.0"]
        # 时间，主力净流入（亿），小单净流入（亿），中单净流入（亿），大单净流入（亿），超大单净流入（亿）,都要除以 100000000
        sequencesIndex = [2, 3, 1, 4, 5]
        sequencesName = ['小','中','主','大','特']
        nameIdx = 0
        for idx in sequencesIndex:
            num = round(float(lastestData[idx]) / 100000000,1)
            if num > 0:
                num = '+{0}'.format(num)
            else:
                num = '{0}'.format(num)
            inlandMoneyFlowData.append({'name' : sequencesName[nameIdx], 'value' : num})
            nameIdx = nameIdx + 1
        # print(inlandMoneyFlowData)
        finalResult.append({'name':'沪深资金净流入（亿）','symbol':'hszjjlr', 'value':inlandMoneyFlowData})

    # 北向资金净流入（亿）  南向资金净流入（亿） 【Finish】
    response = requests.get(hongkongMoneyFlow_url, headers=headers, verify=False)
    if response.status_code == 200:
        # print(response.text)
        data = response.text.replace('updateHKMoneyFlow(','').replace(');','')
        jsonData = json.loads(data)
        # ["15:00", "-88205.65", "5288205.65", "273623.63", "4926376.37", "185417.98"]
        # 时间，沪股通净流入（万），余额（万），深股通净流入（万），余额（万），两市净流入（万）
        sequencesIndex = [1, 3, 5]
        sequencesName = ['沪','深','总']
        # 北向资金
        S2N = jsonData["data"]["s2n"]
        lastestS2N = 0
        for item in S2N:
            dataInfo = item.split(",")
            if dataInfo[1] == '-':
                break
            lastestS2N = dataInfo
        # 赋值
        nameIdx = 0
        for idx in sequencesIndex:
            num = round(float(lastestS2N[idx]) / 10000,1)
            if num > 0:
                num = '+{0}'.format(num)
            else:
                num = '{0}'.format(num)
            hongkongS2NFlowData.append({'name' : sequencesName[nameIdx], 'value' : num})
            nameIdx = nameIdx + 1
        # print(hongkongS2NFlowData)
        finalResult.append({'name':'北向资金净流入（亿）','symbol':'bxzjjlr', 'value':hongkongS2NFlowData})
        # 南向资金
        N2S = jsonData["data"]["n2s"]
        lastestN2S = 0
        for item in N2S:
            dataInfo = item.split(",")
            if dataInfo[1] == '-':
                break
            lastestN2S = dataInfo
        nameIdx = 0
        for idx in sequencesIndex:
            num = round(float(lastestN2S[idx]) / 10000,1)
            if num > 0:
                num = '+{0}'.format(num)
            else:
                num = '{0}'.format(num)
            hongkongN2SFlowData.append({'name' : sequencesName[nameIdx], 'value' : num})
            nameIdx = nameIdx + 1
        # print(hongkongN2SFlowData)
        finalResult.append({'name':'南向资金净流入（亿）','symbol':'nxzjjlr', 'value':hongkongN2SFlowData})
    # 结束时间
    endTS = time.time()
    endTime = time.strftime(timeFormat, time.localtime(endTS))
    duration = round(endTS - startTS, 4)
    result = {'code': 0, 'msg': 'success', 'data': finalResult, 'aliyun_date': endTime, 'duration': duration}
    return Response(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True), status=200, mimetype='application/json')
    # return (json.dumps(finalResult, ensure_ascii=False, sort_keys=True, indent=4))

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求 A 股涨跌平数据
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/zdpinfo', methods=['GET'])
def getZDPInfo():
    # 开始请求时间戳
    startTS = time.time()
    timeFormat = '%Y/%m/%d %H:%M:%S'
    startTime = time.strftime(timeFormat, time.localtime(startTS))

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
    ssl._create_default_https_context = ssl._create_unverified_context
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # 涨跌分布（涨停 -> 5% -> 0 -> -5% -> 跌停）
    zdfb_url = u'http://q.10jqka.com.cn/api.php?t=indexflash'
    response = requests.get(zdfb_url, headers=headers, verify=False)
    finalResult = []
    if response.status_code == 200:
        jsonData = json.loads(response.text)
        arr = jsonData['zdfb_data']['zdfb']
        finalResult.append({'name' : '涨跌分布','symbol' : 'zdfb', 'value' : list(reversed(jsonData['zdfb_data']['zdfb']))})
        finalResult.append({'name' : '涨跌停','symbol' : 'zdt', 'value' : [{'name' : '涨停','symbol' : 'zt', 'value' : jsonData['zdt_data']['last_zdt']['ztzs']},{'name' : '跌停','symbol' : 'dt', 'value' : jsonData['zdt_data']['last_zdt']['dtzs']}]})

    # 指数涨跌平数据(例如:涨:10 平:3 跌:37)
    zdp_url = "https://hq.sinajs.cn/list=sh000002_zdp,sz399107_zdp,sh000003_zdp,sz399108_zdp,sz399102_zdp,sh000016_zdp,sh000300_zdp,sz399905_zdp,sh000852_zdp,sh000842_zdp"
    response = requests.get(zdp_url, headers=headers, verify=False)
    if response.status_code == 200:
        # print(response.text)
        zdpRawData = response.text.split(';')
        # 接口返回的最后一项是个 '\n'
        zdpRawData.pop(-1)
        # 结果集
        results = []
        # 正则匹配集
        rawlist = []
        # 正则匹配
        pattern = re.compile('var hq_str_(.*?)_zdp="(.*?)"')
        for item in zdpRawData:
            # print(item)
            result = re.findall(pattern, item)
            if len(result) > 0:
                rawlist.append(result[0])
        # // e.g.
        # // var hq_str_sh000002_zdp="865,535,97";    沪A
        # // var hq_str_sz399107_zdp="1396,702,95";   深A
        # // var hq_str_sh000003_zdp="26,14,9";       沪B
        # // var hq_str_sz399108_zdp="13,26,7";       深B
        # // var hq_str_sz399102_zdp="559,217,15";    创业
        
        #[('sh000002', '76,1416,5'), ('sz399107', '144,2044,8'), ('sh000003', '1,48,0'), ('sz399108', '3,41,2'), ('sz399102', '48,745,1'), ('sh000016', '2,48,0'), ('sh000300', '17,283,0'), ('sz399905', '20,480,0'), ('sh000852', '54,941,5'), ('sh000842', '37,763,0')]
        allMarkets = ['sh000002','sh000003','sz399107','sz399108']
        indexMapping = {'sz399102':'创业板综','sh000016':'上证50','sh000300':'沪深300','sz399905':'中证500','sh000852':'中证1000','sh000842':'等权800'}
        allUp = 0
        allEqual = 0
        allDown = 0
        for item in rawlist:
            values = item[1].split(',')
            if item[0] in allMarkets:
                allUp = allUp + int(values[0])
                allEqual = allEqual + int(values[2])
                allDown = allDown + int(values[1])
            else:
                name = indexMapping[item[0]]
                up = int(values[0])
                equal = int(values[2])
                down = int(values[1])
                results.append({'name' : name, 'symbol' : item[0], 'z':up, 'p':equal, 'd':down})
        results.insert(0, {'name' : '全市场', 'symbol' : 'all', 'z':allUp, 'p':allEqual, 'd':allDown})
        # print(results)
        finalResult.append({'name' : '指数涨跌平','symbol' : 'zdp', 'value' : results})
    # 结束时间
    endTS = time.time()
    endTime = time.strftime(timeFormat, time.localtime(endTS))
    duration = round(endTS - startTS, 4)
    result = {'code': 0, 'msg': 'success', 'data': finalResult, 'aliyun_date': endTime, 'duration': duration}
    return Response(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True), status=200, mimetype='application/json')

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求债券数据
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/bondinfo', methods=['GET'])
def getBondInfo():
    # 开始请求时间戳
    startTS = time.time()
    timeFormat = '%Y/%m/%d %H:%M:%S'
    startTime = time.strftime(timeFormat, time.localtime(startTS))

    finalResult = []

    ssl._create_default_https_context = ssl._create_unverified_context
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # # 债券指数（国债，企业债）
    # url = "http://10.push2.eastmoney.com/api/qt/clist/get?cb=updateIndexInfos&pn=1&pz=30&fs=i:1.000012,i:1.000013&fields=f14,f12,f2,f4,f3,f18,f6"
    # response = requests.get(url, headers=headers, verify=False)
    # if response.status_code == 200:
    #     # print(response.text)
    #     result = response.text.replace(
    #         'updateIndexInfos(', '').replace(');', '')
    #     # 清洗&重组数据
    #     indexs = purgeEastmoney100Data(json.loads(result),u'债券')
    #     finalResult.append({'name': '债券指数', 'symbol' : 'bondIndex', 'value' : indexs})

    # 货币基金
    url = "https://danjuanapp.com/djapi/fund/003474"
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        # print(response.text)
        data = json.loads(response.text)['data']
        # 清洗&重组数据
        current = '{0}%'.format(round(float(data['fund_derived']['annual_yield7d']),2))
        value = { 'indexName' : u'天天利B', 'indexCode' : '003474','indexArea' : '货基', 'sequence' : 0, 'current' : current, 'lastClose' : current,'dailyChangeValue' : 0.000, 'dealMoney' : 0.000, 'dailyChangRate' : '0.00%'}
        finalResult.append({'name': '货币基金', 'symbol' : 'fund', 'value' : [value]})

    # 钉钉宝90 钉钉宝365 稳稳的幸福
    urlPrefix = u'https://danjuanapp.com/djapi/plan/'
    urls = ['CSI1021','CSI1019','CSI1014']
    plans = []
    count = 0
    for code in urls:
        url = urlPrefix + code
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            # print(response.text)
            data = json.loads(response.text)['data']
            # index = indexModel()
            name = data['plan_name']
            if u'稳稳' in name:
                name = '稳稳的幸福'
            if u'90' in name:
                name = '钉钉宝90'
            if u'365' in name:
                name = '钉钉宝365'
            current = '{0}%'.format(round(float(round(float(data['yield_middle']),2)),2))
            value = { 'indexName' : name, 'indexCode' : data['plan_code'],'indexArea' : '组合', 'sequence' : count, 'current' : current, 'lastClose' : current,'dailyChangeValue' : 0.000, 'dealMoney' : 0.000, 'dailyChangRate' : '0.00%'}
            count = count + 1
            plans.append(value)
    finalResult.append({'name': '混合债券', 'symbol' : 'plan', 'value' : plans})

    # 财政部国债债券信息
    url = u'http://yield.chinabond.com.cn/cbweb-czb-web/czb/czbChartSearch'
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        jsonData = json.loads(response.text)
        # print(jsonData)
        workDate = jsonData['worktime']
        # 5 7 10 年国债
        bond5year = 0.0
        bond7year = 0.0
        bond10year = 0.0
        values = jsonData['seriesData']
        for valueArray in values:
            if valueArray[0] == 5.0:
                bond5year = '{0}%'.format(round(float(valueArray[1]),2))
            elif valueArray[0] == 7.0:
                bond7year = '{0}%'.format(round(float(valueArray[1]),2))
            elif valueArray[0] == 10.0:
                bond10year = '{0}%'.format(round(float(valueArray[1]),2))
        result5year = { 'indexName' : u'5年期国债', 'indexCode' : '5YEAR','indexArea' : '债券', 'sequence' : 0, 'current' : bond5year, 'lastClose' : bond5year,'dailyChangeValue' : 0.000, 'dealMoney' : 0.000, 'dailyChangRate' : '0.00%', 'year' : 5}
        result7year = { 'indexName' : u'7年期国债', 'indexCode' : '7YEAR','indexArea' : '债券', 'sequence' : 1, 'current' : bond7year, 'lastClose' : bond7year,'dailyChangeValue' : 0.000, 'dealMoney' : 0.000, 'dailyChangRate' : '0.00%', 'year' : 7}
        result10year = { 'indexName' : u'10年期国债', 'indexCode' : '10YEAR','indexArea' : '债券', 'sequence' : 2, 'current' : bond10year, 'lastClose' : bond10year,'dailyChangeValue' : 0.000, 'dealMoney' : 0.000, 'dailyChangRate' : '0.00%', 'year' : 10}

        finalResult.append({'name': '国债', 'symbol' : 'bond', 'value' : [result5year, result7year, result10year]})
    # 结束时间
    endTS = time.time()
    endTime = time.strftime(timeFormat, time.localtime(endTS))
    duration = round(endTS - startTS, 4)
    result = {'code': 0, 'msg': 'success', 'data': finalResult, 'aliyun_date': endTime, 'duration': duration}
    return Response(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True), status=200, mimetype='application/json')
    pass

@app.route('/api/today', methods=['GET'])
def dayType():
    # 开始请求时间戳
    startTS = time.time()
    timeFormat = '%Y/%m/%d %H:%M:%S'
    startTime = time.strftime(timeFormat, time.localtime(startTS))

    today = time.strftime('%Y%m%d', time.localtime())
    url = "http://www.easybots.cn/api/holiday.php?d=" + today
    response = requests.get(url, headers=headers, verify=False)
    jsonData = json.loads(response.text)
    dayType = jsonData[today]
    print(dayType, jsonData)
    weekday = '0'
    weekend = '0'
    holiday = '0'
    if dayType == '0':
        weekday = '1'
        weekend = '0'
        holiday = '0'
    elif dayType == '1':
        weekday = '0'
        weekend = '1'
        holiday = '0'
    elif dayType == '2':
        weekday = '0'
        weekend = '0'
        holiday = '1'
    jsonData = {'weekday' : weekday, 'weekend' : weekend, 'holiday' : holiday }
    # 结束时间
    endTS = time.time()
    endTime = time.strftime(timeFormat, time.localtime(endTS))
    duration = round(endTS - startTS, 4)
    result = {'code': 0, 'msg': 'success', 'data': jsonData, 'aliyun_date': endTime, 'duration': duration}
    return Response(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True), status=200, mimetype='application/json')

# debug
if __name__ == '__main__':
    app.run(port=5000)
