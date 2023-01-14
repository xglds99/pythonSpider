
# get请求


import urllib.request

url = 'http://36.134.96.232:8399/seal/hongxing/getShipForecastPage?appId=ad1f8b6ee4680a954bfe5de939aa677d&pageNum=1&pageSize=98'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56',
    'Cookie': 'JSESSIONID=92FC00A46CFCFA104F9CADDF90CC2799'
}

# (1) 请求对象的定制
request = urllib.request.Request(url=url,headers=headers)

# （2）获取响应的数据
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')

# (3) 数据下载到本地
# open方法默认情况下使用的是gbk的编码  如果我们要想保存汉字 那么需要在open方法中指定编码格式为utf-8
print(content)
with open('sail.json','w',encoding='utf-8') as fp:
    fp.write(content)