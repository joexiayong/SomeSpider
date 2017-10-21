#!/usr/bin/python3
#coding=UTF-8
import requests,re,bs4,pymysql,time
from bs4 import BeautifulSoup
sTime = time.clock()
db1 = pymysql.connect('localhost','root','3525','learn')
db2 = pymysql.connect('localhost','root','3525','learn')

fdb = 0
cnt = 0

cursor1 = db1.cursor()
cursor2 = db2.cursor()

cursor1.execute("select Url from list;")
#cursor2.execute(
for result in cursor1:
    r=requests.get(cursor1.fetchone()[0])
    r.encoding = r.apparent_encoding

    soup = BeautifulSoup(r.text,'html.parser')
    try:
        title=soup.find('h1').string.strip()
    except :
        title=''
        continue
    l= soup('div',class_='zhxxcontent')
    pTag = l[0].find_all('p')
    try:
        dateTime = pTag[2].string.strip()[5:]
    except:
        deteTime =''
        continue
        
    if pTag[3].string :
        hall = pTag[3].string.strip()[5:].replace('\xa0','')
    else:
        hall = pTag[3].find('a').string
    industry = pTag[4].find('a').string
    city = pTag[5].string.strip()[5:]
#    times = [15].string[5:]
#    cycle = a[17].string[5:]

    zhgkcon= soup('div',class_='zhgkcon')
    s=''
    intr= zhgkcon[0].contents
    for child in intr[1]:
        try:
            s= s+child.string
        except:
            continue

    introduce = s.replace('\n','').replace('\xa0','')

    ran=''
    for child in zhgkcon[1]:
        try:
            ran=ran+child.string
        except:
            continue   
        ran = ran.replace('\n','').replace('\xa0','')
    try :
        cursor2.execute("insert into details(title,dateTime,hall,industry,city,\
            introduce,ran) values\
            ('%s','%s','%s','%s','%s','%s','%s');" %(title, dateTime,hall,industry,\
            city,introduce,ran)
    )
    except:
        fdb +=1
        continue
    db2.commit()
    cnt+=1
    print(cnt,':',title)
db1.close()
db2.close()
eTime= time.clock()

print('程序耗时'+str(eTime-sTime)+'秒')
print(fdb)
