# -*- coding: utf-8 -*-

import os
import sys
# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
sys.path.append(srcDir)
from config.assetCategoryManager import assetCategoryManager

class assetCategoryConstants:

    def __init__(self):
        self.categoryManager = assetCategoryManager()
        self.category1Array = self.categoryManager.category1Array
        self.category2Array = self.categoryManager.category2Array
        self.category3Array = self.categoryManager.category3Array
