import json
import time

import requests
import xlwt
from bs4 import BeautifulSoup
from lxml import etree
import os
import zipfile
import openai

print(os.getcwd())
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

inout_dict = {
    "Fill-Mask": {
        "input": ["string"],
        "output": ["dict<string,float,int,string>"],
    },
    "Summarization": {
        "input": ["string", "dict<string>"],
        "output": ["string"],
    },
    "Question Answering": {
        "input": ["string", "string"],
        "output": ["dict<float,int,int,string>"],
    },
    "Table Question Answering": {
        "input": ["string", "dict<list,list,list,list>"],
        "output": ["dict<string,list,list,string>"],
    },
    "Sentence Similarity": {
        "input": ["string", "list"],
        "output": ["list"],
    },
    "Text Classification": {
        "input": ["string"],
        "output": ["dict<string,float>"]
    },
    "Text Generation": {
        "input": ["string"],
        "output": ["dict<string,float,string>"],
    },
    "Text2Text Generation": {
        "input": ["string"],
        "output": ["dict<string,float,string>"],
    },
    "Token Classification": {
        "input": ["string"],
        "output": ["dict<string, float, string, int, int>"]
    },
    "Named Entity Recognition (NER)": {
        "input": ["string"],
        "output": ["dict<string, float, string, int, int>"]
    },
    "Translation": {
        "input": ["string", "dict<string>"],
        "output": ["string"],
    },
    "Zero-Shot Classification": {
        "input": ["string", "dict"],
        "output": ["string", "list", "list"]
    },
    "Conversational": {
        "input": ["string", "list", "list"],
        "output": ["string", "dict", "list"]
    },
    "Feature Extraction": {
        "input": ["string", "list"],
        "output": ["list", "float"]
    },
    "Automatic Speech Recognition": {
        "input": ["audio"],
        "output": ["string"]
    },
    "Audio Classification": {
        "input": ["audio"],
        "output": ["dict"]
    },
    "Image Classification": {
        "input": ["image"],
        "output": ["float", "string"]
    },
    "Object Detection": {
        "input": ["image"],
        "output": ["string", "float", "dict"]
    },
    "Image Segmentation": {
        "input": ["image"],
        "output": ["string", "float", "string"]
    }
}


def get_description(model_name):
    openai.organization = "org-YxfRI9xrAhzz29hv1q7ETQlE"
    openai.api_key = "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"
    q = "Get the description of the api:https://huggingface.co/model/" + model_name
    rsp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": q}
        ]
    )
    return rsp.get("choices")[0]["message"]["content"]


if __name__ == '__main__':
    # 初始化拼接请求url
    url = ''
    # 初始化结果列表
    result_list = []
    os.chdir("../data")
    # 封装的api前缀
    base_api = "https://api-inference.huggingface.co/models/"

    model_url = "https://huggingface.co/"
    # 定义目标关键词
    target_keyword = "Unable to determine this model’"
    proxy = {
        "http":"127.0.0.1:7890"
    }
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
    for i in range(1, 2):
        # 生成每页访问的url
        if i == 1:
            # https://huggingface.co/models?sort=downloads
            url = baseurl + "sort=downloads"
        else:
            url = baseurl + "p=" + str(i) + "?sort=downloads"
        # 发送请求
        response = requests.get(url, headers, proxies =proxy)
        # 得到响应
        content = response.text
        # 使用过xpath解析html
        html = etree.HTML(content)
        # 找到想要的数据
        tmp_list = html.xpath("/html/body/div/main/div/div/section/div[2]/div/article/a/header/h4/text()")

        for model in tmp_list:
            print(model)
            dirpath = model
            if model.count('/') > 0:
                dirpath = model.replace('/', '')
            os.mkdir(dirpath)
            os.chdir("./" + dirpath)
            os.mkdir("env")
            os.mkdir("test")
            os.mkdir("exec")
            os.mkdir("lib")
            # 封装每个模型的信息
            model_detail = []
            # 拼接url
            real_url = model_url + model
            model_response = requests.get(url=real_url, headers=headers, proxies = proxy)
            # 使用过xpath解析html
            model_html = etree.HTML(model_response.text)
            # 找到想要的数据
            overview = model_html.xpath("/html/body/div[*]/main/div[*]/section[2]/div[*]/div/div/div[2]/a/div/span/text()")
                                       # "/html/body/div/main/div[2]/section[2]/div[5]/div/div/div[2]/a/div/span"
            print(overview)
            "/html/body/div[1]/main/div[2]/section[2]/div[3]/div/div/div[2]/a/div/span"
            # isaction = model_html.xpath("/html/body/div/main/div/section[2]/div[3]/div/div/div[3]/div/text()")
            # example = model_html.xpath("/html/body/div/main/div/section[2]/div[3]/div/div/form/label/span/text()")
            # print(example)
            if len(overview) > 0 and overview[0] in inout_dict:
                print(overview[0])
                # 拼装config文件
                config_json = {"name": model, "description": "", "type": "0", "duration": "0",
                               "control_output_args": [{}], "data_input_args": [], "data_output_args": [],
                               "execution": {
                                   "post_url": "https://api-inference.huggingface.co/models/",
                                   "type": ""
                               }}
                # 封装输入信息
                description = ""
                config_json["description"] = description
                for i, type1 in enumerate(inout_dict[overview[0]]["input"]):
                    config_json["data_input_args"].append({"name": "inputs", "id": i + 1, "type": type1, })
                # 封装输出信息
                for j, type2 in enumerate(inout_dict[overview[0]]["output"]):
                    config_json["data_output_args"].append({"name": "outputs", "id": j + 1, "type": type2, })
                # 封装完配置文件信息，开始下载readme.md
                post_url = config_json["execution"]["post_url"]
                config_json["execution"]["post_url"] = post_url + model
                if "Audio" in overview[0] or "Image" in overview[0] or "Object" in overview[0] or "Automatic" in \
                        overview[0]:
                    config_json["execution"]["type"] = "huggingface-binary"
                else:
                    config_json["execution"]["type"] = "huggingface-text"
                model_req_response = requests.get(url=model_url + model,
                                                  headers=headers,
                                                  proxies = proxy)
                f1 = open(dirpath + ".config", 'w', encoding='utf8')
                f1.write(str(config_json))
                f1.close()
                markdown_html = etree.HTML(model_req_response.text)
                readmeurl = markdown_html.xpath("/html/body/div/main/div[1]/header/div/div[2]/div[1]/a[2]/@href")
                # /facebook/dino-vits8/blob/main/README.md
                print(model_url + model + "/resolve/main/README.md")
            readmemd = requests.get(url=model_url + model + "/resolve/main/README.md", proxies = proxy)
            f = open("readme.md", 'w', encoding='utf8')
            f.write(readmemd.text)
            f.close()
            os.chdir("../")
        time.sleep(20)
