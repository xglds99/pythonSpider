import json

import requests
import xlwt

# https://api.smb.museum/search/?q=Rembrandt+Harmensz+van+Rijn+&lang=de&limit=15&offset=0
url = 'https://api.smb.museum/search/?q=Adolph+Menzel&lang=de&limit=15&offset='
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('馆藏信息', cell_overwrite_ok=True)
col = ('作者', '作品名', '年代', '作品类型', '馆藏信息', '图片地址', '链接')
for i in range(0, 7):
    sheet.write(0, i, col[i])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                  'Safari/537.36 Edg/110.0.1587.63 ',
    'origin': 'https://recherche.smb.museum',
    'referer': 'https://recherche.smb.museum/',
    'upgrade-insecure-requests': '1',
    'sec-fetch-user': '?1',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
    'sec-ch-ua-mobile': '?0',
    'content-type': 'application/json',
}
data = {
    "q_advanced": [
        {
            "operator": "AND",
            "field": "attachments",
            "q": "true"
        },
        {
            "operator": "AND",
            "field": "collectionKey",
            "q": "KK*"
        }
    ]
}
# /id/作者姓名
photo_dianji = "https://recherche.smb.museum/detail/"
index = 0
for p in range(133, 153):
    response = requests.post(url=url + str(p * 15), data=json.dumps(data), headers=headers)
    content = response.text
    obj = json.loads(content, encoding='utf-8')
    # 取出馆藏信息
    infos = obj.get("objects")
    print(infos)
    # https://api.smb.museum/v1/graphql
    photo_url = "https://api.smb.museum/v1/graphql"
    info_lists = []
    ids = []
    for i in range(15):
        info = []
        involvedParties = ''
        if infos[i].get("involvedParties"):
            involvedParties = infos[i].get("involvedParties")[0]
        else:
            involvedParties = 'None ('
        name = involvedParties[0: involvedParties.find('(') - 1]
        info.append(name)
        titles = ''
        if infos[i].get("titles"):
            titles = infos[i].get("titles")
            info.append(titles)
        else:
            titles = 'None'
            info.append("None")
        info.append(infos[i].get("dating"))
        info.append(infos[i].get("technicalTerm"))
        info.append(infos[i].get("collection"))
        if titles != 'None':
            info.append(photo_dianji + str(infos[i].get("id")) + "/" + infos[i].get('titles')[0].replace(' ', '-'))
        else:
            info.append(0)
        # 拼接图片地址
        ids.append(infos[i].get("id"))
        # info.append(photo_base + id_photo_map[id] + '_300x300.jpg')
        info_lists.append(info)
    # 第一行作者，第二行作品名 第三行年代，第四行作品类型 第五行馆藏信息

    data1 = {
        "operationName": "FetchPrimaryAttachmentsForObjects",
        "query": "query FetchPrimaryAttachmentsForObjects($object_ids: [bigint!]!) {\n  smb_objects(where: {id: {_in: $object_ids}}) {\n    id\n    attachments(order_by: [{primary: desc}, {attachment: asc}], limit: 1) {\n      attachment\n    }\n  }\n}\n",
        "variables": {
            "object_ids": ids
        },
    }
    p_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                      'Safari/537.36 Edg/110.0.1587.63 ',
        'origin': 'https://recherche.smb.museum',
        'referer': 'https://recherche.smb.museum/',
        'upgrade-insecure-requests': '1',
        'sec-fetch-user': '?1',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?0',
        'content-type': 'application/json',
        # 'content-length': '446',
        'accept': '*/*'
    }
    # 获取图片地址
    p_response = requests.post(url=photo_url, data=json.dumps(data1), headers=p_headers)
    photo_ids = json.loads(p_response.text, encoding='utf-8').get("data").get("smb_objects")
    id_photo_map = {}
    photo_base = "https://recherche.smb.museum/images/"
    for smb in photo_ids:
        photo_path = smb.get("attachments")[0].get("attachment")
        id_photo_map[smb.get("id")] = photo_path[0: photo_path.find('.')]

    for i in range(15):
        id = infos[i].get("id")
        info_lists[i].append(photo_base + id_photo_map[id] + "_300x300.jpg")

    print(info_lists)
    for i in range(15):
        m = info_lists[i]
        for j in range(7):
            sheet.write(i + 1 + index, j, m[j])
    index += 15
save_path = './excel1表格.xls'
book.save(save_path)
