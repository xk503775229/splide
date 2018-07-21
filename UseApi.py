import json
import urllib
import requests
import re
import requests
from bs4 import BeautifulSoup
from urllib import parse
def getPageUrl(count, fip):
    newsdata = {}
    newslink = 'http://api.search.sina.com.cn/?c=news&q=%E8%8B%8F%E5%B7%9E&stime=2017-07-19&etime=2018-07-21&sort=rel&highlight=1&num=10&ie=utf-8'

    newslink_2 = 'http://api.search.sina.com.cn/?c=news&t=&q=%E8%8B%8F%E5%B7%9E&pf=2131491050&ps=2130770168&page={}&stime=2017-07-20&etime=2018-07-22&sort=rel&highlight=1&num=10&ie=utf-8'.format(count)
    newslink_3 = 'http://api.search.sina.com.cn/?c=news&t=&q=%E4%B8%AD%E5%9B%BD&pf=2131425523&ps=2130770168&page=2&stime=2017-07-20&etime=2018-07-22&sort=rel&highlight=1&num=10&ie=utf-8'
    comments = requests.get(newslink_2)
    comments.encoding = 'utf-8'
    soupContent = BeautifulSoup(comments.text, 'html.parser')
    data_str = comments.text
    # print(data_str)
    r = re.compile('\{.*\}')
    res = re.findall(r,data_str)
    jd = json.loads(res[0])
    for list in jd['result']['list']:
        # print(list['title'])
        print(list['url'])
        if list['url'].endswith('html') and 'slide.tech.sina.com.cn' not in list['url']:
            newsdata = getNewsDetail(list['url'])
            json.dump(newsdata,fip)
            json.dump('\n',fip)



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
    fip = open("sinaSearchData.txt","w")
    for i in range(1,2):
        getPageUrl(i,fip)
    # content = "苏州"
    # keyNewsURl = 'http://www.sina.com.cn/mid/search.shtml?range=all&c=news&q={}&from=home&ie=utf-8'.format(content)
    # print(keyNewsURl)
