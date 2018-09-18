
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import re
import os
import csv


# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# browers = webdriver.Chrome('D:/python/chromedriver.exe',chrome_options = chrome_options)
# waits = WebDriverWait(browers,2)


browers = webdriver.Chrome('D:/python/chromedriver.exe')
browers.maximize_window() 
waits = WebDriverWait(browers,2)
basic_url = 'https://bbs.hupu.com'
listData = []

# local_phantomJS_path = 'C:/Users/6407000963/Desktop/phantomjs-2.1.1-windows/bin/phantomjs.exe'
# browers = webdriver.PhantomJS(local_phantomJS_path)
# waits = WebDriverWait(browers,2)

def main():
    # i = 1
    # while True:
    #     url = 'https://bbs.hupu.com/4846-%s' %(i)
    #     data = get_one(url)
    #     if not data:
    #         break
    #     parse_one(data,i)
    #     i += 1
    
    # writeToCSV(listData)
    getFromCSV()
    get_url_data()

def get_one(url):
    print('正在爬取...',url)
    try:
        browers.get(url)
        # browers.set_page_load_timeout(10)
        data = browers.find_element_by_class_name('for-list').find_elements_by_tag_name('li')
        # html = browers.page_source
        if data:
            # print('-------------',html)
            return data
    except Exception as e:
        print(e)
        return None


def parse_one(data,page):
    
    for index in range(len(data)):
        item = data[index]
        title_item = item.find_element_by_class_name('titlelink').find_element_by_class_name('truetit')
        title = title_item.text
        href = title_item.get_attribute("href")
        try:
            author_item = item.find_element_by_class_name('author').find_elements_by_tag_name('a')
            author = author_item[0].text
            create_date = author_item[1].text
        except Exception as e:
            print(e)
       
        print(title,href)
        listData.append([str(page)+'.'+str(index),title,href,author,create_date])

        
   


def writeToCSV(listData):
    headers = ['id','title','href','author','createDate']

    with open('hupu.csv','a') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(listData)


def getFromCSV():
    with open("hupu.csv", "r") as csvfile:
        reader2 = csv.reader(csvfile) # 读取csv文件，返回的是迭代类型
        for item2 in reader2:
            if item2:
                listData.append(item2)
        csvfile.close()

def get_url_data():
    listData.remove(listData[0])
    listData.remove(listData[0])
    for index in range(len(listData)):
       item = listData[index]
       title = item[1]
       url = item[2]
       get_detail_page(url,title)


def get_detail_page(url,title):
    try:
        browers.get(url)
        images = browers.find_element_by_class_name('quote-content')
        srcs = images.find_elements_by_tag_name('img')
        print(srcs[0].get_attribute('src'))
        for index in range(len(srcs)):
            imageUrl = srcs[index].get_attribute('src')
            if '?' in imageUrl:
                imageUrl = imageUrl[0:imageUrl.index('?')]
            write_to_file(imageUrl,title,index)
    except Exception as e:
        print(e)
        # browers.execute('window.close()')


def write_to_file(url,title,count):
    dirName = './picture/hupu/{0}/'.format(title)
    if not os.path.exists(dirName):
        os.makedirs(dirName)

    fileExname = url.split(".")[-1]
    fileName = '%s/%s/%s.%s' % (os.path.abspath('.'),dirName,count,fileExname)
    print(fileName)
    with open(fileName,'wb+') as jpg:
        jpg.write(requests.get(url).content)


def pares_one_of_num(html):
    soup = BeautifulSoup(html,'lxml')
    imgs = soup.select('img')
    currentPage = soup.select('#body #comments .comments .cp-pagenavi span')[0].text
    url = soup.select('#body #comments .comments .cp-pagenavi a')[-1]
    href = re.findall('href="(.*?)"',str(url))
    # percent_num = percent[0]+'.'+percent[1]
    next_url = 'https:'+href[0]
    print('next_url---------->',next_url)

    count  =0
    for img in imgs:
        img_url = re.findall('src="(.*?)"',str(img))
        if not img_url[0][-3:] == 'gif':
            if not img_url[0][-3:] == 'png':
                if img_url[0][-3:]:
                    print('正在下载：%s第%s张' % (img_url[0],count))
                    write_to_file(img_url[0],currentPage,count)
        count += 1

    return currentPage,next_url


main()




