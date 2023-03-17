# (1) 请求对象的定制
# （2）获取网页的源码
# （3）下载


# 需求 下载的前十页的图片
# https://sc.chinaz.com/tupian/qinglvtupian.html   1
# https://sc.chinaz.com/tupian/qinglvtupian_page.html

import urllib.request
from lxml import etree
import os


def create_request(page):
    if (page == 1):
        url = 'https://sc.chinaz.com/tupian/qinglvtupian.html'
    else:
        url = 'https://sc.chinaz.com/tupian/qinglvtupian_' + str(page) + '.html'

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "sc.chinaz.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/106.0.0.0 Safari/537.36',
        "Cookie": 'cz_statistics_visitor=e9581725-4fb4-74c4-d588-c78adf09ecfe; '
                  'Hm_lvt_398913ed58c9e7dfe9695953fb7b6799=1670595697; __bid_n=184f7435d577e3e9604207; '
                  'FEID=v10-1ae3823c6f141a09529982f28aa3351e33a9b2db; __xaf_fpstarttimer__=1670595698138; '
                  '__xaf_ths__={"data":{"0":1,"1":86400,"2":60},"id":"190279ab-2e58-4dc3-8eb7-a5ec3b9102d1"}; '
                  '__xaf_thstime__=1670595698386; '
                  'FPTOKEN=f6SH+DRSjGZhSuUmLvYW815SZbytja6CKulTZicEyub5Vynm3jGdaNMt2Y7eBYr6HlXbBtdTgu+OExlovUCCK'
                  '/y6sOOm9RZSskoylwk+x7JbtARw3fOHnIfsUjvM32ESwstu7vbL1AnwcMmRAnMoV0VQ9eVydBIpYL/mwye1Eq8gw2JtUDEWD'
                  '/zRQ8fmZDYg+2GY9+yKW2y2CHh4Ea7JXkS07QOBt8iHrtxVo0BZVufcJ82Cc28v7Ivd7VUWRkiiDuxQ+NkZD5OI'
                  '/HYxEfu6PrdJqFCfKkiYLZeXfgU9O5xQHRZEGaAsVsYP6E1788oDbiSAQo8NC7ySrLiqQW6kNq8X8'
                  '/IqJ8sN6fCfBW8TgxgWmVKgmLHa4b5uIWZ5bwOr6wZMj0wpTrhJKpvc3MpwhA==|HS6huz1MecBfJq9EYvcAJ6ico9Z'
                  '+raYorxEtkuZROGM=|10|6345e27de084e23ee92aab2924c2a090; __xaf_fptokentimer__=1670595698546; '
                  'Hm_lvt_ca96c3507ee04e182fb6d097cb2a1a4c=1670597839; '
                  'Hm_lpvt_ca96c3507ee04e182fb6d097cb2a1a4c=1670597839; '
                  'ucvalidate=859d9826-d5e7-b987-7a75-e8f9e6de1e38; CzScCookie=cd4f1345-1455-e276-2069-7c50ff98aaa1; '
                  'Hm_lpvt_398913ed58c9e7dfe9695953fb7b6799=1670597870 ',
        "Referer": "https://uc.chinaz.com/",
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }

    request = urllib.request.Request(url=url, headers=headers)
    return request


def get_content(request):
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    return content


def down_load(content):
    #     下载图片
    # urllib.request.urlretrieve('图片地址','文件的名字')
    # with open("zz.html", "w", encoding="utf-8") as f:
    #     f.write(content)
    # return 0
    tree = etree.HTML(content)
    print(os.path.basename(__file__))

    name_list = tree.xpath('//div[@class="tupian-list com-img-txt-list"]//div['
                           '@class="item"]/img/@alt')
    # 一般设计图片的网站都会进行懒加载
    src_list = tree.xpath('//div[@class="tupian-list com-img-txt-list"]//div['
                          '@class="item"]/img/@data-original')
    print(len(name_list))
    print(len(src_list))
    if not os.path.exists("loveImg"):
        print("Could not find loveImg,create a new one")
        os.makedirs("loveImg")
    for i in range(len(name_list)):
        name = name_list[i]
        src = src_list[i]
        print(src)
        url = 'https:' + src
        urllib.request.urlretrieve(url=url, filename='./loveImg/' + name + '.jpg')


if __name__ == '__main__':
    start_page = int(input('请输入起始页码'))
    end_page = int(input('请输入结束页码'))

    for page in range(start_page, end_page + 1):
        # (1) 请求对象的定制
        request = create_request(page)
        # （2）获取网页的源码
        content = get_content(request)
        # （3）下载
        down_load(content)
