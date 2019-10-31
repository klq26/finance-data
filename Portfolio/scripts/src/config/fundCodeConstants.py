

class fundCodeConstants:
    def __init__(self):
        # 场内基金代码（持续更新）
        self.innerMarketCodes =     \
        {   \
            u"50ETF" : u"510050",	\
            u"300ETF" : u"510300",	\
            u"500ETF" : u"510500",	\
            u"环保ETF" : u"512580",	\
            u"证券ETF" : u"512880",	\
            u"传媒ETF" : u"512980",	\
            u"黄金ETF" : u"518880",	\
            u"中 小 板" : u"159902",	\
            u"创业板" : u"159915",	\
            u"广发医药" : u"159938",	\
        }   \

        # 场外基金代码（持续更新）
        self.outerMarketCodes = \
        {	\
            u"华夏沪深300ETF联接A" : u"000051",	\
            u"华夏恒生ETF联接A" : u"000071",	\
            u"广发美国房地产指数" : u"000179",	\
            u"华安黄金易ETF联接A" : u"000216",	\
            u"华安德国30(DAX)联接" : u"000614",	\
            u"广发养老指数A" : u"000968",	\
            u"华夏上证50ETF联接A" : u"001051",	\
            u"华夏收益债券(QDII)A" : u"001061",	\
            u"广发中证环保ETF联接A" : u"001064",	\
            u"东方红中国优势混合" : u"001112",	\
            u"广发医药卫生联接A" : u"001180",	\
            u"广发中证全指金融地产联接A" : u"001469",	\
            u"广发中证500ETF联接C" : u"002903",	\
            u"广发中债7-10年国开债指数A" : u"003376",	\
            u"创金合信中证1000指数增强A" : u"003646",	\
            u"创金合信中证1000指数增强C" : u"003647",	\
            u"广发创业板ETF联接A" : u"003765",	\
            u"广发中证传媒ETF联接A" : u"004752",	\
            u"富国中证红利指数增强" : u"100032",	\
            u"富国沪深300指数增强" : u"100038",	\
            u"易方达消费行业股票" : u"110022",	\
            u"易方达创业板ETF联接A" : u"110026",	\
            u"易方达安心回报债券A" : u"110027",	\
            u"富国中证500指数(LOF)" : u"161017",	\
            u"招商中证白酒指数分级" : u"161725",	\
            u"华宝标普油气上游股票" : u"162411",	\
            u"华宝中证1000指数分级" : u"162413",	\
            u"广发中证500ETF联接A" : u"162711",	\
            u"交银中证海外中国互联网指数" : u"164906",	\
            u"兴全可转债混合" : u"340001",	\
            u"易方达证券公司分级" : u"502010",	\
            u"长信可转债债券A" : u"519977",	\
        }	\

        # 货币基金代码（持续更新）
        self.monetaryFundCodes = \
        {   \
            u"广发钱袋子货币A" : u"000509",	\
            u"招商招钱宝货币A" : u"000588",	\
            u"汇添富和聚宝货币" : u"000600",	\
            u"富国富钱包货币" : u"000638",	\
            u"华安汇财通货币" : u"000709",	\
            u"博时现金宝货币Ｂ" : u"000891",	\
            u"鹏华添利宝货币" : u"001666",	\
            u"华夏现金增利货币A/E" : u"003003",	\
            u"建信现金添益货币A" : u"003022",	\
            u"南方天天利货币Ｂ" : u"003474",	\
            u"光大货币" : u"360003",	\
            u"工银货币" : u"482002",	\
            u"活期宝" : u"------",	\
        }   \
        
        # 虚拟代码（持续更新）
        self.simulateCodes = \
        {   \
            u"货币基金综合" : u"999990",	\
            u"房地产P2P" : u"999991",	\
            u"住房公积金" : u"899990",	\
            u"无息外借款" : u"899991",	\
        }   \

if __name__ == "__main__":
    codes = fundCodeConstants()

