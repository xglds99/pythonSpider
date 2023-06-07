from lxml import etree

import requests

base_url = 'https://huggingface.co/docs/api-inference/detailed_parameters#summarization-task'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/110.0.0.0 Safari/537.36',
    'cookie': '_ga=GA1.2.133465926.1678101368; __stripe_mid=baedc115-44cf-4a88-9fad-6a4a60ce605d4fb1de; '
              '_gid=GA1.2.96097041.1678886809; '
              'token'
              '=QyPZhhrAGBQSTtuDthTVaXGMpPkxxINtdGdfXUSrGnBcfHcCujAmoMTDPtzsXbScjZYJpGpEwYfvvKnSOLvUtInUVeRzQZeyNTxHdPxNGuivuyLNRMRXKirUCMwqCmDV; __stripe_sid=2e95b33e-c4bd-49d4-93db-a47f86ea5754256440; _gat=1',
    'referer': 'https://huggingface.co/models'
}

response = requests.get(url=base_url, headers=headers)
content = response.text
with open('1.html', 'w', encoding='utf-8') as f:
    f.write(content)
html = etree.HTML(content)
# 找到想要的数据
tmp_list = html.xpath("/html/body/div/main/div[1]/div[2]/div/div[1]/div[*]/div/pre")
for i in tmp_list:
    print(i)
