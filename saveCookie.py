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

def prepare():
    global browser
    global wait
    try:
        browser.get('https://www.letpub.com.cn/index.php?page=login')
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#form > div:nth-child(6) > img'))
        )
        Email = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#email'))
        )
        Password = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#password'))
        )
        Email.send_keys('weiwei.zhg@gmail.com')
        Password.send_keys('zww666666')
        submit.click()
        search_jorunal = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#container > div.feedback > div > div.right_layout > div.keycode > p:nth-child(1) > a'))
        )
        search_jorunal.click()
        notify = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#msgShut'))
        )
        notify.click()
        get_cookie()
        # save_message(['ISSN', 'Name', 'ImpactFactor', 'Partition', 'MajorSubject', 'SmallSubject'])
    except Exception:
        print("prepare Exception:  " + "重新准备")
        browser.close()
        browser = webdriver.Chrome()
        wait = WebDriverWait(browser, 30)
        prepare()

def get_cookie():
    cookies = browser.get_cookies()
    jsonCookies = json.dumps(cookies)
    with open('D:\\pyPractice\\crawling\\cookies.json', 'w') as f:
        f.write(jsonCookies)



if __name__ == '__main__':
    prepare()
    # firstIssn, IssnList = read_file('E:\Hilab项目\issn_inset.csv')
    # search(firstIssn)
    # issn_list = IssnList
    # pool = Pool()
    # pool.map(main, issn_list)
