# -*- coding:utf-8 -*-
# @Time    : 2018/4/17 14:18
# @File    : zhaifuli_spider.py
import requests
from bs4 import BeautifulSoup
import re
import os
import threading
import time
from multiprocessing import Pool

url = 'http://www.mzitu.com/'
#获取当前工作目录
os.getcwd()
#更改当前工作目录
os.chdir('e:\meinv')
#
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}

class MyThread(threading.Thread):
    def __init__(self,href):
        threading.Thread.__init__(self)
        self.href = href
    def run(self):
        parsers_channer(self.href)

# #解析主页的链接
def parsers_menu(url):
    headers['Referer'] = url
    menu_href = []
    data = requests.get(url,headers = headers).text
    soup = BeautifulSoup(data,'lxml')
    t = soup.find_all('ul',class_='menu')
    for i in t:
        j = i.find_all('a')[1:-1]
        for m in j:
            menu_href.append(m.get('href'))
    mythread(menu_href)

lock = threading.Lock()
def parsers_channer(href):
    lock.acquire()
    t = []
    data = requests.get(href,headers = headers).text
    soup = BeautifulSoup(data, 'lxml')
    t = soup.find_all('div', class_='currentpath')[0].text[11:]
    page_max = soup.find_all('div',class_='nav-links')
    if os.path.exists(t) == False:
        os.makedirs(t)
        os.chdir(os.getcwd()+os.path.sep+t)
        paths = os.getcwd()
        for i in page_max:
            page = (i.find_all('a'))[-2].text
            parsers_href(page,href,paths)
    else:
        print('文件夹已存在...')
    os.chdir('D:\meinv')
    lock.release()

#解析所有页面
def parsers_href(page,href,paths):
    for a in range(2,int(page)+1):
        one_href = str(href)+'page/{}/'.format(a)
        href_list= []
        num_list = []
        data = requests.get(one_href,headers = headers).text
        soup = BeautifulSoup(data,'lxml')
        content = soup.find_all('div',class_ = 'postlist')
        for co in content:
            href_list.append(co.find('a').get('href'))
        for ig in href_list:
            m = re.findall(re.compile(r'http://www.mzitu.com/([0-9]*)'),ig)
            num_list.append(m)
        down_pic(num_list[0], paths)

# 下载图片到本地
def down_pic(num, paths):
    for a in num:
        img_list = []
        title_list = []
        href = 'http://www.mzitu.com/' + a + ''
        print(href)
        headers['Referer'] = href
        data = requests.get(href, headers=headers).text
        soup = BeautifulSoup(data, 'lxml')
        title = soup.find('h2', class_='main-title').text
        content = soup.find_all('div', class_='pagenavi')
        os.chdir(paths)
        con = soup.find_all('div', class_='main-image')
        for m in content:
            page = (m.find_all('a'))[-2].text
            if os.path.exists(title) == False:
                os.makedirs(title)
                os.chdir(os.getcwd() + os.path.sep + title)
                print('开始下载：' + title)
                for pa in range(2, int(page) + 1):
                    hrefs = 'http://www.mzitu.com/' + a + '/' + str(pa)
                    print(hrefs)
                    data = requests.get(hrefs, headers=headers)
                    soup2 = BeautifulSoup(data.text, 'lxml')
                    imr = soup2.find_all('div', class_='main-image')
                    for eic in imr:
                        pic = eic.find('img').get('src')
                        img = requests.get(pic, headers=headers)
                        if img.status_code == 200:
                            with open(os.getcwd() + os.path.sep + pic.split('/')[-1], 'wb') as file:
                                file.write(img.content)
                        else:
                            break
                print('----------------------------------------')
                print(title + "：下载完毕！")
            else:
                print('文件夹已存在...')
            os.chdir(paths)

#多线程执行链接
def mythread(menu_href):
    threads = []
    for href in menu_href:
        thread = MyThread(href)
        thread.start()
        threads.append(thread)
    #time.sleep(2)
    for tr in threads:
        tr.join(2)

def main():
   parsers_menu(url)

if __name__ == '__main__':
     main()