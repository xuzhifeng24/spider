# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 14:56
# @Author  : xuzhifeng
# @File    : start_nba_spider.py
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests
import pymysql

def get_conn():
    config = {
        "host":"localhost",
        "user":"root",
        "password":"123456",
        "port":3306,
        "db":"nba_db",
        "charset":"utf8"
    }
    conn = pymysql.connect(**config)
    return conn

def get_html():
    # for i in range(2007,2017):
    #     data2 = {
    #         "QueryType":"ss",
    #         "SsType":"season",
    #         "Formular":"result_out_wdivideleftbracketresult_out_waddresult_out_lrightbracketmultiply100",
    #         "PageNum":30,
    #         "Season0":i,
    #         "Season1":i+1,
    #         "crtcol":"formular",
    #         "order":1
    #     }
    #     url = "http://www.stat-nba.com/query_team.php?" + urlencode(data2)
    #     get_resp(url,i+1)
    data2 = {
        "QueryType": "ss",
        "SsType": "season",
        "Formular": "result_out_wdivideleftbracketresult_out_waddresult_out_lrightbracketmultiply100",
        "PageNum": 30,
        "Season0": 2017,
        "Season1": 2018,
        "crtcol": "formular",
        "order": 1
    }
    url = "http://www.stat-nba.com/query_team.php?" + urlencode(data2)
    return url
    # data1 = {
    #     "page": 13,
    #     "QueryType": "ss",
    #     "SsType": "season",
    #     "Isnba": 1,
    #     "AT": "avg",
    #     "crtcol": "pts",
    #     "order": 1,
    #     "Season0": 2007,
    #     "Season1": 2008,
    #     "G0": 57
    # }
    #url = "http://www.stat-nba.com/query.php?" + urlencode(data1)


def get_resp():
    url =get_html()
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    resp = requests.get(url=url,headers=headers)
    resp.encoding = 'utf-8'
    try:
        if resp.status_code == 200:
            parser_html(resp.text)
        else:
            print("Request hava exception")
    except RequestException as e:
        print(e)

def parser_html(response):
    x = -1
    bs = BeautifulSoup(response,'lxml')
    f = bs.find_all("table",class_='stat_box')
    for i in f:
        s = i.find_all('tr')
        for j in s[1:]:
            x += 1
            team = j.find('td',class_='normal tm_out change_color col1 row{}'.format(x)).text # 赛季两分投篮命中率
            sjtl_2 = str(j.find('td',class_='normal fgper change_color col3 row{}'.format(x)).text).strip('%') # 赛季两分投篮命中率
            sjmz_2 = j.find('td', class_='normal fg change_color col4 row{}'.format(x)).text  # 赛季两分命中数
            sjcs_2 = j.find('td', class_='normal fga change_color col5 row{}'.format(x)).text  # 赛季两分出手数
            sjsf_3 = str(j.find('td', class_='normal threepper change_color col6 row{}'.format(x)).text).strip('%')  # 赛季三分命中率
            sjmz_3 = j.find('td', class_='normal threep change_color col7 row{}'.format(x)).text # 赛季三分命中数
            sjcs_3 = j.find('td', class_='normal threepa change_color col8 row{}'.format(x)).text  # 赛季三分出手数
            fq = str(j.find('td', class_='normal ftper change_color col9 row{}'.format(x)).text).strip('%') # 罚球命中率
            fq_mz = j.find('td', class_='normal ft change_color col10 row{}'.format(x)).text  # 罚球命中数
            fq_cs = j.find('td', class_='normal fta change_color col11 row{}'.format(x)).text  # 罚球出手数
            lb = j.find('td', class_='normal trb change_color col12 row{}'.format(x)).text  # 篮板个数
            lb_qc = j.find('td', class_='normal orb change_color col13 row{}'.format(x)).text  # 前场篮板数
            lb_hc = j.find('td', class_='normal drb change_color col14 row{}'.format(x)).text  # 后场篮板数
            zg = j.find('td', class_='normal ast change_color col15 row{}'.format(x)).text  # 助攻个数
            qd = j.find('td', class_='normal stl change_color col16 row{}'.format(x)).text  # 抢断个数
            gm = j.find('td', class_='normal blk change_color col17 row{}'.format(x)).text  # 盖帽个数
            sw = j.find('td', class_='normal tov change_color col18 row{}'.format(x)).text  # 失误次数
            fg = j.find('td', class_='normal pf change_color col19 row{}'.format(x)).text  # 犯规次数
            score = j.find('td', class_='normal pts change_color col20 row{}'.format(x)).text  # 场均得分
            lost_score = j.find('td', class_='normal scoreo change_color col21 row{}'.format(x)).text  # 场均失分
            victory = j.find('td', class_='normal result_out_l change_color col23 row{}'.format(x)).text  # 胜场数
            defeat = j.find('td', class_='normal result_out_l change_color col23 row{}'.format(x)).text  # 负场数

            conn = get_conn()
            with conn.cursor() as cursor:
                sql = 'insert into team_2018(team,sjtl_2,sjmz_2,sjcs_2,sjsf_3,sjmz_3,sjcs_3,fq,fq_mz,fq_cs,lb,lb_qc,lb_hc,zg,qd,gm,sw,fg,score,lost_score,victory,defeat) ' \
                      'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                print("正在存储：",team,sjtl_2,sjmz_2,sjcs_2,sjsf_3,sjmz_3,sjcs_3,fq,fq_mz,fq_cs,lb,lb_qc,lb_hc,zg,
                  qd,gm,sw,fg,score,lost_score,victory,defeat)
                cursor.execute(sql,(team,sjtl_2,sjmz_2,sjcs_2,sjsf_3,sjmz_3,sjcs_3,fq,fq_mz,fq_cs,lb,lb_qc,lb_hc,zg,
                  qd,gm,sw,fg,score,lost_score,victory,defeat))
            conn.commit()
            print("存储完毕！")
            cursor.close()

if __name__ == "__main__":
    get_resp()
