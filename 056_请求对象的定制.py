import urllib.request

url = 'https://www.baidu.com'

# url的组成
# 请求对象的定制可以解决ua反爬

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44'
}

request = urllib.request.Request(url,headers = headers)
response = urllib.request.urlopen(request)

content = response.read().decode('utf-8')
print(content)


