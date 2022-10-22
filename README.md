# GISAID spider
usage: gisaid_fasta_downloader [-h] -n NAME -p PASSWORD [-f MISSION_FILE] [-ms MISSION_STR [MISSION_STR ...]] [-sp SAVE_PATH] [-g] [-nm] [-r]
                               [--driver DRIusage: gisaid_fasta_downloader [-h] -n NAME -p PASSWORD [-f MISSION_FILE] [-ms MISSION_STR [MISSION_STR ...]] [-sp SAVE_PATH] [-g] [-nm] [-r]
                               [--driver DRIVER] [-dr DOWNLOAD_RANKS [DOWNLOAD_RANKS ...]]
gisaid_fasta_downloader: error: the following arguments are required: -n/--name, -p/--password
PS F:\PyProjects\Test\gisfasta4> python .\gisaid_fasta_downloader.py -h
usage: gisaid_fasta_downloader [-h] -n NAME -p PASSWORD [-f MISSION_FILE] [-ms MISSION_STR [MISSION_STR ...]] [-sp SAVE_PATH] [-g] [-nm] [-r]
                               [--driver DRIVER] [-dr DOWNLOAD_RANKS [DOWNLOAD_RANKS ...]]

a web spider to download gisaid fasta using selenium.这是基于selenium的爬虫脚本，用于获取gisaid序列数据。 在启动前请确保下载了Firefox（任意版本）+geckodriv
er.exe（任意版本）
脚本通过网页上选择并下载的序列csv文件精准下载。 默认解压tar文件、合并所有本次下载的.fasta和.tsv文件到-sp（即save_path）文件夹内，并删除下载的源文件； 能够
断点继续下载，如仍想要从头下载，请删除advance文件夹内对应csv名称的json文件； 使用示例如下：
python源码版本的： python gisaid_fasta_downloader.py -n 账号名 -p 密码 -f GISAID_hcov-19_ids_2022_07_20_12_50.csv（csv文件名） 可执行文件版本的： gisaid_fa
sta_downloader -n 账号名
-p 密码 -f GISAID_hcov-19_ids_2022_07_20_12_50.csv（csv文件名） 如需要保存原始文件，加入-r参数； 如不需自动解开tar与合并文件，加入-nm参数； --by cquxiaoy

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  账号名
  -p PASSWORD, --password PASSWORD
                        密码  
  -f MISSION_FILE, --mission_file MISSION_FILE
                        包含序列号的csv文件
  -ms MISSION_STR [MISSION_STR ...], --mission_str MISSION_STR [MISSION_STR ...]
                        通过此参数直接输入一至多个序列号下载
  -sp SAVE_PATH, --save_path SAVE_PATH
                        结果的保存路径
  -g, --is_graphic      开启浏览器界面，默认不开启
  -nm, --do_not_merge_data
                        不解压、合并数据，默认为解压+合并
  -r, --retain_raw_data
                        保留原始数据（无——nm时无效），默认不保留
  --driver DRIVER       浏览器类型，目前支支持firefox和chrome
  -dr DOWNLOAD_RANKS [DOWNLOAD_RANKS ...], --download_ranks DOWNLOAD_RANKS [DOWNLOAD_RANKS ...]
                        通过此参数传入配置下载的数据类型，可一次多下。默认为[2,]，即fasta和metadata的tar文件。其中数字是对应类型选项从上向下的序号： 1：Dat
es and Location 2：Input for the Augur pipeline
                        3：Nucleotide Sequences (FASTA) 4：Patient status metadata 5：Sequencing technology metadata
VER] [-dr DOWNLOAD_RANKS [DOWNLOAD_RANKS ...]]
参数：
  -h, --help            show this help message and exit
  -n NAME, --name NAME  账号名
  -p PASSWORD, --password PASSWORD
                        密码
  -f MISSION_FILE, --mission_file MISSION_FILE
                        包含序列号的csv文件
  -ms MISSION_STR [MISSION_STR ...], --mission_str MISSION_STR [MISSION_STR ...]
                        通过此参数直接输入一至多个序列号下载
  -sp SAVE_PATH, --save_path SAVE_PATH
                        结果的保存路径
  -g, --is_graphic      开启浏览器界面，默认不开启
  -nm, --do_not_merge_data
                        不解压、合并数据，默认为解压+合并
  -r, --retain_raw_data
                        保留原始数据（无——nm时无效），默认不保留
  --driver DRIVER       浏览器类型，目前支支持firefox和chrome
  -dr DOWNLOAD_RANKS [DOWNLOAD_RANKS ...], --download_ranks DOWNLOAD_RANKS [DOWNLOAD_RANKS ...]
                        通过此参数传入配置下载的数据类型，可一次多下。默认为[2,]，即fasta和metadata的tar文件。其中数字是对应类型选项从上向下的序号：
                        1：Dates and Location 
                        2：Input for the Augur pipeline
                        3：Nucleotide Sequences (FASTA) 
                        4：Patient status metadata 
                        5：Sequencing technology metadata
