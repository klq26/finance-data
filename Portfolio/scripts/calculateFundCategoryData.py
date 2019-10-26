# -*- coding: utf-8 -*-

# for reduce method of lambda
from functools import reduce
# groupby & itemgetter
from itertools import groupby
from operator import itemgetter
# model
from model.fundModel import fundModel
from model.echartsModel import echartsModel
# output
from echartsJson import echartsJson

class calculateFundCategoryData:

    def __init__(self):
        print()
        self.category1Array = [u'A 股',u'海外新兴',u'海外成熟',u'债券',u'商品'] # ,u'现金类'
        self.category2Array = [u'大盘股',u'中小盘股',u'红利价值',u'行业股',u'香港',u'海外互联',u'海外成熟',u'国内债券',u'海外债券',u'商品'] # ,u'保本理财'
        self.category3Array = [u'上证50',u'50AH',u'沪深300',u'300价值',u'基本面60',u'基本面120',u'中小板',u'中证500',u'500低波动',u'中证1000',u'创业板',u'中证红利',u'标普红利',u'养老产业',u'全指医药',u'中证环保',u'中证传媒',u'证券公司',u'金融地产',u'恒生',u'香港中小',u'海外互联网',u'德国30',u'可转债',u'美元债',u'黄金',u'原油']
    
    # 格式化浮点数
    def beautify(self,num):
        return round(float(num),2)
    
    def calculate(self,modelArray):
        # 总市值
        allMarketCaps = [x.marketCap for x in modelArray]
        totalMarketCap = reduce(lambda x,y: x+y, allMarketCaps)
        print(u'总市值：{0}'.format(self.beautify(totalMarketCap)))
        # 总盈亏
        allTotalGains = [x.totalGain for x in modelArray]
        totalGain = reduce(lambda x,y: x+y, allTotalGains)
        print(u'总盈亏：{0}'.format(self.beautify(totalGain)))
        print(u'组合收益率：{0}%'.format(self.beautify(totalGain/totalMarketCap * 100)))
        print('\n一级分类：\n')
        for category in self.category1Array:
            marketCaps = [x.marketCap for x in modelArray if x.category1 == category]
            marketCap = reduce(lambda x,y: x+y, marketCaps)
            
            totalGains = [x.totalGain for x in modelArray if x.category1 == category]
            gain = reduce(lambda x,y: x+y, totalGains)
            
            print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain)))
        print('\n二级分类：\n')
        for category in self.category2Array:
            marketCaps = [x.marketCap for x in modelArray if x.category2 == category]
            marketCap = reduce(lambda x,y: x+y, marketCaps)
            
            totalGains = [x.totalGain for x in modelArray if x.category2 == category]
            gain = reduce(lambda x,y: x+y, totalGains)
            
            print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain)))
        print('\n三级分类：\n')
        for category in self.category3Array:
            marketCaps = [x.marketCap for x in modelArray if x.category3 == category]
            marketCap = reduce(lambda x,y: x+y, marketCaps)
            
            totalGains = [x.totalGain for x in modelArray if x.category3 == category]
            gain = reduce(lambda x,y: x+y, totalGains)
            
            print(u'{0} 市值：{1}\t占比：{2}%\t盈亏：{3}'.format(category, self.beautify(marketCap), self.beautify(marketCap / totalMarketCap * 100), self.beautify(gain)))

    def generateEchartsJson(self,modelArray):
        # 内部排序函数，按 category id 升序排列
        #def fundModelSortFunc(item):
        #    return item.category4
        # 排序
        #modelArray.sort(key=fundModelSortFunc)
        # 按对象的 category4 字段升序排序
        modelArray.sort(key=itemgetter('category4'))
        # 资产配置总市值
        totalMarketCap = 0.0
        for item in modelArray:
            totalMarketCap = totalMarketCap + item.marketCap
            #print(item.__dict__)
        totalMarketCap = self.beautify(totalMarketCap)
        #print(totalMarketCap)
        
        # 一级分类
        for category in self.category1Array:
            echart1 = echartsModel()
            category1Models = [x for x in modelArray if x.category1 == category]
            
            for category2, category2Array in groupby(category1Models,key=itemgetter('category2')):
                print(category2)
                for category3, category3Array in groupby(category1Models,key=itemgetter('category3')):
                    
                    for j in category3Array:
                        if j.category2 == category2:
                            print('\t' + category3)
                    #print(len(list(category2Array)))
                    for i in category3Array:
                        if i.category2 == category2:
                            print('\t\t{0}'.format(i.__dict__))
            print('\n\n\n')
            
            
            # 一级分类市值
            #category1MarketCap = 0.0
            #for cate1 in category1Models:
            #    category1MarketCap = category1MarketCap + cate1.marketCap
            #    echart1.name = cate1.category1
            #    echart1.value = 0.0
            #    echart1.itemStyle['color'] = '#0AA3B5'
                
                #for cate2 in category1Models:
                    
                #echart1.children.append(cate2)
                
            #print(category1MarketCap)
            #print('\n')
