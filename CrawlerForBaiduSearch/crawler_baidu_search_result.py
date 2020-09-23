#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# time:2020/09/20 周日 22:06:40.78
# By  Hasaki-h1

import urllib
from urllib import request
from urllib.request import quote
from bs4 import BeautifulSoup
import re
import lxml
import requests
import sys
import getopt
import multiprocessing


headersParameters = {  # 发送HTTP请求时的HEAD信息，用于伪装为浏览器
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Cookie': 'BD_UPN=12314753; sugstore=1; BAIDUID=5620FFD3AC7F5C161F287F9919FF67F2:FG=1; PSTM=1600359901; BIDUPSID=A756A3839937B3190A7FB464FE677BD6; delPer=0; BD_CK_SAM=1; PSINO=5; BD_HOME=1; BDRCVFR[eHt_ClL0b_s]=mk3SLVN4HKm; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; COOKIE_SESSION=9580_0_5_5_20_1_0_0_5_1_0_0_9580_0_2_0_1600618956_0_1600618954%7C9%23775_34_1600522842%7C9; H_PS_PSSID=32617_1420_7567_7580_32706_7607_32116_32718; H_PS_645EC=84f1qOD4N5Ggs60d1QZ47DE9B5WoDfgmerYjZq1oIJ3lPaJvsyQjLK1MjGA; BDSVRTM=0'
}

# 根据nums搜索所有返回页面


def search(nums, keyword):
    print("\n[+-+-+-+-+-+-+-+-+-SEARCH-INFO-+-+-+-+-+-+-+-+-+]\n The total number of pages is: {p}  search keyword is: {k}\n".format(p=nums, k=keyword))
    # 创建进程池
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # 循环调用多进程
    for n in range(0, int(nums)):
        # print('遍历页面{n1}.'.format(n1=n))
        pool.apply_async(geturl, args=(n, keyword))
        # print("done")
    pool.close()
    pool.join()


# 输入关键字返回搜索href(某一搜索页面)
def geturl(num, keyword):
    url = 'http://www.baidu.com.cn/s?wd=' + urllib.parse.quote(keyword) + '&pn='
    path = url + str(num * 10)
    #path = "https://www.baidu.com/s?wd=inurl%3Alogin&pn=100&oq=inurl%3Alogin&ie=utf-8&usm=1&rsv_pq=af4c51f50005518d&rsv_t=ec5er2afzCVzUvtaVuTZ9Z7vOhwCSTFiZ58MLcRrosj8J%2FbmoV1m%2F3SRLB8"
    response = requests.get(path, headers=headersParameters, timeout=5)
    # print('路径信息{n1}.'.format(n1=path))
    #print("状态码", response.status_code)
    soup = BeautifulSoup(response.text, 'lxml')
    tag_h3 = soup.find_all('h3')
    # print(tag_h3)
    with open('result.txt', 'w', encoding='utf-8') as f:
        for h3 in tag_h3:
            href = h3.find('a').get('href')
            #print('href=->', href)
            baidu_url = requests.get(url=href, headers=headersParameters, allow_redirects=False, timeout=2)
            real_url = baidu_url.headers['location']
            #url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', real_url)
            # print(url)
            f.write(real_url + '\n')
            print(real_url)


def main():
    help = """
--------Crawl Baidu Page [Version is 1.0]--------
    
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
                print('\n--------Crawl Baidu Page [Version is 1.0]--------')
                sys.exit()
        if len(keyword1) > 0:
            # print(len(keyword1))
            #print(num, keyword1)
            search(nums=num, keyword=keyword1)
        else:
            print("[Parameters is missing!!!] Please input a keyword for search of Baidu.")
            sys.exit()
    except getopt.GetoptError:
        print("[Parameters error!!!] Please input the right argv, see python crawler.py -h")
        pass


if __name__ == '__main__':
    #search(num=14, keyword="inurl:login")
    main()
