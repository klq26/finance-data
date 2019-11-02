# -*- coding: utf-8 -*-

import os
import sys
import subprocess

klqSpiderArray = ['tiantianSpider.py','guangfaSpider.py','qiemanSpider.py','danjuanSpider.py','huataiSpider.py']
parentSpidersArray = ['tiantianSpider.py','danjuanSpider.py']

for pyFile in klqSpiderArray:
    args = [r"powershell","python",pyFile,"a"]
    print('[Executing] {0}...'.format(pyFile))
    p = subprocess.Popen(args)#, stdout=subprocess.PIPE)
    #out = p.stdout.readlines()
    #for line in out:
    #    print(line.strip().decode('utf-8'))
