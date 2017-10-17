#!/usr/bin/python3
import bs4,re,requests
from bs4 import BeautifulSoup
import time
import pymysql
cnt = 0
def findResult(num):
    #修改头部信息
    payload= {'tag': 0, 'starttime': '2017/1/1', 'startendtime': '2017/12/31','page':num}
    header = {"X-Requested-With":"XMLHttpRequest","User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3368.400 QQBrowser/9.6.11860.400"
}
    #发送post请求
    r = requests.post('http://www.eshow365.com/ZhanHui/Ajax/AjaxSearcherV3.aspx',headers =header ,data = payload)
    r.encoding = r.apparent_encoding
    
    #找到待解析字段
    starIndex = r.text.find('<div class="sslist">')
    endIndex = r.text.find('<div class="searchpage" id="strpageendg" >')
    newStr = r.text[starIndex:endIndex]
    #煲一锅汤
    soup = BeautifulSoup(newStr , "html.parser")

    listData = soup('div' ,class_='sslist')
    webSite='http://www.eshow365.com'
    result=''
    global cnt
    

    for Data in listData:
        title = Data.find(class_='zhtitle').find('a').string.strip().replace('\n','')
        url = webSite + Data.find(class_='zhtitle').find('a').get('href')
        category = Data.find(class_='zhtitle').contents[0].string.strip().replace("\n","")
        node0 = Data.find(class_='time')
        node1 = node0.next_sibling.next_sibling
        startDate = node0.contents[0].replace('/','-')
        location = node1.contents[0]
        #result = result + "[" + "'" + title + "','" + url + "','" + trade + "','" + city + "','" + date + "'" + "]" + "\n"
        cnt = cnt+1
        #result = title + "," + url + "," + trade + "," + city + "," + date + "\n"
        sql = "insert into eshow_info(Title,Url,Category,Location,startDate) values('%s','%s','%s','%s','%s');" %(title,url,category,location,startDate)
        cursor.execute(sql)
        db.commit()
    return result
'''
def findNum():
    r = requests.get('http://www.eshow365.com/zhanhui/0-0-0-20170101/20171231/')
    r.encoding = r.apparent_encoding
    
    startIndex = r.text.find('<div class="searchpage" id="strpage" >')
    endIndex = r.text.find('<div class="searchpage" id="strpageendg" >')

    newStr = r.text[startIndex:endIndex]

    soup  = BeautifulSoup(newStr,'html.parser')
    pagetiao = soup.find(class_='pagetiao')
    return count
'''    
    
def main():
    startTime = time.clock()
    db = pymysql.connect('localhost','root','3525','learn')
    cursor = db.cursor()
    global cursor,db
    for i in range(1,80):
        findResult(i)
        
    print("共抓取了 " + str(cnt) + " 条数据" + "\n")
    
    endTime = time.clock()
    db.close()
    print("程序耗时"+ str(endTime-startTime) + "秒")

main()
    
    
