# -*- coding: utf-8 -*-

import os
import sys
# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
sys.path.append(srcDir)
# config
from config.assetCategoryConstants import assetCategoryConstants


class colorConstants:

    def __init__(self):
        categoryConstants = assetCategoryConstants()
        self.category1Array = categoryConstants.category1Array

    # 不同 APP 配色
    def getFundColorByAppSourceName(self, name):
        # 色值转换 https://www.sioe.cn/yingyong/yanse-rgb-16/
        if name in [u'螺丝钉', u'螺丝钉母', u'螺丝钉父']:
            return 'F0DC5A'
        elif name in [u'且慢 150 份', u'且慢 S 定投', u'稳稳的幸福父',u'稳稳的幸福']:
            return '6EB5FF'
        elif u'天天基金' in name:
            return 'FF8361'
        elif u'支付宝' in name:
            return 'DBB6AC'
            # return '5587F0' # 绍鹏给的颜色，和绿色太撞色，看不清楚
        elif u'股票账户' in name:
            return 'FF7C9E'
        elif name in [u'现金账户',u'现金账户父母']:
            return 'FFC751'
        elif u'冻结资金' in name:
            return 'DCDCDC'
        elif u'整体' in name:
            return '50C2F9'
        else:
            return 'FFFFFF'

    # 资产分类的 echarts 背景色
    def colorForCategory1(self, category1):
        if category1 == self.category1Array[0]:
            # return '#0AA3B5'
            return '#50C2F9'
        elif category1 == self.category1Array[1]:
            return '#BBEDA8'
        elif category1 == self.category1Array[2]:
            return '#FFC751'
        elif category1 == self.category1Array[3]:
            # return '#2196F3'
            return '#FF7C9E'
        elif category1 == self.category1Array[4]:
            return '#FF8361'
        elif category1 == self.category1Array[5]:
            return '#DBB6AC'
        elif category1 == self.category1Array[6]:
            return '#DCDCDC'
        elif category1 == self.category1Array[7]:
            return '#F0DC5A'
        else:
            return 'FFFFFF'

    # 返回申万 28 行业的制图背景色
    def getIndustryColorByName(self, name):
        swIndexInfos = [{'color': '#E57373', 'name': '农林牧渔I'}, {'color': '#EF6492', 'name': '采掘I'}, {'color': '#B869C8', 'name': '化工I'}, {'color': '#9375CD', 'name': '钢铁I'}, {'color': '#7987CB', 'name': '有色金属I'}, {'color': '#66B5F3', 'name': '电子I'}, {'color': '#50C2F9', 'name': '家用电器I'}, {'color': '#4DD1E2', 'name': '食品饮料I'}, {'color': '#4FB4AD', 'name': '纺织服装I'}, {'color': '#81C686', 'name': '轻工制造I'}, {'color': '#B0D482', 'name': '医药生物I'}, {'color': '#DCE877', 'name': '公用事业I'}, {'color': '#FFF177', 'name': '交通运输I'}, {'color': '#FCDB62', 'name': '房地产I'}, {
            'color': '#FDB84D', 'name': '商业贸易I'}, {'color': '#FD8B66', 'name': '休闲服务I'}, {'color': '#BEBEBE', 'name': '综合I'}, {'color': '#91A4AE', 'name': '建筑材料I'}, {'color': '#A38680', 'name': '建筑装饰I'}, {'color': '#2196F3', 'name': '电气设备I'}, {'color': '#02AAF3', 'name': '国防军工I'}, {'color': '#01BCD6', 'name': '计算机I'}, {'color': '#009786', 'name': '传媒I'}, {'color': '#4EAF51', 'name': '通信I'}, {'color': '#8CC249', 'name': '银行I'}, {'color': '#CCDE37', 'name': '非银金融I'}, {'color': '#FACD20', 'name': '汽车I'}, {'color': '#FF5723', 'name': '机械设备I'}]
        for swIndexInfo in swIndexInfos:
            if name == swIndexInfo['name']:
                return swIndexInfo['color']
        return '#000000'

    # 根据涨跌，返回颜色
    def getGainColor(self, value):
        # http://www.yuangongju.com/color
        changeValueColor = 'DD2200'
        if value >= 0:
            # 221,34,0
            # changeValueColor = 'FE0002'
            return self.getGradationColorForRaise(1.0)
        else:
            # 0,153,51
            # changeValueColor = '009900'
            return self.getGradationColorForFall(1.0)
        return changeValueColor

    # 10 进制色值转 16 进制
    def hexColorString(self, r=255, g=255, b=255):
        stringR = str(hex(int(r)))[2:4].upper()
        if len(stringR) == 1:
            stringR = '0'+stringR
        stringG = str(hex(int(g)))[2:4].upper()
        if len(stringG) == 1:
            stringG = '0'+stringG
        stringB = str(hex(int(b)))[2:4].upper()
        if len(stringB) == 1:
            stringB = '0'+stringB
        colorString = stringR + stringG + stringB
        return colorString

    def rgbTupleFromHexString(self,hexString):
        hexString = hexString.replace('#','')
        assert len(hexString) == 6, u'16 进制颜色必须是 6 字符长'
        r = int(hexString[0:2],16)
        g = int(hexString[2:4],16)
        b = int(hexString[4:6],16)
        return (r,g,b)


    def hexColorStringByPercent(self, origin, zero = '#FFFFFF', rate = 1.0):
        minR,minG,minB = self.rgbTupleFromHexString(zero)
        maxR,maxG,maxB = self.rgbTupleFromHexString(origin)

        return self.hexColorString(minR - (minR - maxR) * rate,
                                   minG - (minG - maxG) * rate,
                                   minB - (minB - maxB) * rate,)


    # 获取上涨级别色阶，取值范围 0 ~ 1.0，1.0是最红，0 是最浅色
    def getGradationColorForRaise(self, rate):
        assert rate >= 0 and rate <= 1.0, u'{0} 超出 getGradationColorForRise 取值范围'.format(
            rate)
        redMin = (252, 252, 255)
        redMax = (248, 105, 107)
        return self.hexColorString(redMin[0]-(redMin[0]-redMax[0]) * rate,
                                   redMin[1]-(redMin[1]-redMax[1]) * rate,
                                   redMin[2]-(redMin[2]-redMax[2]) * rate)

    # 获取下跌级别色阶，取值范围 0 ~ 1.0，1.0是最绿，0 是最浅色
    def getGradationColorForFall(self, rate):
        assert rate >= 0 and rate <= 1.0, u'{0} 超出 getGradationColorForRise 取值范围'.format(
            rate)
        redMin = (252, 252, 255)
        redMax = (99, 190, 123)
        return self.hexColorString(redMin[0]-(redMin[0]-redMax[0]) * rate,
                                   redMin[1]-(redMin[1]-redMax[1]) * rate,
                                   redMin[2]-(redMin[2]-redMax[2]) * rate)


if __name__ == "__main__":
    color = colorConstants()
    # for rate in range(0,11):
    #    print('#'+color.getGradationColorForFail(rate/10))
