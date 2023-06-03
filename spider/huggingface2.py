import json

import requests
import xlwt
from bs4 import BeautifulSoup
from lxml import etree

baseurl = "https://huggingface.co/models?"
model_dict = {
    'Fill-Mask': {"inputs": "The answer to the universe is [MASK]."},
    'Summarization': {
        "inputs": "The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, "
                  "and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each "
                  "side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the "
                  "tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building "
                  "in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. "
                  "Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller "
                  "than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the "
                  "second tallest free-standing structure in France after the Millau Viaduct.",
        "parameters": {"do_sample": False},
    },
    'Question Answering': {
        "inputs": {
            "question": "What's my name?",
            "context": "My name is Clara and I live in Berkeley.",
        }
    },
    'Table Question Answering': {
        "inputs": {
            "query": "How many stars does the transformers repository have?",
            "table": {
                "Repository": ["Transformers", "Datasets", "Tokenizers"],
                "Stars": ["36542", "4512", "3934"],
                "Contributors": ["651", "77", "34"],
                "Programming language": [
                    "Python",
                    "Python",
                    "Rust, Python and NodeJS",
                ],
            },
        }
    },
    'Sentence Similarity': {
        "inputs": {
            "source_sentence": "That is a happy person",
            "sentences": ["That is a happy dog", "That is a very happy person", "Today is a sunny day"],
        }
    },
    'Text Classification': {"inputs": "I like you. I love you"},
    'Text Generation': {"inputs": "The answer to the universe is"},
    'Text2Text Generation': {"inputs": "My name is Sarah Jessica Parker but you can call me Jessica"},
    'Translation': {
        "inputs": "Меня зовут Вольфганг и я живу в Берлине",
    },
    'Zero-Shot Classification': {
        "inputs": "Hi, I recently bought a device from your company but it is not working as advertised and I would "
                  "like to get reimbursed!",
        "parameters": {"candidate_labels": ["refund", "legal", "faq"]},
    },
    'Conversational': {
        "inputs": {
            "past_user_inputs": ["Which movie is the best ?"],
            "generated_responses": ["It's Die Hard for sure."],
            "text": "Can you explain why ?",
        },
    },
    # 'Feature Extraction': "sample1.flac",
    # 'Audio Classification': 'sample1.flac',
    # 'Image Classification': 'cats.jpg',
    # 'Object Detection': 'cats.jpg',
    # 'Image Segmentation': 'cats.jpg'

}
if __name__ == '__main__':
    # 初始化拼接请求url
    url = ''
    # 初始化结果列表
    result_list = []
    # 封装的api前缀
    base_api = "https://api-inference.huggingface.co/models/"

    model_url = "https://huggingface.co/"
    # 定义目标关键词
    target_keyword = "Unable to determine this model’"

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('模型信息', cell_overwrite_ok=True)
    col = ('api地址', '概述', '是否可以调用', '实例', '实例结果')
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
        'referer': 'https://huggingface.co/models'
    }

    index = 1
    x = 1
    for i in range(1, 50):
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
            model_response = requests.get(url=real_url, headers=headers)
            # 使用过xpath解析html
            model_html = etree.HTML(model_response.text)
            # 找到想要的数据
            overview = model_html.xpath("/html/body/div[1]/main/div/section[2]/div[3]/div/div/div[2]/a/div/span/text()")
            if len(overview) > 0:
                model_detail.append(overview[0])
            else:
                model_detail.append('None')
            isaction = model_html.xpath("/html/body/div/main/div/section[2]/div[3]/div/div/div[3]/div/text()")

            # example = model_html.xpath("/html/body/div/main/div/section[2]/div[3]/div/div/form/label/span/text()")
            # print(example)
            if len(isaction) > 0:
                model_detail.append("可以调用")
                # 发送请求拿到结果
                if overview[0] in model_dict:
                    model_detail.append(model_dict[overview[0]])
                    fizai = json.dumps(model_dict[overview[0]])
                    print(model_dict[overview[0]])
                    print("https://api-inference.huggingface.co/models/" + model)
                    model_req_response = requests.post(url='https://api-inference.huggingface.co/models/' + model, headers=headers,
                                                       data=fizai)
                    model_detail.append(model_req_response.text)
                elif 'Feature' in overview[0] or 'Audio' in overview[0]:
                    model_detail.append('sample1.flac')
                    model_detail.append('sample1.flac')
                elif 'Image' in overview[0] or 'Object' in overview[0] :
                    model_detail.append('cats.jpg')
                    model_detail.append('cats.jpg')
                else:
                    model_detail.append('None')
                    model_detail.append('None')
            else:
                model_detail.append('不可以调用')
                model_detail.append('NULL')
                model_detail.append('None')
            print(model_detail)
            for i in range(5):
                sheet.write(index, i, str(model_detail[i]))
            index += 1
            book.save('./' + str(x) + 'excel2表格.xls')
            x += 1