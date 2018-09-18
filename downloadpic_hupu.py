import urllib
from urllib import request
import re
import os
import sqlite3

totalPages = -1
# 根据url获取网页html内容
def getHtmlContent(url):
    # request = urllib.request.Request(url)
    page = urllib.request.urlopen(url)
    return page.read().decode('utf-8', errors='ignore')

# 从html中解析出所有jpg图片的url
# 百度贴吧html中jpg图片格式为<img ... src='xxx.jpg' width..>
def getJPGS(html):
    # 解析jpg图片地址的正则表达式
    jpgReg = re.compile(r'<img src="(.+?,webp)" data-w')
    # 解析出jpg的url列表
    jpgs = re.findall(jpgReg,html)
    # 解析出gif的url列表
    jpgReg = re.compile(r'<img src="(.+?.gif)" .+?/>')
    gifList=re.findall(jpgReg,html)
    jpgs.extend(gifList)
    # 解析出gif的url列表
    jpgReg = re.compile(r'data-original="(.+?,webp)" data-w')
    jepgList = re.findall(jpgReg,html)
    jpgs.extend(jepgList)
    print(jpgs)


    urls= []
    for url in jpgs:
        if not url:
            continue
        # if url.rfind('placeholder')>0:
        #     continue
        if url.rfind('data-original')>0:
            url = url.split(' ')[1]
            print(url)
            imageurl = url[url.rfind('"')+1:]
            # imageurl = url[:url.rfind(' data-original')][:-1]
            urls.append(imageurl)
        else:
            urls.append(url)
    imagesUrl = set(urls)
    print('无重复图片地址-------------',imagesUrl)
    return imagesUrl

# 用图片url下载图片并保存成指定文件名
def downloadJPG(imgUrl,fileName):
    urllib.request.urlretrieve(imgUrl,fileName)

# 批量下载图片，默认保存到当前目录下
# path='./picture/hupu/'
def batchDownloadJPG(imgUrl,item,page,title):
    path = './picture/hupu/{0}/'.format(title)
    createDir(path)
    count = 1
    
    for url in imgUrl:
        try:
            if not url:
                continue
            if url.rfind('?')>0:
                iamgeSource = url[:url.rfind('?')]
                fileExname = url[url.rfind('.'):url.rfind('?')]
            else:
                iamgeSource = url
                fileExname = url[-4:]
            downloadJPG(iamgeSource,''.join([path,str(item)+'-'+str(page)+'-'+'{0}{1}'.format(count,fileExname)]))
        except Exception as e:
            print(e)   
            # downloadJPG()
        finally:
            count += 1

def createDir(path):
    isExists=os.path.exists(path)
     # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        #创建目录操作函数
        os.makedirs(path) 
        print(path,'创建成功')
        # return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path,'目录已存在')
        # return False

# 从百度贴吧下载图片
def download(url,item,title,page):
    try:
        html = getHtmlContent(url)
        jpgs = getJPGS(html)
        getTotalPages(title,html)
        batchDownloadJPG(jpgs,item,page,title)
    except Exception as e:
        print('出错链接：',e.url)

def getTotalPages(title,html):
    global totalPages
    if totalPages<0:
        pageCompile = r'maxpage:(\d*)'
        pages = re.findall(pageCompile,html)
        totalPages = int(pages[0])
        print(title,'------------------>总页数',totalPages)



def main(id,title):
    # url = 'http://tieba.baidu.com/p/2256306796'
    con = sqlite3.connect('./databases/hupu.db')
    cur = con.cursor()
    page = -2
    # item = '2256306796'
    # item = '4803144798'
    # global totalPages
    pageInfo = cur.execute('select * from pageinfo where id={0}'.format(id)).fetchone()
    if pageInfo:
        page=pageInfo[2]
        global totalPage
        totalPage=pageInfo[1]

    while page<totalPages:
        try:
            if page <0:
                page = 1
            url = 'https://bbs.hupu.com/{0}-{1}.html'.format(id,page)
            print('------------------>',url)

            savePageinfoToDB(cur,id,totalPages,page)
            con.commit()

            download(url,id,title,page)
            page += 1
        except Exception as e:
            print(e)
        finally:
            cur.close()
            con.close()
    
    if __name__ == '__main__':
        main()

def savePageinfoToDB(cur,id,totalpage,currentpage):

    one = [id,totalpage,currentpage]
    try:
        cur.execute('insert into pageinfo values (?,?,?)',one)
        # print(str(data['id'])+' : success')
    except Exception as e:
        print(e)

# main()

# page = 9
# count = 8
# path='../picture/tieba/'
# item='4803144798'
# ''.join([path,item+'-'+str(page)+'-'+'{0}.jpg'.format(count)])
