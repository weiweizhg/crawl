# -*- coding: utf-8 -*-
import json
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from multiprocessing import  Pool
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 30)

count=0
loadCount =0

def set_cookies(startURL,targetURL):
    browser.get(startURL)#必须先登陆网站才能设置cookie
    browser.delete_all_cookies()
    with open('D:\\pyPractice\\crawling\\cookies.json', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
        for cookie in listCookies:
            print(cookie['domain'],cookie['name'],cookie['value'])
            browser.add_cookie({'domain': cookie['domain'], 'name': cookie['name'], 'value': cookie['value']})#设置cookie
    browser.get(targetURL)


if __name__ == '__main__':
    set_cookies()