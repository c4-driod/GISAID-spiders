# GISAID downloader GISAID数据爬虫（下载器）
基于selenium，用于全自动下载GISAID数据
需要火狐浏览器或者谷歌浏览器（谷歌开无界面会被服务器拒绝）
## 示例
### 下载metadata和fasta
1.
python gisaid_downloader -n 这里填你的账号名 -p 这里填密码 -f 这里填csv文件

全部参数：
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

