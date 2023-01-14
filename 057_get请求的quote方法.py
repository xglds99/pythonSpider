import urllib.request
import urllib.parse


url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd='

name = urllib.parse.quote('周杰伦')

url = url + name
headers = {
    'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44'
}
request = urllib.request.Request(url, headers = headers)
response = urllib.request.urlopen(request)
content = response.read()
print(content)
