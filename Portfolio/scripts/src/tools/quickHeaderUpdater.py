# -*- coding: utf-8 -*-
import os
import sys
from config.requestHeaderManager import requestHeaderManager

class quickHeaderUpdater:

    def __init__(self,strategy):
        print(r'(https://trade.gffunds.com.cn/mapi/account/assets/summary)|(https://qieman.com/pmdj/v2/uma/(.*?)/detail)|(https://danjuanapp.com/djapi/account/user_info_check)|(https://trade.1234567.com.cn/do.aspx/CheckLogin)')
        self.headerManager = requestHeaderManager()
        if strategy == 'a':
            for file in self.headerManager.klqHeaderfiles:
                os.startfile(file)
        elif strategy == 'b':
            for file in self.headerManager.parentsHeaderfiles:
                os.startfile(file)

if __name__ == '__main__':
    strategy = 'a'
    if len(sys.argv) >= 2:
        #print(u'[ERROR] 参数不足。需要键入策略编号。a：康力泉 b：父母')
        strategy = sys.argv[1]
    if strategy == 'a':
        quickHeaderUpdater('a')
    elif strategy == 'b':
        quickHeaderUpdater('b')