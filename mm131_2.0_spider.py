# -*- coding:utf-8 -*-
# @Time    : 2018/4/26 9:59
# @File    : mayi.py
import requests
from bs4 import BeautifulSoup
import re
import os
import random
from 图片爬虫.MM131 import ip_test

url = 'http://www.mm131.com/'
target_url = 'http://www.mm131.com/'
path_ip = 'ip.txt'
path_correct_ip = os.getcwd() + os.path.sep + '合法ip.txt'
ip_correct_list = []

# 获取ip的方法
def get_ip():
    ip_test.getip(target_url, path_ip)

# 检查IP地址是否在目标网站上有用的方法
def ip_checks():
    ip_list = ip_test.read(path_ip)
    ip_test.truncatefile(path_correct_ip) #检查合法IP前将其清空
    for ip in ip_list:
        headers = ip_test.getheaders()  # 定制请求头
        proxies = {'http': ip}  # 代理ip
        try:
            response = requests.get(url=target_url, proxies=proxies, headers=headers).status_code
            if response == 200:
                print("正在存储的ip:" + ip)
                with open(path_correct_ip, 'a', encoding='utf-8') as f:
                    f.writelines(ip)
                    f.write('\n')
            else:
                print(ip+"不能用")
        except:
            print(ip + "不能用")

# 下载图片
def parser_page(href,img_href,path_s):
    os.chdir(str(path_s))
    headers = ip_test.getheaders()
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'}
    headers['referer'] = href
    filename = img_href.split('/')[-1]
    proxies = {'http': random.choice(ip_correct_list[0])}
    img = requests.get(img_href, headers=headers,).content
    with open(filename, 'wb') as f:
        f.write(img)

# 获取下载页面
def get_page(href,num,path_s):
    headers = ip_test.getheaders()
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'}
    headers['referer'] = href
    proxies = {'http': random.choice(ip_correct_list[0])}
    response = requests.get(href, headers=headers,proxies = proxies)
    response.encoding = 'gb2312'

    soup = BeautifulSoup(response.text, 'lxml')
    s = soup.find_all('div',class_='content-page')
    n = re.findall(re.compile(r'<span class="page-ch">共([0-9]*)页</span>'),str(s))[0]

    for a in range(1,int(n)+1):
        img_href = 'http://img1.mm131.me/pic/{}/{}.jpg'.format(num,a)
        parser_page(href,img_href,path_s)

# 建立文件夹
def set_page(navname,url):
    pathss = os.getcwd()
    # socket.setdefaulttimeout(3)#设置socket的超时时间
    # time.sleep(3)
    if os.path.exists(navname) == False:
        os.makedirs(navname)
        os.chdir(pathss + os.path.sep + navname)
        pathsss = os.getcwd()
        for urls in url:
            headers = ip_test.getheaders()
            # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'}
            headers['referer'] = urls
            proxies = {'http': random.choice(ip_correct_list[0])}
            # print(proxies)
            response = requests.get(urls, headers = headers,proxies = proxies)
            response.encoding = 'gb2312'

            soup = BeautifulSoup(response.text, 'lxml')
            p = soup.find_all('dl',class_='list-left public-box')
            for f in p:
                s = f.find_all('dd')[:-1]
                for k in s:
                    filename = k.text
                    href = str(k.find('a').get('href'))
                    hrefs = str(k.find('a').get('href')).split('/')[-1]
                    if os.path.exists(filename) ==False:
                        os.makedirs(filename)
                        os.chdir(os.getcwd()+os.path.sep+filename)
                        path_s = os.getcwd()
                        get_page(href,hrefs[0:4],path_s)
                    os.chdir(pathsss)
    os.chdir(pathss)

# 获取各模块详情链接
def get_href(dic):
    for key in dic:
        if key == "性感美女":
            url = []
            for a in range(2,int(dic[key])+1):
                url.append('http://www.mm131.com/xinggan/list_6_{}.html'.format(a))
            set_page(key, url)

        elif key == "清纯美眉":
            url = []
            for a in range(2, int(dic[key]) + 1):
                url.append('http://www.mm131.com/qingchun/list_1_{}.html'.format(a))
            set_page(key, url)

        elif key == "美女校花":
            url = []
            for a in range(2, int(dic[key]) + 1):
                url.append('http://www.mm131.com/xiaohua/list_2_{}.html'.format(a))
            set_page(key, url)

        elif key == "性感车模":
            url = []
            for a in range(2, int(dic[key]) + 1):
                url.append('http://www.mm131.com/chemo/list_3_{}.html'.format(a))
            set_page(key, url)

        elif key == "旗袍美女":
            url = []
            for a in range(2, int(dic[key]) + 1):
                url.append('http://www.mm131.com/qipao/list_4_{}.html'.format(a))
            set_page(key, url)

        else:
            url = []
            for a in range(2, int(dic[key]) + 1):
                url.append('http://www.mm131.com/mingxing/list_5_{}.html'.format(a))
            set_page(key, url)

# 解析主模块
def get_nav(url):
    headers = ip_test.getheaders()
    # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'}
    # print(headers)
    headers['referer'] = url
    proxies = {'http':random.choice(ip_correct_list[0])}
    response = requests.get(url,headers = headers,proxies = proxies)
    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text,'lxml')
    s = soup.find_all('div',class_='nav')
    for i in s:
        m = i.find_all('a')
        k = 0
        page = ['138', '31', '6', '10', '4', '8']
        for j in m[1:]:
            navname = j.get_text()
        #    navhref = re.findall(re.compile(r'<a href="(.*)">'),str(j))[0]
            dic = {}
            key = navname
            value = page[k]
            dic[key] = value
            get_href(dic)
            k = k+1

def main():
    # get_ip()
    # ip_checks() # 设置合法IP
    get_nav(url) # 全局函数开始

if __name__ == '__main__':
    ip_correct_list.append(ip_test.read(path_correct_ip))
    main()

