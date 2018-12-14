# -*- coding:utf-8 -*-
# @Time    : 2018/7/29 13:47
# @File    : zbb_spider.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import multiprocessing as mp
import time,re
import os

count = 1
link = ''

os.getcwd()
#
os.chdir('g:\meinv')

def get_url(url):
    headers = {
        "Upgrade-Insecure-Requests": 1,
        "X-DevTools-Emulate-Network-Conditions-Client-Id": "4EAE80F00C03F36085DD0B585CF70899",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    }

    resp = requests.get(url, headers)
    resp.encoding = "gb2312"

    bs = BeautifulSoup(resp.text,"lxml")
    s = bs.find_all("h2")[0].find_all("a")
    for i in s:
        href = "https://92zfls.com/" + i.get("href")
        print("正在下载",href)
        get_page(href)

def get_page(href):
    global count,link
    i = ''
    p = ''
    q = []
    headers = {
        "if-none-match": "bdb8a7de8125d41:0",
        "upgrade-insecure-requests": 1,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    }
    resp = requests.get(href, headers)
    resp.encoding = "gb2312"
    bs = BeautifulSoup(resp.text, "lxml")
    while count == 1:
        link = re.search(r'(.*)/([0-9]{4}).html',href).group(1)
        count  = count + 1
    s = bs.find_all("div",{"class":"pagination pagination-multi"})[0].find_all("li")
    p = re.search(r"<li class=\"(.*)\"><",str(s[-1])).group(1)
    if p == "next-page":
        h = link + r"/" + re.search(r"<a href=\"(.*)\">", str(s[-1])).group(1)
        get_content(h)
        get_page(h)
    elif p == "active":
        count = 1

def get_content(url):
    headers = {
        "if-none-match": "bdb8a7de8125d41:0",
        "referer": "https://92zfls.com/index.html",
        "upgrade-insecure-requests": 1,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    }

    resp = requests.get(url,headers)
    resp.encoding = "gb2312"

    bs = BeautifulSoup(resp.text,"lxml")
    s = bs.find_all("article",{"class":"article-content"})[0].find_all("p")
    for i in s[1:]:
        img_src = i.img.get("src")
        img = requests.get(img_src,headers).content
        img_name = str(img_src).split("/")[-1]
        print("正在下载",img_name)
        if os.path.exists(img_name) == False:
            print("正在下载",img_name)
            with open(img_name,"wb") as file:
                file.write(img)
        else:
            print(img_name,"已存在")

def main():
    pool = mp.Pool(5)
    for i in range(1,300):
        url = "https://92zfls.com/luyilu/list_5_{}.html".format(i)
        pool.apply_async(get_url,args=(url,))

    pool.close()
    pool.join()

if __name__ == "__main__":
    main()

