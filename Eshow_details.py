#!/usr/bin/python3
#coding=UTF-8
import requests,re,bs4,pymysql,time
from bs4 import BeautifulSoup
sTime = time.clock()
db1 = pymysql.connect('localhost','root','3525','learn')
db2 = pymysql.connect('localhost','root','3525','learn')

cursor1 = db1.cursor()
cursor2 = db2.cursor()

cursor1.execute("select Url from list;")
#cursor2.execute(
for result in cursor1:
    r=requests.get(cursor1.fetchone()[0])
    r.encoding = r.apparent_encoding

    soup = BeautifulSoup(r.text,'html.parser')
    title=soup.find('h1').string.strip()
    l= soup('div',class_='zhxxcontent')
    a=l[0].contents
    dateTime = a[3].string.strip()[5:]
    if a[5].string :
        hall = a[5].string.strip()[5:].replace('\xa0','')
    else:
        b=a[5].contents
        hall = b[1].string.replace('\xa0','')
    industry = a[7].find('a').string
    city = a[9].string.strip()[5:]
    organizer = a[11].string.strip()[5:]
    area = a[13].string.strip()[5:]
    times = a[15].string[5:]
    cycle = a[17].string[5:]

    zhgkcon= soup('div',class_='zhgkcon')
    s=''
    intr= zhgkcon[0].contents
    for child in intr[1]:
        s= s+child.string
    introduce = s.replace('\n','').replace('\xa0','')

    ran=''
    for child in zhgkcon[1]:
        ran=ran+child.string
    ran = ran.replace('\n','').replace('\xa0','')
    cursor2.execute("insert into details(dateTime,hall,industry,city,\
        organizer,area,times,cycle,introduce,ran) values\
        ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" %(dateTime,hall,industry,\
        city,organizer,area,times,cycle,introduce,ran)
)
    db2.commit()
db1.close()
db2.close()
eTime= time.clock()

print('程序耗时'+str(eTime-sTime)+'秒')
