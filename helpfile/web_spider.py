import json
import time
import urllib.request
import re
import sys
import chardet
import requests
from bs4 import BeautifulSoup


def get_content(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'}
    cookies = dict(uuid='b18f0e70-8705-470d-bc4b-09a8da617e15',
                   UM_distinctid='15d188be71d50-013c49b12ec14a-3f73035d-100200-15d188be71ffd')
    # proxies = {'https': '123.117.205.77', 'http': '110.52.8.180:53281'}
    con = requests.get(url, headers=header, cookies=cookies).content
    if 'zhidao.baidu.com' in url:
        charcode = chardet.detect(con)
        if charcode['encoding'] == 'UTF-8' or charcode['encoding'] == 'utf-8':
            charset = 'utf-8'
        else:
            charset = 'gbk'
        html_doc = con.decode(charset, errors='ignore')
        return html_doc
    else:
        html_doc = con.decode('utf-8', errors='ignore')
        return html_doc


def get_label(data):
    url = data['url']
    label = ''
    if 'iask.sina.com.cn' in url:
        try:
            con = get_content(url)
            s1 = con.find('qname')
            if s1:
                s2 = con.find('"', s1)
                s3 = con.find('"', s2+1)
                label = con[s2+1:s3].replace('/', '')
                if not label:
                    label = '其它'
            else:
                label = '其它'
        except:
            label = '其它'

    elif 'zhidao.baidu.com' in url:
        try:
            html_doc = get_content(url)
            if '_百度宝宝知道' in html_doc:
                label = '母婴知识'
            elif '百度知道 - 信息提示' in html_doc:
                label = '其它'
            else:
                s1 = html_doc.find('<nav')
                s2 = html_doc.find('</nav>', s1)
                temp = html_doc[s1: s2+6]           # 定位到源代码中有关分类的html语句
                soup = BeautifulSoup(temp, 'lxml')
                a_list = soup.find_all('a')
                try:
                    label = a_list[1].string.replace('/', '')
                except:
                    label = '其它'
        except:
            label = '其它'

    elif 'wenda.so.com' in url or 'wenda.haosou.com' in url:
        # time.sleep(10)    # 停顿5s
        try:
            con = get_content(url)
            soup = BeautifulSoup(con, 'lxml')
            temp = soup.find('div', class_="text").get_text()
            s1 = temp.find('分类：')
            s2 = temp.find('被浏览')
            label = temp[s1+3:s2]
        except:
            label = '其它'
            # print('GG', url)

    elif 'www.zhihu.com' in url:  # 知乎
        try:
            html_doc = get_content(url)
            temp = html_doc.find('keywords')
            s1 = html_doc.find('content="', temp)
            s2 = html_doc.find('"', s1+9)
            label = html_doc[s1+9: s2]
            if not label:
                label = '其它'
        except:
            label = '其它'

    elif 'wenda.tianya.cn' in url:  # 天涯问答：多个标签
        try:
            con = get_content(url)
            soup = BeautifulSoup(con, 'lxml')
            temp = soup.find('div', class_="tags fl").get_text()
            label = temp.strip()
            if not label:
                label = '其它'
        except:
            label = '其它'

    elif 'wenwen.sogou.com' in url:  # 搜狗问问：有关键词
        try:
            con = get_content(url)
            soup = BeautifulSoup(con, 'lxml')
            temp = soup.find('div', class_="tags").get_text()
            label = temp.strip()
        except:
            label = '其它'

    if 'wenda.chinaso.com' in url:  # 国搜问答：原网页打不开了
        label = '其它'

    return label


def write_label(filename):
    fin = open('QA-result/' + filename, 'r', encoding='utf-8', errors='ignore')
    fout = open('QA-label/' + filename + '-label', 'w', encoding='utf-8')
    line = fin.readline()
    while line:
        data = json.loads(line)
        data['label'] = get_label(data)
        fout.write(json.dumps(data, ensure_ascii=False))
        fout.write('\n')

        line = fin.readline()

    fin.close()
    fout.close()


def get_file(n):
    file = ''
    if 0 <= n <= 9:
        file = 'part-0000' + str(n) + '-result'    # 文件名 1 位
    elif 10 <= n <= 99:
        file = 'part-000' + str(n) + '-result'      # 文件名 2 位
    else:
        file = 'part-00' + str(n) + '-result'       # 文件名 3 位

    return file


if __name__ == '__main__':
    start = time.clock()

    for n in range(int(sys.argv[1]), int(sys.argv[2])):
        file = get_file(n)
        write_label(file)  # 依次处理每一个文件

    end = time.clock()
    print('运行时间为：%.3f 秒' % (end-start))
