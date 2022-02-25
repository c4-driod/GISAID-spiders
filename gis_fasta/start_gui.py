from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
from threading import Thread
from datetime import datetime, timedelta
import ctypes
import pickle
import time
import os
import gis_fasta as gf

# 清晰化
ctypes.windll.shcore.SetProcessDpiAwareness(True)
# 主窗口
r = Tk()
r.title('GISAID Spider for FASTA')

# 风格配置
std_font = '微软雅黑 13'
style = Style()
style.configure('TLabel', font=std_font)
style.configure('TButton', font=std_font)
# 运行信息文件储存位置
store_filename = 'last_info.dat'
# 数据储存文件名 ， 储存为字典对象
date_filename = 'fasta_accession_num_obj.dat'
if_need_store_info = True


def show_mission_panel():
    def store_counts_date_info():
        global if_need_store_info
        if if_need_store_info:
            if_need_store_info = False

            ac_nums = gf.ac_num_analysis.ac_nums
            dates_str = gf.sms_start_date + 'to' + gf.sms_end_date
            filename = gf.destination_folder + os.sep + date_filename
            if os.path.exists(filename):
                with open(filename, 'rb')as f:
                    try:
                        info_dict = pickle.load(f)
                    except:
                        info_dict = {}
                if dates_str not in info_dict:
                    with open(filename, 'wb') as f:
                        info_dict[dates_str] = ac_nums
                        pickle.dump(info_dict, f)
            else:
                with open(filename, 'wb') as f:
                    pickle.dump({dates_str: ac_nums}, f)

    def get_complete_percentage():
        if gf.ac_num_analysis.full_length:
            store_counts_date_info()
            cp = (1 - gf.ac_num_analysis.get_length() / gf.ac_num_analysis.full_length) * 100
            cp = round(cp, 2)
        else:
            cp = 0
        return cp

    def get_current_date_pair():
        return gf.mission_now

    def spider_stop_continue():
        bt.config(text='暂停' if gf.if_stop else '继续')
        gf.if_stop = not gf.if_stop

    def return_to_root():
        r.deiconify()
        t.destroy()

    def auto_update():
        sep_time = 1
        t1 = time.time()
        while True:
            # 获取当前的日期对
            date_pair = get_current_date_pair()
            # 将日期对组成字符串
            date_pair_str = 'to'.join(date_pair)
            # 获取完成百分比
            cp = get_complete_percentage()
            # 初始化sub_time
            sub_time = timedelta(seconds=0)
            if cp >= 0.5:
                # 预计剩余用时
                left_time = timedelta(seconds=int((100 - cp) / cp * (time.time() - t1)))
                # 已用时间
                sub_time = timedelta(seconds=int(time.time() - t1))
                # 预计总时间
                max_time = left_time + sub_time
                # 组成字符串
                time_str = str(sub_time) + '<' + str(max_time)
            else:
                time_str = '-<-'
            if not gf.if_done:
                # 未全部完成
                lb_text = '当前日期段：{}\n进度<={}%\n{}'.format(date_pair_str, str(cp), time_str)
                lb.config(text=lb_text)
                pb['value'] = cp
                pb.update()
                time.sleep(sep_time)
            else:
                # 全部完成
                lb_text = '{}完成，用时{}'.format(date_pair_str, str(sub_time))
                lb.config(text=lb_text)
                bt.config(text='确定',command=return_to_root)
                break

    t = Toplevel(r)
    t.geometry('700x250')
    lb = Label(t, style='TLabel')
    pb = Progressbar(t)
    bt = Button(t, text='暂停', command=spider_stop_continue)
    pb['maximum'] = 100
    lb.pack(fill=BOTH, expand=True)
    pb.pack(fill=BOTH, expand=True)
    bt.pack()
    Thread(target=auto_update, daemon=True).start()


def store_info():
    info_list = [e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get(), e7.get()]
    with open(store_filename, 'wb') as f:
        pickle.dump(info_list, f)


def load_info():
    if os.path.exists(store_filename):
        try:
            with open(store_filename, 'rb') as f:
                info_list = pickle.load(f)
            e1.insert(0, info_list[0])
            e2.insert(0, info_list[1])
            e3.insert(0, info_list[2])
            e4.insert(0, info_list[3])
            e5.insert(0, info_list[4])
            e6.insert(0, info_list[5])
            e7.insert(0, info_list[6])
            return True
        except:
            print('{}文件损坏'.format(store_filename))
            return False
    else:
        return False


def if_right_date_str(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        return False


def if_right_path_str(path_str):
    try:
        # 去除最右边的文件分隔符
        path_str.rstrip('\\')
        path_str.rstrip('/')
        # 判断该文件夹是否存在
        os.path.isdir(path_str)
        return path_str
    except:
        return False


def if_right_num_str(num_str):
    try:
        return int(num_str)
    except:
        return False


def fill_in_last_info():
    if not load_info():
        messagebox.showinfo(title='提醒', message='找不到上一次的信息')


def spider_start():
    # 获取参数
    spider_args = [e1.get(), e2.get(), if_right_date_str(e3.get()), if_right_date_str(e4.get()),
                   if_right_path_str(e5.get()), if_right_path_str(e6.get()), if_right_num_str(e7.get())]
    print('爬虫参数：', spider_args)

    gf.login_name = spider_args[0]
    gf.login_password = spider_args[1]
    gf.sms_start_date = spider_args[2]
    gf.sms_end_date = spider_args[3]
    gf.default_folder = spider_args[4]
    gf.destination_folder = spider_args[5]
    gf.average_wait_time = spider_args[6]

    warning_info_str = ''
    if not gf.login_name:
        warning_info_str += '没有填写名字！\n\r'
    if not gf.login_password:
        warning_info_str += '没有填写密码！\n\r'
    if not gf.sms_start_date:
        warning_info_str += '没有填写或填写了格式错误的开始日期(submission start date)!\n\r'
    if not gf.sms_end_date:
        warning_info_str += '没有填写或填写了格式错误的终止日期(submission end date)!\n\r'
    if not gf.default_folder:
        warning_info_str += '没有填写或填写了格式错误的Chrome默认下载路径！\n\r'
    if not gf.destination_folder:
        warning_info_str += '没有填写或填写了格式错误的目标文件夹路径！\n\r'
    if (not gf.average_wait_time) or int(gf.average_wait_time) < 4:
        warning_info_str += '没有填写等待时间或等待时间过短(<4s)，或填写的不是整数！\n\r'

    def spider_loop():
        while not gf.if_done:
            # 转到第一个窗口
            gf.if_terminate = False
            gf.d.switch_to.window(gf.d.window_handles[0])
            gf.start()

    if warning_info_str:
        messagebox.showwarning(title='爬虫不能开始的原因', message=warning_info_str)
    else:
        store_info()
        Thread(target=spider_loop, daemon=True).start()
        r.withdraw()
        show_mission_panel()


iframe = Frame(r)
iframe.pack(padx=2, pady=2, fill=X, expand=True)
iframe.columnconfigure(1, weight=1)

pady = 6

Label(iframe, text='Name', style='TLabel').grid(row=0, column=0, pady=pady)
Label(iframe, text='Password', style='TLabel').grid(row=1, column=0, pady=pady)
Label(iframe, text='Submission start date', style='TLabel').grid(row=2, column=0, pady=pady)
Label(iframe, text='Submission end date', style='TLabel').grid(row=3, column=0, pady=pady)
Label(iframe, text='浏览器的默认下载位置', style='TLabel').grid(row=4, column=0, pady=pady)
Label(iframe, text='文件存放目标位置', style='TLabel').grid(row=5, column=0, pady=pady)
Label(iframe, text='最少等待时长（秒）', style='TLabel').grid(row=6, column=0, pady=pady)

e1 = Entry(iframe, font=std_font)
e2 = Entry(iframe, font=std_font)
e3 = Entry(iframe, font=std_font)
e4 = Entry(iframe, font=std_font)
e5 = Entry(iframe, font=std_font)
e6 = Entry(iframe, font=std_font)
e7 = Entry(iframe, font=std_font)

e1.grid(row=0, column=1, pady=pady, sticky='wens')
e2.grid(row=1, column=1, pady=pady, sticky='wens')
e3.grid(row=2, column=1, pady=pady, sticky='wens')
e4.grid(row=3, column=1, pady=pady, sticky='wens')
e5.grid(row=4, column=1, pady=pady, sticky='wens')
e6.grid(row=5, column=1, pady=pady, sticky='wens')
e7.grid(row=6, column=1, pady=pady, sticky='wens')

set_frame = Frame(r)
set_frame.pack(fill=BOTH, expand=True)
b1 = Button(set_frame, text='填入上次的信息', style='TButton', command=fill_in_last_info) \
    .pack(side=LEFT, fill=BOTH, expand=True)
b2 = Button(set_frame, text='开始', style='TButton', command=spider_start) \
    .pack(side=LEFT, fill=BOTH, expand=True)

menu = Menu(r)

tips = '1. 默认下载位置一般在C:\\Users\\你的用户名\\downloads下\n' \
       '2. 日期只支持year-month-day的形式\n' \
       '3. 最少等待时间控制着脚本的速度，请根据自己的网速选择，太少可能被封号，国内一般6s比较合适\n' \
       '4. 只要输入的两个日期不变，程序就能断点继续，想重新开始请删除advance文件夹内的对应日期范围文件\n\n' \
       '更多内容请访问https://www.cnblogs.com/roundfish/'
about = '作者：cquxiaoy\n本脚本完全免费\n\n' \
        '更多内容请访问https://www.cnblogs.com/roundfish/'

menu.add_command(label='教程', command=lambda: messagebox.showinfo('教程', tips))
menu.add_command(label='关于', command=lambda: messagebox.showinfo('关于', about))

r.config(menu=menu)

r.mainloop()
