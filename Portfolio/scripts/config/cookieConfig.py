# -*- coding: utf-8 -*-

class cookieConfig:   
    """
    所有爬虫需要的请求 Header 验证字段常量集合
    之后抓取前，仅需要更新这一个文件即可
    """
    def __init__(self):
        # 雪球 Cookie。主要是为了查询场内基金净值信息
        self.xueqiuCookie = u'Cookie: device_id=24700f9f1986800ab4fcc880530dd0ed; s=bu12f52zv3; bid=6e97accacf189cc998bcde7951604689_k04m5ssh; snbim_minify=true; Hm_lvt_1db88642e346389874251b5a1eded6e3=1569827043,1570625764,1570625774; remember=1; xq_a_token=c0c9fa4a3b3bba0c9b2409ae44e6af75bb464a9f; xqat=c0c9fa4a3b3bba0c9b2409ae44e6af75bb464a9f; xq_r_token=d1896db710adc144921c6f81cb73e4fe2d5b2813; xq_is_login=1; u=2812376209; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1572263932'
        
        
        # 天天基金
        self.tiantianCookieKLQ = u'Cookie: https://trade.1234567.com.cn/MyAssets/bankcardtb-banktbb=0; st_si=48193464463530; ASP.NET_SessionId=rvw2hcfyyuwbsm4h1zg2vw4j; st_asi=delete; b_p_log_key=UXRF8fAgsvU1SArYSDZb1vNi/JgRlELFdZEJcyP6AshghN+GTGQZhKJmUzB8WTAY5eYgy3QDKWSkjTh6709wxqrYbnqGW8s/gMglTQ0MCnP4PcCtIi4=; b_pl_bq=de9612a5f90c4a9bab2a853807e9822c; FundTradeLoginTab=0; FundTradeLoginCard=0; st_pvi=69416177127426; st_sp=2019-08-25%2008%3A06%3A30; st_inirUrl=https%3A%2F%2Ftrade7.1234567.com.cn%2FQuery%2Fbill; st_sn=20; st_psi=20191026065644909-112200304021-4233583121; cp_token=ab89bd25736f4305b7d19e1f10c79eec; FundTradeLoginUser=HMhBYUSroghdVSqY57eBBeqyPe81Oc7ImX3zg18+2Dx4Yv+qN2/SHyJxLApgsAp9f67b1QNM; fund_trade_cn=HUSRPA3SdB2od5gk1dLm5arbLx7+edszEkwNMc0mJ+1xjQcFL53NgdvtgSJSMcki4hI8e5v/YTfj+FPuD6dgJq4n/6wSgN/mbK97dxGzeWsWJAIrlr0=; fund_trade_name=HtKCBFB3igtQ8IQgK1eNvUPqUJF1joI1Bi5ggUNGTqpYlvtwXMLU1QJ6OEQLU8e9Wi/sv3EK; fund_trade_visitor=HiKjwrAHcgM6HuKT5Xeu/zwl61Y1EOq5ThvvgzsTW7LqNvQHwvZy30J0HBm4ax29Fu9mQTZg; fund_trade_risk=HRC7/r3lagWVk7JLGAeOvYIAfXc1eahNmplagcw9KvyEyvODjJ/p9nJY1J6LOki9vw4voeSe; fund_trade_gps=6; VipLevel=1; TradeLoginToken=615668015c66452289031b631a7d9710; UTOKEN=HUSRPA3SdB2od5gk1dLm5arbLx7+edszEkwNMc0mJ+1xjQcFL53NgdvtgSJSMcki4hI8emvnicdze09EO3SqJOBAPNWI8CFxQT9zRYBn/+MeZ4WWUZY=; LToken=0dd8a54a5bfa4264869cca04392ae7dd; fund_trade_trackid=l3Jz95v70op6jqul9QqcMaoTxvqLAircTVgbl4KsCmh/ojZ/fmAoy/VIaPe+y2pe9dqzXN8PwkYcraRpiGnARQ=='



        self.tiantianCookieMother = u'Cookie: st_si=48193464463530; ASP.NET_SessionId=hqkpy1axbawl4t5dpyxap44r; st_asi=delete; b_p_log_key=UXRF8fAgsvU1SArYSDZb1vNi/JgRlELFdZEJcyP6AshghN+GTGQZhKJmUzB8WTAY5eYgy3QDKWSkjTh6709wxqrYbnqGW8s/gMglTQ0MCnP4PcCtIi4=; b_pl_bq=de9612a5f90c4a9bab2a853807e9822c; FundTradeLoginTab=0; FundTradeLoginCard=0; st_pvi=69416177127426; st_sp=2019-08-25%2008%3A06%3A30; st_inirUrl=https%3A%2F%2Ftrade7.1234567.com.cn%2FQuery%2Fbill; st_sn=22; st_psi=20191026181215414-112200304021-4218660324; cp_token=1117a16e9ce14d4b8df09846140e9b40; FundTradeLoginUser=PI07xSOJ5lMM6nu8lSAW7ZZrr5+Q3uk7RyeRsVFWtZPpHoZ7iJuWzUIToTk/IPeU4fLNpPz3; fund_trade_cn=PYJ5c18gH4JEEflNeq1aJm5Rd+c3Az3mmVDVoJE1Z4QwHeyXCiaDQobysiBqK7pzAvP52io+JYNk5g2QSET2IalOKS3gAjdqomUPM0nTzskVfXxksJs=; fund_trade_name=Petz5uNrGl13ZMDb4HAGNWOUnXiQ93Sdwe7fsMP2VkBk2oOXSDvX2yIpGjLSE0tUSxzkn3Ca; fund_trade_visitor=Pxo+GVWLwluGAuxZFPAaQmxL1bEQpxQTAXI5s19sZnqGookf63CqMsIUvHH2NwgUz/OmvYXY; fund_trade_risk=P5qOPnvBtl140zsw5VAhjEo/DhJQQw1Nitbcs7bZn9O+VoajYaQF7gIandV/05bUtLuwtg6e; fund_trade_gps=7; VipLevel=1; TradeLoginToken=6103d95b9dcb417ebef22a9a9e7a9b77; UTOKEN=PYJ5c18gH4JEEflNeq1aJm5Rd+c3Az3mmVDVoJE1Z4QwHeyXCiaDQobysiBqK7pzAvP52doPpeQ4UJVm05CWIqM6JxJqQKjWkEUP0XZoW047AJ4JP5E=; LToken=1bfdfc393a8847f5a1518be8b5b153cd; fund_trade_trackid=Kq6ljAT0tmZAzQ50QNHghigFM4h/artgpsOvff7gK5M2C72DWASM8iFY53346OQ2AdzzbzQxHB7MaUc8I8dtsQ=='
        
        
        self.tiantianCookieFather = u''
        
        
        # 蛋卷基金
        self.danjuanCookieKLQ = u'Cookie: device_id=web_ByL9-IyHH; _ga=GA1.2.1578122713.1566691726; gr_user_id=07a8b8b8-e04f-4bfa-b6bd-3492bb42b3a6; thirdparty_token=; thirdparty_source=; thirdparty_nickname=; thirdparty_avatar=; xq_a_token=489a94320ff7bc390513c200bc41187b51db60d2; Hm_lvt_b53ede02df3afea0608038748f4c9f36=1569888571; _gid=GA1.2.2054521569.1571888134; channel=1300100141; gr_session_id_94b96c7a661bf17a=863c6d03-fdc3-4893-8449-37a2168b5f15; gr_session_id_94b96c7a661bf17a_863c6d03-fdc3-4893-8449-37a2168b5f15=true; _gat_gtag_UA_16079156_7=1; accesstoken=2400200003f67a5d8529dc72490a4120205d081c0596633fe; uid=203274561; refreshtoken=2400200008076cc9f34c243ace0052b329753dab3dc9466b2; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22203274561%22%2C%22%24device_id%22%3A%2216cc61a9198303-0a4b8d7e767657-7373e61-3686400-16cc61a9199311%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216cc61a9198303-0a4b8d7e767657-7373e61-3686400-16cc61a9199311%22%7D; Hm_lpvt_b53ede02df3afea0608038748f4c9f36=1571891904; timestamp=1571891914488'
        
        
        self.danjuanCookieMother = u'Cookie: device_id=web_ByL9-IyHH; _ga=GA1.2.1578122713.1566691726; gr_user_id=07a8b8b8-e04f-4bfa-b6bd-3492bb42b3a6; thirdparty_token=; thirdparty_source=; thirdparty_nickname=; thirdparty_avatar=; xq_a_token=489a94320ff7bc390513c200bc41187b51db60d2; Hm_lvt_b53ede02df3afea0608038748f4c9f36=1569888571; accesstoken=24002000044084327ac204d6b9759b4331bba0cb995965fbd; refreshtoken=240020000e085adf5202568b98a9eb2d03fb7399755ca84dd; uid=194897199; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22194897199%22%2C%22%24device_id%22%3A%2216cc61a9198303-0a4b8d7e767657-7373e61-3686400-16cc61a9199311%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216cc61a9198303-0a4b8d7e767657-7373e61-3686400-16cc61a9199311%22%7D; _gid=GA1.2.2054521569.1571888134; channel=1300100141; Hm_lpvt_b53ede02df3afea0608038748f4c9f36=1571888426; _gat_gtag_UA_16079156_7=1; timestamp=1571888426460'
        
        
        self.danjuanCookieFather = u'Cookie: device_id=web_ByL9-IyHH; _ga=GA1.2.1578122713.1566691726; gr_user_id=07a8b8b8-e04f-4bfa-b6bd-3492bb42b3a6; thirdparty_token=; thirdparty_source=; thirdparty_nickname=; thirdparty_avatar=; xq_a_token=489a94320ff7bc390513c200bc41187b51db60d2; Hm_lvt_b53ede02df3afea0608038748f4c9f36=1569888571; _gid=GA1.2.2054521569.1571888134; channel=1300100141; _gat_gtag_UA_16079156_7=1; gr_session_id_94b96c7a661bf17a=863c6d03-fdc3-4893-8449-37a2168b5f15; gr_session_id_94b96c7a661bf17a_863c6d03-fdc3-4893-8449-37a2168b5f15=true; accesstoken=240020000d176abe5f5153802ff08f4dc9a1b43462cc8ea53; uid=576923716; refreshtoken=2400200009298cd46784d85ceb8cf6aaecb19c333aee9e001; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22576923716%22%2C%22%24device_id%22%3A%2216cc61a9198303-0a4b8d7e767657-7373e61-3686400-16cc61a9199311%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216cc61a9198303-0a4b8d7e767657-7373e61-3686400-16cc61a9199311%22%7D; Hm_lpvt_b53ede02df3afea0608038748f4c9f36=1571891597; timestamp=1571891605116'
        
        
        # 广发基金（*支付宝）
        self.guangfaCookie = u'Cookie: _ga=GA1.3.2121823865.1572009211; _gid=GA1.3.2018311132.1572009211; BIGipServerpool_trade_web_ids_weixin=43472906.22811.0000; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%225073100%22%2C%22%24device_id%22%3A%2216e030cf28193-079d692a99b32d-7711439-3686400-16e030cf282884%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216e030cf28193-079d692a99b32d-7711439-3686400-16e030cf282884%22%7D; JSESSIONID=node01nsjuk3petdbwkqdau42ag40m8546.node0; SSO_TOKEN_KEY=TGT-229b9ea4-8271-4cfa-9709-324a9273143b'
        
        
        # 且慢
        self.qiemanAuthorization = u'Bearer eyJ2ZXIiOiJ2MSIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiI3OTQ1NDkiLCJpc3MiOiJzc28ucWllbWFuLmNvbSIsImlzQWRtaW4iOmZhbHNlLCJleHAiOjE1NzI4MzM5NjgsImlhdCI6MTU3MTUzNzk2OCwianRpIjoiZTc2NTE2ZjgtZmI5MC00NmU2LThkN2EtYTQ5OTM4MGNlMzdlIn0.P2MoNRhOw-SwZhn1Rhqnxt60XyYvH2VVk79LmjHp6vlnti7iDbZowl9k562m4zJNQKdhk9OJzsnoHWekv6XYCQ'

        
        self.qiemanXSign = u'1572044082067188CDCFB0355779867A76AD05DF7F4A5'
        
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self,key,value)