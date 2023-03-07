# coding:utf-8
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from parse_acnums import AcNumAnalysis
import argparse
import tarfile
import shutil
import json

__author__ = 'cquxiaoy'

select_all = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/table/thead/tr/th[1]/div/span/input'
download = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/button[4]'
download2 = '/html/body/form/div[5]/div/div[2]/div/div/div[2]/div/button'
select_bt_path = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/button[2]'
accession_num_textarea = '/html/body/form/div[5]/div/div[1]/div/div[1]/table[2]/tbody/tr/td/div/div[1]/textarea'
ok1_bt = '/html/body/form/div[5]/div/div[2]/div/div/div[2]/div/button'
ok2_bt = '/html/body/div[2]/div[1]/div[3]/div/button'
return_bt_xpath = '/html/body/form/div[5]/div/div[2]/div/div/div[1]/div/button'
sys_timer1_xpath = '//*[@id="sys_timer"]'
sys_timer2_xpath = '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/div[3]/table/tbody[1]'
i_agree = '/html/body/form/div[5]/div/div[2]/div[1]/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/div[1]/div/input'
download3 = '/html/body/form/div[5]/div/div[2]/div[2]/div/div[2]/div/button'

iframes = {
    1: '/html/body/iframe',
    2: '/html/body/iframe[2]',  # 验证码和病例数据?或许不是
}

advance_path = './advance'


class V:
    def __init__(self, value):
        self.value = value

    def __bool__(self):
        return self.value

    def set(self, other):
        self.value = other


if_terminate = V(False)
if_stop = V(False)
if_done = V(False)
signal = V(True)


def keep(exe, *args, max_times=180):
    if not signal or if_terminate:
        # 退出
        if_terminate.set(True)
        print('Timeout, Restarting...')
        return
    else:
        signal.set(False)
    for i in range(max_times):
        try:
            result = exe(*args)
            signal.set(True)
            return result
        except Exception as e:
            # print(str(e).split('\n')[0])
            time.sleep(0.5)


def _into_iframe(d, frame_xpath):
    keep(lambda: d.switch_to.frame(d.find_element(By.XPATH, frame_xpath)))


def login_basic(d, name='', password=''):
    name_input_locator = (By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div/div/div[1]/div/div/div[2]/input[1]')
    password_input_locator = (By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div/div/div[1]/div/div/div[2]/input[2]')
    login_bt_locator = (By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div/div/div[1]/div/div/div[2]/input[3]')
    d.get('https://www.epicov.org/epi3/frontend')
    keep(lambda: d.find_element(*name_input_locator).send_keys(name))
    keep(lambda: d.find_element(*password_input_locator).send_keys(password))
    keep(lambda: d.find_element(*login_bt_locator).click())

    tab_locator = (By.XPATH, '/html/body/form/div[5]/div/div[1]/div/div/div/div/div[2]/div/ul/li[3]/a')
    search_bt = (By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div[1]/div/div/div[3]')
    keep(lambda: d.find_element(*tab_locator).click())
    keep(lambda: d.find_element(*search_bt).click())


def load_ids(d, ids_str):
    select_bt_locator = (By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/button[2]')
    text_area_locator = (
    By.XPATH, '/html/body/form/div[5]/div/div[1]/div/div[1]/table[2]/tbody/tr/td/div/div[1]/textarea')
    select_ok = (By.XPATH, '/html/body/form/div[5]/div/div[2]/div/div/div[2]/div/button')
    select_ok2 = (By.XPATH, '/html/body/div[2]/div[1]/div[3]/div/button')

    keep(lambda: d.find_element(*select_bt_locator).click())
    _into_iframe(d, iframes[1])
    keep(lambda: d.find_element(*text_area_locator).clear())
    js = '$("textarea").val("%s");'%ids_str
    keep(lambda: d.execute_script(js))
    time.sleep(1)
    keep(lambda: d.find_element(*text_area_locator).send_keys(' '))

    keep(lambda: d.find_element(*select_ok).click())
    keep(lambda: d.find_element(*select_ok2).click())
    keep(lambda: d.switch_to.default_content())


def download_fasta(d, driver, d_rank=2):
    # 点击下载按钮, d_rank代表从上往下数第几个单选按钮
    keep(lambda: d.find_element(By.XPATH, download).click())
    _into_iframe(d, iframes[1])

    keep(lambda: d.find_element(By.XPATH, '/html/body/form/div[5]/div/div[1]/div/div/table[1]/tbody/tr/td[2]/div/div[1]/div[2]/div[%d]/input' % d_rank).click())  # 点击对应radio button
    keep(lambda: d.find_element(By.XPATH, download2).click())
    keep(lambda: d.switch_to.default_content())
    time.sleep(1)
    _into_iframe(d, iframes[1])
    keep(lambda: d.find_element(By.XPATH, i_agree).click())
    keep(lambda: d.find_element(By.XPATH, download3).click())
    keep(lambda: d.switch_to.default_content())
    filename = keep((lambda: wait_downloaded_filename(d) if driver=='firefox' else (lambda: getDownLoadedFileName(d))))
    if filename is not None: print('\ndownload_complete:', filename)


def load_advance(advance_filename):
    if os.path.exists(advance_filename):
        with open(advance_filename, 'r') as f:
            return json.loads(f.read())
    else:
        open(advance_filename, 'a+').close()
        return None


def store_advance(advance_filename, content):
    with open(advance_filename, 'w') as f:
        f.write(json.dumps(content))


def merge_data(temp_path, save_path, raw_file_path='raw_file'):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    tarfiles = []
    for filename in os.listdir(temp_path):
        filename = temp_path + os.sep + filename
        if os.path.splitext(filename)[1] == '.tar' and os.path.getsize(filename):
            tarfiles.append(filename)
            with tarfile.open(filename, 'r:tar') as f:
                f.extractall(save_path)

    fasta_files = []
    tsv_files = []
    for filename in os.listdir(save_path):
        if 'merge' not in filename:
            filename = save_path + os.sep + filename
            if os.path.splitext(filename)[-1] == '.fasta':
                fasta_files.append(filename)
            elif os.path.splitext(filename)[-1] == '.tsv':
                tsv_files.append(filename)
    # 处理fasta，直接连接
    fasta_str, tsv_str = '', ''
    for filename in fasta_files:
        with open(filename, encoding='utf-8') as f:
            fasta_str += f.read()
    time_str = time.strftime('%Y_%m_%d_%H_%M_%S')
    fn = save_path + os.sep + 'merged_fasta_'+time_str+'.fasta'
    while os.path.exists(fn):
        fn += 'a'
    with open(fn, mode='w', encoding='utf-8') as ff:
        ff.write(fasta_str)
    del fasta_str
    # 处理tsv文件
    head = True
    for filename in tsv_files:
        with open(filename, encoding='utf-8') as f:
            if head:
                head = False
            else:
                f.readline()
            tsv_str += f.read()
    fn = save_path + os.sep + 'merged_tsv_'+time_str+'.metadata.tsv'
    while os.path.exists(fn):
        fn += 'a'
    with open(fn, mode='w', encoding='utf-8') as ft:
        ft.write(tsv_str)
    # 删除解压后的文件
    for filename in fasta_files+tsv_files:
        os.remove(filename)
    if raw_file_path is not None:
        if not os.path.exists(raw_file_path):
            os.mkdir(raw_file_path)
        # 把原始文件放到raw_file_path的文件夹里
        for raw_file in tarfiles:
            shutil.move(raw_file, raw_file_path)
    else:
        # 否则删除原始文件
        for raw_file in tarfiles:
            os.remove(raw_file)


def getDownLoadedFileName(driver, waitTime=3000):
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
            downloadPercentage = driver.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            signal = True
            if downloadPercentage == 100:
                # return the file name once the download is completed
                fname = driver.execute_script(
                    "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
                if not os.path.exists('C:/Users/小扬/Downloads/'+fname):
                    raise NameError()
                else:
                    break

        except:
            try:
                fname = driver.execute_script(
                    "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
                if os.path.exists('C:/Users/小扬/Downloads/'+fname):
                    break
            except:
                print('.', end='')

        time.sleep(0.01)  # 增加检测次数
        if time.time() > endTime:
            return ''
    driver.switch_to.window(driver.window_handles[0])
    return fname


def wait_downloaded_filename(d, waitTime=3000):
    d.execute_script("window.open()")
    WebDriverWait(d, 30).until(EC.new_window_is_opened)
    d.switch_to.window(d.window_handles[-1])
    d.get("about:downloads")
    time.sleep(1)

    sen = 0.05  # 灵敏程度
    endTime = time.time()+waitTime
    while True:
        try:
            #progress = driver.execute_script("return document.querySelector('.downloadContainer progress:first-of-type').value")
            dldetail = d.execute_script("return document.querySelector('.downloadDetailsNormal').value")
            download_ever_started = False
            while True:
                if "剩余时间" in dldetail or ' left' in dldetail:
                    download_ever_started = True
                    time.sleep(sen)
                    dldetail = d.execute_script("return document.querySelector('.downloadDetailsNormal').value")
                    #progress = driver.execute_script("return document.querySelector('.downloadContainer progress:first-of-type').value")
                elif download_ever_started:
                    break
                elif '失败' in dldetail or 'fail' in dldetail:
                    if_terminate.set(True)
                    print('下载失败，重启浏览器...')
                    return None
                else:
                    time.sleep(sen)
                    dldetail = d.execute_script("return document.querySelector('.downloadDetailsNormal').value")
                print('\r%s' % dldetail, end=' '*20)
            # 获取文件名
            fileName = d.execute_script("return document.querySelector('.downloadContainer description:first-of-type').value")

            d.close()
            d.switch_to.window(d.window_handles[0])
            time.sleep(2*sen)
            return fileName
        except:
            pass
        time.sleep(sen)
        if time.time() > endTime:
            break


def start(name, password, mission_file='', mission_str='', save_path='./downloads', is_gui=False, not_merge_data=False, retain_raw_data=False, download_ranks=None, driver='firefox'):
    if_terminate.set(False)
    signal.set(True)
    # 设置保存路径
    save_path = os.path.abspath(save_path)
    filepath_set = [save_path]
    if not not_merge_data:
        # 设置临时文件夹
        download_dir = os.path.abspath('./temp')
        filepath_set.append(download_dir)
    else:
        download_dir = save_path
    filepath_set.append(advance_path)
    # 文件系统预备
    for fpath in filepath_set:
        if not os.path.exists(fpath):
            os.mkdir(fpath)
    # 标准化download_ranks：需要下载的数据类型
    download_ranks = download_ranks or [2, ]
    # 准备任务序列
    analysis = AcNumAnalysis()
    # 如果要下载patient_data，将间隔调成2000
    if 4 in download_ranks: analysis.default_num = 2000
    advance_file = advance_path + '/' + 'cache.json'
    if mission_file:
        advance_file = advance_path + '/' + os.path.basename(mission_file) + '.json'
        if not os.path.exists(advance_file):
            print('分离序列中（'+str(analysis.default_num)+'条）...')
            with open(mission_file, 'r') as f:
                analysis.refresh(f.read())
            mission_list = analysis.get_whole_list()
            store_advance(advance_file, mission_list)
        else:
            print('读取缓存...')
            mission_list = load_advance(advance_file)
            if not mission_list:
                print('已结束...')
                if_done.set(True)
                return
    elif mission_str:
        analysis.refresh(mission_str)
        mission_list = analysis.get_whole_list()
        store_advance(advance_file, mission_list)
    else:
        print('无任务序列输入，结束。')
        return
    # 释放内存
    del analysis
    print('一共%d个下载任务'%len(mission_list))

    # 设置浏览器

    print('Opening Browser...')
    options = Options()
    if not is_gui:
        #  开启无头模式
        options.add_argument('--headless')
    # MIME types
    mime_types = "application/octet-stream"
    mime_types += ",application/excel,application/vnd.ms-excel"
    mime_types += ",application/pdf,application/x-pdf"
    mime_types += ",application/x-bzip2"
    mime_types += ",application/x-gzip,application/gzip"

    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", mime_types)
    options.set_preference(
        "plugin.disable_full_page_plugin_for_types", mime_types)
    options.set_preference("pdfjs.disabled", True)

    d = webdriver.Firefox(
        options=options,
    ) if driver.lower() == 'firefox' else webdriver.Chrome()

    print('Logging...')
    login_basic(d, name, password)

    for index, ids_str in enumerate(mission_list):
        print('Putting Accession Numbers...')
        if ids_str == 'E':  # 补丁
            print('警告，数据可能发生了错误（E），将跳过本次下载，记得检查最终数据完整性！')
            continue
        load_ids(d, ids_str)
        print('Downloading file %d/%d↓↓↓' % (index+1, len(mission_list)))
        for i in download_ranks:
            #  下载大于等于1个指定类型的数据
            download_fasta(d, driver, i + 1)
        if if_terminate:
            d.close()
            return
        store_advance(advance_file, mission_list[index+1:])
    #  等待所有下载完成
    print('Closing Browser...')
    if_done.set(True)
    d.close()
    if not not_merge_data:
        print('Untar and Merging Data...（只合并 Input for the Augur pipeline）')
        raw_file_path = 'raw_file' if retain_raw_data else None
        merge_data(download_dir, save_path, raw_file_path)
    print('结束')


def spider_loop(name, password, mission_file='', mission_str='', save_path='./downloads', is_gui=False, not_merge_data=False, retain_raw_data=False, download_ranks=None, driver='firefox'):
    if not mission_file and not mission_str:
        print('无任务！')
        return 1
    while not if_done:
        start(
            name=name,
            password=password,
            mission_file=mission_file,
            mission_str=mission_str,
            save_path=save_path,
            is_gui=is_gui,
            not_merge_data=not_merge_data,
            retain_raw_data=retain_raw_data,
            download_ranks=download_ranks,
            driver=driver
        )


argp = argparse.ArgumentParser(prog='gisaid_fasta_downloader', description="""
a web spider to download gisaid fasta using selenium.这是基于selenium的爬虫脚本，用于获取gisaid序列数据。
在启动前请确保下载了Firefox（任意版本）+geckodriver.exe（任意版本）
脚本通过网页上选择并下载的序列csv文件精准下载。
默认解压tar文件、合并所有本次下载的.fasta和.tsv文件到-sp（即save_path）文件夹内，并删除下载的源文件；
能够断点继续下载，如仍想要从头下载，请删除advance文件夹内对应csv名称的json文件；
使用示例如下：
python源码版本的：
python gisaid_downloader.py -n 账号名 -p 密码 -f GISAID_hcov-19_ids_2022_07_20_12_50.csv（csv文件名）
可执行文件版本的：
gisaid_fasta_downloader -n 账号名 -p 密码 -f GISAID_hcov-19_ids_2022_07_20_12_50.csv（csv文件名）
如需要保存原始文件，加入-r参数；
如不需自动解开tar与合并文件，加入-nm参数；

请注意，如果爬虫卡住，可能是以下原因：
1.还没下载就卡住了，这种情况很可能是firefox的日志文件导致的（会导致跳过按某些按钮，具体原因不明），删除脚本目录下的geckodriver.log文件一般能解决。
如果还不能，再试试不开启界面模式，或者多试几次； 
2.卡在了下载patient status 的过程中，具体表现就是下载停留在了patient status（dr=4）那一步。 
这是因为GISAID网站在处理这个数据（patient status）的时候，如果id一次性非常大（比如5000），将会非常慢（手动下载也会这样）。比较合适的一个值是2000。 
第一次下载时使用的dr没有4（即不包含patient status这类数据），爬虫就会把一次性下载的数量设为5000（也就是一次性能下载的最大值）， 
之后使用的包含了4，还是会按5000一次来下载，所以会卡住。 
解决方法： 
删掉advance文件夹下同名json文件，dr参数值带上4（或者界面上选中patient status下载选项），重新开始下载。
--by cquxiaoy
""")
argp.add_argument('-n', '--name', nargs=1, required=True, type=str, help='账号名')
argp.add_argument('-p', '--password', nargs=1, required=True, type=str, help='密码')
argp.add_argument('-f', '--mission_file', nargs=1, type=str, help='包含序列号的csv文件')
argp.add_argument('-ms', '--mission_str', default='', nargs='+', type=str, help='通过此参数直接输入一至多个序列号下载')
argp.add_argument('-sp', '--save_path', nargs=1, type=str, default=['./downloads'], help='结果的保存路径')
argp.add_argument('-g', '--is_graphic', action='store_true', default=False, help='开启浏览器界面，默认不开启')
argp.add_argument('-nm', '--do_not_merge_data', dest='not_merge', action='store_true', default=False, help='不解压、合并数据，默认为解压+合并')
argp.add_argument('-r', '--retain_raw_data', action='store_true', default=False, help='保留原始数据（无——nm时无效），默认不保留')
argp.add_argument('--driver', default='firefox', help='浏览器类型，目前支支持firefox和chrome')
argp.add_argument('-dr', '--download_ranks', default=[2, ], nargs='+', type=int,
                  help="""通过此参数传入配置下载的数据类型，可一次多下。默认为[2,]，即fasta和metadata的tar文件。其中数字是对应类型选项从上向下的序号：
                  1：Dates and Location
                  2：Input for the Augur pipeline
                  3：Nucleotide Sequences (FASTA)
                  4：Patient status metadata
                  5：Sequencing technology metadata
""")


if __name__ == '__main__':
    args = argp.parse_args()
    os.chdir(os.path.split(__file__)[0])
    spider_loop(
        name=args.name[0],
        password=args.password[0],
        mission_file=args.mission_file[0] if args.mission_file else '',
        mission_str=', '.join(args.mission_str) if args.mission_str else None,
        save_path=args.save_path[0],
        is_gui=args.is_graphic,
        not_merge_data=args.not_merge,
        retain_raw_data=args.retain_raw_data,
        download_ranks=args.download_ranks,
        driver=args.driver,
    )
