# -*- coding: utf-8 -*-
import json
import requests
from requests.exceptions import  RequestException
from bs4 import BeautifulSoup
from multiprocessing import  Pool

def get_one_page(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
        }
        proxies = {
            'http': 'http://67.63.33.7:80',
            'https': 'https://195.235.204.60:3128'
        }
        response = requests.get(url,proxies=proxies,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    soup = BeautifulSoup(html,'lxml')
    res=[]
    for dd in soup.select('dd'):
        ele=[]
        ele.append(dd.select('a')[0]['title'].strip())
        ele.append(dd.select('.star')[0].get_text().strip())
        res.append(ele)
    return res

def write_to_file(content):
    with open('D:\\pyPractice\\crawling\\res.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(offset):
    url='http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    res=parse_one_page(html)
    for item in res:
        write_to_file(item)
    print(res)


if __name__== '__main__':
    for i in range(10):
        main(i*10)
    # pool = Pool()
    # pool.map(main, [i*10 for i in range(10)])