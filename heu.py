import requests
from bs4 import BeautifulSoup


class LianJiaSpider():  # 创建链家爬虫类
    def __init__(self):  # 初始化
        self.url = 'https://bj.lianjia.com/chengjiao/pg{0}/'  # 这里{0}表示的是字符串的格式化
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
            'Accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cookie': 'lianjia_uuid=29855287-693f-4acb-b3f0-ae9c6a02baae; '
                      '_jzqy=1.1668045117.1668045117.1.jzqsr=baidu.-; _smt_uid=636c593c.1d9beb1c; '
                      'sensorsdata2015jssdkcross={'
                      '"distinct_id":"1845f3c95af24c-0736b65904ba92-7d5d5474-2359296-1845f3c95b09b0",'
                      '"$device_id":"1845f3c95af24c-0736b65904ba92-7d5d5474-2359296-1845f3c95b09b0",'
                      '"props":{"$latest_traffic_source_type":"&#x76F4;&#x63A5;&#x6D41;&#x91CF;",'
                      '"$latest_referrer":"","$latest_referrer_host":"",'
                      '"$latest_search_keyword":"&#x672A;&#x53D6;&#x5230;&#x503C;_&#x76F4;&#x63A5;&#x6253;&#x5F00'
                      ';"}}; _ga=GA1.2.1510932416.1670594679; select_city=110000; '
                      'lianjia_ssid=b62e57d3-2f2b-4ebd-98a1-bc5b9647f746; '
                      'crosSdkDT2019DeviceId=214vwc-u2h4ea-t7k0m4fxdsadl6u-w0x86ud4z; login_ucid=2000000299536734; '
                      'lianjia_token=2.0012c18cb17ab07003036ca58072dc5316; '
                      'lianjia_token_secure=2.0012c18cb17ab07003036ca58072dc5316; '
                      'security_ticket=pEA2zzIVxhRgw7hwdnKMh7ttKMUTT1SrWrn8qVsBpXKgS/TI6MuDRIvc75o6B'
                      '/9fieZx9Z1zbnaIyKytd0F8ZQZumw109wpk3mlXoGqBBx9bK/eGBkWgW+YhrglTP/A'
                      '+QlIW30CeDtt98k20m0dZallDECfnivmIuzZjBlr0SYw=; '
                      'Hm_lvt_9152f8221cb6243a53c83b956842be8a=1670594677,1672736271; '
                      '_jzqa=1.2072012866109405000.1668045117.1670594677.1672736272.3; _jzqc=1; '
                      '_jzqx=1.1672736272.1672736272.1.jzqsr=clogin.lianjia.com|jzqct=/.-; _jzqckmp=1; '
                      '_gid=GA1.2.830560896.1672736273; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1672737035; '
                      '_jzqb=1.3.10.1672736272.1 '
        }

    def send_request(self, url):  # 发送请求函数
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            return resp

    def parse_html(self, resp):  # 数据解析函数,resp作为解析的参数传入
        html = resp.text
        print(html)
        bs = BeautifulSoup(html, 'lxml')
        ul = bs.find('ul', class_='listContent')
        print(ul)
        li_list = ul.find_all('li')
        # li_list=bs.find_all('li')
        print(len(li_list))

    def save(self):  # 保存数据
        pass

    def start(self):  # 启动爬虫程序
        for i in range(0, 2):  # 产生1-2的整数，不包含2
            full_url = self.url.format(i)  # 这里进行字符串的拼接操作，因为之前url字符串中有个占位符{0}
            print(full_url)
            resp = self.send_request(full_url)
            # print(resp.text)
            self.parse_html(resp)


if __name__ == '__main__':
    lianjia = LianJiaSpider()  # 创建链家爬虫的对象
    lianjia.start()
