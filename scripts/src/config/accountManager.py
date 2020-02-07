# -*- coding: utf-8 -*-

import os
import sys
import json
# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
sys.path.append(srcDir)

from config.pathManager import pathManager
from config.colorConstants import colorConstants
from model.accountModel import accountModel

class accountManager:

    def __init__(self):
        self.pm = pathManager()
        self.colorManager = colorConstants()
        self.allAccounts = []
        dataPath = os.path.join(self.pm.configPath, 'account.json')
        
        if os.path.exists(dataPath):
            with open(dataPath,'r', encoding='utf-8') as f:
                self.allAccounts = json.loads(f.read())

    def getAccountByName(self,name):
        results = [x for x in self.allAccounts if name == x['accountName']]
        if len(results):
            return results[0]
        else:
            return '未知账户'

    def getSortIdByName(self,name):
        results = [x for x in self.allAccounts if name == x['accountName']]
        if len(results):
            return results[0]['sortId']
        else:
            return '未知账户'

    def getRecommendColorByName(self,name):
        results = [x for x in self.allAccounts if name == x['accountName']]
        if len(results):
            return results[0]['recommendColor']
        else:
            return '未知账户'

    def generateJsonFile(self):
        accounts = []

        account = accountModel()
        account.accountName = u'康力泉整体'
        account.sortId = 1
        account.owner = u'klq'
        account.appSource = u'all'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'父母整体'
        account.sortId = 2
        account.owner = u'parent'
        account.appSource = u'all'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'华泰证券'
        account.sortId = 101
        account.owner = u'klq'
        account.appSource = u'huatai'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'华宝证券'
        account.sortId = 102
        account.owner = u'klq'
        account.appSource = u'huabao'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)
        
        account = accountModel()
        account.accountName = u'天天基金'
        account.sortId = 201
        account.owner = u'klq'
        account.appSource = u'tiantian'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'天天基金母'
        account.sortId = 202
        account.owner = u'parent'
        account.appSource = u'tiantian'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'且慢 150 份'
        account.sortId = 301
        account.owner = u'klq'
        account.appSource = u'qieman'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'且慢 S 定投'
        account.sortId = 302
        account.owner = u'klq'
        account.appSource = u'qieman'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'稳稳的幸福父'
        account.sortId = 303
        account.owner = u'parent'
        account.appSource = u'qieman'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)
    # ZHIFUBAO = 5
    # FREEZE = 6
    # CASH = 7
    # NA = -1
        account = accountModel()
        account.accountName = u'螺丝钉'
        account.sortId = 401
        account.owner = u'klq'
        account.appSource = u'danjuan'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'钉钉宝90'
        account.sortId = 402
        account.owner = u'klq'
        account.appSource = u'danjuan'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'钉钉宝365'
        account.sortId = 403
        account.owner = u'klq'
        account.appSource = u'danjuan'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'螺丝钉母'
        account.sortId = 404
        account.owner = u'parent'
        account.appSource = u'danjuan'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'钉钉宝90母'
        account.sortId = 405
        account.owner = u'parent'
        account.appSource = u'danjuan'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'螺丝钉父'
        account.sortId = 406
        account.owner = u'parent'
        account.appSource = u'danjuan'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'钉钉宝365父'
        account.sortId = 407
        account.owner = u'parent'
        account.appSource = u'danjuan'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'支付宝'
        account.sortId = 501
        account.owner = u'klq'
        account.appSource = u'zhifubao'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'冻结资金'
        account.sortId = 601
        account.owner = u'klq'
        account.appSource = u'freeze'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'现金账户'
        account.sortId = 701
        account.owner = u'klq'
        account.appSource = u'cash'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        account = accountModel()
        account.accountName = u'现金账户父母'
        account.sortId = 702
        account.owner = u'parent'
        account.appSource = u'cash'
        account.marketcap = 0.00
        account.gain = 0.00
        account.gainRate = 0.00
        account.recommendColor = '#' + self.colorManager.getFundColorByAppSourceName(account.accountName)
        accounts.append(account.__dict__)

        with open(os.path.join(self.pm.configPath, 'account.json'),'w+', encoding='utf-8') as f:
            f.write(json.dumps(accounts, ensure_ascii=False, indent = 4, separators=(',', ':')))

        self.allAccounts = accounts

if __name__ == "__main__":
    manager = accountManager()
    manager.generateJsonFile()
    # print(manager.getAccountByName('康力泉整体'))
    manager.allAccounts.sort(key=lambda x : x['sortId'])
    for i in manager.allAccounts:
        print(i)