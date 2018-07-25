
import json
import re
from urllib import parse
import requests
from bs4 import BeautifulSoup

from selenium import webdriver


'''
模拟浏览器登录
请求网址，返回网页资源
'''

def gerURL(url):


    driver = webdriver.PhantomJS()
    # 浏览器driver访问url
    driver.get(url)
    # 隐式等待6秒，,等待js加载
    driver.implicitly_wait(1)
    # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
    driver.set_page_load_timeout(1)
    # 获取网页资源（获取到的是网页所有数据）
    html = driver.page_source
    driver.quit()
    # 返回网页资源
    print(type(html))
    r = re.compile('\{.*\}')
    res = re.findall(r,html)
    #print(res[0])
    jd = json.loads(res[0])
    return jd

# def isChinese(content):
#     for i in range(len(content)):
#         if '0x4E00' <= content[i] <= '0x9FA5':
#
#             continue
#
#         else:
#             content[i]=''

'''
处理网页数据，并写入相关文件
'''

def dealWitndata(jd,fip):

    for i in range(len(jd['data'])):

       # print(jd['data'][i])
       # 如果该问题存在
        if  'question'  in  jd['data'][i]['object'].keys():
            data = {}
            #print(jd['data'][i]['question'])
            #print(jd['data'][i]['object']['question'])

            #获取问题名称
            question = jd['data'][i]['object']['question']['name']
            #print(question)
            question = re.sub('&lt;em&gt;','',question)
            question = re.sub('&lt;/em&gt;', '', question)
            print(question)
            data['question'] = question
            #print(jd['data'][i]['object']['content'])

            # 获取答案内容
            answer = jd['data'][i]['object']['content']
            answer = re.sub(r'&lt;figure.*/figure&gt;', '', answer)
            answer = re.sub('&lt;p&gt;|&lt;/p&gt;|&lt;br&gt;|&lt;b&gt|&lt;/b&gt|&lt;li&gt;|&lt;/li&gt', '', answer)
            print(answer)
            data['answer'] = answer
            fip.writelines(json.dumps(data)+'\n')


if __name__ == '__main__':
    keyword = '苏州'
    fip = open('zhihuSearchData.txt','w')
    for i in range(1,300):

        url = 'https://www.zhihu.com/api/v4/search_v3?t=general&q={}&correction=1&offset={}&limit=10&search_hash_id=f8efa9fb5f0a503aac4e5a818388bb3f'.format(parse.quote(keyword),i)
        data = gerURL(url)
        dealWitndata(data,fip)
    fip.close()