from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from urllib import parse

from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
browser.get('http://www.sina.com.cn/mid/search.shtml?range=all&c=news&q=%E8%8B%8F%E5%B7%9E&from=home&ie=utf-8')
url = browser.find_element_by_link_text("下一页")
print(url)
# data =  browser.find_element_by_xpath('//*[@id="_function_code_page"]/a[11]')
# actions = ActionChains(browser)
#
# actions.click(data).perform()
# actions.click(data).perform()
# Actions action = new Actions(driver) ;
# action.contextClick(driver.findElement(By.xpath(xpath)))