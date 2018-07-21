import re

from selenium import webdriver
import requests
from bs4 import BeautifulSoup

from urllib import parse



# 搜索出来的新闻是一页10 个， 获取搜索到的新闻条目，然后获取页数，数字范围可以控制。不要超过页数
def dynamic_view(url):
    '''
    使用自动化工具获取网页数据
    :param url: 待获取网页url
    :return: 页面数据
    '''

    driver = webdriver.PhantomJS()
    # 浏览器driver访问url
    driver.get(url)
    # 坑：不同frame间的转换(网易云在数据展示中会将数据动态添加到'g_iframe'这个框架中，如果不切换，会报"元素不存在"错误。)
    # driver.switch_to.frame("g_iframe")
    # 隐式等待6秒，,等待js加载
    driver.implicitly_wait(2)
    # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
    driver.set_page_load_timeout(6)
    # 获取网页资源（获取到的是网页所有数据）
    html = driver.page_source
    # 坑：退出浏览器driver，必须手动退出driver。
    driver.quit()
    # 返回网页资源
    return html

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
    if len(match.group()) > 1:
        newsID = match.group(1)
        newsModel['newsID'] = newsID
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

        # 获取编辑/作者
        if len(soupContent.select('.show_author')) > 0:
            show_author = soupContent.select('.show_author')[0].text
            print(show_author)
            newsModel['show_author'] = show_author

        newsModel['newsHref'] = newsURL
        newsModel['title'] = title
        newsModel['time'] = time
        newsModel['source'] = source
        newsModel['article'] = article


        return newsModel
def getPageList(page_source):

    pass
if __name__ == '__main__':
    nurl = 'http://www.sina.com.cn/mid/search.shtml?range=all&c=news&q=%E8%8B%8F%E5%B7%9E&from=home&ie=utf-8'
    nurl_2 ='http://api.search.sina.com.cn/?c=news&amp;t=&amp;q=%E8%8B%8F%E5%B7%9E&amp;pf=2131491049&amp;ps=2130770168&amp;page=4'
    page_source = dynamic_view(nurl)
    soupContent = BeautifulSoup(page_source, 'html.parser')
    # print(soupContent)
    newsSoupList = soupContent.select('.l_v2')

    print(type(newsSoupList[0]))
    # page_countbox = soupContent.select('.pagebox')
    # print(page_countbox)
    # count = 0
    # for news in newsSoupList:
    #     count += 1
    #     a = news.select('a')[0]
    #     newsHref = a['href']
    #     #print(newsHref)
    #     # getNewsDetail(newsHref)
    # print(count)
