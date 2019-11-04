# -*- coding: utf-8 -*-
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# API Doc: https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
class dingtalk:

    def __init__(self):
        self.url = u'https://oapi.dingtalk.com/robot/send?access_token=626ff44da3081625d25d9d589c3f7d758acfdc124826ca0c8b66c87667ed28d8'
        self.headers = \
        {   \
            'Content-Type': 'application/json',\
        }

    def sendMessage(self,text):
        dict = {'msgtype':'text'}
        print(text)
        assert u'市值' in text or u'估值' in text or u'账户' in text, '钉钉机器人文案信息中必须包含对应的“标签”，否则服务器验证失败'
        dict['text'] = {'content':text}
        data = json.dumps(dict)
        #print(data)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(self.url, verify=False, headers=self.headers, data=data)
        if response.status_code != 200:
            print(response.text)
        #response.text = \
        #{  \
        #	"errcode": 0,   \
        #	"errmsg": "ok"  \
        #}
        
if __name__ == "__main__":
    dingtalk().sendMessage(u'市值测试')