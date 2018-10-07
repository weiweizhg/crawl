# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# browser = webdriver.Chrome()
browser = webdriver.PhantomJS()
wait = WebDriverWait(browser, 30)
browser.set_window_size(1400,900) #因为PhantomJS页面比较小，可能影响页面加载，所以设置的大一些，如果是Chrome则不用设置

#访问页面，输入要查询的关键字，并获取总共有多少页
def search():
    try:
        browser.get('https://www.taobao.com/')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button'))
        )
        input.send_keys('美食')
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total'))
        )
        get_products()
        return total.text
    except TimeoutException:
        return search()

#实现翻页操作
def next_page(page_number):
    print('正在加载 : ',page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number))
        )
        get_products()
        print('加载完毕', page_number)
    except TimeoutException:
        print('重试: ',page_number)
        next_page(page_number)



def get_products():
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item'))
    )
    items = browser.find_elements_by_css_selector('div[class="item J_MouserOnverReq  "]')
    print('items', items)
    for item in items:
        product = {
            'image' : item.find_element_by_css_selector('img').get_attribute('src'),
            'price' : item.find_element_by_css_selector('strong').text,
            'deal' : item.find_element_by_class_name('deal-cnt').text,
            'title': item.find_elements_by_class_name('J_ClickStat')[1].text,
            'location':item.find_element_by_class_name('location').text
        }
        print(product)




def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2,total+1):
            next_page(i)
    except Exception:
        print('出错了')
    finally:
        browser.close()

if __name__ == '__main__':
    main()
    # total = search()
    # print('1')
    # next_page(2)



