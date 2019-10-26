# -*- coding: utf-8 -*-

import os

class huataiSpider:
    
    # 初始化构造函数
    def __init__(self):
        self.path = os.path.join(os.getcwd(),u'input',u'huatai.txt')
        self.results = []
        self.neededColumnNames = [u'证券名称',u'证券代码',u'成本价',u'证券数量',u'最新市值',u'浮动盈亏']
        self.neededColumnIndexs = []
        self.totalMarketCap = 0.0
        self.totalGain = 0.0
    
    def dataFormat(self):
        if not os.path.exists(self.path):
            print(u'[ERROR] 当前文件夹下未找到 {0}'.format(self.path))
            exit()
        
        # 读取 + 计算必要信息
        with open(self.path,'r',encoding='utf-8') as inputfile:
            headers = inputfile.readline().replace('\n','').split('\t')
            for col in self.neededColumnNames:
                if col in headers:
                    index = headers.index(col)
                    #print(col,index)
                    self.neededColumnIndexs.append(index)
                else:
                    continue
            if len(self.neededColumnIndexs) < 6:
                print(u'[ERROR] 所需列数不足。当前列数：{0}'.format(len(self.neededColumnIndexs)))
                exit()
            # 读取并暂存数据（inputfile.readline() 已经让内部游标 +1 了，所以 readlines() 将是从第一行数据开始）
            for line in inputfile.readlines():
                data = line.replace('\n','').split('\t')
                # 名称，代码，持仓成本，持仓份额，持仓市值，累计收益
                seq = (data[self.neededColumnIndexs[0]],data[self.neededColumnIndexs[1]],data[self.neededColumnIndexs[2]],\
                        data[self.neededColumnIndexs[3]],data[self.neededColumnIndexs[4]],data[self.neededColumnIndexs[5]])
                self.totalMarketCap = self.totalMarketCap + round(float(data[self.neededColumnIndexs[4]]),2)
                self.totalGain = self.totalGain + round(float(data[self.neededColumnIndexs[5]]),2)
                self.results.append(u'\t'.join(seq))
        
        # 写入输出文件
        with open(os.path.join(os.getcwd(),u'output',u'huatai_康力泉.txt'),'w',encoding='utf-8') as outfile:
            titleLine = u'{0}\t总市值\t{1}\t累计收益\t{2}'.format(u'股票账户',round(self.totalMarketCap,2),round(self.totalGain,2))
            print(titleLine)
            outfile.write(titleLine + '\n')
            headerLine = u'基金名称\t基金代码\t持仓成本\t持仓份额\t持仓市值\t累计收益'
            print(headerLine)
            outfile.write(headerLine + '\n')
            for item in self.results:
                # 名称，代码，持仓成本，持仓份额，持仓市值，累计收益
                print(item)
                outfile.write(item + '\n')
            print('\n')
            
spider = huataiSpider()
# huatai.txt 本来就是从 xls 文件中拷贝出来的。重组后，重新生成该文件，所以叫 dataFormat
# 因为华泰生成的 xls 文件格式有问题，用 xlrd 读取会崩溃，所以才出此折衷办法
spider.dataFormat()