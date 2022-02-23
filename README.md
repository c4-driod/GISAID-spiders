# GISAID-spider
这是我完成的python爬虫，需要谷歌浏览器+一些python软件包才能运行。  
  
These scripts are python spiders. To run them, Chrome & Some python packages are needed.  

## GISEND (GISEND.zip)
**功能：全自动爬取GISAID EpiCoV病例数据，默认勾选“w/patient”，能够自动识别GISAID的验证码**  
步骤：  
1.提前安装好Chrome浏览器（谷歌浏览器）；  
2.安装python3；  
3.安装scikit-image、selenium、pillow包：  
步骤为：DOS窗口依次输入：“pip install”+“空格”+以上包名之一  
4.下载GISEND.zip->解压->运行gui.py->开始爬虫  
  
**This Script is used for getting GISAID EpiCoV patient data full-automatically. "w/patient" checkbox is checked by default. It can recognize GISAID captcha automatically.**  
Steps:   
1.install Chrome browser;  
2.install Python3.  
3.install python packages "scikit-image, selenium, pillow".  
Steps: Enter "pip install xxx" in DOS window.  
4.download GISEND.zip->unzip->run "gui.py"->start spider.  

## GISFASTA (gis_fasta.zip)
**功能：全自动爬取GISAID EpiCoV里的 fasta数据**  
步骤：  
1.提前安装好Chrome浏览器（谷歌浏览器）；  
2.安装python3；  
3.安装selenium包：  
步骤为：DOS窗口输入：“pip install selenium” 
4.下载gis_fasta.zip->解压->运行start_gui.py->开始爬虫  
  
**This Script is used for getting GISAID EpiCoV fasta data full-automatically.**  
Steps:   
1.install Chrome browser;  
2.install Python3.  
3.install python package selenium.  
Steps: Enter "pip install selenium" in DOS window.  
4.download gis_fasta.zip->unzip->run "start_gui.py"->start spider.  

## 其他
"OCR.py" 和 "CharsPrecise.py"是验证码识别接口，不需要下载，它们已经包含在"GISEND.zip"文件里了。放在外面是方面查看和单独下载。 
接口为CharOcr类的Ocr(png_filename)方法，它能识别GISAID的验证码，将会返回结果字符串.  
示例：  
from time import time  
from Ocr import CharOcr  
  
ocr = CharOcr()  
t1 = time.time()  
ans = ocr.Ocr('test4.png')  
t2 = time.time()  
print('用时：', t2 - t1, 's')  
print(ans)  

