import sys
import os
import re
import json
import requests
# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
sys.path.append(srcDir)
from config.assetCategoryManager import assetCategoryManager

class fundNavManager:

    def __init__(self):
        self.categoryManager = assetCategoryManager()
        self.allCodes = self.categoryManager.getCanUpdateNavFunds().values()
        # print(self.categoryManager.getCanUpdateNavFunds())
        pass

    def getFundNav(self, code):
        url = f'http://hq.sinajs.cn/?list=f_{code}'
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        response = requests.get(url, headers=header)
        # e.g. # var hq_str_f_001064="广发中证环保ETF联接A,0.5486,0.5486,0.5474,2019-12-04,21.9453";
        pattern = re.compile(r'var hq_str_f_([0-9]{6})="(.*?)";')
        result = re.findall(pattern, response.text)
        if len(result[0]) > 1 and len(result[0][1]) > 0:
            keys = ['基金代码','单位净值','净值日期','基金名称']
            values = result[0][1].split(',')
            navName = values[0]
            navValue = values[1]
            navDate = values[4]
            return dict(zip(keys,[code, round(float(navValue),4), navDate, navName]))
        else:
            print(f'{code} 获取净值失败')
            return None
        pass


if __name__ == "__main__":
    manager = funNavManager()
    for code in manager.allCodes:
        print(manager.getFundNav(code))