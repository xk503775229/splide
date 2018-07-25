# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 10:34:27 2017
@author: gzs10227
"""

import urllib, urllib2, re, json
from imp import reload

import requests

urllib.getproxies_registry = lambda: {}
import sys

stderr = sys.stderr
stdout = sys.stdout
reload(sys)
sys.setdefaultencoding('utf8')
sys.stderr = stderr
sys.stdout = stdout
from lxml import etree
import re
import pandas as pd
from pandas import DataFrame
import os
import random
import datetime, time

url = 'https://www.zhihu.com/topic/20105184/top-answers?page=1'

headers = {
    'accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'authorization': 'Bearer 2|1:0|10:1514185979|4:z_c0|92:Mi4xZzZSRkFnQUFBQUFBZ0VJeThBYTdEQ1lBQUFCZ0FsVk4tdkl0V3dCSHVJTm93T3d6a3lBSmotSjJQR0xzaV82QUJR|fd43b64c754f3e2d34658961f5db3f233ea367c86eb90c299685746fb8e1cbf8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '',
    'Host': 'www.zhihu.com',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'X-UDID': 'AIBCMvAGuwyPThPGhuYxg9CTUALjTwfhGYg='}

url = 'https://www.zhihu.com/question/31116099'
header2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}


def get_question_link(url):
    url = 'https://www.zhihu.com/search?type=content&q=荒野行动'
    requests.get(url, )


def deal_dict(di):
    result_df = {}
    author_info = di['author']
    result_df['created_time'] = di['created_time']
    result_df['id'] = di['id']
    result_df['content'] = di['content']
    result_df['comment_count'] = di['comment_count']
    result_df['url'] = di['url']
    return result_df, author_info


def get_zhihu_dict(url):
    time.sleep(1)
    req = urllib2.Request(url, None, header2)
    content = urllib2.urlopen(req).read()
    content2 = content.split('http://www.zhihu.com/api/v4/questions/')[-2].split('limit=')[0].replace('amp;', '')
    apiurl = 'http://www.zhihu.com/api/v4/questions/%s' % content2
    print(apiurl)
    limit = 20
    offset = 0
    answers_url = '%slimit=%s&offset=%s' % (apiurl, limit, offset)
    print(answers_url)
    temp = requests.get(answers_url, headers=headers)
    html = temp.content
    data = json.loads(html)
    totals = data['paging']['totals']
    result = data['data']

    while len(result) <= totals and not data['paging']['is_end']:
        time.sleep(1)
        try:
            next_url = data['paging']['next']
            print
            next_url
            temp = requests.get(next_url, headers=headers)
            html = temp.content
            data = json.loads(html)
            result.extend(data['data'])
        except:
            break
    all_result = map(deal_dict, result)
    author_info = [];
    comment_info = []
    for dict2 in all_result:
        author_info.append(dict2[1])
        comment_info.append(dict2[0])
    author_info_df = pd.DataFrame(author_info)
    comment_df = pd.DataFrame(comment_info)
    comment_df['id'] = comment_df['id'].astype(str)
    return author_info_df, comment_df


author_info_df, comment_df = get_zhihu_dict(url)
author_info_df = author_info_df[['id', 'name', 'gender', 'url']]
comment_url = list(comment_df['url'][comment_df['comment_count'] > 0])
Str_p = '/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=20&offset=0&status=open'
comment_url = map(lambda i: i + Str_p, comment_url)


def get_comment_more(url):
    time.sleep(1)
    temp = requests.get(url, headers=headers).content
    data = json.loads(temp)
    result = data['data']
    totals = data['paging']['totals']
    while len(result) <= totals and not data['paging']['is_end']:
        time.sleep(1)
        try:
            next_url = data['paging']['next']
            print
            next_url
            temp = requests.get(next_url, headers=headers)
            html = temp.content
            data = json.loads(html)
            result.extend(data['data'])
        except:
            break
    return result


Comment_list = map(get_comment_more, comment_url)
comment_more = []
for C in Comment_list:
    comment_more.extend(C)
comment_more_df = pd.DataFrame(comment_more)
more_anchor = pd.DataFrame(list(comment_more_df['author']))
more_anchor_df = pd.DataFrame(list(more_anchor['member']))
author_df = more_anchor_df[['id', 'name', 'gender', 'url']]
all_author_info = pd.concat([author_info_df, author_df], axis=0)
all_author_info = all_author_info.drop_duplicates()
more_comment_df = comment_more_df[['id', 'url', 'created_time', 'content', 'vote_count']]
all_comment_df = pd.concat([more_comment_df, comment_df])
