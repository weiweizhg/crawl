# -*- coding: utf-8 -*-
import json

from selenium import webdriver
chromeOptions = webdriver.ChromeOptions()
# 设置代理http://67.63.33.7:80,一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
chromeOptions.add_argument("--proxy-server=http://67.63.33.7:80")
browser = webdriver.Chrome(chrome_options = chromeOptions)

# 查看本机ip，查看代理是否起作用
browser.get("http://httpbin.org/ip")
print(browser.page_source)

# 退出，清除浏览器缓存
browser.close()
