from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error #指定url，获取网页数据

import pymysql.cursors
# 连接数据库
connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123',
    db='spider',
    charset='utf8'
)
cursor = connect.cursor()
# 插入到 爬虫库的分类表
def insert_category(first_level,second_level,third_level):
    try:
        sql="insert into category(first_level,second_level,third_level) values ('%s','%s','%s')"
        data = (first_level,second_level,third_level)
        cursor.execute(sql % data)
        connect.commit()
        print('成功插入', cursor.rowcount, '条数据')

    except Exception:
        print("插入失败")




# 获取数据
def getData():
    head={
        "User-Agent":"Mozilla / 5.0(Macintosh;Intel Mac OS X 10.16;rv: 86.0) Gecko / 20100101 Firefox / 86.0"
    }
    url="https://list.suning.com/?safp=d488778a.homepagev8.126605238626.1&safpn=10001"

    request=urllib.request.Request(url,headers=head)
    html=""
    try:
        response=urllib.request.urlopen(request)
        html=response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reson"):
            print(e.reason)

    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div',id=re.compile('\d+')):
        item1=str(item)
        first_level=re.findall(re.compile('<h2>(.*)</h2>'),item1)[0]
        third_level=''
        for item2 in item.find_all(attrs={'class':'t-left fl clearfix'}):
            if item2=='\n':
                continue
            second_level=item2.find('a').text
            for item3 in item2.next_siblings:
                if item3 == '\n':
                    continue
                # 可能有三级分类为空的情况，直接保存
                if item3.find('a')==None:
                    insert_category(first_level, second_level, third_level)
                else:
                    for item4 in item3:
                        if item4 == '\n':
                            continue
                        third_level=item4.text

                        insert_category(first_level,second_level,third_level)

getData()