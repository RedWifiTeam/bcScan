# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     scan
   Description :
   Author :       CoolCat
   date：          2019/3/14
-------------------------------------------------
   Change Activity:
                   2019/3/14:
-------------------------------------------------
"""

# coding=utf-8

import re
import requests
from selenium import webdriver
import time
import os
import socket

global info

try:
    os.system("mkdir reports")
    os.system("mkdir images")
except:
    pass
htmlHeader = """
<title>网站扫描报告</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
<style>
.reports{
width:800px;
height:600px;
display:flex;
justify-content:center;
}

.reports img{
    width:100%;
    height:auto;
}
</style>
"""



reportFile = str(time.strftime("%Y-%m-%d")) + ".html"

if not os.path.exists("./reports/" + reportFile):
    f = open("./reports/" + reportFile, "w")
    f.write(htmlHeader)
    f.close()

def getIP(domain):
    myaddr = socket.getaddrinfo(domain, 'http')
    return str(myaddr[0][4][0])

def getInfo(res):
    try:
        Server = res.headers["Server"]
    except:
        Server = None
        pass
    try:
        code = res.headers["X-Powered-By"]
    except:
        code = None
        pass
    return "Server:" + str(Server) + "\tCode:" + str(code)

def scanurl(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    res = requests.get(url=url, headers=headers, timeout=1)
    return res

def urlformat(site):

    site = site.replace("\"", "").replace("\n", "")
    if "http" in site:
        return site
    elif site.strip():
        return "http://" + site + "/"
    else:
        pass

def outPut(target,title,imageName):
    ip = getIP(str(re.compile('http://(.*?)/').findall(target)[0]))
    f = open("./reports/" + reportFile,"a")
    f.write('<h1>URL:<a href="' + target +'" target="_blank">' + target +'</a></h1>\n')
    f.write('<h3>ip:' + str(ip) + '</h3>')
    f.write('<h3>TITLE:' + str(title) +'</h3><h4>' + str(info) +'</h4>')
    f.write('<div class="reports"><img src="../images/' + imageName +'.png"/></div><hr/>')
    f.close()

def screenshot(target):
    imageName = str(re.compile('http://(.*?)/').findall(target)[0])
    option = webdriver.FirefoxOptions()
    option.set_headless()
    driver = webdriver.Firefox(firefox_options=option)
    driver.get(target)

    try:
        if os.path.exists('./images/' + imageName + '.png'):
            print("screenshot exists")
        else:
            driver.get_screenshot_as_file('./images/' + imageName + '.png')
            print("screenshot success" + "\n")
    except BaseException as msg:
        print(msg)
        pass
    title = driver.title.encode("utf-8")
    driver.quit()
    outPut(target,title,imageName)

if __name__ == '__main__':

    for site in open("sites.txt"):
        site = site.replace("\r", "").replace("\n", "").replace(" ", "")
        if site == "":
            pass
        else:
            url = urlformat(site)
            try:
                res = scanurl(url)
                try:
                    info = getInfo(res)
                except:
                    info = None
                    pass
                try:
                    print("[*]" + str(res.status_code) + "\t" + url)
                    print(info)
                    filename = str(res.status_code) + ".txt"
                except:
                    pass
                try:
                    f = open(filename, "a")
                    f.write(url + "\t\t" + info + "\n")
                    f.close()
                except:
                    pass
                if res.status_code == 200:
                    try:
                        screenshot(url)
                    except:
                        pass
            except:
                pass

