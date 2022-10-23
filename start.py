# coding: utf-8
from tkinter import *
import ctypes
from tkinter.filedialog import askopenfilename
from gisaid_downloader import spider_loop


font = '微软雅黑 12'


def choose_file():
    fname = askopenfilename()
    en.delete(0, END)
    en.insert(0, fname)


def mb(b):
    if b.cget('text') == '√':
        b.config(text=' ')
    else:
        b.config(text='√')


def start_download():
    blist = [b1, b2, b3, b4, b5]
    name = e1.get()
    password = e2.get()
    filename = en.get()
    try:
        spider_loop(
            name=name,
            password=password,
            mission_file=filename,
            is_gui=eb.cget('text')=='√',
            download_ranks=[
                blist.index(i) for i in blist if i.cget('text')=='√'
            ],
        )
    except:
        r.title('gisaid 数据下载（信息填写错误）')


ctypes.windll.shcore.SetProcessDpiAwareness(True)
r = Tk()

r.title('gisaid 数据下载')
f = Frame(r)
f.pack(fill=X)
f.rowconfigure(0, weight=1)

en = Entry(f, font=font)
en.pack(side=LEFT, expand=True, fill=X)
Button(f, text='选择文件', command=choose_file, font=font, relief='solid').pack(side=LEFT)

f2 = Frame(r)
f2.pack(fill=X)

Label(f2, text='账号名', font=font).grid(row=0, column=0)
Label(f2, text='密码', font=font).grid(row=1, column=0)
e1 = Entry(f2, font=font)
e2 = Entry(f2, font=font)
e1.grid(row=0, column=1, sticky='we')
e2.grid(row=1, column=1, sticky='we')

Label(f2, text='选择要下载的类型', font=font).grid(row=2, column=0, columnspan=2, sticky='we')
Label(f2, text='1.Dates and Location', font=font).grid(row=3, column=0)
Label(f2, text='2.Input for the Augur pipeline', font=font).grid(row=4, column=0)
Label(f2, text='3.Nucleotide Sequences (FASTA)', font=font).grid(row=5, column=0)
Label(f2, text='4.Patient status metadata', font=font).grid(row=6, column=0)
Label(f2, text='5.Sequencing technology metadata', font=font).grid(row=7, column=0)

b1 = Button(f2, text=' ', relief='solid', font=font, command=lambda:mb(b1))
b2 = Button(f2, text='√', relief='solid', font=font, command=lambda:mb(b2))
b3 = Button(f2, text=' ', relief='solid', font=font, command=lambda:mb(b3))
b4 = Button(f2, text=' ', relief='solid', font=font, command=lambda:mb(b4))
b5 = Button(f2, text=' ', relief='solid', font=font, command=lambda:mb(b5))

b1.grid(row=3, column=1, sticky='we')
b2.grid(row=4, column=1, sticky='we')
b3.grid(row=5, column=1, sticky='we')
b4.grid(row=6, column=1, sticky='we')
b5.grid(row=7, column=1, sticky='we')

f2.columnconfigure(1, weight=1)

f3 = Frame(r)
Label(f3, text='是否开启界面', font=font).grid(row=0, column=0)
eb = Button(f3, text=' ', font=font, relief='solid', command=lambda:mb(eb))
eb.grid(row=0, column=1, sticky='we')
f3.columnconfigure(1, weight=1)
f3.pack(fill=X, expand=True)

Button(r, text='开始下载', command=start_download, font=font, relief='solid', bg='tomato').pack(fill=X)

r.mainloop()
