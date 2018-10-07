# -*- coding: utf-8 -*-
import json
import os
import re
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from _hashlib import md5
def get_page_index(offset, keyword):
    data={
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
    }
    url ='https://www.toutiao.com/search_content/?'+urlencode(data)  #构造Ajax动态请求链接
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

def parse_page_index(html):
    data = json.loads(html)  #转化为json对象
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错', url)
        return None

def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    if soup.select('title'):
        title = soup.select('title')[0].get_text()
        images_pattern = re.compile('var gallery = (.*?);',re.S)
        result = re.search(images_pattern,html)
        if result:
            data = json.loads(result.group(1))
            if data and 'sub_images' in data.key():
                sub_images = data.get('sub_images')
                images = [item.get('url') for item in sub_images]
                return {
                    'title':title,
                    'url': url,
                    'images':images
                }

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')#设置文件名，第一部分为项目路径，
    # 第二部分可以防止相同图片的重复下载，相同图片的md5值相同。 第三部分为图片的格式。
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)

def main():
    html = get_page_index(0,'街拍')
    for url in parse_page_index(html):
        html = get_page_detail(url)
        print(html)
        if html:
            result = parse_page_detail(html,url)
            print(result)
if __name__ == '__main__':
    main()