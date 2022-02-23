from tkinter import *
from tkinter.ttk import *
import ctypes
import OneBrowser_auto
from threading import Thread


def start_browser():
    OneBrowser_auto.login_name = na.get()
    OneBrowser_auto.login_password = pa.get()
    sd1 = sd.get()
    sd2 = ed.get()
    t = Thread(target=OneBrowser_auto.autoPatch, args=(sd1, sd2), daemon=True)
    t.start()
    r.withdraw()


ctypes.windll.shcore.SetProcessDpiAwareness(True)
r = Tk()
r.title('gisaid 病例数据爬虫')
font = '微软雅黑 18'


na = Entry(r, font=font, width=11)
pa = Entry(r, font=font, width=11)
sd = Entry(r, font=font, width=11)
ed = Entry(r, font=font, width=11)
na.grid(row=0, column=1, pady=2)
pa.grid(row=0, column=3, pady=2)
sd.grid(row=1, column=1, pady=2)
ed.grid(row=1, column=3, pady=2)
Label(r, text='账号', font=font).grid(row=0, column=0)
Label(r, text='密码', font=font).grid(row=0, column=2)
Label(r, text='起始日期', font=font).grid(row=1, column=0)
Label(r, text='终止日期', font=font).grid(row=1, column=2)
Button(r, text='开始', command=start_browser).grid(row=2, columnspan=4)
r.mainloop()
