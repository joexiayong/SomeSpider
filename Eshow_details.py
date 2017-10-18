#!/usr/bin/python3
import requests,re,bs4
from bs4 import BeautifulSoup

r = requests.get('http://www.eshow365.com/zhanhui/html/124073_0.html')

r.encoding = r.apparent_encoding


soup = BeautifulSoup(r.text,'html.parser')
title=soup.find('h1').string.strip()
l= soup('div',class_='zhxxcontent')
a=l[0].contents
date = a[3].string[5:]
hall = a[5].string[5:]
industry = a[7].find('a').string
city = a[9].string[5:]
organizer = a[11].string.strip()[5:]
area = a[15].string.strip()[5:]
times = a[17].string[5:]
cycle = a[19].string[5:]

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


print(date,hall,industry,city,organizer,area,times,cycle,introduce,ran)

