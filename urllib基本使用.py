import urllib.request

url = 'http://www.baidu.com'
response = urllib.request.urlopen(url)
print(type(response))
content = response.read().decode('utf-8')
