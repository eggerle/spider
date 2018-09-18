#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : Woolei
# @File : download_txt.py 
 
 
import urllib
import urllib.request
import time
import os
from bs4 import BeautifulSoup
from multiprocessing import Pool
 
url = 'https://www.136book.com/huaqiangu/ebxeeql/'
headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}
 
 
# 获取小说章节内容，并写入文本
def getChapterContent(each_chapter_dict):
    # content_html = requests.get(each_chapter_dict['chapter_url'], headers=headers).text
    req = urllib.request.Request(each_chapter_dict['chapter_url'],headers=headers)
    content_html = urllib.request.urlopen(req)
    soup = BeautifulSoup(content_html, "html.parser")
    print('------------------------>soup',soup)
    content_tag = soup.find('div', {'id': 'content'})
    print('------------------------>content_tag',content_tag)
    if content_tag:
        try:
            p_tag = content_tag.find_all('p')
            print('正在保存的章节 --> ' + each_chapter_dict['name'])
            for each in p_tag:
                paragraph = each.get_text().strip()
                with open(each_chapter_dict['name'] + r'.txt', 'a', encoding='utf8') as f:
                    f.write('  ' + paragraph + '\n\n')
                    f.close()
        except Exception as e:
            print(e)
    # else:
 
 
# 获取小说各个章节的名字和url
def getChapterInfo(novel_url):
    # chapter_html = requests.get(novel_url, headers=headers).text
    req = urllib.request.Request(novel_url,headers=headers)
    chapter_html = urllib.request.urlopen(req)
    soup = BeautifulSoup(chapter_html, "html.parser")
    chapter_list = soup.find_all('li')
    chapter_all_dict = {}
    title = soup.find_all('h1')
    for each in chapter_list:
        import re
        chapter_each = {}
        chapter_each['name'] = each.find('a').get_text()  # 获取章节名字
        chapter_each['chapter_url'] = each.find('a')['href']  # 获取章节url
        chapter_num = int(re.findall('\d+', each.get_text())[0])  # 提取章节序号
        chapter_all_dict[chapter_num] = chapter_each  # 记录到所有的章节的字典中保存
    return chapter_all_dict,title
 
 
if __name__ == '__main__':
    start = time.process_time()
    novel_url = 'http://www.136book.com/chenghongniandai/'
    novel_info,title = getChapterInfo(novel_url)
    dir_name = title[0].text
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    os.chdir(dir_name)
    pool = Pool(processes=10)   # 创建10个进程
    pool.map(getChapterContent, [novel_info[each] for each in novel_info])
    pool.close()
    pool.join()
    end = time.process_time()
    print('多进程保存小说结束，共保存了 %d 章，消耗时间：%f s' % (len(novel_info), (end - start)))
