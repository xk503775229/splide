import re

strData ='http://www.zhihu.com/search_v3?content_length=150&vertical_info=0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0&advert_count=0&correction=1&search_hash_id=36d524e3259f4ca92b71f428b3123cdf&q=%E8%8B%8F%E5%B7%9E&limit=10&t=general&offset=25&topic_filter=0"'


answer = re.findall(r'offset=(.*)&topic',strData)
num = answer[0]

# answer = re.sub(temp)
print(num)