# -*- coding:utf-8 -*-
from datetime import *
import random
import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from parse_acnums import AcNumAnalysis
from advance import *


sys_timer1_xpath = '//*[@id="sys_timer"]'
sys_timer2_xpath = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/div[3]/table/tbody[1]'


iframe_xpath = '/html/body/iframe'
iframe_xpath_2 = '/html/body/iframe[2]'
clt_date_1 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr[4]/td[2]/div[1]/div/div[1]/input'
clt_date_2 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/div[1]/input'
sms_date_1 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr[4]/td[2]/div[5]/div/div[1]/input'
sms_date_2 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr[4]/td[2]/div[7]/div/div[1]/input'
select_all = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/table/thead/tr/th[1]/div/span/input'
download = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/button[4]'
download2 = '/html/body/form/div[5]/div/div[2]/div/div/div[2]/div/button'
select_bt_path = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/button[2]'
accession_num_textarea = '/html/body/form/div[5]/div/div[1]/div/div[1]/table[2]/tbody/tr/td/div/div[1]/textarea'
ok1_bt = '/html/body/form/div[5]/div/div[2]/div/div/div[2]/div/button'
ok2_bt = '/html/body/div[2]/div[1]/div[3]/div/button'
return_bt_xpath = '/html/body/form/div[5]/div/div[2]/div/div/div[1]/div/button'

fmt = '%Y-%m-%d'

signal = True
if_stop = False
if_terminate = False
if_done = False

seconds = 8


def set_breakpoint():
    # 设置暂停点
    while if_stop:
        time.sleep(1)


def prepare_driver():
    options = Options()

    if if_headless:
        #  开启无头模式
        options.add_argument('--headless')

    #  设置mime
    mime_types = "application/octet-stream"
    mime_types += ",application/excel,application/vnd.ms-excel"
    mime_types += ",application/pdf,application/x-pdf"
    mime_types += ",application/x-bzip2"
    mime_types += ",application/x-gzip,application/gzip"

    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", destination_folder)
    options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", mime_types)
    options.set_preference(
        "plugin.disable_full_page_plugin_for_types", mime_types)
    options.set_preference("pdfjs.disabled", True)

    d = webdriver.Firefox(options=options)
    return d


def click(d, element_xpath):
    bt = d.find_element(By.XPATH, element_xpath)
    bt.click()


def send(d, element_xpath, msg):
    bt = d.find_element(By.XPATH, element_xpath)
    bt.clear()
    bt.send_keys(msg)


def is_sys_timer_on(d):
    #  两个sys_timer是否出现一个
    try:
        status1 = d.find_element(By.XPATH, sys_timer1_xpath).get_attribute('style')
    except:
        status1 = 'none'
    try:
        status2 = d.find_element(By.XPATH, sys_timer2_xpath).get_attribute('style')
    except:
        status2 = 'none'
    if 'none' in status1 and 'none' in status2:
        return False
    else:
        return True


def wait_one_timer(d):
    #  等待sys_timer结束，至少出现过一个
    timer_sign = False  # 是否出现过sys_timer
    while True:
        if is_sys_timer_on(d):
            timer_sign = True
        elif timer_sign:
            break
        time.sleep(0.5)


def find_element_by_xpath(d, xpath):
    return d.find_element(By.XPATH, xpath)


def Keep(exe, *args, times=120):
    #  最大次数默认为无限
    #  保持尝试直到成功完成
    counter = 0
    global signal
    while True:
        set_breakpoint()
        if if_terminate:
            return
        signal = True
        counter += 1
        try:
            if (counter < times) or (times <= 0):
                get = exe(*args)
                # 返回函数的输出
                return get
            else:
                break
        except Exception as e:
            print('Keep--',str(exe.__name__),':失败-',counter)
            pass

        time.sleep(0.5)


def SwitchToIframe(d):
    def s11():
        WebDriverWait(d, 3, 0.5).until(EC.presence_of_element_located((By.XPATH, iframe_xpath)))
        iframe = d.find_element(By.XPATH, iframe_xpath)
        d.switch_to.frame(iframe)

    Keep(s11)


def SwitchToIframe2(d):
    def s12():
        WebDriverWait(d, 3, 0.5).until(EC.presence_of_element_located((By.XPATH, iframe_xpath_2)))
        iframe = d.find_element(By.XPATH, iframe_xpath_2)
        d.switch_to.frame(iframe)

    Keep(s12)


def SwitchToDefault(d):
    def s2():
        d.switch_to.default_content()

    Keep(s2)


def Select_all(d):
    sela = d.find_element(By.XPATH, select_all)
    sela.click()


def GetWeb(d):
    d.get('https://www.epicov.org/epi3/frontend')
    time.sleep(1)


def Login(d):
    login_xpath = '/html/body/form/div[5]/div/div[2]/div/div/div/div[1]/div/div/div[2]/input[1]'
    password_xpath = '/html/body/form/div[5]/div/div[2]/div/div/div/div[1]/div/div/div[2]/input[2]'
    login_bt_xpath = '/html/body/form/div[5]/div/div[2]/div/div/div/div[1]/div/div/div[2]/input[3]'

    Keep(send, d, login_xpath, login_name)
    Keep(send, d, password_xpath, login_password)
    Keep(click, d, login_bt_xpath)
    print('Login')


def click_Epicov(d):
    epicov_xpath = '/html/body/form/div[5]/div/div[1]/div/div/div/div/div[2]/div/ul/li[3]/a'
    d.find_element(By.XPATH, epicov_xpath).click()


def ClickSearch(d):
    search_bt = '/html/body/form/div[5]/div/div[2]/div/div[1]/div/div/div[3]'
    WebDriverWait(d, 3, 0.5).until(EC.presence_of_element_located((By.XPATH, search_bt)))
    Keep(click, d, search_bt)
    print('点击搜索按钮')


def confirm_tips(d):
    #  点击通知的ok键
    tips_xpath = '/html/body/div[2]/div[1]/div[3]/div/button'
    Keep(click, d, tips_xpath)


def Submission_date(d, date1, date2):
    print('输入sd', date1, ' to ', date2)
    if date1 != '':
        Keep(send, d, sms_date_1, date1)
        wait_one_timer(d)
    else:
        Keep(send, d, sms_date_1, '')
    if date2 != '':
        Keep(send, d, sms_date_2, date2)
        wait_one_timer(d)
    else:
        Keep(send, d, sms_date_2, '')


def Collection_date(d, date1, date2):
    if date1 != '':
        Keep(send, d, clt_date_1, date1)
        wait_one_timer(d)
    else:
        Keep(send, d, clt_date_1, '')
    if date2 != '':
        Keep(send, d, clt_date_2, date2)
        wait_one_timer(d)
    else:
        Keep(send, d, clt_date_2, '')


def download_fasta(d, filename):
    global if_terminate
    global signal
    print('开始下载')
    if if_terminate:
        return
    print('点击下载键')
    Keep(click, d, download)
    wait_one_timer(d)
    SwitchToIframe2(d)
    set_breakpoint()
    print('点击下载键二')
    #  选择数据类型--基础型
    Keep(click, d, '/html/body/form/div[5]/div/div[1]/div/div/table[1]/tbody/tr/td[2]/div/div[1]/div[2]/div[1]/input')
    Keep(click, d, download2)
    SwitchToDefault(d)
    wait_one_timer(d)
    fn = get_download_filename_firefox()
    print('filename:{}'.format(fn))
    print('下载结束')
    if fn == '':
        if_terminate = True
        print('网络错误，重启，if_terminate=True')
        return

    suffix = os.path.splitext(fn)[1]
    # 给文件寻找合适的命名
    num = 1
    while True:
        new_fn = filename
        new_fn += ('(' + str(num) + ')')
        if os.path.exists(destination_folder + os.sep + new_fn + suffix):
            num += 1
        else:
            filename = new_fn + suffix
            break

    # 进行重命名和移动
    os.rename(default_folder + os.sep + fn, default_folder + os.sep + filename)
    print('文件已重命名：\n\r{} -> {}'.format(fn, filename))
    # command = 'move "' + default_folder + os.sep + filename + '" "' + destination_folder + os.sep + '"'
    # os.system(command)
    # print('文件已移动到{}'.format(destination_folder))
    print('结束下载')


def getDownLoadedFileName(driver, waitTime):
    if len(driver.window_handles) == 1:
        driver.execute_script("window.open()")
        # switch to new tab
        driver.switch_to.window(driver.window_handles[-1])
        # navigate to chrome downloads
        driver.get('chrome://downloads')
    else:
        # switch to new tab
        driver.switch_to.window(driver.window_handles[-1])

    # define the endTime
    endTime = time.time() + waitTime
    global signal
    while True:
        try:
            # 获取下载百分比
            download_percentage = driver.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            # 检查百分比是否为100
            signal = True
            if download_percentage == 100:
                # 赋值并检查文件是否存在。不存在则是上一次的
                fname = driver.execute_script(
                    "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
                if not os.path.exists(default_folder + os.sep + fname):
                    raise NameError()
                else:
                    break
        except:
            #  不在下载界面，或没有正在下载的项目
            try:
                fname = driver.execute_script(
                    "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
                if os.path.exists(default_folder + os.sep + fname):
                    break
            except:
                print('.', end='')

        time.sleep(3)
        if time.time() > endTime:
            driver.switch_to.window(driver.window_handles[0])
            return ''
    driver.switch_to.window(driver.window_handles[0])
    return fname


def get_download_filename_firefox():
    def get_once_filename():
        filenames = os.listdir(destination_folder)
        downloading_filename = ''
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.part':
                downloading_filename = filename.split('.')[0] + '.' + filename.split('.')[2]
                break
        return downloading_filename
    #  等待直到下载开始，并获取文件名
    while True:
        filename = get_once_filename()
        if filename:
            break
        time.sleep(1)
    #  等待直到下载结束
    while True:
        downfn = get_once_filename()
        if not downfn:
            break
        time.sleep(1)
    return filename


def delete_unneeded_cache_file():
    to_delete_list = []
    filenames = os.listdir(destination_folder)
    for filename in filenames:
        if os.path.splitext(filename)[1] == '.part':
            to_delete_list.append(filename)
    for filename in to_delete_list:
        os.remove(destination_folder+os.sep+filename)
        zero_kb_filename = filename.split('.')[0] + '.' + filename.split('.')[2]
        os.remove(destination_folder+os.sep+zero_kb_filename)


def download_less_than_xdays(d, start_date, end_date):
    #  下载日期范围内的数据
    adv = get_advance(start_date + 'to' + end_date)
    if adv is None:
        # 没有找到进度
        # 输入日期
        Submission_date(d, start_date, end_date)
        # 点击全选
        Keep(Select_all, d)
        # 等待
        wait_one_timer(d)
        # 点击select
        Keep(click, d, select_bt_path)
        # 等待
        wait_one_timer(d)
        # 复制序列号文本
        SwitchToIframe2(d)
        text_area = Keep(find_element_by_xpath, d, accession_num_textarea)
        text = text_area.text
        # print('text_area文本：{}'.format(text))
        SwitchToDefault(d)
        print('找到序列号：{}...'.format(text[:15]))
    elif adv:
        # 有进度，断点继续
        text = adv  # nums_list
        print('断点继续')
        # 输入日期
        Submission_date(d, start_date, end_date)
        # 点击全选
        Keep(Select_all, d)
        # 等待
        wait_one_timer(d)
        # 点击select
        Keep(click, d, select_bt_path)
        # 等待
        wait_one_timer(d)
        # 复制序列号文本
    else:
        print('已完成，跳过')
        return
    # 分析序列号，进行拆分
    ac_num_analysis.refresh(text)
    print('共{}个序列'.format(str(ac_num_analysis.full_length)))
    # 按拆分结果下载
    for ac_nums_str in ac_num_analysis.get():
        if if_terminate:
            return
        SwitchToIframe2(d)
        # 清空序列号区域
        # time.sleep(seconds)
        text_area = Keep(find_element_by_xpath, d, accession_num_textarea)
        text_area.clear()
        # 输入对应序列
        Keep(send, d, accession_num_textarea, ac_nums_str)
        # 点击OK
        # 大ok+小ok
        print('等待')
        # time.sleep(5)
        print('点击ok1')
        WebDriverWait(d, 30).until(EC.element_to_be_clickable((By.XPATH, ok1_bt)))
        # time.sleep(5)
        Keep(click, d, ok1_bt)
        # d.find_element(By.XPATH, ok1_bt).click()
        # wait_one_timer(d)
        print('点击ok2')
        WebDriverWait(d, 30).until(EC.element_to_be_clickable((By.XPATH, ok2_bt)))
        Keep(click, d, ok2_bt)
        wait_one_timer(d)
        SwitchToDefault(d)
        # 下载
        download_fasta(d, start_date + 'to' + end_date)
        # 下载完成
        set_advance(start_date + 'to' + end_date, ac_num_analysis.ac_nums)
        # 点击select
        Keep(click, d, select_bt_path)
        wait_one_timer(d)
    else:
        # 点击返回
        SwitchToIframe2(d)
        Keep(click, d, return_bt_xpath)
        SwitchToDefault(d)
        wait_one_timer(d)
        # 重置全选按钮
        Keep(Select_all, d)
        print(start_date+'to'+end_date+'完成！')
        wait_one_timer(d)


def analysis_args():
    max_day_span = 7
    ml = []
    std = datetime.strptime(sms_start_date, fmt)
    edd = datetime.strptime(sms_end_date, fmt)
    days = (edd - std).days + 1
    if days <= max_day_span:
        ml = [[sms_start_date, sms_end_date]]
    else:
        for i in range(int(days/max_day_span)):
            ml.append([std.strftime(fmt), (std + timedelta(days=max_day_span - 1)).strftime(fmt)])
            std += timedelta(days=max_day_span)
        else:
            if days % max_day_span:
                ml.append([std.strftime(fmt), edd.strftime(fmt)])
    print('任务分段：{}'.format(str(ml)))
    return ml


def start():
    #  删除浏览器异常退出产生的无效缓存文件
    delete_unneeded_cache_file()
    #  准备驱动
    d = prepare_driver()
    # 进入网页
    GetWeb(d)
    # 登录
    Login(d)
    #  点击epicov
    Keep(click_Epicov, d)
    # 点击搜索按钮
    ClickSearch(d)
    # 等待页面刷新
    wait_one_timer(d)
    # 点击通知ok键
    print('点击确认通知')
    confirm_tips(d)
    # 解析参数，如果日期跨度大于max_day_span天，就截成max_day_span天的多个分段。形式[[start_date1, end_date2],...]
    mission_list = analysis_args()
    global mission_now
    # 依次爬取每个分段
    for mission in mission_list:
        if if_terminate:
            #  关闭浏览器
            d.close()
            return
        mission_now = mission[:]
        download_less_than_xdays(d, mission[0], mission[1])
    global if_done
    if_done = True


# 参数
login_name = ''
login_password = ''

sms_start_date = ''
sms_end_date = ''

destination_folder = ''  # 目标文件夹地址

if_headless = False


# 运行时参数
mission_now = ['', '']
# 字符串分析器
ac_num_analysis = AcNumAnalysis()


if __name__ == '__main__':
    # 命令行模式
    arguments = sys.argv
    login_name = arguments[1]
    login_password = arguments[2]
    sms_start_date = arguments[3]
    sms_end_date = arguments[4]
    default_folder = arguments[5]
    destination_folder = arguments[6]
    start()
