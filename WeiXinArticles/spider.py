# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
import requests

base_url = 'https://weixin.sogou.com/weixin?'
headers = {
    'Cookie': 'IPLOC=CN2201; SUID=3B28A8DE1F13940A000000005BB226E0; SUV=1538402015470005; ABTEST=0|1538402027|v1; SNUID=1C0080F9282D50030A46BFDC28A46DEB; weixinIndexVisited=1; sct=1; JSESSIONID=aaa0B_YBXj06qhuT0aCvw; ppinf=5|1538403344|1539612944|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTklODMlOTElRTQlQkMlOUYlRTQlQkMlOUZ8Y3J0OjEwOjE1Mzg0MDMzNDR8cmVmbmljazoyNzolRTklODMlOTElRTQlQkMlOUYlRTQlQkMlOUZ8dXNlcmlkOjQ0Om85dDJsdVBNU20wMlo4WXVVWUQyVTZ6YkNIWUFAd2VpeGluLnNvaHUuY29tfA; pprdig=h3te-WlIHvjEA1957EskmkHi6kVCRiax0V7UFCaSSoa9zOYS905BbzuuHHKRUjvaJgTudGY6Ww5CWGPOyYLo-1a-yVrelVxSULzV6f0ZFy9HPtfg1xfv-ia79qROPOEXTuW55B3NRgCe5kuncY0Uk6vMj-JXICLp9QBKYs_uLVs; sgid=16-37311027-AVuyLBAH2JlPEe9HH8ATKfk; ppmdig=153840334400000035619ad18f92f774aafb66faeffa991d',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
proxy=None
max_count=5
def get_proxy():
    ip = '67.63.33.7:80'
    return ip

def get_html(url, count = 1):
    global proxy
    if count >=5:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:
            proxies = {
                'http':'http://'+proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers,proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False,headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302: #说明ip被封掉
            #Need Proxy
            print('302')
            proxy=get_proxy()
            if proxy:
                print('using proxy',proxy)
                count+=1
                return get_html(url)
            else:
                print('get proxy failed')
                return None
    except ConnectionError as e:
        print('Error Occured',e.args)
        proxy = get_proxy()
        count+=1
        return get_html(url)

def get_index(keyword,page):
    data={
        'query': keyword,
        '_type': 2,
        'page': page,
    }
    queries = urlencode(data)
    url = base_url+queries
    html = get_html(url)
    return html

def main():
    while(True):
        for page in range(1, 8):
            html = get_index('风景', page)
            print(html)


if __name__ == '__main__':
    main()
