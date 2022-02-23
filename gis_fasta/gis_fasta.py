from datetime import *
import random
import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from parse_acnums import AcNumAnalysis
from advance import *

iframe_xpath = '/html/body/iframe'
clt_date_1 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div[4]/table/tbody/tr/td[2]/table/tbody/tr/td[' \
             '1]/div/div[1]/input '
clt_date_2 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div[4]/table/tbody/tr/td[2]/table/tbody/tr/td[' \
             '3]/div/div[1]/input '
sms_date_1 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div[4]/table/tbody/tr/td[2]/table/tbody/tr/td[' \
             '5]/div/div[1]/input '
sms_date_2 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div[4]/table/tbody/tr/td[2]/table/tbody/tr/td[' \
             '7]/div/div[1]/input '
select_all = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/table/thead/tr/th[1]/div/span/input'
download = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/button[3]'
download2 = '/html/body/form/div[5]/div/div[2]/div/div/div[2]/div/button'
select_bt_path = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/button[1]'
accession_num_textarea = '/html/body/form/div[5]/div/div[1]/div/div[1]/table[2]/tbody/tr/td/div/div[1]/textarea'
ok1_bt = '/html/body/form/div[5]/div/div[2]/div/div/div[2]/div/button'
ok2_bt = '/html/body/div[2]/div[1]/div[3]/div/button'
return_bt_xpath = '/html/body/form/div[5]/div/div[2]/div/div/div[1]/div/button'

fmt = '%Y-%m-%d'

signal = True
if_stop = False
if_terminate = False
if_done = False


def set_breakpoint():
    # 设置暂停点
    while if_stop:
        time.sleep(1)


def click(element_xpath):
    bt = d.find_element_by_xpath(element_xpath)
    bt.click()


def send(element_xpath, msg):
    bt = d.find_element_by_xpath(element_xpath)
    bt.clear()
    bt.send_keys(msg)


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


def SwitchToIframe():
    def s1():
        WebDriverWait(d, 3, 0.5).until(EC.presence_of_element_located((By.XPATH, iframe_xpath)))
        iframe = d.find_element_by_xpath(iframe_xpath)
        d.switch_to.frame(iframe)

    Keep(s1)


def SwitchToDefault():
    def s2():
        d.switch_to.default_content()

    Keep(s2)


def Select_all():
    sela = d.find_element_by_xpath(select_all)
    sela.click()


def FindPatientNums():
    #  返回项目总数
    total_num_xpath = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/span/span'
    total_num_str = d.find_element_by_xpath(total_num_xpath).text
    #
    total_num = total_num_str[7:-8].replace(',', '')
    # print('共',total_num,'个病例')
    return int(total_num)


def GetWeb():
    d.get('https://www.epicov.org/epi3/frontend')
    time.sleep(1)


def Login():
    login_xpath = '/html/body/form/div[5]/div/div[2]/div/div/div/div[1]/div/div/div[2]/input[1]'
    password_xpath = '/html/body/form/div[5]/div/div[2]/div/div/div/div[1]/div/div/div[2]/input[2]'
    login_bt_xpath = '/html/body/form/div[5]/div/div[2]/div/div/div/div[1]/div/div/div[2]/input[3]'

    Keep(send, login_xpath, login_name)
    Keep(send, password_xpath, login_password)
    Keep(click, login_bt_xpath)
    print('Login')


def ClickSearch():
    search_bt = '/html/body/form/div[5]/div/div[2]/div/div[1]/div/div/div[3]'
    WebDriverWait(d, 3, 0.5).until(EC.presence_of_element_located((By.XPATH, search_bt)))
    Keep(click, search_bt)
    print('点击搜索按钮')


def Submission_date(date1, date2):
    print('输入sd', date1, ' to ', date2)
    if date1 != '':
        Keep(send, sms_date_1, date1)
        wait_one_timer()
    else:
        Keep(send, sms_date_1, '')
    if date2 != '':
        Keep(send, sms_date_2, date2)
        wait_one_timer()
    else:
        Keep(send, sms_date_2, '')


def Collection_date(date1, date2):
    if date1 != '':
        Keep(send, clt_date_1, date1)
        wait_one_timer()
    else:
        Keep(send, clt_date_1, '')
    if date2 != '':
        Keep(send, clt_date_2, date2)
        wait_one_timer()
    else:
        Keep(send, clt_date_2, '')


def wait_one_timer(base_time=0.0):
    if not base_time:
        # 赋予默认值
        base_time = average_wait_time
    max_time = int(base_time * (1 + random.random() / 2))  # *1~1.5
    print('等待{}秒'.format(str(max_time)), end='  ')
    global signal
    for i in range(max_time):
        if if_terminate:
            return
        signal = True
        set_breakpoint()
        time.sleep(1)
    print('结束等待')


def download_fasta(filename):
    global if_terminate
    global signal
    print('开始下载')
    if if_terminate:
        return
    print('点击下载键')
    Keep(click, download)
    wait_one_timer()
    SwitchToIframe()
    set_breakpoint()
    print('点击下载键二')
    Keep(click, download2)
    time.sleep(5)
    SwitchToDefault()
    # 10分钟无反应，默认网络错误
    fn = getDownLoadedFileName(d, 600)
    print('filename:{}'.format(fn))
    print('下载结束')
    if fn == '':
        if_terminate = True
        print('网络错误，重启，if_terminate=True')
        return

    # 给文件寻找合适的命名
    num = 1
    while True:
        new_fn = filename
        new_fn += ('(' + str(num) + ')')
        if os.path.exists(destination_folder + os.sep + new_fn + '.fasta'):
            num += 1
        else:
            filename = new_fn + '.fasta'
            break

    # 进行重命名和移动
    os.rename(default_folder + os.sep + fn, default_folder + os.sep + filename)
    print('文件已重命名：\n\r{} -> {}'.format(fn, filename))
    command = 'move "' + default_folder + os.sep + filename + '" "' + destination_folder + os.sep + '"'
    os.system(command)
    print('文件已移动到{}'.format(destination_folder))
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
            # get downloaded percentage
            download_percentage = driver.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            signal = True
            if download_percentage == 100:
                # return the file name once the download is completed
                fname = driver.execute_script(
                    "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
                if not os.path.exists(default_folder + os.sep + fname):
                    raise NameError()
                else:
                    break
        except:
            try:
                fname = driver.execute_script(
                    "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
                if os.path.exists(default_folder + os.sep + fname):
                    break
            except:
                print('.', end='')

        time.sleep(5)
        if time.time() > endTime:
            driver.switch_to.window(driver.window_handles[0])
            return ''
    driver.switch_to.window(driver.window_handles[0])
    return fname


def download_less_than_xdays(start_date, end_date):
    # 输入日期
    Submission_date(start_date, end_date)
    # 等待
    wait_one_timer(average_wait_time*2)
    # 点击全选
    Keep(Select_all)
    # 等待
    wait_one_timer(average_wait_time*1.5)
    # 点击select
    Keep(click, select_bt_path)
    # 等待
    wait_one_timer()
    adv = get_advance(start_date + 'to' + end_date)
    if adv is None:
        # 没有找到进度
        # 复制序列号文本
        SwitchToIframe()
        text_area = d.find_element_by_xpath(accession_num_textarea)
        text = text_area.text
        # print('text_area文本：{}'.format(text))
        SwitchToDefault()
        print('找到序列号：{}...'.format(text[:15]))
    else:
        # 有进度，断点继续
        text = adv  # nums_list
        print('断点继续')
    # 分析序列号，进行拆分
    ac_num_analysis.refresh(text)
    print('共{}个序列'.format(str(ac_num_analysis.full_length)))
    # 按拆分结果下载
    for ac_nums_str in ac_num_analysis.get():
        SwitchToIframe()
        # 清空序列号区域
        text_area = d.find_element_by_xpath(accession_num_textarea)
        text_area.clear()
        wait_one_timer()
        # 输入对应序列
        Keep(send, accession_num_textarea, ac_nums_str)
        wait_one_timer()
        # 点击OK
        # 大ok+小ok
        Keep(click, ok1_bt)
        print('点击ok1')
        wait_one_timer()
        Keep(click, ok2_bt)
        print('点击ok2')
        wait_one_timer(2*average_wait_time)
        SwitchToDefault()
        # 下载
        download_fasta(start_date + 'to' + end_date)
        # 下载完成
        set_advance(start_date + 'to' + end_date, ac_num_analysis.ac_nums)
        # 点击select
        Keep(click, select_bt_path)
        wait_one_timer(average_wait_time)
    else:
        # 点击返回
        SwitchToIframe()
        Keep(click, return_bt_xpath)
        SwitchToDefault()
        wait_one_timer()
        # 重置全选按钮
        Keep(Select_all)
        print(start_date+'to'+end_date+'完成！')
        wait_one_timer()


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
    # 进入网页
    GetWeb()
    # 登录
    Login()
    # 点击搜索按钮
    ClickSearch()
    # 等待页面刷新
    wait_one_timer()
    # 解析参数，如果日期跨度大于max_day_span天，就截成max_day_span天的多个分段。形式[[start_date1, end_date2],...]
    mission_list = analysis_args()
    global mission_now
    # 依次爬取每个分段
    for mission in mission_list:
        mission_now = mission[:]
        download_less_than_xdays(mission[0], mission[1])
    global if_done
    if_done = True


# 参数
login_name = ''
login_password = ''

sms_start_date = ''
sms_end_date = ''

default_folder = ''  # 这个参数代表默认下载地址
destination_folder = ''  # 目标文件夹地址

average_wait_time = 8  # 平均等待时间

# 打开浏览器
d = webdriver.Chrome()


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
    if len(arguments) >= 8:
        average_wait_time = arguments[7]
    start()
