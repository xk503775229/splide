from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from urllib import parse

from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/api/v4/search_v3?t=general&q=%E8%8B%8F%E5%B7%9E&correction=1&offset=25&limit=10&search_hash_id=68f1b59096f67b7623034bc510546502')

print(url)
# data =  browser.find_element_by_xpath('//*[@id="_function_code_page"]/a[11]')
# actions = ActionChains(browser)
#
# actions.click(data).perform()
# actions.click(data).perform()
# Actions action = new Actions(driver) ;
# action.contextClick(driver.findElement(By.xpath(xpath)))