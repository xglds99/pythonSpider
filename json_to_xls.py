import json

import tablib

f = open('douban1.json', 'r', encoding='utf-8', errors='ignore')
rows = json.load(f)
print(rows)
headers = tuple([i for i in rows[0].keys()])
print(headers)
data = []
for row in rows:
    body = []
    for v in row.values():
        body.append(v)
    data.append(tuple(body))
data_xls = tablib.Dataset(*data, headers=headers)
open('data.xls', 'wb').write(data_xls.xls)
