import requests
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

    # 定制请求头,加入cookie防止网站出现cookie反爬
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) '
                      'Chrome/110.0.0.0 Safari/537.36 ',
        'cookie': '_ga=GA1.2.1567546240.1678100568; _gid=GA1.2.2114067746.1678100568; '
                  '__stripe_mid=4ffa3d97-66a6-4bfd-8561-e456f94e4adac00681 '
    }

    f = open('./model.txt', mode='w', encoding='utf-8', )

    for i in range(1, 4886):
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
            # 保存至model.txt文件，
            f.write(base_api + model + '\n')

    f.close()
    # result_list.append(tmp_list)
    # print(result_list)
