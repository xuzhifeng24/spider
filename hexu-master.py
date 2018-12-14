import requests
import re
import pymysql
from urllib.parse import urlencode

config = {
        "port": 3306,
        "user": "root",
        "password": "123456",
        "charset": "utf8",
        "host": "localhost",
        "db": "hexun"
    }
conn = pymysql.connect(**config)

def get_data():
    date_list = ["{0}-12-31".format(i) for i in range(2010, 2018)]
    page_list = [120, 133, 143, 157, 176, 179, 178, 178]
    info = [{'date': date_list[i], 'page':page_list[i]} for i in range(len(page_list))]
    for j in range(len(page_list)):
        db = str(info[j]['date']).replace('-', '_')
        cursor = conn.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS {0}(id int PRIMARY KEY NOT NULL auto_increment,
            industry VARCHAR(20),
            industryrate VARCHAR(20),
            Pricelimit VARCHAR(20),
            stockNumber VARCHAR(20),
            lootingchips VARCHAR(20),
            Scramble VARCHAR(20),
            rscramble VARCHAR(20),
            Strongstock VARCHAR(20))""".format(db)
        cursor.execute(sql)
        for p in range(1, int(info[j]['page']) + 1):
            data = {
                "date": info[j]['date'],
                "count":"20",
                "pname": "20",
                "titType": "null",
                "page": p,
                "callback": "hxbase_json11538378403020"
            }
            url = "http://stockdata.stock.hexun.com/zrbg/data/zrbList.aspx?" + urlencode(data)
            parse_html(url, db)
        print(db, "的数据库抓取完毕...")
        cursor.close()

def parse_html(url,db):
     headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "__jsluid=02654ede7079a57cacbbe01de0669726",
        "Host": "stockdata.stock.hexun.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3",
        }
     response = requests.get(url,headers=headers).text
     c = response.split(',{')
     for i in c:
         industry = re.search(r',industry:\'(.*)\',stockNumber',i).group(1) # 股票名称/代码
         industryrate = re.search(r',industryrate:\'(.*)\',Pricelimit', i).group(1) # 总得分
         Pricelimit = re.search(r',Pricelimit:\'(.*)\',lootingchips', i).group(1) # 等级
         stockNumber = re.search(r',stockNumber:\'(.*)\',industryrate', i).group(1) # 股东责任
         lootingchips = re.search(r',lootingchips:\'(.*)\',Scramble', i).group(1) # 员工责任
         Scramble = re.search(r',Scramble:\'(.*)\',rscramble', i).group(1)  # 供应商、客户和消费者权益责任
         rscramble = re.search(r',rscramble:\'(.*)\',Strongstock', i).group(1)  # 环境责任
         Strongstock = re.search(r',Strongstock:\'(.*)\',Hstock', i).group(1)  # 社会责任
        # print(industry, industryrate, Pricelimit, stockNumber, lootingchips, Scramble, rscramble, Strongstock)
         with conn.cursor() as cursor:
             sql = "insert into {0}(industry,industryrate,Pricelimit,stockNumber,lootingchips,Scramble,rscramble,Strongstock) values (%s,%s,%s,%s,%s,%s,%s,%s)".format(db)
             cursor.execute(sql, (industry,industryrate,Pricelimit,stockNumber,lootingchips,Scramble,rscramble,Strongstock))
         conn.commit()
         cursor.close()

def main():
    get_data()

if __name__ == "__main__":
    main()