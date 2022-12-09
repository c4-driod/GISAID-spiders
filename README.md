# GISAID downloader GISAID数据爬虫（附界面程序）
**基于selenium，用于全自动下载GISAID数据.** Based on selenium, aiming at download GISAID data automatically.\
需要火狐浏览器或者谷歌浏览器（谷歌开无界面会被服务器拒绝），默认用火狐浏览器。\
使用火狐，需要准备： 
  * 百度搜索**geckodriver.exe**，下载并把文件放在脚本同文件夹下； 
  * 安装**火狐浏览器**； 
  * 安装Python第三方包**selenium**； 

可以使用**命令行**（如下）或者**用户操作界面**（start.py）进行操作;\

打包好的exe程序在gisaid_downloader.zip内，windows下可以直接使用。

感谢大佬的资助，项目得以完成。

---
## 功能
1.全自动下载一些基础数据\
2.断点续下（如果想重新下，可以把advance文件夹里对应名字的json文件删除）

---
## 示例
### 下载metadata和fasta
python gisaid_downloader -n 这里填你的账号名 -p 这里填密码 -f 这里填csv文件
### 下载metadata、fasta和病例数据
python gisaid_downloader -n name -p password -f xx.csv -dr 2 4

---
## 所有参数
-n NAME, --name NAME  账号名\
  -p PASSWORD, --password PASSWORD\
                        密码\
  -f MISSION_FILE, --mission_file MISSION_FILE\
                        包含序列号的csv文件\
  -ms MISSION_STR [MISSION_STR ...], --mission_str MISSION_STR [MISSION_STR ...]\
                        通过此参数直接输入一至多个序列号下载\
  -sp SAVE_PATH, --save_path SAVE_PATH\
                        结果的保存路径\
  -g, --is_graphic      开启浏览器界面，默认不开启\
  -nm, --do_not_merge_data\
                        不解压、合并数据，默认为解压+合并\
  -r, --retain_raw_data\
                        保留原始数据（无——nm时无效），默认不保留\
  --driver DRIVER       浏览器类型，目前支支持firefox和chrome\
  -dr DOWNLOAD_RANKS [DOWNLOAD_RANKS ...], --download_ranks DOWNLOAD_RANKS [DOWNLOAD_RANKS ...]\
                        通过此参数传入配置下载的数据类型，可一次多下。默认为[2,]，即fasta和metadata的tar文件。其中数字是对应类型选项从上向下的序号： \
                        1：Dates and Location \
                        2：Input for the Augur pipeline\
                        3：Nucleotide Sequences (FASTA) \
                        4：Patient status metadata \
                        5：Sequencing technology metadata

