# -*- coding: utf-8 -*-

# config
from config.assetCategoryConstants import assetCategoryConstants

class colorConstants:

    def __init__(self):
        categoryConstants = assetCategoryConstants()
        self.category1Array = categoryConstants.category1Array
        
    def getFundColorByAppSourceName(self, name):
        # 色值转换 https://www.sioe.cn/yingyong/yanse-rgb-16/
        if name in [u'螺丝钉定投',u'李淑云螺丝钉',u'康世海螺丝钉']:
            return 'F0DC5A'
        elif name in [u'且慢补充 150 份',u'且慢 S 定投']:
            return '6EB5FF'
        elif u'天天基金' in name:
            return 'FF8361'
        elif u'支付宝' in name:
            return 'DBB6AC'
            #return '5587F0' # 绍鹏给的颜色，和绿色太撞色，看不清楚
        elif u'股票账户' in name:
            return 'FF7C9E'
        elif u'现金账户' in name:
            return 'FFC751'
        elif u'冻结资金' in name:
            return 'DCDCDC'
        else:
            return 'FFFFFF'

    # 不同 APP 配色
    def getFundColorByAppSourceNameOld(self, name):
        # 色值转换 https://www.sioe.cn/yingyong/yanse-rgb-16/
        if name in [u'螺丝钉定投',u'李淑云螺丝钉',u'康世海螺丝钉']:
            # 242,195,0
            return 'F2C300'
        elif name in [u'且慢补充 150 份',u'且慢 S 定投']:
            # 0,176,204
            return '00B1CC'
        elif u'天天基金' in name:
            # 233,80,26
            return 'E9501A'
        elif u'支付宝' in name:
            # 0,161,233
            return '00A1E9'
        elif u'股票账户' in name:
            # 222,48,49
            return 'DE3031'
        elif u'现金账户' in name:
            # 0,161,233
            return 'F7A128'
        elif u'冻结资金' in name:
            # 222,48,49
            return '8B8C90'
        else:
            return 'FFFFFF'

    # 资产分类的 echarts 背景色
    def colorForCategory1(self,category1):
        #self.category1Array = [u'A 股',u'海外新兴',u'海外成熟',u'债券',u'商品']
        
        # js code
        #var aStockColor = {color: '#0aa3b5'};			// A 股（大盘股，中小盘股，红利价值，行业股）
        #var outSideNewColor = {color: '#187a2f'};		// 海外新兴（香港，海外互联网）
        #var outSideMatureColor = {color: '#ebb40f'};	// 海外成熟（德国）
        #var universalGoodsColor = {color: '#dd4c51'};	// 商品（黄金，白银，原油）
        #var bondColor = {color: '#be8663'};				// 债券（可转债，美元债）
        #var cashColor = {color: '#f7a128'};				// 低风险理财（货币基金，地产P2P）
        #var frozenCashColor = {color: '#8b8c90'};		// 冻结资金（公积金，外借款）
        if category1 == self.category1Array[0]:
            return '#0AA3B5'
        elif category1 == self.category1Array[1]:
            return '#BBEDA8'
        elif category1 == self.category1Array[2]:
            return '#FFC751'
        elif category1 == self.category1Array[3]:
            return '#FF8361'
        elif category1 == self.category1Array[4]:
            return '#DBB6AC'
        elif category1 == self.category1Array[5]:
            return '#F0DC5A'
        elif category1 == self.category1Array[6]:
            return '#DCDCDC'
        else:
            return 'FFFFFF'

    # 资产分类的 echarts 背景色
    def colorForCategory1Old(self,category1):
        #self.category1Array = [u'A 股',u'海外新兴',u'海外成熟',u'债券',u'商品']
        
        # js code
        #var aStockColor = {color: '#0aa3b5'};			// A 股（大盘股，中小盘股，红利价值，行业股）
        #var outSideNewColor = {color: '#187a2f'};		// 海外新兴（香港，海外互联网）
        #var outSideMatureColor = {color: '#ebb40f'};	// 海外成熟（德国）
        #var universalGoodsColor = {color: '#dd4c51'};	// 商品（黄金，白银，原油）
        #var bondColor = {color: '#be8663'};				// 债券（可转债，美元债）
        #var cashColor = {color: '#f7a128'};				// 低风险理财（货币基金，地产P2P）
        #var frozenCashColor = {color: '#8b8c90'};		// 冻结资金（公积金，外借款）
        if category1 == self.category1Array[0]:
            return '#0AA3B5'
        elif category1 == self.category1Array[1]:
            return '#187A2F'
        elif category1 == self.category1Array[2]:
            return '#EBB40F'
        elif category1 == self.category1Array[3]:
            return '#BE8663'
        elif category1 == self.category1Array[4]:
            return '#DD4C51'
        elif category1 == self.category1Array[5]:
            return '#F7A128'
        elif category1 == self.category1Array[6]:
            return '#8B8C90'
        else:
            return 'FFFFFF'

    # 根据涨跌，返回颜色
    def getGainColor(self,value):
        # http://www.yuangongju.com/color
        changeValueColor = 'DD2200'
        if value >= 0:
            # 221,34,0
            changeValueColor = 'DD2200'
        else:
            # 0,153,51
            changeValueColor = '009933'
        return changeValueColor

if __name__ == "__main__":
    colorConstants()