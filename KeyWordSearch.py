import requests
from bs4 import BeautifulSoup
from urllib import parse

import re



def getNewsListData(NewsURl):
    newsList = []

    reContent = requests.get(NewsURl)
    reContent.encoding = 'utf-8'
    print(reContent)
    soupContent = BeautifulSoup(reContent.text, 'html.parser')
    # print(soupContent)
    newsSoupCount = soupContent.select('.ft-info')
    print(soupContent)

    print(newsSoupCount)

            # newsList.encoding('UTF-8')
# def

    #return newsList
if __name__ == '__main__':
    content = "苏州"
    keyNewsURl = 'http://www.sina.com.cn/mid/search.shtml?range=all&c=news&q={}&from=home&ie=utf-8'.format(parse.quote(content))

    getNewsListData(keyNewsURl)