import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import re
import os


# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# browers = webdriver.Chrome('D:/python/chromedriver.exe',chrome_options = chrome_options)
# waits = WebDriverWait(browers,2)


browers = webdriver.Chrome('D:/python/chromedriver.exe')
browers.maximize_window() 
waits = WebDriverWait(browers,2)


# local_phantomJS_path = 'C:/Users/6407000963/Desktop/phantomjs-2.1.1-windows/bin/phantomjs.exe'
# browers = webdriver.PhantomJS(local_phantomJS_path)
# waits = WebDriverWait(browers,2)

def main():
    url = 'https://jandan.net/ooxx/'
    html = get_one(url)
    next_url = parse_one(html)
    next(next_url)
    # if __name__ == '__main__':
    #     main()


def get_one(url):
    print('正在爬取...')
    try:
        browers.get(url)
        # browers.set_page_load_timeout(10)
        html = browers.page_source
        if html:
            # print('-------------',html)
            return html
    except Exception as e:
        print(e)
        return None


def parse_one(html):
    soup = BeautifulSoup(html,'lxml')
    imgs = soup.select('img')
    currentPage = soup.select('#body #comments .comments .cp-pagenavi span')[0].text
    url = soup.select('#body #comments .comments .cp-pagenavi a')[-1]
    href = re.findall('href="(.*?)"',str(url))
    next_url = 'https:'+href[0]
    print('next_url---------->',next_url)

    count = 0
    for img in imgs:
        img_url = re.findall('src="(.*?)"',str(img))
        if not img_url[0][-3:] == 'gif':
            if not img_url[0][-3:] == 'png':
                print('正在下载：%s第%s张'%(img_url[0],count))
                write_to_file(img_url[0],currentPage,count)
        
        count += 1
    return next_url


def next(url):
    html = get_one(url)
    currentPage,next_url = pares_one_of_num(html)
    while currentPage != '[1]':
        next(next_url)


def write_to_file(url,percent_num,count):
    # dirName = u'{}/{}'.format('jiandan',percent_num)
    dirName = './picture/jiandan/{0}/'.format(percent_num)
    if not os.path.exists(dirName):
        os.makedirs(dirName)

    fileName = '%s/%s/%s.jpg' % (os.path.abspath('.'),dirName,count)
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

