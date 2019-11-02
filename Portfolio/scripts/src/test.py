# -*- coding: utf-8 -*-

import os
import sys
import subprocess

args = ['debug']
p = subprocess.Popen("huataiSpider.py",args, stdout=subprocess.PIPE)
out = p.stdout.readlines()
print(out)
