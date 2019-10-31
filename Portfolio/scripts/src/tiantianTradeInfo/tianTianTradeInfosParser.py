# -*- coding: utf-8 -*-
import os
import sys
import json
from bs4 import BeautifulSoup

# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
sys.path.append(srcDir)
#for p in sys.path:
#    print(p)
from config.pathManager import pathManager
from tiantianTradeInfoModel import tiantianTradeInfoModel

class tiantianTradeInfosParser:

    def __init__(self, strategy='a'):
        self.pm = pathManager()
        # strategy
        if strategy == 'a':
            self.userName = u'康力泉'
        if strategy == 'b':
            self.userName = u'李淑云'
        if strategy == 'c':
            self.userName = u'康世海'
        self.dataFolder = os.path.join(self.pm.outputPath, u'tiantianTradeInfos',u'htmls', self.userName)
        self.tradeInfosOutputPath = os.path.join(self.pm.outputPath, u'tiantianTradeInfos',u'data', self.userName)
        if not os.path.exists(self.tradeInfosOutputPath):
            os.makedirs(self.tradeInfosOutputPath)
        self.filepaths = []
        for root, dirs, files in os.walk(self.dataFolder, topdown=False):
            for name in files:
                self.filepaths.append(os.path.join(root,name))
        self.modelArray = []
        
    def loadData(self):
        for filepath in self.filepaths:
            with open(filepath, 'r', encoding='utf-8') as htmlFile:
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
                        #state = data.select('td')[6].text
                        url = u'https://query.1234567.com.cn' + data.select('td')[7].select('a')[0].get('href')
                        # 模型
                        model = tiantianTradeInfoModel()
                        model.date = date
                        model.year = date[0:4]  # 年份
                        month = int(date[5:7])       # 月份
                        if month in [1,2,3]:
                            model.quarter = 'Q1'
                        if month in [4,5,6]:
                            model.quarter = 'Q2'
                        if month in [7,8,9]:
                            model.quarter = 'Q3'
                        if month in [10,11,12]:
                            model.quarter = 'Q4'
                        model.name = name
                        model.code = code
                        model.operate = operate
                        model.cost = cost
                        model.costUnit = costUnit
                        model.gain = gain
                        model.gainUnit = gainUnit
                        model.url = url
                        self.modelArray.append(model)

    def outputToText(self):
        if os.path.exists(os.path.join(self.tradeInfosOutputPath, u'tiantianTradeInfosData.txt')):
            os.remove(os.path.join(self.tradeInfosOutputPath, u'tiantianTradeInfosData.txt'))
        with open(os.path.join(self.tradeInfosOutputPath, u'tiantianTradeInfosData.txt'),'a',encoding='utf-8') as outputFile:
            outputFile.write(u'交易发起日期\t年\t季度\t产品名称\t产品代码\t业务类型\t申请数额\t申请单位\t确认数额\t确认单位\t链接\n')
            for model in self.modelArray:
                outputFile.write(model.__str__() + '\n')
        
    def outputToJson(self):
        if os.path.exists(os.path.join(self.tradeInfosOutputPath, u'tiantianTradeInfosData.json')):
            os.remove(os.path.join(self.tradeInfosOutputPath, u'tiantianTradeInfosData.json'))
        with open(os.path.join(self.tradeInfosOutputPath, u'tiantianTradeInfosData.json'),'a',encoding='utf-8') as outputFile:
            contentList = []
            for model in self.modelArray:
                contentList.append(model.__dict__)
            outputFile.write(json.dumps(contentList, ensure_ascii=False, sort_keys = True, indent = 4, separators=(',', ':')))

if __name__ == "__main__":
    strategy = 'a'
    if len(sys.argv) >= 2:
        #
        strategy = sys.argv[1]
    else:
        print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：李淑云 c：康世海 debug：测试代码')
        exit()
    # 传入配置，开始流程
    if strategy == 'debug':
        # 测试代码
        parser = tiantianTradeInfosParser('a')
    else:
        parser = tiantianTradeInfosParser(strategy)
        parser.loadData()
        parser.outputToText()
        parser.outputToJson()
        os.startfile(parser.tradeInfosOutputPath)