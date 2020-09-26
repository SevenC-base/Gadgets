#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# time:2020/09/20 周日 22:06:40.78
# By  Hasaki-h1


import selenium
import requests
import time
import random
import json
import sys
import datetime
import getopt
import progress
import urllib
from progress.bar import Bar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import request
from urllib.request import quote


driver_path = "C:\\Users\\Administrator\\Desktop\\Try Harder\\SRC漏洞\\自动化爬取漏洞\\chrome-win\\chromedriver.exe"

headersParameters = {  # 发送HTTP请求时的HEAD信息，用于伪装为浏览器
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
    'Cookie': 'BIDUPSID=ADFE6E768D6FAAFDF07535A6AF4B8FD1; PSTM=1600924354; BAIDUID=ADFE6E768D6FAAFDE778DBB5DDD281D5:FG=1; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; BD_CK_SAM=1; PSINO=3; H_PS_645EC=68b3C9JCXh4yO4VWg4b3yAa9XIg1TpoS%2FKpAjomEcZB9zSmOsCtejHZQEcA; BDSVRTM=131; H_PS_PSSID=32617_1431_32743_7566_7547_31253_32706_7552_7631_32117_7565_26350'
}


# 随机useragent获取
def random_userAgent(headersParameters):
    version = ['Mozilla/1.22', 'Mozilla/2.0', 'Mozilla/3.0', 'Mozilla/4.0', 'Mozilla/4.08']
    os = ["Windows 3.1", "Windows NT", "Windows NT 5.0", "Windows NT 5.1", "Windows NT 5.2", "Windows NT 3.51", "Windows NT 6.3", "Windows 95", "Windows 98", "Windows CE", ]
    browser = ["Firefox/", "Chrome/", "Safari/", "Edge/", "Opera/"]
    browser_version = str(random.randint(0, 9)) + "." + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
    browser_str = random.choice(browser) + browser_version
    user_agent = random.choice(version) + " (compatible; " + random.choice(os) + ") " + browser_str
    headersParameters["User-Agent"] = user_agent
    # print(user_agent)
    return headersParameters


# 开始执行程序
def run(path, keyword, num=5):
    if num == 1:
        print("☀✘✘✘-----Num needs to be greater than 1")
        sys.exit()
    else:
        tips = "Starting the browser driver in about 3 seconds"
        # print(tips)
        bar = Bar("Starting the browser driver in about 3 seconds", max=10, fill="█", suffix="%(percent)d%%")
        for i in range(10):
            time.sleep(0.3)
            bar.next()
        bar.finish()
        print("\n✈✈✈✈✈✈✈✈✈✈ Search info ✈✈✈✈✈✈✈✈✈✈\n The total number of pages is: {p}  search keyword is: {k}\n".format(p=num, k=keyword))
        results_list = []  # 存储百度链接
        cookie_dict = {}  # 存储cookie字典
        click_num = num  # 设置点击页数，也是爬取的页数
        get_current_page_xpath = ""  # 爬取当前页面的full_xpth
        chrome_driver = driver_path

        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 设置无界面模式运行浏览器
        # chrome_options.add_argument('--incognito')  # 设置无痕模式
        # chrome_options.add_argument('--disable-infobars')  # 设置禁用浏览器正在被自动化程序控制的提示
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        driver.get("https://www.baidu.com/s?ie=UTF-8&wd={k}".format(k=urllib.parse.quote(keyword)))
        time_sleep = random.randint(0, 3)
        # 随机延时，避免百度安全机制识别
        time.sleep(time_sleep)
        #title = driver.title
        # print(title)
        # cookie获取、格式转换、设置cookie
        cookie_list = driver.get_cookies()
        for c in cookie_list:
            cookie_dict[c['name']] = c['value']
        cookies_str = json.dumps(cookie_dict)
        cookies_str = cookies_str.replace('{', '').replace('}', '').replace(":", "=").replace('"', "").replace(" ", "").replace(",", ";").replace("=FG", ":FG")
        headersParameters['Cookie'] = cookies_str

        # 循环点击页数1
        print("Start crawl page {cn} ------------------------------------------------------".format(cn=(1)))
        for num in range(1, 11):
            try:
                get_link_xpath = "/html/body/div[1]/div[3]/div[1]/div[3]/div[" + str(num) + "]/h3/a"
                # /html/body/div[1]/div[3]/div[1]/div[3]/div[4]/div
                b = driver.find_element_by_xpath(get_link_xpath).get_attribute('href')
                print(b)
                results_list.append(b)
            except Exception as e:
                # 如果有推荐百度搜索div块进行+1
                get_link_xpath = "/html/body/div[1]/div[3]/div[1]/div[3]/div[" + str(num + 1) + "]/h3/a"
                b = driver.find_element_by_xpath(get_link_xpath).get_attribute('href')
                print(b)
                results_list.append(b)
                print("☀✔✔✔✔✔✔✔✔✔ Read the next div block ", get_link_xpath)
                #raise e
            finally:
                pass
        driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[1]/a[1]/span[2]").click()
        time.sleep(2)
        # print(title)
        print("Start crawl page {cn} ------------------------------------------------------".format(cn=(2)))
        for num in range(1, 11):
            try:
                get_link_xpath = "/html/body/div[1]/div[3]/div[1]/div[3]/div[" + str(num) + "]/h3/a"
                # print(get_link_xpath)
                b = driver.find_element_by_xpath(get_link_xpath).get_attribute('href')
                print(b)
                results_list.append(b)
            except Exception as e:
                get_link_xpath = "/html/body/div[1]/div[3]/div[1]/div[3]/div[" + str(num + 1) + "]/h3/a"
                b = driver.find_element_by_xpath(get_link_xpath).get_attribute('href')
                print(b)
                results_list.append(b)
                print("☀✔✔✔✔✔✔✔✔✔ Read the next div block ", get_link_xpath)
                #raise e
            finally:
                pass
        for click_n in range(3, click_num + 1):
            if click_n > 7:
                get_current_page_xpath = "/html/body/div[1]/div[3]/div[2]/div/a[7]/span[2]"
            else:
                get_current_page_xpath = "/html/body/div[1]/div[3]/div[2]/div/a[" + str(click_n) + "]/span[2]"
            print("Start crawl page {cn} ------------------------------------------------------".format(cn=(click_n)))
            # print(get_current_page_xpath)
            driver.find_element_by_xpath(get_current_page_xpath).click()
            # print(title)
            time.sleep(2)
            for num in range(1, 11):
                get_link_xpath = "/html/body/div[1]/div[3]/div[1]/div[3]/div[" + str(num) + "]/h3/a"
                try:
                    b = driver.find_element_by_xpath(get_link_xpath).get_attribute('href')
                    print(b)
                    results_list.append(b)
                    # time.sleep(2)  # 等待driver加载完成
                except Exception as e:
                    # 如果有推荐百度搜索div块进行+1
                    get_link_xpath = "/html/body/div[1]/div[3]/div[1]/div[3]/div[" + str(num + 1) + "]/h3/a"
                    b = driver.find_element_by_xpath(get_link_xpath).get_attribute('href')
                    print("☀✔✔✔✔✔✔✔✔✔ Read the next div block ", get_link_xpath)  # 此时出现相关搜索的div块，对此div块已加1
                    results_list.append(b)
                    #print("error------------------", get_link_xpath)
                    #raise e
                finally:
                    pass
        # 对获取的百度链接进行处理
        with open('result.txt', 'w', encoding='utf-8') as f:
            with open('log.txt', 'w', encoding='utf-8') as f1:
                print("\n☀☀☀ Get the real url -----------------------------------------------------------------")
                for r in results_list:
                    try:
                        last_url = ""
                        headersParameters1 = random_userAgent(headersParameters)
                        # 对获取的含有baidu连接的URL进行跳转
                        baidu_url = requests.get(url=r, headers=headersParameters1, allow_redirects=False, timeout=3)
                        time_sleep = random.randint(0, 3)
                        # 随机延时，避免百度安全机制识别
                        time.sleep(time_sleep)
                        # 获取百度链接跳转之后的URL
                        real_url = baidu_url.headers['location']
                        b_url_responese = requests.get(url=real_url, headers=headersParameters1, allow_redirects=False, timeout=3)
                        # 循环直到不是302
                        if b_url_responese.status_code == 302 or b_url_responese.status_code == 301 or b_url_responese.status_code == 303:
                            # 对获取到的URL进行访问
                            #real_url = last_url
                            driver.set_page_load_timeout(10)  # 设置最大超时时间
                            driver.set_script_timeout(10)
                            try:
                                driver.get(real_url)  # 新建标签
                                last_url = driver.current_url
                            except Exception as e:
                                print("☀✘✘✘----- Domain name not accessible!!!", last_url)
                            else:
                                pass
                            finally:
                                pass
                            # time.sleep(2)
                            if last_url:
                                print("200---", last_url)
                            else:
                                print("☀✘✘✘----- Read timeout!!!")
                        elif b_url_responese.status_code == 200:
                            last_url = real_url
                            print("200---", last_url)
                        else:
                            #last_url = b_url_responese.status_code + "is not setting"
                            print(b_url_responese.status_code, "is not setting")  # 除301,302,200,外未设置的url
                        f.write(last_url + '\n')
                    except Exception as e:
                        txt = str(results_list.index(r)) + " " + r + " " + str(e)
                        f1.write(txt)
                        #raise e
                        print("☀✘✘✘----- Connect error !!!", real_url)
                    finally:
                        pass
    driver.quit()


def main():
    help = """
☀☀☀ Crawl Baidu Pages [Version is 1.0] ☀☀☀
    
Usage:python crawler.py -p 5 -k inurl:login

Attention:
The scan results are saved in the current directory and the file name is result.txt

    -h, --help     dispaly this help and exit
    -p, --pages    set the crawl pages, default set is 5
    -k, --keyword  set the crawl keyword, default set is Hasaki-h1
    -v, --version  dispaly the version and exit

    """
    if len(sys.argv) == 1:
        #print("Crawl Baidu Page [Version is 1.0]")
        print(help)
        sys.exit()
    try:
        opts, args = getopt.getopt(sys.argv[1:], '-k:-p:-h-v', ['keyword', 'pages', 'help', 'version'])
        keyword1 = ''
        num = 5
        for opt_name, opt_value in opts:
            if opt_name in ('-k', '--keyword'):
                keyword1 = opt_value
            if opt_name in ('-p', '--pages'):
                num = opt_value
            if opt_name in ('-h', '--help'):
                print(help)
                sys.exit()
            if opt_name in ('-v', '--version'):
                print('\n☀☀☀ Crawl Baidu Pages [Version is 1.0] ☀☀☀')
                sys.exit()
        if len(keyword1) > 0:
            # print(len(keyword1))
            #print(num, keyword1)
            start = datetime.datetime.now()
            print('\n☀☀☀ Crawl Baidu Pages [Version is 1.0] ☀☀☀')
            run(driver_path, keyword=keyword1, num=int(num))
            end = datetime.datetime.now()
            print("\n☯☯☯☯☯☯☯☯ Program execution time is", end - start, "Everything is done, result.txt is saved current directory!")
        else:
            print("[Parameters is missing!!!] Please input a keyword for search of Baidu.")
            sys.exit()
    except getopt.GetoptError:
        print("[Parameters error!!!] Please input the right argv, see python crawler.py -h")
        pass


if __name__ == '__main__':
    #geturl(0, keyword="inurl:login")
    main()
