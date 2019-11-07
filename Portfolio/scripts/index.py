# coding=utf-8
import requests
import os

class indexYearCompare:

    def __init__(self):
        self.indexInfos = [ \
            {u"category1":u"A 股",u"category2":u"大盘股",u"category3":u"上证50",u"indexCode":u"000016",u"requestCode":u"0000161",u"categoryId":u"111"}, \
            {u"category1":u"A 股",u"category2":u"大盘股",u"category3":u"50AH",u"indexCode":u"000170",u"requestCode":u"0001701",u"categoryId":u"112"}, \
            {u"category1":u"A 股",u"category2":u"大盘股",u"category3":u"沪深300",u"indexCode":u"000300",u"requestCode":u"0003001",u"categoryId":u"113"}, \
            {u"category1":u"A 股",u"category2":u"大盘股",u"category3":u"300价值",u"indexCode":u"000919",u"requestCode":u"0009191",u"categoryId":u"114"}, \
            {u"category1":u"A 股",u"category2":u"大盘股",u"category3":u"基本面60",u"indexCode":u"399701",u"requestCode":u"3997012",u"categoryId":u"115"}, \
            {u"category1":u"A 股",u"category2":u"大盘股",u"category3":u"基本面120",u"indexCode":u"399702",u"requestCode":u"3997022",u"categoryId":u"116"}, \
            {u"category1":u"A 股",u"category2":u"大盘股",u"category3":u"中小板",u"indexCode":u"399005",u"requestCode":u"3990052",u"categoryId":u"117"}, \
            {u"category1":u"A 股",u"category2":u"中小盘股",u"category3":u"中证500",u"indexCode":u"000905",u"requestCode":u"0009051",u"categoryId":u"121"}, \
            {u"category1":u"A 股",u"category2":u"中小盘股",u"category3":u"中证1000",u"indexCode":u"000852",u"requestCode":u"0008521",u"categoryId":u"123"}, \
            {u"category1":u"A 股",u"category2":u"中小盘股",u"category3":u"创业板",u"indexCode":u"399006",u"requestCode":u"3990062",u"categoryId":u"124"}, \
            {u"category1":u"A 股",u"category2":u"红利价值",u"category3":u"中证红利",u"indexCode":u"000922",u"requestCode":u"0009221",u"categoryId":u"131"}, \
            {u"category1":u"A 股",u"category2":u"行业股",u"category3":u"养老产业",u"indexCode":u"399812",u"requestCode":u"3998122",u"categoryId":u"141"}, \
            {u"category1":u"A 股",u"category2":u"行业股",u"category3":u"全指医药",u"indexCode":u"000991",u"requestCode":u"0009911",u"categoryId":u"142"}, \
            {u"category1":u"A 股",u"category2":u"行业股",u"category3":u"中证环保",u"indexCode":u"000827",u"requestCode":u"0008271",u"categoryId":u"143"}, \
            {u"category1":u"A 股",u"category2":u"行业股",u"category3":u"中证传媒",u"indexCode":u"399971",u"requestCode":u"3999712",u"categoryId":u"144"}, \
            {u"category1":u"A 股",u"category2":u"行业股",u"category3":u"证券公司",u"indexCode":u"399975",u"requestCode":u"3999752",u"categoryId":u"145"}, \
            {u"category1":u"A 股",u"category2":u"行业股",u"category3":u"金融地产",u"indexCode":u"000992",u"requestCode":u"0009921",u"categoryId":u"146"}, \
            {u"category1":u"A 股",u"category2":u"行业股",u"category3":u"全指消费",u"indexCode":u"000990",u"requestCode":u"0009901",u"categoryId":u"147"}, \
            {u"category1":u"海外新兴",u"category2":u"香港",u"category3":u"恒生",u"indexCode":u"HSI5",u"requestCode":u"HSI5",u"categoryId":u"211"}, \
            {u"category1":u"海外新兴",u"category2":u"台湾",u"category3":u"台湾加权",u"indexCode":u"TWII_UI",u"requestCode":u"TWII_UI",u"categoryId":u"213"}, \
            {u"category1":u"海外新兴",u"category2":u"日本",u"category3":u"日经225",u"indexCode":u"N225_UI",u"requestCode":u"N225_UI",u"categoryId":u"214"}, \
            {u"category1":u"海外成熟",u"category2":u"海外成熟",u"category3":u"德国30",u"indexCode":u"GDAXI_UI",u"requestCode":u"GDAXI_UI",u"categoryId":u"311"}, \
            {u"category1":u"海外成熟",u"category2":u"海外成熟",u"category3":u"富时100",u"indexCode":u"FTSE_UI",u"requestCode":u"FTSE_UI",u"categoryId":u"312"}, \
            {u"category1":u"海外成熟",u"category2":u"海外成熟",u"category3":u"法国40",u"indexCode":u"FCHI_UI",u"requestCode":u"FCHI_UI",u"categoryId":u"313"}, \
            {u"category1":u"海外成熟",u"category2":u"海外成熟",u"category3":u"道琼斯",u"indexCode":u"DJIA_UI",u"requestCode":u"DJIA_UI",u"categoryId":u"314"}, \
            {u"category1":u"海外成熟",u"category2":u"海外成熟",u"category3":u"纳斯达克",u"indexCode":u"NDX_UI",u"requestCode":u"NDX_UI",u"categoryId":u"315"}, \
            {u"category1":u"海外成熟",u"category2":u"海外成熟",u"category3":u"标普500",u"indexCode":u"SPX_UI",u"requestCode":u"SPX_UI",u"categoryId":u"316"}, \
            {u"category1":u"商品",u"category2":u"商品",u"category3":u"黄金",u"indexCode":u"GC00Y",u"requestCode":u"GC00Y0",u"categoryId":u"511"}, \
            {u"category1":u"商品",u"category2":u"商品",u"category3":u"原油",u"indexCode":u"CL00Y",u"requestCode":u"CL00Y0",u"categoryId":u"512"}, \
            {u"category1":u"商品",u"category2":u"商品",u"category3":u"白银",u"indexCode":u"SI00Y",u"requestCode":u"SI00Y0",u"categoryId":u"513"} \
        ]

        self.filePaths = ['D:\\github\\finance-data\\Portfolio\\scripts\\test\\111_上证50_000016.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\112_50AH_000170.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\113_沪深300_000300.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\114_300价值_000919.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\115_基本面60_399701.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\116_基本面120_399702.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\117_中小板_399005.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\121_中证500_000905.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\123_中证1000_000852.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\124_创业板_399006.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\131_中证红利_000922.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\141_养老产业_399812.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\142_全指医药_000991.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\143_中证环保_000827.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\144_中证传媒_399971.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\145_证券公司_399975.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\146_金融地产_000992.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\147_全指消费_000990.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\211_恒生_HSI5.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\213_台湾加权_TWII_UI.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\214_日经225_N225_UI.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\311_德国30_GDAXI_UI.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\312_富时100_FTSE_UI.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\313_法国40_FCHI_UI.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\314_道琼斯_DJIA_UI.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\315_纳斯达克_NDX_UI.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\316_标普500_SPX_UI.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\511_黄金_GC00Y.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\512_原油_CL00Y.txt', 'D:\\github\\finance-data\\Portfolio\\scripts\\test\\513_白银_SI00Y.txt']
        
        self.filePrefix = u'D:\\github\\finance-data\\Portfolio\\scripts\\test\\'
        
    def getData(self):
        for indexInfo in self.indexInfos:
            code = indexInfo['requestCode']
            url = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id={0}&TYPE=yk'.format(code)
            response = requests.get(url)
            dataList = response.text.split('\r\n')
            filePath = os.path.join(os.getcwd(),'test','{0}_{1}_{2}.txt'.format(indexInfo['categoryId'],indexInfo['category3'],indexInfo['indexCode']))
            self.filePaths.append(filePath)
            with open(filePath,'w',encoding='utf-8') as f:
                print(indexInfo['category3'])
                for data in dataList:
                    values = str(data).replace('(','').split(',')
                    if len(values) < 3:
                        continue
                    result = '{0}\t{1}\t{2}\t{3}%'.format(values[0],values[1],values[2],round((float(values[2])/float(values[1])-1)*100,2))
                    print(result)
                    f.write(result + '\n')
                print('\n')
        print(self.filePaths)
    
    def showByYear(self):
        years = [x for x in range(1990,2020)]
        for year in years:
            print(year)
            for filePath in self.filePaths:
                with open(filePath,'r',encoding='utf-8') as f:
                    allText = f.read()
                    # 包含对应年份
                    if '{0}-'.format(year) in allText:
                        f.seek(0)
                        lines = f.readlines()
                        name = filePath.replace(self.filePrefix,'').replace('.txt','')
                        for line in lines:
                            if '{0}-'.format(year) in line:
                                values = line.replace('\n','').split('\t')
                                print('{0} {1}'.format(name,values[3]))
                                break
                    else:
                        #print('{0} has no year {1}'.format(filePath,year))
                        continue
            print('\n')
        
if __name__ == "__main__":
    obj = indexYearCompare()
    #obj.getData()
    obj.showByYear()