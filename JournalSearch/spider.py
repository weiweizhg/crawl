# -*- coding: utf-8 -*-

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
        # save_message(['ISSN', 'Name', 'ImpactFactor', 'Partition', 'MajorSubject', 'SmallSubject'])
    except Exception:
        print("prepare Exception:  " + "重新准备")
        browser.close()
        browser = webdriver.Chrome()
        wait = WebDriverWait(browser, 30)
        prepare()

def get_products(fileCount):
    global count
    # wait.until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR,'#yxyz_content > table.table_yjfx > tbody > tr:nth-child(2) > th:nth-child(1) > a'))
    # )
    try:
        ISSN =browser.find_element_by_css_selector(
            '#yxyz_content > table.table_yjfx > tbody > tr:nth-child(3) > td:nth-child(1)').text
        if len(ISSN)>10:
            ISSN=browser.find_element_by_css_selector('#yxyz_content > form > table > tbody > tr:nth-child(1) > td:nth-child(2) > input[type="text"]').get_attribute('value')
            Name = "#"
            ImpactFactor='#'
            Partition = '#'
            MajorSubject = "#"
            SmallSubject = "#"
        else:
            Name = browser.find_element_by_css_selector(
                '#yxyz_content > table.table_yjfx > tbody > tr:nth-child(3) > td:nth-child(2) > a').text
            if not Name:
                Name="#"
            ImpactFactor = browser.find_element_by_css_selector(
                '#yxyz_content > table.table_yjfx > tbody > tr:nth-child(3) > td:nth-child(3)').text
            if not ImpactFactor:
                ImpactFactor="#"
            Partition = browser.find_element_by_css_selector(
                '#yxyz_content > table.table_yjfx > tbody > tr:nth-child(3) > td:nth-child(4)').text
            if not Partition:
                Partition="#"
            MajorSubject = browser.find_element_by_css_selector(
                '#yxyz_content > table.table_yjfx > tbody > tr:nth-child(3) > td:nth-child(5)').text
            if not MajorSubject:
                MajorSubject="#"
            SmallSubject = browser.find_element_by_css_selector(
                '#yxyz_content > table.table_yjfx > tbody > tr:nth-child(3) > td:nth-child(6)').text
            if not SmallSubject:
                SmallSubject="#"
        message = [ISSN, Name, ImpactFactor, Partition, MajorSubject, SmallSubject]
        save_message(message,fileCount)
        # save_log('count: %s'%(count), fileCount)
    except Exception as e:
        print('存储异常： ',ISSN)
        message = [ISSN, "*", "*", "*", "*", "*"]
        save_message(message, fileCount)
#实现下一个信息的操作
def next_page(ISSN_number,fileCount):
    global loadCount
    global wait
    global browser
    # save_log('正在加载 : %s'%ISSN_number, fileCount)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '#yxyz_content > form > table > tbody > tr:nth-child(1) > td:nth-child(2) > input[type="text"]'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '#yxyz_content > form > table > tbody > tr:nth-child(1) > td:nth-child(6) > input[type="submit"]:nth-child(2)'))
        )
        input.clear()
        input.send_keys(ISSN_number)
        submit.click()
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#yxyz_content > table.table_yjfx > tbody > tr:nth-child(2) > th:nth-child(1) > a'))
        )
        get_products(fileCount)
        loadCount = 0
    except Exception:
            print('重试: ',ISSN_number)
            # save_log('重试: ' + ISSN_number, fileCount)
            browser.close()
            browser = webdriver.Chrome()
            wait = WebDriverWait(browser, 30)
            prepare()
            next_page(ISSN_number, fileCount)

def save_message(proxy,fileCount):
    with open('D:\\pyPractice\\crawling\\message'+str(fileCount)+'.csv','a') as f:
        f.write(proxy[0]+','+proxy[1]+','+proxy[2]+','+proxy[3]+','+proxy[4]+','+proxy[5]+'\n')

def save_log(message,fileCount):
    with open('D:\\pyPractice\\crawling\\log'+str(fileCount)+'.txt','a') as f:
        f.write(message+'\n')

def read_file(file):
    IssnList=[]
    lineNum=0
    with open(file,'r') as fr:
        for line in fr.readlines():
            if lineNum>=1:
                IssnList.append(line.strip()[1:-1])
            lineNum+=1
    return IssnList
def main(fileCount):
    try:
        prepare()
        IssnList = read_file('E:\Hilab项目\issn_inset.csv')
        for i in IssnList[10000:11000]:
            next_page(i,fileCount)
    except Exception as reason:
        print('出错了: '+reason)
    finally:
        browser.close()

if __name__ == '__main__':
    main(11)
    # firstIssn, IssnList = read_file('E:\Hilab项目\issn_inset.csv')
    # search(firstIssn)
    # issn_list = IssnList
    # pool = Pool()
    # pool.map(main, issn_list)
