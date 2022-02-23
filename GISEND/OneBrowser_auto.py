import time
import os
from ast import literal_eval
from threading import Thread, Lock
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Ocr import CharOcr
import traceback
import random

login_name_2 = 'yiyiwen'
login_password_2 = 'Zyz)MeKA'
login_name = '103000zhqM'
login_password = '2GZfPoAS'

start_date = '2021-01-01'
end_date = '2021-01-15'

#  验证码所在iframe与病例数据一样
iframe_xpath = '/html/body/iframe'
#  验证码框关键字'Repeat:'
captcha_Repeat_xpath = '/html/body/form/div[5]/div/div[1]/div/div/table[2]/tbody/tr/td[1]/div'
#  验证码图片xpath
captcha_xpath = '/html/body/form/div[5]/div/div[1]/div/div/table[1]/tbody/tr/td[2]/div/div[1]/img'
#  验证码输入框xpath
captcha_entry_xpath = '/html/body/form/div[5]/div/div[1]/div/div/table[2]/tbody/tr/td[2]/div/div[1]/input'
#  验证码提交按钮
captcha_submit_xpath = '/html/body/form/div[5]/div/div[2]/div/div/div/div/button'

#  第一页按钮
first_page_bt_xpath = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/a[1]'
#  上一页按钮
former_page_bt_xpath_middle = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/a[2]'
#  上两页按钮
former2_page_bt_xpath_middle = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/span/a[1]'
#  当前页按钮
current_page_bt_xpath_page1 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/span[3]/span'
current_page_bt_xpath_page_middle = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/span/span'
current_page_bt_xpath_page_last = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/span[1]/span'
#  第一页按钮
first_page_bt = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/a[1]'
#  下一页按钮
next_page_bt_xpath_page1 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/a[1]'
next_page_bt_xpath_middle = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/a[3]'
#  下两页按钮
next2_page_bt_xpath_page1 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/span[3]/a[2]'
next2_page_bt_xpath_middle = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/span/a[4]'
#  最后一页按钮
last_page_bt_xpath = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/a[2]'
#  验证码错误标记
captcha_wrong_xpath = '/html/body/form/div[5]/div/div[1]/div/div/table[2]/tbody/tr/td[2]/div/div[2]/div'
#  返回主界面的按钮'<'
to_main_bt_xpath = '/html/body/form/div[5]/div/div[2]/div[2]/div/div[1]/div/button/img'

#  Data error.
data_error_label_xpath = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/div[3]/table/tbody[1]/tr/td/div'
#  internal error
internal_error_frame_xpath = '/html/body/div[2]/div[1]/div[1]'
internal_error_warning_text_xpath = '/html/body/div[2]/div[1]/div[2]/text()'

#  信息列表，len=34
informationList = ['Accession ID', 'Type', 'Clade', 'Pango Lineage', 'AA Substitutions', 'Variant',
                   'Passage details/history',
                   'Collection date', 'Location', 'Host', 'Additional location information', 'Gender', 'Patient age',
                   'Patient status',
                   'Specimen source', 'Additional host information', 'Sampling strategy', 'Outbreak', 'Last vaccinated',
                   'Treatment', 'Sequencing technology', 'Assembly method', 'Coverage', 'Comment', 'Originating lab',
                   'Address1', 'Sample ID given by the originating laboratory', 'Submitting lab', 'Address2',
                   'Sample ID given by the submitting laboratory', 'Authors', 'Submitter', 'Submission Date',
                   'Address3']

#  重要变量
if_stop = False

signal = False
ifdone = False
#  是否终止程序
ifTerminate = False
runningInfo = {}

#  重要常量
#  病例信息储存位置
datafolder = '../采集到的病例数据'
#  进度信息储存位置
advfilefolder = '../爬虫进度'
#  验证码临时储存位置
captchafolder = '../验证码'

#  Ocr类
OcrMachine = CharOcr()


def activateSignal():
    global signal
    signal = True


def disactivateSignal():
    global signal
    signal = False


adLock = Lock()


def setAdvance(Name, advance):
    Name = str(Name)
    sfileName = advfilefolder + '/' + '进度_' + Name + '.txt'
    #  没有就创建这个文件，有也不会改变内容
    if not os.path.exists(sfileName):
        if not os.path.exists(advfilefolder):
            os.mkdir(advfilefolder)
        else:
            open(sfileName, 'a').close()

    with open(sfileName, 'w') as f:
        adLock.acquire()
        f.write(str(advance))
        adLock.release()


def getAdvance(Name):
    Name = str(Name)
    sfileName = advfilefolder + '/' + '进度_' + Name + '.txt'
    #  没有就创建这个文件，有也不会改变内容
    if not os.path.exists(sfileName):
        setAdvance(Name, 0)
        return 0
    else:
        with open(sfileName, 'r') as f:
            ad = f.read()
        return literal_eval(ad)


def printAdvance(d, Name):
    ad = getAdvance(Name)
    all_ = FindPatientNums(d)
    string = '▉' * int(20 * ad / all_)
    print(Name, '当前进度：', ad, '/', all_, '__', '%.2f' % (100 * ad / all_), '%__', string.ljust(20), '▉')


storeLock = Lock()


def StoreInfoDict(fileName, InfoDict):
    if not os.path.exists(datafolder):
        os.mkdir(datafolder)

    #  转换成字符串
    infoStr = ''
    for item in InfoDict:
        infoStr += item + ':' + InfoDict[item] + '\n'
    infoStr += '\n'

    with open(datafolder + '/' + fileName, 'a+', encoding='utf-8') as f:
        storeLock.acquire()
        f.write(infoStr)
        storeLock.release()


def Click(d, element_xpath):
    for i in range(20):
        try:
            bt = d.find_element_by_xpath(element_xpath)
            bt.click()
            return bt.text
        except Exception as e:
            pass
            # print('点击失败')
        time.sleep(0.5)


def Send(d, element_xpath, msg):
    for i in range(20):
        try:
            bt = d.find_element_by_xpath(element_xpath)
            bt.send_keys(msg)
            break
        except Exception as e:
            pass
            # print('点击失败')
        time.sleep(0.5)


def Keep(exe, times=20):
    #  最大次数默认为无限
    #  保持尝试直到成功完成
    counter = 0
    while True:
        if ifTerminate:
            return
        counter += 1
        try:
            if (counter < times) or (times <= 0):
                exe()
                break
            else:
                break
        except Exception as e:
            pass
            # print('Keep--',str(exe.__name__),':失败-',counter)

        time.sleep(0.5)


def SwitchToIframe(d):
    def s1():
        WebDriverWait(d, 3, 0.5).until(EC.presence_of_element_located((By.XPATH, iframe_xpath)))
        iframe = d.find_element_by_xpath(iframe_xpath)
        d.switch_to.frame(iframe)

    Keep(s1)


def SwitchToDefault(d):
    def s2():
        d.switch_to.default_content()

    Keep(s2)


def IfIframeExist(d):
    try:
        d.find_element_by_xpath(iframe_xpath)
        return True
    except Exception:
        return False


def IfInframeExist(d, element_xpath):
    #  不能用循环，网卡时程序会以为不正常而无限循环检查，卡死在这个函数里
    try:
        iframe = d.find_element_by_xpath(iframe_xpath)
        d.switch_to.frame(iframe)
        d.find_element_by_xpath(element_xpath)
        d.switch_to.default_content()
        return True
    except Exception as e:
        pass

    SwitchToDefault(d)
    return False


def IfDataError(d):
    #  检查数据是否损坏
    try:
        data_error_label = d.find_element_by_xpath(data_error_label_xpath)
        if data_error_label.text == 'Data error.':
            # print('发现数据错误（Data error），应该重启')
            return True
        else:
            return False
    except Exception:
        return False


def IfInternalError(d):
    #  检查是否网络错误
    try:
        internal_iframe = d.find_element_by_xpath(internal_error_frame_xpath)
        d.switch_to.frame(internal_iframe)
        d.find_element_by_xpath(internal_error_warning_text_xpath)
        d.switch_to.default_content()
        # print('网络连接失败（internal error），应该重启')
        return True
    except:
        return False


def GetWeb(d):
    d.get('https://www.epicov.org/epi3/frontend')


def Login(d):
    login_xpath = '/html/body/form/div[5]/div/div[2]/div/div/div/div[1]/div/div/div[2]/input[1]'
    password_xpath = '/html/body/form/div[5]/div/div[2]/div/div/div/div[1]/div/div/div[2]/input[2]'
    login_bt_xpath = '/html/body/form/div[5]/div/div[2]/div/div/div/div[1]/div/div/div[2]/input[3]'

    Send(d, login_xpath, login_name)
    Send(d, password_xpath, login_password)
    Click(d, login_bt_xpath)
    print('Login')


def ClickSearch(d):
    search_bt = '/html/body/form/div[5]/div/div[2]/div/div[1]/div/div/div[2]'
    WebDriverWait(d, 3, 0.5).until(EC.presence_of_element_located((By.XPATH, search_bt)))
    Click(d, search_bt)
    print('点击搜索按钮')


def setDate(d, cd1='0', cd2='0', sd1='0', sd2='0'):
    clt_date_1 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div[3]/table/tbody/tr/td[2]/table/tbody/tr/td[' \
                 '1]/div/div[1]/input '
    clt_date_2 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div[3]/table/tbody/tr/td[2]/table/tbody/tr/td[' \
                 '3]/div/div[1]/input '
    sms_date_1 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div[3]/table/tbody/tr/td[2]/table/tbody/tr/td[' \
                 '5]/div/div[1]/input '
    sms_date_2 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div[3]/table/tbody/tr/td[2]/table/tbody/tr/td[' \
                 '7]/div/div[1]/input '
    if cd1 != '0':
        Send(d, clt_date_1, cd1 + '\n')
    if cd2 != '0':
        Send(d, clt_date_2, cd2 + '\n')
    if sd1 != '0':
        Send(d, sms_date_1, sd1 + '\n')
    if sd2 != '0':
        Send(d, sms_date_2, sd2 + '\n')


def ensurePatientStatus(d):
    w_patient = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr/td[3]/table[' \
                '2]/tbody/tr/td[2]/div/div[1]/div[2]/input '
    Click(d, w_patient)


def SetMoreInfo(d, infoDict):
    virus_name = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/table[' \
                 '1]/tbody/tr/td[2]/div/div[1]/input '
    location = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr/td[1]/table[2]/tbody/tr/td[' \
               '2]/div/div[1]/input '
    host = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/table[2]/tbody/tr/td[' \
           '2]/div/div[1]/input '

    complete = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr/td[3]/table[1]/tbody/tr/td[' \
               '2]/div/div[1]/div[1]/input '
    download = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/button[3]'
    print('还没写，啥都没做')


def start_wait(num):
    # print('等待数据刷新')
    for i in range(num):
        # print(num-i)
        time.sleep(1)


def FindPatientNums(d):
    #  返回项目总数
    total_num_xpath = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/span/span'
    total_num_str = d.find_element_by_xpath(total_num_xpath).text
    #
    total_num = total_num_str[7:-8].replace(',', '')
    # print('共',total_num,'个病例')
    return int(total_num)


def ParseOnePatient(d):
    #  处理完数据并点击离开
    #  创建单个病例的信息字典,34个普通数据和1个fasta数据。
    infoDict = {'Accession ID': 3, 'Type': 4, 'Clade': 5, 'Pango Lineage': 6, 'AA Substitutions': 7, 'Variant': 8,
                'Passage details/history': 9, 'Collection date': 11, 'Location': 12, 'Host': 13,
                'Additional location information': 14, 'Gender': 15, 'Patient age': 16, 'Patient status': 17,
                'Specimen source': 18, 'Additional host information': 19, 'Sampling strategy': 20, 'Outbreak': 21,
                'Last vaccinated': 22, 'Treatment': 23, 'Sequencing technology': 24, 'Assembly method': 25,
                'Coverage': 26, 'Comment': 27, 'Originating lab': 29, 'Address1': 30,
                'Sample ID given by the originating laboratory': 31, 'Submitting lab': 32, 'Address2': 33,
                'Sample ID given by the submitting laboratory': 34, 'Authors': 35, 'Submitter': 37,
                'Submission Date': 38, 'Address3': 39}
    #  xpath
    xpa_1 = '/html/body/form/div[5]/div/div[1]/div/div/table/tbody/tr['
    xpa_3 = ']/td[2]'
    fasta_xpath = '/html/body/form/div[5]/div/div[1]/div/div/pre'
    SwitchToIframe(d)
    #  获取一般数据
    for item in infoDict:
        num = infoDict[item]
        infoDict[item] = d.find_element_by_xpath(xpa_1 + str(num) + xpa_3).text

    #  获取fasta
    fasta = d.find_element_by_xpath(fasta_xpath).text
    infoDict['fasta'] = fasta
    #  点击离开按钮
    Click(d, to_main_bt_xpath)
    SwitchToDefault(d)
    # print('收集-Accession ID:',infoDict['Accession ID'])
    #  返回信息字典
    return infoDict


def if_cap_wrong(d):
    #  验证码是否错误
    text = str()
    try:
        iframe = d.find_element_by_xpath(iframe_xpath)
        d.switch_to.frame(iframe)
        for i in range(7):
            try:
                time.sleep(1)
                text = d.find_element_by_xpath(captcha_wrong_xpath).text
            except:
                pass
    except Exception as e:
        try:
            d.switch_to.default_content()
        except Exception:
            pass
        return False
    SwitchToDefault(d)
    if text == 'Try again!':
        return True
    else:
        return False


def ifGisPage(d):
    GisAidPageUrl = 'https://www.gisaid.org/'
    if d.current_url == GisAidPageUrl:
        return True
    else:
        return False


def CheckStatus(d):
    if ifGisPage(d):
        return 'gis_page'
    elif IfDataError(d):
        return 'data_error'
    elif IfInternalError(d):
        return 'internal_error'


def DoOneCaptcha(d, Name):
    #  在验证码界面输入验证码并提交
    def shoot_and_get_cap_filename():
        SwitchToIframe(d)
        captcha_img_filename = captchafolder + '/' + Name + '.png'
        #  先删除已有的图片
        if os.path.exists(captcha_img_filename):
            os.remove(captcha_img_filename)

        def shoot():
            d.find_element_by_xpath(captcha_xpath).screenshot(captcha_img_filename)

        Keep(shoot)
        SwitchToDefault(d)
        return captcha_img_filename

    def submit_cap_answer(answer):
        def clear():
            d.find_element_by_xpath(captcha_entry_xpath).clear()

        SwitchToIframe(d)
        Keep(clear)
        Send(d, captcha_entry_xpath, answer)

        Click(d, captcha_submit_xpath)
        # print('验证码：' + answer + '提交成功')
        SwitchToDefault(d)

    #  不存在就创建一个文件夹
    if not os.path.exists(captchafolder):
        os.mkdir(captchafolder)

    png_filename = shoot_and_get_cap_filename()
    #  像素匹配
    answer = OcrMachine.Ocr(png_filename)
    submit_cap_answer(answer)
    #  删除验证码图片
    os.remove(png_filename)


def CaptchaLoop(d, Name):
    activateSignal()
    DoOneCaptcha(d, Name)
    #  等待服务器响应,6s
    #  如果验证码错误就再解一次验证码
    if if_cap_wrong(d):
        #  等待验证码刷新
        time.sleep(0.5)
        CaptchaLoop(d, Name)


def DoReboot(d, Name):
    #  先转到百度，触发刷新
    d.get('https://www.baidu.com')
    cd1, cd2, sd1, sd2, w_patient = runningInfo[Name][0], runningInfo[Name][1], \
                                    runningInfo[Name][2], runningInfo[Name][3], runningInfo[Name][4]
    #  重新定位到原位置
    Patch_Basic(d)
    Patch_setInfo(d, cd1=cd1, cd2=cd2, sd1=sd1, sd2=sd2, w_patient=w_patient)
    Patch_GoToPage(d, Name)


def HandleExceptions(d, Name):
    status = CheckStatus(d)
    if status == ('data_error' or 'internal_error' or 'gis_page'):
        #  三种错误，重启
        DoReboot(d, Name)


whichone = ''


def CollectOnePage(d, Name, sttNum=1, endNum=50):
    if ifTerminate:
        return
    #  进行修正：endNum0->50
    if endNum == 0:
        endNum = 50
        # print('修正endNum')

    xpath_m1 = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/div[3]/table/tbody[2]/tr['
    # xpath_m2 = 1-50 是序列号码，不写出来
    xpath_m3 = ']/td[4]/div'

    def new_Step(d, i):
        if ifTerminate:
            return
        #  无论如何，完成这一个病例的采集
        xpath = xpath_m1 + str(i) + xpath_m3

        def oneloop(d, xpath):
            def doJudge():
                try:
                    WebDriverWait(d, 6, 0.25).until(EC.presence_of_element_located((By.XPATH, iframe_xpath)))
                    iframe = d.find_element_by_xpath(iframe_xpath)
                    d.switch_to.frame(iframe)

                    def ifframe():
                        try:
                            global whichone
                            d.find_element_by_xpath(captcha_xpath)
                            whichone = 'captcha'
                            d.switch_to.default_content()
                        except Exception as e:
                            pass

                    def ifnormal():
                        #  正常界面标记
                        normal_sign_xpath = '/html/body/form/div[5]/div/div[1]/div/div/table/tbody/tr[2]/td[1]'
                        try:
                            global whichone
                            d.find_element_by_xpath(normal_sign_xpath)
                            whichone = 'normal'
                            d.switch_to.default_content()
                        except Exception as e:
                            pass

                    t1 = Thread(target=ifframe)
                    t2 = Thread(target=ifnormal)
                    t1.start()
                    t2.start()
                    global whichone
                    while True:
                        if ifTerminate:
                            return
                        if whichone != '':
                            return
                        time.sleep(0.45)
                except Exception as e:
                    pass

            #  最大普通尝试次数
            max_tries = 8
            #  信息列表
            infoDict = {}
            #  每隔0.5秒试点击一次，直到点击成功或超过次数
            counter = 0
            for i in range(max_tries):
                try:
                    d.find_element_by_xpath(xpath).click()
                    break
                except:
                    counter += 1
                time.sleep(0.5)
            #  项目点击完成

            doJudge()
            global whichone
            if whichone == 'captcha':
                #  判断平均用时0.2s
                #  处理完验证码后继续循环
                CaptchaLoop(d, Name)
                whichone = ''
                #  返回空字典
                return infoDict
            elif whichone == 'normal':
                #  判断平均用时2.3s，所以取消了判断
                #  正常页面
                infoDict = ParseOnePatient(d)
                whichone = ''
                return infoDict

        while True:
            if ifTerminate:
                return
            infoDict = oneloop(d, xpath)
            if infoDict != {}:
                return infoDict

    for i in range(sttNum, endNum + 1):
        while True:
            if not if_stop:
                break

        time1 = time.time()
        #  进行一次解析
        infoDict = new_Step(d, i)
        if ifTerminate:
            return
        elif type(infoDict) != dict:
            #  避免错误
            return
        #  回复信号，表示正常运行
        activateSignal()
        #  记录进度
        adv = getAdvance(Name)
        setAdvance(Name, adv + 1)
        #  即时储存得到的信息；储存位置
        StoreInfoDict(Name + '.txt', infoDict)
        #  打印进度
        printAdvance(d, Name)
        #  控制速度
        time2 = time.time()
        usedtime = round((time2 - time1), 2)
        averageTime = usedtime
        #  设置固定的等待时间
        waittime = 6 + 4*(0.5 - random.random())
        if averageTime < waittime:
            time.sleep(waittime - averageTime)

        time3 = time.time()
        usedtime2 = round((time3 - time1), 2)
        averageTime2 = usedtime2
        print('爬虫速度为：', '%.2f' % averageTime2, '秒/个', '|真实速度为：'
              , '%.2f' % averageTime, '秒/个', '--------', time.strftime('%H:%M'))


def get_current_page_num_sub(d, page_xpath):
    #  确保在浏览页调用此函数，获取当前页码
    page_num = None
    try:
        page_num = int(d.find_element_by_xpath(page_xpath).text)
    except Exception as e:
        # print('找不到页码')
        pass
    return page_num


def get_current_page_num(d):
    MaybeList = (current_page_bt_xpath_page1, current_page_bt_xpath_page_middle, current_page_bt_xpath_page_last)
    for item in MaybeList:
        pageNum = get_current_page_num_sub(d, item)
        if pageNum is not None:
            # print('找到当前页码：' + str(pageNum))
            return pageNum


def go_to_former_page(d):
    #  到上一页
    Click(d, former_page_bt_xpath_middle)


def go_to_former2_page(d):
    #  到上第二页
    Click(d, former2_page_bt_xpath_middle)


def go_to_next_page(d, cur):
    #  到下一页
    if cur == 1:
        Click(d, next_page_bt_xpath_page1)
    else:
        Click(d, next_page_bt_xpath_middle)


def go_to_next2_page(d, cur):
    #  到下第二页
    if cur == 1:
        Click(d, next2_page_bt_xpath_page1)
    else:
        Click(d, next2_page_bt_xpath_middle)


def go_to_page(d, num):
    marker_num = 0
    global ifTerminate
    while True:
        if ifTerminate:
            return
        # print('正在翻到第' + str(num) + '页')
        #  获取当前页码
        cur_page_num = get_current_page_num(d)
        if cur_page_num == marker_num:
            #  data error了
            time.sleep(5)
            cur_page_num = get_current_page_num(d)
            if cur_page_num == marker_num:
                print('也许是data error或网速太慢，爬虫决定等待重启')
                ifTerminate = True
        #  正常
        marker_num = cur_page_num
        if cur_page_num == num:
            # print(str(cur_page_num) + '等于目标页码' + str(num))
            break
        elif cur_page_num < num:
            # print(str(cur_page_num) + '小于目标页码' + str(num))
            if num - cur_page_num > 1:
                go_to_next2_page(d, cur_page_num)
            else:
                go_to_next_page(d, cur_page_num)
        elif cur_page_num > num:
            # print(str(cur_page_num) + '大于目标页码' + str(num))
            if cur_page_num - num > 1:
                go_to_former2_page(d)
            else:
                go_to_former_page(d)
        activateSignal()
        time.sleep(2.5)

    return True


def Patch_Basic(d):
    #  最基础的操作
    GetWeb(d)
    Login(d)
    ClickSearch(d)


def Patch_setInfo(d, cd1='0', cd2='0', sd1='0', sd2='0', w_patient=True):
    #  输入信息并等待，这里只写了最基础的部分
    if w_patient:
        ensurePatientStatus(d)
    setDate(d, cd1, cd2, sd1, sd2)
    start_wait(6)


def Patch_GoToPage(d, Name, sttNum=1, endNum=-1):
    itemNum = FindPatientNums(d)
    if itemNum == 0:
        #  没有病例,直接结束
        return
    #  是否断点继续，默认继续，这不是bug
    if_breakon = True
    if sttNum > 1:
        #  特殊起始项目要求
        setAdvance(Name, sttNum - 1)
        if_breakon = False
    if endNum != -1:
        #  特殊终止项目要求
        itemNum = endNum

    #  初始化项目，获取项目进度
    adv = getAdvance(Name)
    if adv == itemNum:
        # print('已收集')
        return
    if adv > 0 and if_breakon:
        print('断点继续:', adv, '/', itemNum)
    #  起始页
    sttpage = int(adv / 50 + 1)
    #  末尾页
    endpage = int(itemNum / 50 + 1)
    #  开始项目的列表排序
    startNumOnPage = adv % 50 + 1
    #  最后一个项目的列表排序
    endNumOnPage = itemNum % 50
    if endNumOnPage == 0:
        endNumOnPage = 50
    #  到达开始页
    go_to_page(d, sttpage)
    return sttpage, endpage, startNumOnPage, endNumOnPage


def Patch_Collection(d, Name, sttpage, endpage, startNumOnPage, endNumOnPage):
    #  开始爬取
    if sttpage < endpage:
        #  病例有多页
        #  第一页
        CollectOnePage(d, Name, startNumOnPage, 50)
        if ifTerminate:
            return
        #  中间页
        for i in range(sttpage + 1, endpage):
            go_to_page(d, i)
            CollectOnePage(d, Name, 1, 50)
            if ifTerminate:
                return
        #  末尾页
        go_to_page(d, endpage)
        CollectOnePage(d, Name, 1, endNumOnPage)
    elif sttpage == endpage:
        #  病例只有一页
        CollectOnePage(d, Name, startNumOnPage, endNumOnPage)
    else:
        print('数据分析出错：sttpage-', sttpage, '>endpage-', endpage)


def OneThreadPatch(d, Name, cd1='0', cd2='0', sd1='0', sd2='0'):
    w_patient = True
    global runningInfo
    runningInfo[Name] = [cd1, cd2, sd1, sd2, w_patient]
    Patch_Basic(d)
    activateSignal()
    Patch_setInfo(d, cd1=cd1, cd2=cd2, sd1=sd1, sd2=sd2, w_patient=w_patient)
    activateSignal()
    #  翻到对应页
    sp, ep, snp, enp = Patch_GoToPage(d, Name)
    #  名字应该用日期
    #  开始收集
    Patch_Collection(d, Name, sp, ep, snp, enp)
    if ifTerminate:
        return
    #  已经做完，不需要再重复
    global ifdone
    ifdone = True
    print(Name, '完成!')


#  单个
def OneBrowser(date1, date2, type):
    #  方便版的单线程爬虫
    cd1, cd2, sd1, sd2 = '0', '0', '0', '0'
    if type == 'cd':
        cd1, cd2 = date1, date2
    elif type == 'sd':
        sd1, sd2 = date1, date2
    ops = webdriver.ChromeOptions()
    # ops.add_argument('--headless')
    # ops.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
    d = webdriver.Chrome(options=ops)
    Name = date1 + 'to' + date2
    OneThreadPatch(d, Name, cd1, cd2, sd1, sd2)
    if ifTerminate:
        d.close()
        return


def checker():
    global ifTerminate
    global signal
    #  每七分钟检验一次，如果没有回应就终止
    while True:
        time.sleep(60 * 9)
        if signal == False:
            ifTerminate = True
        else:
            signal = False
        if ifdone:
            break


def autoPatch(sd1, sd2):
    check = Thread(target=checker)
    check.start()
    global ifTerminate
    for i in range(100):
        print('第', i + 1, '次启动')
        try:
            ifTerminate = False
            OneBrowser(sd1, sd2, 'sd')
        except Exception as e:
            traceback.print_exc()
            print(e)
        if ifdone:
            break


if __name__ == '__main__':
    sd1 = '2020-01-01'
    sd2 = '2020-03-01'
    autoPatch(sd1, sd2)
    #  8-14之前的都是Address不准确的
