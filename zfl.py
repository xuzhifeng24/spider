# -*- coding: utf-8 -*-
# @Time    : 2018/10/27 13:30
# @Author  : xuzhifeng
# @File    : zfl.py
import re
import time,os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.parse import quote
from urllib.parse import urljoin
import multiprocessing as mp
import threading as td

count = 1
link = ''

os.getcwd()
#
os.chdir('g:\meinv')

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
}

def input_keyword():
    keyword = ['PR','完具少女','傲娇','推女郎','极品','美乳','无圣光','美模','无忌影社','柚木','露出','元气小奈音']
    pool = mp.Pool(12)
    for i in keyword:
        pool.apply_async(get_url, args=(i,))
    pool.close()
    pool.join()

def get_url(data):
    if os.path.exists(data) is False:
        os.makedirs(data)
        os.chdir(os.getcwd() + os.path.sep + data)
        paths = os.getcwd()
        data = {
            "keyword":data,

        }
        url = "https://sozfl.com/serch.php?"+urlencode(data,encoding='gb2312')
        resp = requests.get(url,headers=headers)
        resp.encoding = "gb2312"
        bs = BeautifulSoup(resp.text,"lxml")
        page = str(bs.find_all('li',class_='active')[0].find('span').text).split('/')[-1]
        # for i in range(1, int(page)+1):
        #     html = url + "&page={}".format(i)
        #     parse_page(html,paths)
        threads = []
        for i in range(1, int(page)+1):
            html = url + "&page={}".format(i)
            thread = td.Thread(target=parse_page, args=(html,paths))
            thread.start()
            threads.append(thread)

            # time.sleep(2)
            for tr in threads:
                tr.join()
    else:
        print('文件夹已存在...')

    os.chdir('g:\meinv')

def parse_page(html,paths):
    try:
        resp = requests.get(html , headers=headers)
        resp.encoding = "gb2312"
        bs = BeautifulSoup(resp.text, "lxml")
        s = bs.find_all("h2")
        threads = []
        hrefs = []
        for i in s:
            href = i.find('a').get('href')
            print("正在下载",href)
            # get_page(href, paths)
            hrefs.append(href)

        for url in hrefs:
            thread = td.Thread(target=get_page,args=(url,paths))
            thread.start()
            threads.append(thread)
            # time.sleep(2)
            for tr in threads:
                tr.join()
    except:
        pass

def get_page(href, paths):
    global count,link
    i = ''
    p = ''
    q = []
    # headers = {
    #     "if-none-match": "bdb8a7de8125d41:0",
    #     "upgrade-insecure-requests": 1,
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    # }
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
        get_content(h,paths)
        get_page(h,paths)
    elif p == "active":
        count = 1

def get_content(url,paths):
    try:
        resp = requests.get(url,headers)
        resp.encoding = "gb2312"

        bs = BeautifulSoup(resp.text,"lxml")
        s = bs.find_all("article",{"class":"article-content"})[0].find_all("p")
        for i in s[1:]:
            img_src = i.img.get("src")
            os.chdir(paths)
            img = requests.get(img_src,headers).content
            img_name = str(img_src).split("/")[-1]
            if os.path.exists(img_name) == False:
                print("正在下载",img_name)
                with open(img_name,"wb") as file:
                    file.write(img)
            else:
                print(img_name, "已存在")
            os.chdir(paths)
    except:
        pass

def main():
    input_keyword()

if __name__ == "__main__":
    main()

