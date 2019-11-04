# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess

# 子线程监听剪切板
import threading

from tkinter import *
import tkinter as tk
import tkinter.messagebox

# 把父路径加入到 sys.path 供 import 搜索
currentDir = os.path.abspath(os.path.dirname(__file__))
srcDir = os.path.dirname(currentDir)
sys.path.append(srcDir)
from config.pathManager import pathManager

# 跨线程沟通 key
thread_key_window = 'window'
thread_key_clipboard_text_callback = 'callback'

# 剪切板监控子线程
class clipboardObserveThread(threading.Thread):
     def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
         super().__init__(group=group, target=target, name=name, daemon=daemon)
         self.args = args
         self.kwargs = kwargs
 
     def run(self):
        #print("running with %s and %s" % (self.args, self.kwargs))
        window = self.kwargs[thread_key_window]
        mainThreadCallback = self.kwargs[thread_key_clipboard_text_callback]
        # recent_txt 存放最近一次剪切板文本
        recent_txt = window.clipboard_get()
        print(f'\n当前剪切板内容\n\n{recent_txt}')
        
        while True:
            # txt 存放当前剪切板文本
            txt = window.clipboard_get()
            # 剪切板内容和上一次对比如有变动，再进行内容判断，判断后如果发现有指定字符在其中的话，再执行替换
            if txt != recent_txt:
                print(f'\n当前剪切板内容:\n\n{txt}')
                recent_txt = txt
                mainThreadCallback(txt)
            # 检测间隔（延迟0.2秒）
            time.sleep(0.5)

class functionPanel:
    def __init__(self):
        # 主窗口
        self.window = tk.Tk()
        self.window.wm_attributes('-topmost',1)

        # 窗口标题
        self.window.title('Finance Data Operation Panel')
        # 窗口尺寸
        self.window.geometry('542x360+100-100') # +{0} = origin.x 80 +{1} = origin.y
        self.clipboardValue = StringVar()   
        self.clipboardValue.set(self.window.clipboard_get())
        self.createWidgets()
        # 开启剪切板监控子线程
        t = clipboardObserveThread(kwargs={ \
        thread_key_window : self.window,    \
        thread_key_clipboard_text_callback: self.clipboardTextUpdate   \
        })
        t.start()
    
    # 创建子视图
    def createWidgets(self):
        klqHeaders = [u'tiantian_klq.txt',u'guangfa_klq.txt',u'qieman_klq.txt',u'danjuan_klq.txt',u'xueqiu_klq.txt']
        parentsHeaders = [u'tiantian_lsy.txt',u'tiantian_ksh.txt', u'danjuan_lsy.txt',u'danjuan_ksh.txt']
        
        shorthands = [u'all webs', u'src Folder', u'config Folder',u'input Folder', u'output Folder',u'echarts Folder']
        operations = [u'allFundSpider a',u'allFundSpider b',u'assetCombine c',u'assetCombine b', u'estimateExcel a', u'estimateExcel b']
        col = 0
        tk.Label(self.window,text=u'My Headers',width=15,height=1).grid(row=0, column=col, padx=10, pady=10)
        for i in range(1,len(klqHeaders)+1):
            row = klqHeaders[i-1]
            # tkinter 要求由按钮（或者其它的插件）触发的控制器函数不能含有参数，如果有，需要 lambda，下同
            button = tk.Button(self.window, text=row,width=15,height=1, bg="#F7A128")
            button.grid(row=i, column=col, padx=10, pady=10)
            # 为左键单击事件绑定处理方法
            button.bind(u'<Button>', self.saveHeaderToFile)
            # 为左键双击事件绑定处理方法
            #bn.bind('<Double-1>', self.double)
        col = 1
        tk.Label(self.window,text=u'Parents Headers',width=15,height=1).grid(row=0, column=col, padx=10, pady=10)
        for i in range(1, len(parentsHeaders)+1):
            row = parentsHeaders[i-1]
            button = tk.Button(self.window, text=row,width=15,height=1, bg="#F2C300")
            button.grid(row=i, column=col, padx=10, pady=10)
            # 为左键单击事件绑定处理方法
            button.bind(u'<Button>', self.saveHeaderToFile)
            
        col = 2
        tk.Label(self.window,text=u'shorthands',width=15,height=1).grid(row=0, column=col, padx=10, pady=10)
        for i in range(1, len(shorthands)+1):
            row = shorthands[i-1]
            button = tk.Button(self.window, text=row,width=15,height=1, bg="#BE8663")
            button.grid(row=i, column=col, padx=10, pady=10)
            # 为左键单击事件绑定处理方法
            button.bind(u'<Button>', self.shorthandSelect)

        col = 3
        tk.Label(self.window,text=u'operations',width=15,height=1).grid(row=0, column=col, padx=10, pady=10)
        for i in range(1, len(operations)+1):
            row = operations[i-1]
            button = tk.Button(self.window, text=row,width=15,height=1, bg="#00B1CC")
            button.grid(row=i, column=col, padx=10, pady=10)
            # 为左键单击事件绑定处理方法
            button.bind(u'<Button>', self.functionSelect)
        #tk.Label(self.window,textvariable=self.clipboardValue,width=55,height=8,bg="#00B1CC").grid(row=6, column=0,columnspan=3, padx=10, pady=10)

    # 保存 header 到文件
    def saveHeaderToFile(self, event):
        #print("左键单击:%s" % event.widget['text'])
        clipboardText = self.clipboardValue.get()
        if not self.isSupposeToBeHeaderText(clipboardText):
            result = tkinter.messagebox.showerror(u'错误', u'剪切板信息不像是 Header（不包含 User-Agent）')
            return
        else:
            pm = pathManager()
            filename = event.widget['text']
            filepath = os.path.join(pm.configPath,u'requestHeader',filename)
            print(f'保存文件：{filepath}')
            with open(filepath,'w',encoding='utf-8') as f:
                f.write(clipboardText)
            result = tkinter.messagebox.showinfo('', u'保存成功')
    
    # 快捷打开多个文件夹
    def shorthandSelect(self,event):
        # print("打开：%s" % event.widget['text'].replace(' Folder',''))
        param = event.widget['text'].replace(' Folder','')
        pm = pathManager()
        if param == u'src':
            os.startfile(pm.parentDir)
        if param == u'config':
            os.startfile(pm.configPath)
        if param == u'input':
            os.startfile(pm.inputPath)
        if param == u'output':
            os.startfile(pm.outputPath)
        if param == u'echarts':
            os.startfile(pm.echartsPath)
        if param == u'all webs':
            # 打开所有网页
            os.startfile(u'http://www.1234567.com.cn/')
            os.startfile(u'http://www.gffunds.com.cn/')
            os.startfile(u'http://www.qieman.com/')
            os.startfile(u'http://www.danjuanapp.com/')
            os.startfile(u'http://www.xueqiu.com/')
        
    def functionSelect(self,event):
        print("功能选择：%s" % event.widget['text'])
        params = event.widget['text'].split(' ')
        pm = pathManager()
        if params[0] == u'allFundSpider':
            pyFile = os.path.join(pm.parentDir,u'allFundSpider.py')
            args = [r"powershell","python",pyFile,params[1]]
            print('[Executing] {0} ...'.format(pyFile))
            p = subprocess.Popen(args)
        if params[0] == u'assetCombine':
            pyFile = os.path.join(pm.parentDir,u'assetAllocationCombine.py')
            args = [r"powershell","python",pyFile,params[1]]
            print('[Executing] {0} ...'.format(pyFile))
            p = subprocess.Popen(args)
        if params[0] == u'estimateExcel':
            pyFile = os.path.join(pm.parentDir,u'assetAllocationEstimateExcelParser.py')
            args = [r"powershell","python",pyFile,params[1]]
            print('[Executing] {0} ...'.format(pyFile))
            p = subprocess.Popen(args)
        
    def isSupposeToBeHeaderText(self,text):
        if text == '' or text == None:
            return False
        if u'User-Agent' in text or u'user-agent' in text:
            return True
        else:
            return False
            
    def intelligentMatchHeader(self,text):
        if self.isSupposeToBeHeaderText(text):
            print(u'\n\n[Attention] 监测到疑似 Header 数据')
        pm = pathManager()
        # 尝试匹配且慢
        if u'x-sign' in text:
            print(u'[Success] 成功匹配到网站 Header：且慢')
            result = tkinter.messagebox.askokcancel('成功匹配“且慢”', '要把剪切板上的内容覆盖到 qieman_klq.txt 吗？')
            if result == True:
                filepath = os.path.join(pm.configPath,u'requestHeader',u'qieman_klq.txt')
                print(filepath)
                with open(filepath,'w',encoding=u'utf-8') as f:
                    f.write(text)
            else:
                print(result)
            return
        # 尝试匹配广发基金
        if u'/mapi/account/assets/summary' in text:
            print(u'[Success] 成功匹配到网站 Header：广发基金')
            result = tkinter.messagebox.askokcancel('成功匹配“广发基金”', '要把剪切板上的内容覆盖到 guangfa_klq.txt 吗？')
            if result == True:
                filepath = os.path.join(pm.configPath,u'requestHeader',u'guangfa_klq.txt')
                print(filepath)
                with open(filepath,'w',encoding=u'utf-8') as f:
                    f.write(text)
            else:
                print(result)
            return
        # 尝试匹配雪球
        if u'u=2812376209' in text:
            print(u'[Success] 成功匹配到网站 Header：雪球')
            result = tkinter.messagebox.askokcancel('成功匹配“雪球”', '要把剪切板上的内容覆盖到 xueqiu_klq.txt 吗？')
            if result == True:
                filepath = os.path.join(pm.configPath,u'requestHeader',u'xueqiu_klq.txt')
                print(filepath)
                with open(filepath,'w',encoding=u'utf-8') as f:
                    f.write(text)
            else:
                print(result)
            return
        # 尝试匹配蛋卷基金 - 康力泉
        if u'gr_user_id=07a8b8b8-e04f-4bfa-b6bd-3492bb42b3a6' in text:
            print(u'[Success] 成功匹配到网站 Header：蛋卷基金 - 康力泉')
            result = tkinter.messagebox.askokcancel('成功匹配“蛋卷基金 - 康力泉”', '要把剪切板上的内容覆盖到 danjuan_klq.txt 吗？')
            if result == True:
                filepath = os.path.join(pm.configPath,u'requestHeader',u'danjuan_klq.txt')
                print(filepath)
                with open(filepath,'w',encoding=u'utf-8') as f:
                    f.write(text)
            else:
                print(result)
            return
        # 尝试匹配天天基金 - 康力泉    POST /do.aspx/CheckLogin HTTP/1.1
        #if u'gr_user_id=07a8b8b8-e04f-4bfa-b6bd-3492bb42b3a6' in text:
        #    print(u'[Success] 成功匹配到网站 Header：蛋卷基金 - 康力泉')
        #    result = tkinter.messagebox.askokcancel('成功匹配“蛋卷基金 - 康力泉”', '要把剪切板上的内容覆盖到 danjuan_klq.txt 吗？')
        #    if result == True:
        #        print(result)
        #        with open('danjuan_klq.txt','w',encoding=u'utf-8') as f:
        #            f.write(text)
        #    else:
        #        print(result)
        #    return
        
        
    def clipboardTextUpdate(self,text):
        self.clipboardValue.set(text)
        # 智能匹配
        self.intelligentMatchHeader(text)
    
    def show(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = functionPanel()
    app.show()