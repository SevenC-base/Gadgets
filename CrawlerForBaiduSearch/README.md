# Gadgets
A small tool for get the result of baidu search link.

There are still a few bugs, but I won't update them


Directions for use

1、python -m pip install -r requirements.txt

2、set the chrome driver path, driver_path = "{Your computer path of chromedriver.exe}\\chromedriver.exe", the chromedriver.exe download link is https://npm.taobao.org/mirrors/chromedriver/

3、python crawler.py -p 2 -k inurl:login


Usage:python crawler.py -p 5 -k inurl:login

Attention:
The scan results are saved in the current directory and the file name is result.txt

    -h, --help     dispaly this help and exit
    -p, --pages    set the crawl pages, default set is 5
    -k, --keyword  set the crawl keyword, default set is Hasaki-h1
    -v, --version  dispaly the version and exit
![image](https://github.com/SevenC-base/Gadgets/blob/master/CrawlerForBaiduSearch/pa1.png)
![image](https://github.com/SevenC-base/Gadgets/blob/master/CrawlerForBaiduSearch/pa2.png)
![image](https://github.com/SevenC-base/Gadgets/blob/master/CrawlerForBaiduSearch/pa3.png)
