# -*- coding: utf-8 -*-
import os
import json
from bs4 import BeautifulSoup

from tiantianTradeInfoModel import tiantianTradeInfoModel

class tiantianTradeInfosParser:

    def __init__(self):
        self.dataFolder = 'htmls'
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
        if os.path.exists(os.path.join(u'tiantianTradeInfosData.txt')):
            os.remove(os.path.join(u'tiantianTradeInfosData.txt'))
        with open(os.path.join(u'tiantianTradeInfosData.txt'),'a',encoding='utf-8') as outputFile:
            outputFile.write(u'交易发起日期\t产品名称\t产品代码\t业务类型\t申请数额\t申请单位\t确认数额\t确认单位\t链接\n')
            for model in self.modelArray:
                outputFile.write(model.__str__() + '\n')
        
    def outputToJson(self):
        if os.path.exists(os.path.join(u'tiantianTradeInfosData.json')):
            os.remove(os.path.join(u'tiantianTradeInfosData.json'))
        with open(os.path.join(u'tiantianTradeInfosData.json'),'a',encoding='utf-8') as outputFile:
            contentList = []
            for model in self.modelArray:
                contentList.append(model.__dict__)
            outputFile.write(json.dumps(contentList, ensure_ascii=False, sort_keys = True, indent = 4, separators=(',', ':')))
            
if __name__ == "__main__":
    parser = tiantianTradeInfosParser()
    parser.loadData()
    parser.outputToText()
    parser.outputToJson()

