import requests
import xlwt
from bs4 import BeautifulSoup
from lxml import etree

baseurl = "https://huggingface.co/models?"

if __name__ == '__main__':
    #初始化拼接请求url
    url = ''
    #初始化结果列表
    result_list = []
    #封装的api前缀
    base_api = "https://api-inference.huggingface.co/models/"

    model_url = "https://huggingface.co/"
    # 定义目标关键词
    target_keyword = "Unable to determine this model’"

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('模型信息', cell_overwrite_ok=True)
    col = ('api地址','概述', '是否可以调用', '实例', '实例结果')
    for i in range(0, 5):
        sheet.write(0, i, col[i])
    # 定制请求头,加入cookie防止网站出现cookie反爬
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/110.0.0.0 Safari/537.36',
        'cookie': '_ga=GA1.2.133465926.1678101368; __stripe_mid=baedc115-44cf-4a88-9fad-6a4a60ce605d4fb1de; '
                  '_gid=GA1.2.96097041.1678886809; '
                  'token'
                  '=QyPZhhrAGBQSTtuDthTVaXGMpPkxxINtdGdfXUSrGnBcfHcCujAmoMTDPtzsXbScjZYJpGpEwYfvvKnSOLvUtInUVeRzQZeyNTxHdPxNGuivuyLNRMRXKirUCMwqCmDV; __stripe_sid=2e95b33e-c4bd-49d4-93db-a47f86ea5754256440; _gat=1',
        'referer':'https://huggingface.co/models'
    }

    index = 1
    for i in range(1, 2):
        # 生成每页访问的url
        if i == 1:
            # https://huggingface.co/models?sort=downloads
            url = baseurl + "sort=downloads"
        else:
            url = baseurl + "p=" + str(i) + "?sort=downloads"
        # 发送请求
        response = requests.get(url, headers)
        # 得到响应
        content = response.text
        # 使用过xpath解析html
        html = etree.HTML(content)
        # 找到想要的数据
        tmp_list = html.xpath("/html/body/div/main/div/div/section/div[2]/div/article/a/header/h4/text()")

        for model in tmp_list:
            # 封装每个模型的信息
            model_detail = []
            # 拼接url
            real_url = model_url + model
            model_detail.append(real_url)
            model_response = requests.get(url= real_url, headers = headers)
            # 使用过xpath解析html
            model_html = etree.HTML(model_response.text)
            # 找到想要的数据
            overview = model_html.xpath("/html/body/div[1]/main/div/section[2]/div[3]/div/div/div[2]/a/div/span/text()")
            if len(overview) > 0:
                model_detail.append(overview[0])
            else:
                model_detail.append('None')
            isaction = model_html.xpath("/html/body/div/main/div/section[2]/div[3]/div/div/div[3]/div/text()")

            example = model_html.xpath("/html/body/div/main/div/section[2]/div[3]/div/div/form/label/span/text()")
            print(example)
            if len(isaction) > 0:
                model_detail.append("可以调用")
            else:
                model_detail.append('不可以调用')
            print(model_detail)
            for i in range(3):
                sheet.write(index, i, model_detail[i])
            index +=1

save_path = './excel2表格.xls'
book.save(save_path)
