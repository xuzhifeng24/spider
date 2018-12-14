# -*- coding:utf-8 -*-
# @Time    : 2018/4/28 11:55
# @File    : test_01.py
import requests
from bs4 import BeautifulSoup
import re
from requests.exceptions import ConnectionError
import threading
import os
import time

url = 'http://www.mm131.com/xinggan/'

# proxypool_url = 'http://127.0.0.1:5000/get'
# ip_address = requests.get(proxypool_url).text
# proxies = {'http':ip_address}


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
headers['referer'] =url

local_path = r'E:\pictrue'

# def check_ip(proxies):
#     response = requests.get(url, headers=headers, proxies=proxies)
#     if response.status_code == 200:
#         print(response.status_code)
#     else:
#         proxypool_url = 'http://127.0.0.1:5000/get'
#         ip_address = requests.get(proxypool_url).text
#         proxies = {'http': ip_address}
#         check_ip(proxies)


def get_html(url,path):
    num = url.split('/')[-2]
    paths = path
    try:
        imgname = num+url.split('/')[-1]
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            with open(path+'/'+imgname,'wb') as f:
                f.write(response.content)
        if response.status_code ==302:
            return 303
    except ConnectionError:
        return get_html(url,paths)

def get_index(number):
    try:
        lock.acquire()
        print("开始下载第：" + str(number) + "页")
        href = 'http://www.mm131.com/xinggan/list_6_{}.html'.format(number)
        response = requests.get(href,headers = headers)
        response.encoding = 'gb2312'
        soup = BeautifulSoup(response.text,'lxml')
        h = soup.find('dl').find_all('dd')
        for i in h[:-1]:
            url = i.find('a').get('href')
            num = re.findall(re.compile(r'([0-9]*).html'),str(url).split('/')[-1])
            filename = re.findall(re.compile(r'<img alt="(.*)" height'),str(i))[0]
            os.chdir(r'E:\pictrue')
            if os.path.exists(filename) == False:
                os.makedirs(filename)
                os.chdir(os.getcwd()+os.path.sep+filename)
                path = os.getcwd()
                data = requests.get(url,headers = headers)
                data.encoding = 'gb2312'
                soup = BeautifulSoup(data.text,'lxml')
                p = soup.find_all('div',class_='content-page')
                page = re.findall(re.compile(r'<span class="page-ch">共([0-9]*)页</span><span'),str(p))[0]
                for j in range(1,int(page)+1):
                    img_href = 'http://img1.mm131.me/pic/{}/{}.jpg'.format(num[0],j)
                    print("下载"+img_href+"的图片")
                    get_html(img_href,path)
                    print(img_href + "的图片下载完成！")
            print(str(number) + "页"+"下载完成！")
            os.chdir(r'E:\pictrue')
    finally:
        lock.release()

if __name__ == '__main__':
    threads = []
    lock = threading.Lock()
    for a in range(2, 139):
        thread = threading.Thread(target=get_index, args=(str(a),))
        thread.start()
        threads.append(thread)

    for s in threads:
        s.join()
