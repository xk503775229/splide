import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import selenium
import random

class auto_login():

    def __init__(self):
        self.driver = webdriver.Chrome()

    def run(self):
        driver = self.driver

        driver.get("http://a.suda.edu.cn/")
        # print(not driver.find_element_by_id('logout_username').text)
        if not driver.find_element_by_id('logout_username').text:
            text_input = driver.find_element_by_id('username')
            text_input.send_keys("20165227013")
            text_input = driver.find_element_by_id('password')
            text_input.send_keys("11185998")

            enter = driver.find_element_by_id('login')
            actions = ActionChains(driver)
            actions.click(enter).perform()


    def close(self):
        self.driver.close()







auto_link = auto_login()
auto_link.run()
auto_link.close()




