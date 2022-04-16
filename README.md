# GISAID-spider
这是基于selenium的python爬虫，需要谷歌/**火狐**浏览器+浏览器selenium驱动（chromedriver.exe-谷歌/geckodriver.exe-火狐）+一些python软件包运行。  
  
These scripts are python spiders. To run them, Chrome / **Firefox** & selenium drivers(chromedriver.exe-Chrome/geckodriver.exe-Firefox) & Some python packages are needed.  

## GISEND  
**功能：全自动爬取GISAID EpiCoV病例数据，默认勾选“w/patient”，能够自动识别GISAID的验证码**  
步骤：  
1.提前安装好Chrome浏览器（谷歌浏览器）,把chromedriver.exe放入python所在路径；  
2.安装python3；  
3.安装scikit-image、selenium、pillow包：  
步骤为：DOS窗口依次输入：“pip install”+“空格”+以上包名之一  
4.下载GISEND.zip->解压->运行gui.py->开始爬虫  
  
**Used for getting GISAID EpiCoV patient data full-automatically. "w/patient" checkbox is checked by default. It can recognize GISAID captcha automatically.**  
Steps:   
1.install Chrome browser, put chromedriver.exe into python path;  
2.install Python3.  
3.install python packages "scikit-image, selenium, pillow".  
Steps: Enter "pip install xxx" in DOS window.  
4.download GISEND.zip->unzip->run "gui.py"->start spider.  

## GISFASTA  
**功能：全自动爬取GISAID EpiCoV里的 fasta数据（用火狐）**  
步骤：  
1.提前安装好火狐浏览器,把geckodriver.exe放入python所在路径；  
2.安装python3；  
3.安装selenium包：  
步骤为：DOS窗口输入：“pip install selenium”  
4.下载gis_fasta.zip->解压->运行start_gui.py->开始爬虫（注备：遇到元素无法找到的报错，请将等待时间延长）  
  
**Used for getting GISAID EpiCoV fasta data full-automatically.(use Firefox)**  
Steps:   
1.install Firefox browser, put geckodriver.exe into python path;  
2.install Python3.  
3.install python package selenium.  
Steps: Enter "pip install selenium" in DOS window.  
4.download gis_fasta.zip->unzip->run "start_gui.py"->start spider.  
