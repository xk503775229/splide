import json
import re
from urllib import parse
import requests
from bs4 import BeautifulSoup

from selenium import webdriver

'''
输入第一个有效的的URL和需要爬取的页码数
关键字 和 数据保存的地址
'''


def getPageSource(url, page, keyWord, fip):
    driver = webdriver.PhantomJS()
    # 浏览器driver访问url
    driver.get(url)
    # 隐式等待2秒，,等待js加载
    driver.implicitly_wait(2)
    # 设置秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
    driver.set_page_load_timeout(2)
    # 获取网页资源（获取到的是网页所有数据）
    html = driver.page_source
    driver.quit()
    # 返回网页资源
    print(type(html))
    #匹配数据
    r = re.compile('\{.*\}')
    res = re.findall(r, html)
    # print(res[0])
    pageData = json.loads(res[0])

    url = dealWithData(pageData, keyWord, fip)
    if page >= 1:
        getPageSource(url, page - 1, keyWord, fip)
    else:
        return


'''
输入页面资源和关键字以及数据保存的地址
'''


def dealWithData(pageData, keyword, fip):

    # 首先获取下一页的search_hash_id
    hash_id = pageData['search_action_info']['search_hash_id']
    #print(hash_id)
    strData = pageData['paging']['next']
    print(strData)

    # 获取下一页的页码标签
    awr = re.findall(r'offset=(.*)&amp', strData)
    #print(awr)
    if len(awr) != 0:
        num = awr[0]

        # 接下来的URL
        url = 'https://www.zhihu.com/api/v4/search_v3?t=general&q={}&correction=1&offset={}&limit=10&search_hash_id={}'.format(
            parse.quote(keyword), num, hash_id)
        print(url)
    for i in range(len(pageData['data'])):

        # 如果问题存在获取问题
        if 'title' in pageData['data'][i]['highlight'].keys():
            data = {}

            # print(pageData['data'][i]['object']['question'])
            question = pageData['data'][i]['highlight']['title']
            # print(question)
            question = re.sub('&lt;em&gt;', '', question)
            question = re.sub('&lt;/em&gt;', '', question)
            # print(question)
            data['title'] = question
            # 获取问题的ID
            data['id'] = pageData['data'][i]['object']['id']
            # print(pageData['data'][i]['object']['content'])

            # 如果答案存在，获取答案（有的是个人的文章不一定是问答）
            if len(pageData['data'][i]['highlight']['description']) != 0:
                answer = pageData['data'][i]['object']['content']
                answer = re.sub(r'&lt;figure.*/figure&gt;', '', answer)
                answer = re.sub('&lt;p&gt;|&lt;/p&gt;|&lt;br&gt;|&lt;b&gt|&lt;/b&gt|&lt;li&gt;|&lt;/li&gt', '', answer)
                data['content'] = answer

            # 获取作者的名称，以及他的支持数
            if 'voteup_count' and 'author' in pageData['data'][i]['object'].keys():
                data['author'] = pageData['data'][i]['object']['author']['name']
                data['voteCount'] = pageData['data'][i]['object']['voteup_count']

        # print(pageData['search_action_info'])
        print(data)
        fip.writelines(json.dumps(data) + '\n')

    # hash_id = pageData['search_action_info']['search_hash_id']
    # # strData = pageData['paging']['next']
    # # answer = re.findall(r'offset=(.*)&topic',strData)
    # # num = answer[0]
    # # url ='https://www.zhihu.com/api/v4/search_v3?t=general&q=%E8%8B%8F%E5%B7%9E&correction=1&offset={}&limit=10&search_hash_id={}'.format(num,hash_id)
    # # print(url)
    return url


if __name__ == '__main__':
    # 要搜索的关键字
    keyWord = '苏州'
    # 需要搜索的页数 每页大概有9个,如果页码超出范围有可能会出错
    page = 10

    fip = open('searchZhiHuData.txt', 'w')
    # 这个数字可以更改，要保证第一页有数据如果没有数据再次更改，最好是5的倍数（如果数据始终从无法输出可能是hash_id失效，需要我来手动更改）
    offSet =  10
    url = 'https://www.zhihu.com/api/v4/search_v3?t=general&q={}&correction=1&offset={}&limit=10&search_hash_id=31ad7aa9055bdbb21dbf9b632369d670'.format(
        parse.quote(keyWord), offSet)
    getPageSource(url, page, keyWord, fip)

    fip.close()
