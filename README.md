# GISAID-spider（非常非常非常抱歉，这两个爬虫目前都有bug，不能正常使用，维护可能要等到2022.5.28以后进行）
这是基于selenium的python爬虫.
需要谷歌/**火狐**浏览器+webdriver（chromedriver.exe-谷歌/geckodriver.exe-火狐）+一些python软件包。  
用pip命令安装需要的软件包：  
GISEND: selenium, pillow, scikit-image  
GISFASTA: selenium  

These scripts are python spiders. 
To run them, Chrome / **Firefox** & selenium webdrivers(chromedriver.exe-Chrome/geckodriver.exe-Firefox) & Some python packages are needed.  
use pip to install the packages：  
GISEND: selenium, pillow, scikit-image  
GISFASTA: selenium  

## GISEND  
**功能：全自动获取GISAID EpiCoV病例数据，默认勾选“w/patient”，能够自动识别GISAID的验证码**  
步骤：  
1.提前安装好Chrome浏览器（谷歌浏览器）,把chromedriver.exe放入脚本所在路径；  
2.运行gui.py->开始爬虫  
  
**Used for getting GISAID EpiCoV patient data full-automatically. "w/patient" checkbox is checked by default. It can recognize GISAID captcha automatically.**  
Steps:   
1.install Chrome browser, put chromedriver.exe into script path;   
2.run "gui.py"->start spider.  

## GISFASTA  
**功能：用火狐全自动获取GISAID EpiCoV里的 fasta数据**  
步骤：  
1.提前安装好火狐浏览器,把geckodriver.exe放入脚本所在路径；  
2.运行start_gui.py->开始爬虫
  
**Used for getting GISAID EpiCoV fasta data full-automatically.(use Firefox)**  
Steps:   
1.install Firefox browser, put geckodriver.exe into script path;  
2.run "start_gui.py"->start spider.  
