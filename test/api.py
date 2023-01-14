# import urllib, urllib2, sys
import urllib.request
import json


host = 'https://jisutqybmf.market.alicloudapi.com/weather/query'
method = 'GET'
appcode = 'c91adb3532c84e8993ee22e3013b363f'

# querys = 'city=%E5%AE%89%E9%A1%BA'
querys = 'city=长沙'
#拼接URL
url = host + '?' + querys

#对象 Request
request = urllib.request.Request(url)

#模拟浏览器去请求
request.add_header('Authorization', 'APPCODE ' + appcode)
response = urllib.request.urlopen(request)
content = response.read()
#解码
info =content.decode()
info = json.loads(info)
print(info['result'])
