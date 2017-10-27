 # -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 11:11:45 2017

@author: Xavier
"""

import requests ,bs4 ,re ,pymysql
from bs4 import BeautifulSoup

global headers
global getErrorCnt
getErrorCnt=0
headers ={'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
              AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 \
              Safari/537.36 Core/1.53.3368.400 QQBrowser/9.6.11860.400'}

def getText(m,n):
    url="http://www.cnena.com/showroom/list_time.php"
    
    urlocation={'daytime' : m,'page' : n}
     
    try:
        r = requests.get(url,headers=headers,params = urlocation)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        
        return r.text
    except:
        #doSomeThing
        getErrorCnt +=1

def cutText(pageText) :
    startIndex=pageText.find('<!-- Table goes in the document BODY -->')
    endIndex = pageText.find('<div class="page">')
    newStr = pageText[startIndex:endIndex]
    return newStr

def connectSql()
    db=pymysql.connect('localhost', 'root', '3525', 'cnena')
    cursor = db.cursor()
    return cursor

def insertIntosql(cursor,title,startTime,endTime,location,NOP)
    sql = "INSERT INTO index(title,startTime,endTime,location,NOP) \
    valves('%s','%s','%s','%s','%s');" % (title,startTime,endTime,location,NOP)
    cursor.execute(sql)
    db.commit()

patList=[]
patList.append(re.compile('''target="_blank" title=\'(.*?)\' '''))
patList.append(re.compile('22%"><center>(.*?)&nbsp;'))
patList.append(re.compile('至&nbsp;(.*?)</center>'))
patList.append(re.compile('title="(.*?)展会信息"'))
patList.append(re.compile('<td width="12%">(.*?)人围'))

cnt=0
cursor = connectSql()
for m in range(1,13):
    soup = BeautifulSoup(getText(m,1) ,'html.parser')
    maxM = int(soup('a',title= '尾页')[0].get('href')[-2:])
    for n in range(1,maxM+1):
        targetText = cutText(getText(m,n))
        infoList=[]
        for regex in patList:
            infoList.append(regex.findall(targetText))
        for i in range(len(infoList[0])):
            insertIntosql(cursor,infoList[0][i],infoList[1][i],infoList[2][i]), \
            infoList[3][i],infoList[4][i])

            cnt+=1
            print(cnt)
db.close

'''
        titleList = re.findall(, targetText)
        startTimeList = re.findall( , targetText)
        endTimeList = re.findall(,targetText)
        locationList = re.findall(,targetText)
'''