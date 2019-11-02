# -*- coding: utf-8 -*-

import time

# 子线程监听剪切板
import threading

from tkinter import *
import tkinter as tk
import tkinter.messagebox

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
        # 窗口标题
        self.window.title('Https Header Saver')
        # 窗口尺寸
        self.window.geometry('640x480')
        self.clipboardValue = StringVar()
        self.clipboardValue.set(self.window.clipboard_get())
        self.createWidgets()
        # 开启剪切板监控子线程
        t = clipboardObserveThread(kwargs={ \
        thread_key_window : self.window,    \
        thread_key_clipboard_text_callback: self.clipboardTextUpdate   \
        })
        t.start()
        
    def createWidgets(self):
        klqHeaderRows = [u'tiantian_klq.txt',u'guangfa_klq.txt',u'qieman_klq.txt',u'danjuan_klq.txt',u'xueqiu_klq.txt']
        parentsHeadersRows = [u'tiantian_lsy.txt',u'danjuan_lsy.txt',u'danjuan_ksh.txt']
        operations = [u'抓取所有基金持仓',u'资产配置组合',u'持仓市值估计']
        col = 0
        tk.Label(self.window,text=u'康力泉 Headers',width=15,height=1).grid(row=0, column=col, padx=10, pady=10)
        for i in range(1,len(klqHeaderRows)+1):
            row = klqHeaderRows[i-1]
            tk.Button(self.window, text=row,width=15,height=1, bg="#F7A128", command = self.saveHeaderToFile(row)).grid(row=i, column=col, padx=10, pady=10)
        col = 1
        tk.Label(self.window,text=u'父母 Headers',width=15,height=1).grid(row=0, column=col, padx=10, pady=10)
        for i in range(1, len(parentsHeadersRows)+1):
            row = parentsHeadersRows[i-1]
            tk.Button(self.window, text=row,width=15,height=1, bg="#F2C300", command = self.saveHeaderToFile(row)).grid(row=i, column=col, padx=10, pady=10)
        col = 2
        tk.Label(self.window,text=u'操作',width=15,height=1).grid(row=0, column=col, padx=10, pady=10)
        for i in range(1, len(operations)+1):
            row = operations[i-1]
            tk.Button(self.window, text=row,width=15,height=1, bg="#00B1CC").grid(row=i, column=col, padx=10, pady=10)
        
        tk.Label(self.window,textvariable=self.clipboardValue,width=55,height=9,bg="#00B1CC").grid(row=6, column=0,columnspan=3, padx=10, pady=10)
    
    def intelligentMatchHeader(self,text):
        if text == '' or text == None:
            return
        if u'User-Agent' in text:
            print(u'\n\n[Attention] 监测到疑似 Header 数据')
        # 尝试匹配且慢
        if u'x-sign' in text:
            print(u'[Success] 成功匹配到网站 Header：且慢')
            result = tkinter.messagebox.askokcancel('成功匹配“且慢”', '要把剪切板上的内容覆盖到 qieman_klq.txt 吗？')
            if result == True:
                print(result)
                with open('qieman_klq.txt','w',encoding=u'utf-8') as f:
                    f.write(text)
            else:
                print(result)
            return
        # 尝试匹配广发基金
        if u'/mapi/account/assets/summary' in text:
            print(u'[Success] 成功匹配到网站 Header：广发基金')
            result = tkinter.messagebox.askokcancel('成功匹配“广发基金”', '要把剪切板上的内容覆盖到 guangfa_klq.txt 吗？')
            if result == True:
                print(result)
                with open('guangfa_klq.txt','w',encoding=u'utf-8') as f:
                    f.write(text)
            else:
                print(result)
            return
        # 尝试匹配雪球
        if u'u=2812376209' in text:
            print(u'[Success] 成功匹配到网站 Header：雪球')
            result = tkinter.messagebox.askokcancel('成功匹配“雪球”', '要把剪切板上的内容覆盖到 xueqiu_klq.txt 吗？')
            if result == True:
                print(result)
                with open('xueqiu_klq.txt','w',encoding=u'utf-8') as f:
                    f.write(text)
            else:
                print(result)
            return
        # 尝试匹配蛋卷基金 - 康力泉
        if u'gr_user_id=07a8b8b8-e04f-4bfa-b6bd-3492bb42b3a6' in text:
            print(u'[Success] 成功匹配到网站 Header：蛋卷基金 - 康力泉')
            result = tkinter.messagebox.askokcancel('成功匹配“蛋卷基金 - 康力泉”', '要把剪切板上的内容覆盖到 danjuan_klq.txt 吗？')
            if result == True:
                print(result)
                with open('danjuan_klq.txt','w',encoding=u'utf-8') as f:
                    f.write(text)
            else:
                print(result)
            return
        # 尝试匹配天天基金 - 康力泉
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
    
    def saveHeaderToFile(self,filename):
        print(f'save {filename}')

if __name__ == "__main__":
    app = functionPanel()
    app.show()