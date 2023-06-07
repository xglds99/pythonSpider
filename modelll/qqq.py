import json

import requests
import pandas as pd
import numpy as np
import random
from time import sleep
def get_data(keyword, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"}
    url = f'http://piao.qunar.com/ticket/list.json?keyword={keyword}&region=&from=mpl_search_suggest&page={page}'
    res = requests.request("GET", url, headers=headers)
    sleep(random.uniform(1, 2))
    print(res.text)
    try:
        res_json = json.loads(res.text)
        sightLists = res_json['data']['sightList']  # sightList是感兴趣的
        print(sightLists)
        for sight in sightLists:
            name = (sight['sightName'] if 'sightName' in sight.keys() else None)  # 名称
            districts = (sight['districts'] if 'districts' in sight.keys() else None)  # 地址
            star = (sight['star'] if 'star' in sight.keys() else None)  # 星级
            qunarPrice = (sight['qunarPrice'] if 'qunarPrice' in sight.keys() else None)  # 最低价格
            saleCount = (sight['saleCount'] if 'saleCount' in sight.keys() else None)  # 购买人数
            score = (sight['score'] if 'score' in sight.keys() else None)  # 评分
            point = (sight['point'] if 'point' in sight.keys() else None)  # 坐标位置
            intro = (sight['intro'] if 'intro' in sight.keys() else None)  # 介绍
            # print('名称：{0}，地址:{1},星级：{2}，价格:{3},saleCount:{4}，评分:{5},坐标:{6},介绍:{7}'.format(name,districts,star,qunarPrice,saleCount,score,point,intro))
            shuju = np.array((name, districts, star, qunarPrice, saleCount, score, point, intro))
            shuju = shuju.reshape(-1, 8)
            vsc = pd.DataFrame(shuju, columns=['名称', '地址', '星级', '最低价格', '购买人数', '评分', '坐标位置', '介绍'])
            # print(shuju)
            vsc.to_csv('./重庆景点数据.csv', mode='a+', index=False, header=False)  # mode='a+'追加写入
    except Exception as e:
        print(e)
if __name__ == '__main__':
    keyword = "重庆"
    for page in range(1, 2):  # 控制页数
        print(f"正在提取第{page}页")
        sleep(random.uniform(1, 2))
        get_data(keyword, page)