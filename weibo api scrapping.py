
key = input("请输入爬取关键字:")
for page in range(1,10):
   params = (
       ('containerid', f'100103type=1&q={key}'),
       ('page_type', 'searchall'),
       ('page', str(page)),
   )

   response = requests.get('https://m.weibo.cn/api/container/getIndex', headers=headers, params=params)

import requests

# 设置请求的URL和参数
url = "https://c.api.weibo.com/2/search/statuses/limited.json"
key = input("请输入爬取关键字:")
params = {
    "access_token": "YOUR_ACCESS_TOKEN",
    "q": key,
    "count",
    "page"
}

# 发送GET请求
response = requests.get(url, params=params)

# 解析响应数据
data = response.json()

# 打印热门微博列表
for status in data["statuses"]:
    print(status["text"])

