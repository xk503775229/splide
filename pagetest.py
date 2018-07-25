# -*- coding: UTF-8 -*-
import json
import re
from urllib import parse
from selenium import webdriver
import requests
from bs4 import BeautifulSoup


content = "苏州"
keyNewsURl = 'https://api.zhihu.com/questions/22723641'
driver = webdriver.PhantomJS()
# 浏览器driver访问url
driver.get(keyNewsURl)
# 隐式等待6秒，,等待js加载
driver.implicitly_wait(1)
# 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
driver.set_page_load_timeout(1)
# 获取网页资源（获取到的是网页所有数据）
html = driver.page_source
driver.quit()
# 返回网页资源
print(html)
# r = re.compile('\{.*\}')
# res = str(re.findall(r,html))
# print(res)
# jd = json.loads(res)
# print(jd['title'])

