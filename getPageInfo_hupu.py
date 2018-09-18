import urllib
import urllib.request
import sqlite3
import re
import sys
sys.path
sys.path.append('D:\python\workspace\hupu')
import downloadpic
from downloadpic import main


# sys.path.remove('./../hupu/')

totalPage = -1

def getPageMsg(url):
    req = urllib.request.Request(url)
    page = urllib.request.urlopen(req)
    return page.read().decode('utf-8',errors='ignore')

def getTotalPages(html):
    compiless=r'maxpage:(\d*)'
    reg = re.compile(compiless)
    results = re.findall(reg,html)
    global totalPage
    totalPage = int(results[0])

def getTileAndUrl(html):
    datas={}
    
    compiless='<a  href="/\d*.html".+?>\w*.+?</a>'
    reg = re.compile(compiless)
    results = re.findall(reg,html)
    print(results)
    for result in results:
        # print(result)
        data = {}
        result = result[2:][:-4].strip()
        # result.
        print(result)
        title = result[result.rfind('>')+1:]
        print(title)
        ss=result.split(' ')
        url = ss[0]
        print(url)
        imageUrl = url[url.rfind('/')+1:-1]
        print(imageUrl)
        id = imageUrl[:imageUrl.rfind('.')]
        print(id)
        print('id=',id)
        data['title'] = title
        data['url'] = 'https://bbs.hupu.com/'+imageUrl
        data['id']=id
        datas[data['id']] = data
    return datas

def main():
    try:
        con = sqlite3.connect('./databases/hupu.db')
        cur = con.cursor()
        createDb(cur)
        page = -2
        pageInfo = cur.execute('select * from pageinfo where id={0}'.format('4846')).fetchone()
        if pageInfo:
            page=pageInfo[2]
            global totalPage
            totalPage=pageInfo[1]
        while page<totalPage:
            if page<0:
                page = 1
            url = 'https://bbs.hupu.com/4846-{0}'.format(page)
            html = getPageMsg(url)
            getTotalPages(html)
            print(html)
            datas = getTileAndUrl(html)
            print(datas)

            
            for index in datas:
                saveDataToDB(cur,datas[index])
            
            savePageinfoToDB(cur,'4846',totalPage,page) 
            con.commit()

            results = cur.execute('select * from hupu').fetchall()
            for index in results:
                downloadpic.main(index[0],index[1])
            
            page += 1
        
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
    
def createDb(cur):
    try:
        sql = 'create table if not exists hupu (id integer primary key,title varchar(100),url varchar(50))'
        cur.execute(sql)
        sql = 'create table if not exists pageinfo (id integer primary key,totalpage integer,currentpage integer)'
        cur.execute(sql)
    except Exception as e:
        print(e)

def saveDataToDB(cur,data):

    one = [data['id'],data['title'],data['url']]
    try:
        cur.execute('insert into hupu values (?,?,?)',one)
        print(str(data['id'])+' : success')
    except Exception as e:
        print(e)

def savePageinfoToDB(cur,id,totalpage,currentpage):

    one = [id,totalpage,currentpage]
    try:
        cur.execute('insert into pageinfo values (?,?,?)',one)
        # print(str(data['id'])+' : success')
    except Exception as e:
        print(e)


    

main()
