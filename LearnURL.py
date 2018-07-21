#! /usr/bin/env python
#coding=utf-8
import  json


import requests
from bs4 import BeautifulSoup
import re
import pandas
#sinaNewsURL = 'http://news.sina.com.cn/china'

#1 - 获取china首页新闻列表（后面用不到, 可以用这个拿到新闻链接, 然后再测试新闻详情函数）

def getNewsListData(newsURl):
    newsList = []

    reContent = requests.get(newsURl)
    reContent.encoding = 'utf-8'
    print(reContent)
    soupContent = BeautifulSoup(reContent.text, 'html.parser')
    # print(soupContent)
    newsSoupList = soupContent.select('.news-item')
    print(len(newsSoupList))
    for newsSoup in newsSoupList:

        newsModel = {}

        if len(newsSoup.select('h2')) > 0:

            news = newsSoup.select('h2')[0]
            newsTime = newsSoup.select('.time')[0]

            # 获取Href
            a = news.select('a')[0]
            href = a['href']

            # 获取新闻ID

            m = re.search('doc-i(.*?).shtml', href)
            if len(m.group()) > 1:
                newsID = m.group(1)
                newsModel['newsID'] = newsID
            # 获取title
            title = news.text
            # title = str(title)
            #print(title)
            #获取时间
            time = newsTime.text

            #print("%s" % title)

            newsModel['newsHref'] = href
            newsModel['title'] = title
            newsModel['time'] = time
            newsList.append(newsModel)
            # newsList.encoding('UTF-8')
    return newsList

def getNewsDetail(newsURL):

    newsModel = {}

    reContent = requests.get(newsURL)
    reContent.encoding = 'utf-8'

    soupContent = BeautifulSoup(reContent.text, 'html.parser')
    #print(soupContent)
    # 获取newsURL
    print(newsURL)

    # 新闻ID
    match = re.search('doc-i(.*?).shtml', newsURL)
    newsID = match.group(1)
    print(newsID)
    # 判断网页是否存在
    if len(soupContent.select('.main-title')) > 0:
        # 新闻标题

        title = soupContent.select('.main-title')[0].text
        print(title)

        # 获取时间
        time = soupContent.select('.date-source span')[0].text
        print(time)

        # 获取来源
        source = ''
        if len(soupContent.select('.date-source a')) > 0:
            source = soupContent.select('.date-source a')[0].text
            print(source)
        elif len(soupContent.select('.source')) > 0:
            source = soupContent.select('.source')[0].text
            print(source)
        else:
            print('当前未检测到来源', newsURL)


        #获取内容
        article = ''.join([article.text.strip() for article in soupContent.select('.article p')])
        # for article in soupContent.select('.article p'):
        #     print(article.text)
        print(article)

        #获取编辑/作者
        # show_author = soupContent.select('.show_author')[0].text
        # print(show_author)

        newsModel['newsID'] = newsID
        newsModel['newsHref'] = newsURL
        newsModel['title'] = title
        newsModel['time'] = time
        newsModel['source'] = source
        newsModel['article'] = article
        # newsModel['show_author'] = show_author

        return


def getNewLists(commonPage):

    newsList = []

    for i in range(1, 3):
        newsPage = commonPage.format(i)
        # print(newsPage)

        reContent = requests.get(newsPage)
        reContent.encoding = 'utf-8'

        if reContent.status_code == 200:
            jsonData = json.loads(reContent.text)

            for newDic in jsonData['result']['data']:
                newsURL = newDic['url']

                # print(newsURL)

                newsList.append(getNewsDetail(newsURL))
        else:
            print('分页结束******')
            break

    return newsList

if __name__ == '__main__':
    # commonPage = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}'
    #
    #
    # df = pandas.DataFrame(getNewLists(commonPage))
    # df.to_excel('news.xis')
    # print(getNewsListData(sinaNewsURL))             #打印新闻列表
    # newsList = getNewsListData(sinaNewsURL)
    # for i in newsList:
    #     getNewsDetail(i.get('newsHref'))
    #     print('\n')#打印新闻列表
    # getNewsDetail(sinaNewsURL)
    # getNewLists(commonPage)
    getNewsDetail('http://tech.sina.com.cn/t/2018-07-20/doc-ihfqtahh7988094.shtml')