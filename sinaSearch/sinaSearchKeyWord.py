import json
import re
from urllib import parse
import requests
from bs4 import BeautifulSoup


'''
获取相应的网址
以及写入相应的文件
'''

def getPageUrl(count, fip, word):
    # newsdata = {}
    newslink_2 = 'http://api.search.sina.com.cn/?c=news&t=&q={}&pf=2131491050&ps=2130770168&page={}&stime=2017-07-20&etime=2018-07-22&sort=rel&highlight=1&num=10&ie=utf-8'.format(parse.quote(word),count)
    comments = requests.get(newslink_2)
    comments.encoding = 'utf-8'
    #soupContent = BeautifulSoup(comments.text, 'html.parser')
    data_str = comments.text
    # print(data_str)
    r = re.compile('\{.*\}')
    res = re.findall(r,data_str)
    jd = json.loads(res[0])
    for list in jd['result']['list']:
        # print(list['title'])
        #print(list['url'])
        # 去掉不是相关新闻的网址
        if list['url'].endswith('html') and 'slide.tech.sina.com.cn' not in list['url']:
            newsdata = getNewsDetail(list['url'])
            fip.writelines(json.dumps(newsdata) +'\n')

'''
获取具体网址的内容
'''

def getNewsDetail(newsURL):

    newsModel = {}

    reContent = requests.get(newsURL)
    reContent.encoding = 'utf-8'

    soupContent = BeautifulSoup(reContent.text, 'html.parser')
    # print(soupContent)
    # 获取newsURL
    print(newsURL)

    # 新闻ID
    match = re.search('doc-i(.*?).shtml', newsURL)


    if len(soupContent.select('.main-title')) > 0:
        # 新闻标题

        title = soupContent.select('.main-title')[0].text
        print(title)

        # 获取时间
        if len(soupContent.select('.date-source span')) > 0:
            time = soupContent.select('.date-source span')[0].text
            print(time)
            newsModel['time'] = time
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

        # 获取内容
        article = ''.join([article.text.strip() for article in soupContent.select('.article p')])
        # for article in soupContent.select('.article p'):
        #     print(article.text)
        print(article)

        # 获取编辑/作者
        if len(soupContent.select('.show_author')) > 0:
            show_author = soupContent.select('.show_author')[0].text
            print(show_author)
            newsModel['show_author'] = show_author

        newsModel['newsHref'] = newsURL
        newsModel['title'] = title
        newsModel['source'] = source
        newsModel['article'] = article

        return newsModel


if __name__ == '__main__':

    # python3


    #修改关键词
    keyword = '苏州'

    #爬取的总页数，每页10条新闻
    page = 100
    fip = open("sinaSearchData.txt","w")
    #fip2 = open("sinaSearchData2.txt","w")
    for i in range(1,page):
        getPageUrl(i,fip,keyword)
    # content = "苏州"
    # keyNewsURl = 'http://www.sina.com.cn/mid/search.shtml?range=all&c=news&q={}&from=home&ie=utf-8'.format(content)
    # print(keyNewsURl)
    fip.close()