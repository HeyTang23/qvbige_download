import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
import os

base_url = 'http://www.xbiquge.la/0/10/'
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
def get_url(url):
    text = requests.get(url, header)
    text.encoding = 'utf-8'
    return text.text

def get_data(text):
    doc = etree.HTML(text)
    find_title = doc.xpath('//div[@id="info"]/h1/text()')
    find_list = doc.xpath('//div[@id="list"]//dd//text()')
    list_link = ['http://www.xbiquge.la' + i for i in doc.xpath('//div[@id="list"]//dd/a/@href')]
    mkdir(f"{find_title[0]}")
    return list_link,find_list,find_title

def parser_data(link):
    for i in range(len(link[0])):
        html = get_url(link[0][i])
        doc = etree.HTML(html)
        title = link[1][i]
        title = title.split(" ")
        chapter = doc.xpath('//div[@class="bookname"]/h1/text()')
        soup=BeautifulSoup(html,"html.parser")
        section_text=soup.select('#wrapper .content_read .box_con #content')[0].text        
        section_text=re.sub( '\s+', '\r\n\t', section_text).strip('\r\n')
        if not os.path.exists(f"{link[2][0]}/第{i-1}章 {title[-1]}.txt"):
            with open(f"{link[2][0]}/第{i-1}章 {title[-1]}.txt",'w',encoding='utf8') as f:
                f.write(f"{section_text}")
                print(f'第{i}章 {title[-1]}')
        else:
            print(f"{link[2][0]}/第{i-1}章 {title[-1]}.txt"+' 已存在')
        
    print(f"《{link[2][0]}》爬取完成")


def mkdir(path):
    import os
    path=path.strip()
    if not os.path.exists(path):
        os.makedirs(path) 
        print(path+' 创建成功')
    else:
            print(path+' 目录已存在')


if __name__ == '__main__':
    parser_data(get_data(get_url(base_url)))
