#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# time:2020/11/19 周四 21:24:41.56
# author:White9527


from requests.packages.urllib3.exceptions import InsecureRequestWarning
import mmh3
import requests
import urllib3
import codecs
import sys

try:
    url = sys.argv[1]
    if ("http" in url) or ("https" in url):
        urllib3.disable_warnings()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        print('\n☆ icon_hash = "%s"' % mmh3.hash(codecs.lookup('base64').encode(requests.get(url, verify=False).content)[0]))
    else:
        with open(url, "rb") as f:
            s = f.read()
            s1 = mmh3.hash(codecs.lookup('base64').encode(s)[0])
            print('\n☆ icon_hash = "' + str(s1).strip('\n') + '"')
            # reset_Color()
            # print("")
except Exception as e:
    if "index out of" in str(e):
        # print()
        print("\n--------------------------------------------------------\n▷ example1: python icon_hash.py login_logo.gif\n--------------------------------------------------------\n▷ example2: python icon_hash.py http://www.baidu.com/favicon.ico\n--------------------------------------------------------")
    else:
        print(str(e))
