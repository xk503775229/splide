from urllib import parse

content = "苏州"
keyNewsURl = 'http://www.sina.com.cn/mid/search.shtml?range=all&c=news&q={}&from=home&ie={}'.format(parse.quote(content),'utf-8')

print(keyNewsURl)
keyword = input("请输入关键词：")
print(keyword)
count = input("请输入爬去的数目：")
print(type(count))
print(type(int(count)))
