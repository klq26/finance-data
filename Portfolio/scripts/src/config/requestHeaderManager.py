    # -*- coding: utf-8 -*-
import os

class requestHeaderManager:

    def __init__(self):
        #self.users = [u'klq',u'lsy',u'ksh'] # 康力泉，李淑云，康世海
        #self.webs = [u'danjuan',u'qieman',u'tiantian',u'guangfa']   # 蛋卷，且慢，天天基金，广发基金
        self.folder = os.path.join(os.path.abspath(os.path.dirname(__file__)),u'requestHeader')
        # 便于外部函数快速打开所有的 header.txt
        self.klqHeaderfiles = \
        [\
            os.path.join(self.folder,u'xueqiu_klq.txt'),\
            os.path.join(self.folder,u'danjuan_klq.txt'),\
            os.path.join(self.folder,u'qieman_klq.txt'),\
            os.path.join(self.folder,u'guangfa_klq.txt'),\
            os.path.join(self.folder,u'tiantian_klq.txt'),\
        ]
        self.parentsHeaderfiles = \
        [\
            os.path.join(self.folder,u'tiantian_ksh.txt'),\
            os.path.join(self.folder,u'danjuan_ksh.txt'),\
            os.path.join(self.folder,u'danjuan_lsy.txt'),\
            os.path.join(self.folder,u'tiantian_lsy.txt'),\
            
        ]

    def getDanjuanKLQ(self):
        return self.getHeaders(os.path.join(self.folder,u'danjuan_klq.txt'))
        
    def getDanjuanLSY(self):
        return self.getHeaders(os.path.join(self.folder,u'danjuan_lsy.txt'))
        
    def getDanjuanKSH(self):
        return self.getHeaders(os.path.join(self.folder,u'danjuan_ksh.txt'))
        
    def getTiantianKLQ(self):
        return self.getHeaders(os.path.join(self.folder,u'tiantian_klq.txt'))
        
    def getTiantianLSY(self):
        return self.getHeaders(os.path.join(self.folder,u'tiantian_lsy.txt'))
    
    def getTiantianKSH(self):
        return self.getHeaders(os.path.join(self.folder,u'tiantian_ksh.txt'))
        
    def getQiemanKLQ(self):
        return self.getHeaders(os.path.join(self.folder,u'qieman_klq.txt'))
        
    def getGuangfaKLQ(self):
        return self.getHeaders(os.path.join(self.folder,u'guangfa_klq.txt'))
    
    def getXueqiuKLQ(self):
        return self.getHeaders(os.path.join(self.folder,u'xueqiu_klq.txt'))
        
    def getHeaders(self,filepath):
        headers = {}
        with open(filepath,'r',encoding=u'utf-8') as f:
            lines = f.readlines()
            for i in range(1,len(lines)):
                line = lines[i].strip('\n')
                values = line.split('\t')
                headers[values[0]] = values[1]
        return headers
        
if __name__ == '__main__':
    manager = requestHeaderManager()
    #manager.getHeaders('requestHeader\danjuan_klq.txt')
    print(manager.getDanjuanKLQ())
    print('\n')
    print(manager.getDanjuanLSY())
    print('\n')
    print(manager.getDanjuanKSH())
    print('\n')
    print(manager.getTiantianKLQ())
    print('\n')
    print(manager.getTiantianLSY())
    print('\n')
    print(manager.getQiemanKLQ())
    print('\n')
    print(manager.getGuangfaKLQ())
    print('\n')
    print(manager.klqHeaderfiles)
    print('\n')
    print(manager.parentsHeaderfiles)