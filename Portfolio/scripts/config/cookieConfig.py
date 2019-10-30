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
        self.tiantianCookieKLQ = u'Cookie: https://trade.1234567.com.cn/MyAssets/bankcardtb-banktbb=0; st_si=48193464463530; ASP.NET_SessionId=rvw2hcfyyuwbsm4h1zg2vw4j; st_asi=delete; b_p_log_key=UXRF8fAgsvU1SArYSDZb1vNi/JgRlELFdZEJcyP6AshghN+GTGQZhKJmUzB8WTAY5eYgy3QDKWSkjTh6709wxqrYbnqGW8s/gMglTQ0MCnP4PcCtIi4=; b_pl_bq=de9612a5f90c4a9bab2a853807e9822c; FundTradeLoginTab=0; FundTradeLoginCard=0; st_pvi=69416177127426; st_sp=2019-08-25%2008%3A06%3A30; st_inirUrl=https%3A%2F%2Ftrade7.1234567.com.cn%2FQuery%2Fbill; st_sn=35; st_psi=20191030091626868-112200304021-6184395201; cp_token=e08e3dbaaa7f4885b1b7e6a68f082127; FundTradeLoginUser=JYpZs7wl02NeUAeZPlVGCVlYJd8Rmnx+V4CBTWmHYZxGbKHCZigL5g7O2loGw0pePOWxBzAl; fund_trade_cn=JJSstQscaBdC3g2QKg6ArF5T3c20VFPbX70hiW/zQ1RfcCK9Hf6SHIHqToZwTJu46yhF1TK+X9H+CuZAuVOc71TR2UuaDxxM31eNZd22FKuo12Nv+Ks=; fund_trade_name=JR0jpZmO+2j/oIzxfdVEbegJVDPRHB2gtHejT/tx+Q3NxKa89Qg+yu7GO9TUgxCeG6Bx6GsB; fund_trade_visitor=JA8w7QdW52aDCofp1BVMzEoMHtGRL7rMyuv9TusrCl/nlKpCPStoqx7FDv33p4weWvba2/CX; fund_trade_risk=J5xYNbQac2sxPwRNrqVym1PSJBsRjceBsElETUYF4hvw/KMwbIAcam7ftj1syaKe6r8qNitL; fund_trade_gps=6; VipLevel=1; TradeLoginToken=3df20b61da7d43f9b8e713a177fb900a; UTOKEN=JJSstQscaBdC3g2QKg6ArF5T3c20VFPbX70hiW/zQ1RfcCK9Hf6SHIHqToZwTJu46yhF1+KcANJc1f1ySTy87RTKlQEvAm9hXse00gfVRCQYInzRWbA=; LToken=3197151a70d541768d6be25be713dd75; fund_trade_trackid=IeO4mfzFvR0qAIwK3TV3gYnUtW8LY1HViadb2B1Q28TFqzxYIY/s6mdnlXeQ6rd+OwkW2m4E53s3HaTCEJ0J6g=='



        self.tiantianCookieMother = u'Cookie: st_si=16011911173883; st_sn=1; st_psi=20191029164402971-112200304021-8232083332; st_asi=delete; st_pvi=58108632980853; st_sp=2019-10-29%2016%3A44%3A03; st_inirUrl=http%3A%2F%2F1234567.com.cn%2F; cp_token=e26448a81cb1416c82c12233a5b47cd6; FundTradeLoginUser=KrzGU+Qlorb6bbvngwo0+jcUzR3rgs1jJ75NjyTLX0xuJMH4y0AY7yFFUCE1qWUymiKNM9VL; fund_trade_cn=KU+09YNmCUfnuhrSXYwZE1Zu6nqIojW6u8enQWKA42rBZd/Q/EsOoz3ojROCEwwGKFB7QbMaKX+kRhNvmQSZFONNX+7LDEJSgAyOHUauZhrZmssB6HQ=; fund_trade_name=KgZ/z5iSFrAkCoVwtjoFY0LzgOtrMInbTZdqjvzpj0EnpMVT3JNAsdF9BvyB95iyqJvrj8Ar; fund_trade_visitor=K9+62op4ir6nS8CPE7oIzNfJUHBrAh7rx4KLjUte6hM2jMATfIhNqsF5LxFYoc8y2AKmtpcY; fund_trade_risk=K+OTxocBjrLeBAMGrjoUDWmKSmMrcoXYW4/ej81wELbSnMEFWWgzR5FbM40y1IsyYCmYtrlD; fund_trade_gps=7; VipLevel=1; TradeLoginToken=b14bb0eda3da496ab4adce1b06efe04f; UTOKEN=KU+09YNmCUfnuhrSXYwZE1Zu6nqIojW6u8enQWKA42rBZd/Q/EsOoz3ojROCEwwGKFB7QgMV3Up1itnSR08qF350Bozy9Ru7tWyFDUIhCHUg/qkjkQQ=; LToken=4c3deae85cd74913b51346faeacf838e; fund_trade_trackid=D7+hAhecrWQvkpjpmpvFeFBu2Ob62iBSyIrRq8UiRP8uxZvVN3vPbxOcQMY9nUWrTko4D8hpQBsxjxHC+tqaIg==; FundTradeLoginTab=0; FundTradeLoginCard=0; ASP.NET_SessionId=njifb4pydjfxvahjchm1zvhv'
        
        
        self.tiantianCookieFather = u''
        
        
        # 蛋卷基金
        self.danjuanCookieKLQ = u'Cookie: device_id=web_ByL9-IyHH; _ga=GA1.2.1578122713.1566691726; gr_user_id=07a8b8b8-e04f-4bfa-b6bd-3492bb42b3a6; thirdparty_token=; thirdparty_source=; thirdparty_nickname=; thirdparty_avatar=; xq_a_token=489a94320ff7bc390513c200bc41187b51db60d2; Hm_lvt_b53ede02df3afea0608038748f4c9f36=1569888571; _gid=GA1.2.2054521569.1571888134; channel=1300100141; gr_session_id_94b96c7a661bf17a=863c6d03-fdc3-4893-8449-37a2168b5f15; gr_session_id_94b96c7a661bf17a_863c6d03-fdc3-4893-8449-37a2168b5f15=true; _gat_gtag_UA_16079156_7=1; accesstoken=2400200003f67a5d8529dc72490a4120205d081c0596633fe; uid=203274561; refreshtoken=2400200008076cc9f34c243ace0052b329753dab3dc9466b2; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22203274561%22%2C%22%24device_id%22%3A%2216cc61a9198303-0a4b8d7e767657-7373e61-3686400-16cc61a9199311%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216cc61a9198303-0a4b8d7e767657-7373e61-3686400-16cc61a9199311%22%7D; Hm_lpvt_b53ede02df3afea0608038748f4c9f36=1571891904; timestamp=1571891914488'
        
        
        self.danjuanCookieMother = u'Cookie: device_id=web_ByL9-IyHH; _ga=GA1.2.1578122713.1566691726; gr_user_id=07a8b8b8-e04f-4bfa-b6bd-3492bb42b3a6; thirdparty_token=; thirdparty_source=; thirdparty_nickname=; thirdparty_avatar=; xq_a_token=489a94320ff7bc390513c200bc41187b51db60d2; Hm_lvt_b53ede02df3afea0608038748f4c9f36=1569888571; accesstoken=24002000044084327ac204d6b9759b4331bba0cb995965fbd; refreshtoken=240020000e085adf5202568b98a9eb2d03fb7399755ca84dd; uid=194897199; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22194897199%22%2C%22%24device_id%22%3A%2216cc61a9198303-0a4b8d7e767657-7373e61-3686400-16cc61a9199311%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216cc61a9198303-0a4b8d7e767657-7373e61-3686400-16cc61a9199311%22%7D; _gid=GA1.2.2054521569.1571888134; channel=1300100141; Hm_lpvt_b53ede02df3afea0608038748f4c9f36=1571888426; _gat_gtag_UA_16079156_7=1; timestamp=1571888426460'
        
        
        self.danjuanCookieFather = u'Cookie: device_id=web_ByL9-IyHH; _ga=GA1.2.1578122713.1566691726; gr_user_id=07a8b8b8-e04f-4bfa-b6bd-3492bb42b3a6; thirdparty_token=; thirdparty_source=; thirdparty_nickname=; thirdparty_avatar=; xq_a_token=489a94320ff7bc390513c200bc41187b51db60d2; Hm_lvt_b53ede02df3afea0608038748f4c9f36=1569888571; _gid=GA1.2.2054521569.1571888134; channel=1300100141; _gat_gtag_UA_16079156_7=1; gr_session_id_94b96c7a661bf17a=863c6d03-fdc3-4893-8449-37a2168b5f15; gr_session_id_94b96c7a661bf17a_863c6d03-fdc3-4893-8449-37a2168b5f15=true; accesstoken=240020000d176abe5f5153802ff08f4dc9a1b43462cc8ea53; uid=576923716; refreshtoken=2400200009298cd46784d85ceb8cf6aaecb19c333aee9e001; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22576923716%22%2C%22%24device_id%22%3A%2216cc61a9198303-0a4b8d7e767657-7373e61-3686400-16cc61a9199311%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216cc61a9198303-0a4b8d7e767657-7373e61-3686400-16cc61a9199311%22%7D; Hm_lpvt_b53ede02df3afea0608038748f4c9f36=1571891597; timestamp=1571891605116'
        
        
        # 广发基金（*支付宝）
        self.guangfaCookie = u'Cookie: _ga=GA1.3.2121823865.1572009211; BIGipServerpool_trade_web_ids_weixin=43472906.22811.0000; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%225073100%22%2C%22%24device_id%22%3A%2216e030cf28193-079d692a99b32d-7711439-3686400-16e030cf282884%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216e030cf28193-079d692a99b32d-7711439-3686400-16e030cf282884%22%7D; _gid=GA1.3.1901076293.1572398100; _gat=1; JSESSIONID=node01jm727xhxtkox8ep6d3gktwlv54645.node0; SSO_TOKEN_KEY=TGT-04b34eb6-e1b0-49fe-afa8-40e3fedcd2b3'
        
        
        # 且慢
        self.qiemanAuthorization = u'Bearer eyJ2ZXIiOiJ2MSIsImFsZyI6IkhTNTEyIn0.eyJzdWIiOiI3OTQ1NDkiLCJpc3MiOiJzc28ucWllbWFuLmNvbSIsImlzQWRtaW4iOmZhbHNlLCJleHAiOjE1NzM2Mzg3ODYsImlhdCI6MTU3MjM0Mjc4NiwianRpIjoiYjZlMDYwZDktMjk3MS00MmNlLWFjOTgtODhiMjAzZTM1NjVlIn0.zZf-dhoPWhvgbiHWjiUJzY_gj9fY_jO6jOifKBHhAQxGHBmmvPuHlrMXYDFBhUUgcf2aPsJLU672EfP8HWrOGQ'
        self.qiemanXSign = u'1572398065114D54A927FB18077BBDB14B68E86320772'
        
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self,key,value)