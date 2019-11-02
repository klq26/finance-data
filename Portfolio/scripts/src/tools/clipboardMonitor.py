#import win32clipboard
from tkinter import *
import re
import time

def clipboard_get():
    """获取剪贴板数据"""
    #win32clipboard.OpenClipboard()
    #data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    #win32clipboard.CloseClipboard()
    r = Tk()
    data = r.clipboard_get()
    return data


#def clipboard_set(data):
    #"""设置剪贴板数据"""
    #win32clipboard.OpenClipboard()
    #win32clipboard.EmptyClipboard()
    #win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, data)
    #win32clipboard.CloseClipboard()

def main():
    """后台脚本：每隔几秒，读取剪切板文本，如有变化，询问存入何处"""
    # recent_txt 存放最近一次剪切板文本
    recent_txt = clipboard_get()
    print(f'当前剪切板内容:\n{recent_txt}')

    while True:
        # txt 存放当前剪切板文本
        txt = clipboard_get()

        # 剪切板内容和上一次对比如有变动，再进行内容判断，判断后如果发现有指定字符在其中的话，再执行替换
        if txt != recent_txt:
            print(f'\n当前剪切板内容:\n{txt}')
            recent_txt = txt
        # 检测间隔（延迟0.2秒）
        time.sleep(3)

if __name__ == '__main__':
    main()