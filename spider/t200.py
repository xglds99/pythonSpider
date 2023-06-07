import requests
from lxml import etree
import csv
import time

url = 'https://piao.qunar.com/ticket/list.htm?keyword=青岛&region=null&from=mps_search_suggest&page='
baseurl = 'https://piao.qunar.com'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'cookie': 'SECKEY_ABVK=ixgOEINPMdoruxdvzhVekGLcKz4yYWtbXkuNkk/qlFA=; BMAP_SECKEY=aVX7rcMHAXJL76ICtRNadK6GDMUS4rciJ18Be9UfI8ZK21tA_TpQTYSMJ4aCaMmKoOnWuJRe_hBr0VAl12hCjV2UgwpI6X7XjEYpE45lJeksdVa08aek-gPwFMfbQpIX4IqHAftVEpVAe9b3xZUOCFrBTybr9EiRyBzpN9mcCErkX4Bf59rW9d0STwqyMVsK; QN1=00006300306c4f3add705437; QN300=s=baidu; QN99=8865; QunarGlobal=10.68.38.173_d63949a_1875ea7deff_-5a1d|1680922030948; QN205=s=baidu; QN277=s=baidu; QN601=2cc661fe7ec382d30e93998fee27fbc3; QN269=A9520690D5B711EDB228FA163EE16C88; QN48=9e51ca74-11c3-4f17-a67b-7cbb8ddd1093; fid=a7c06760-7142-453f-88d2-9e4128d539d9; QN57=16809220377460.34514589154593756; QN67=215548,1366; qunar-assist={"version":"20211215173359.925","show":false,"audio":false,"speed":"middle","zomm":1,"cursor":false,"pointer":false,"bigtext":false,"overead":false,"readscreen":false,"theme":"default"}; QN163=0; Hm_lvt_15577700f8ecddb1a927813c81166ade=1680922038,1680953017; ctt_june=1654604625968##iK3wWsgnahPwawPwas3nXP3wESDwXKHhXsoTW2ihWPX=WKvOWDjOWRTDaKvOiK3siK3saKjmaR2AasvnVR2mVuPwaUvt; ctf_june=1654604625968##iK3wWKt8auPwawPwasDOWK2AWRfGVKPOWS0IVK0IXSkRVDa8XKGRVR28aSaNiK3siK3saKjmaR2AasvnVR2NVuPwaUvt; ariaDefaultTheme=null; cs_june=59ce994d9abbfcb150e48c395047feadee27586b048818b4809afc260c5705ec6f5e2aaba5489363270918193206c4efecae5320c037b4706149249f2755a6fbb17c80df7eee7c02a9c1a6a5b97c117922eecca8546232252c8d1c06c5fb43b65a737ae180251ef5be23400b098dd8ca; QN271AC=register_pc; QN271SL=4e17148f379a5061f376bcd050769178; QN271RC=4e17148f379a5061f376bcd050769178; _q=U.mtxcdmg5240; csrfToken=iclPYpjqAyKx33wOTCCX2oZKvamjeAqe; _s=s_XNWL7OTFTU2OI6PKF3NKTWATG4; _t=28125323; _v=5vBlWNrjIG_vIZlBw02Re4VXV0Uj7wwV5S7s2sU3Vb4hB82-cqDUIJGT6-YqVzzePiL0cEftH-h0UNXR3oJ0oa3BZ52r3622obTSbBxpQinBqGnhnLIKaCQ0X7IM6oLadpjRsjNfHY2IhScu4GF9wDXTDbUh-De_lhk-qJZ3E6bQ; QN43=""; QN42=wdhc0134; QN44=mtxcdmg5240; QN267=01802938525084cc30b; _i=ueHd8pLGrXk7eEGA-rASgOTHnf0X; _vi=PHa1MzPInxMeRdUNsCEceG9v6UoGHh3l2mtQ352ds3F6SB95nE7ST7HKlB2mOGddRpkii3I4rg3rrbaEie2G_bU03ezqvcFUnWNIcwgBkEb8vv5gTt28_d-knUeStbmwFYU538iCs5Sb8I_fadI0Rn0O4Nbk8S2ahoLFyRxIEMUe; QN58=1680953016498|1680953037364|2; JSESSIONID=65492CE5D1F9CFEB9397D3C834F9C389; __qt=v1|VTJGc2RHVmtYMStxNGkxMk9oT3JNSU5MM3B6Mk9UMmdxalFlOGZDQXNXTjdQakJTelRJbWVQbnBLcFdKazBGWlJuSWZOMUNXQ2ZiUEN5aXlUQzI5WnpVZHc4RTh4OTVzSzBENE9aMDhGQjR5aXhmalhCTjhsUXpZdTlSSFAzdUxyTWNkd3NLNktzRG5vS3R1Zm5ZbS9lTUdvcmFBaVBsNG1zTnFIMUV5YlJjPQ==|1680953037618|VTJGc2RHVmtYMTlYcStZSGJVb1orTTd2a3NUVjNnc2M5M2dUV1Y3eHRxYWUyV0pLWWIyZmpySE51aGZNL1pVbTUyZ2dPdWROYUNQNE5OVkpua25EdEE9PQ==|VTJGc2RHVmtYMSswN0I0dnRiQXFMWFVvdnBtZnZTMG1IQTVScVkra0owWkhlenBPZzhzSld6UTQ3S053NDhRcTRyYkliRjloQzM4WnFRdFpMTks1YUNHeDFic0N0VXk5RW5yR1RMRlFmbnJqM2FUTW9sa05DMkUxWmhOZ3dEejlrVExzZzU4ZmhucGcxcU1kNXRIWkpGaHpwdExTc3RrUllzTThrS3U5SS9OK3hzaGxDQnRoaU00MmJQQnQxNlp1UDJlSG0wM294RnYveHV0RXo1ZlptNmRCczNid0dmU1ZnRDhJdjhPU3htb3hwK3p3V2FKNXQ2VXRNbmRiVGp0NlVtYnhQWUJuVjc2dHBWOUtaOERHZ3J0UldsRW1lS3FaNUFGcUNxQ0Z3NVNHTXlleWxXeXRHZmt0dnRNYXBVNnRsd0s2alRHcnRSNkpEM1Znd2czSjFHblJ3QjJLOFBzazNONHQxb3NDWTA4Q3UyV0NMcjRTbDBQc3V1SUFQcUQzTlVpdmRPSFdVTlh5VVJPL0Vja2V4eS9JQ3I4bWJHUHBEdWtXQldyYUJObVducHZ5bDQxRzFrUVBzQWROLzRoc3ZKSVF4cFVTTTRrdFFWY3RLSUZPU3NtS0dYZVd1ZDI1R0lmaHg4bzhvL2FWQVVKUk5peURBUTFUTkpTSFlPYnRJUnNzSVdhRG5XRGhycGg0RWUxL0tMWFlNclNBaFpsYTE4SGlxcjFLT1hjbUxPVDZ0V2RwbUNRb2thMWhSOXc4UGEvVk5GL005UnB5V1RnSXR3OGdOUFkzT0lGd3lGRUM0NWpROEI5WkR6UlRMcUU4THMzZy9CZ3VSNzJVd1BCdEwwMFc2VGl1U2U1UThEaHJaa1dKam0zdzRtbTFVNE5aRlhwa3IzZk5FaTh0VTN2ZS9BYUxWaUZkUEhWRU1uNlNpMTlJQ1RvRjBLMHV6RzdBVGJQR2crWWJCaWgwUVRwbTlFaUhvZnRacVhEVVdsMkprTFdDSkFZbWk3Z3ZPTHVy; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1680953038; QN271=03a70b36-4250-4b80-b478-550a42763eb8',
    'referer': 'https://www.qunar.com/'

}
# 使用代理ip
proxy = {
    'http': '58.57.170.154:9002',
    'http': '112.6.178.53:8085',
    'http': '58.57.170.146:9002',
    'http': '106.75.86.143:1080',
    'http': '112.6.174.110:9091',
    'http': '123.130.115.217:9091',
    'http': '119.166.232.228:9091',
    'http': '112.250.110.172:9091',
    'http': '27.209.130.99:9091',
    'http': '60.210.40.190:9091',
    'http': '210.5.10.87:53281',
    'http': '182.139.110.14:9000',
    'http': '27.42.168.46:55481',
    'http': '210.5.10.87:53281'
}
file = open("data2.csv", "a", encoding='utf-8', newline="")
writer = csv.writer(file)
writer.writerow(["名称", "星级", '地址', '热度', '销量', '价格', '评论数量'])  # 写入逗号
for i in range(1, 55):
    print('第' + str(i) + '页')
    response = requests.get(url=url + str(i), headers=headers, proxies=proxy)
    # response = requests.get(url = url + str(i), headers = headers)
    html = etree.HTML(response.text)
    # 获取名称列表
    name_list = html.xpath('//*[@id="search-list"]/div[*]/div/div[2]/h3/a/text()')
    # //*[@id="search-list"]/div[*]/div/div[2]/h3/a
    print(name_list)
    detail_list = html.xpath('//*[@id="search-list"]/div[*]/div/div[2]/h3/a/@href')

    # 获取星级
    star_list = html.xpath('//*[@id="search-list"]/div[*]/div/div[*]/div/div[*]/span[1]/text()')
    print(star_list)
    # 获取地点
    address_list = html.xpath('//*[@id="search-list"]/div[*]/div/div[*]/div/div[*]/span[*]/a/text()')
    print(address_list)
    # 获取热度
    hot_list = html.xpath('//*[@id="search-list"]/div[*]/div/div[2]/div/div[1]/div/span[1]/em/span/text()')
    print(hot_list)
    # 获取销量
    sales_list = html.xpath('//*[@id="search-list"]/div[*]/div/div[*]/table/tr[4]/td/span/text()')
    for u in range(15):
        sales_list.append(0)
    print(sales_list)
    # 获取价格
    prices_list = html.xpath('//*[@id="search-list"]/div[*]/div/div[3]/table/tr[1]/td/span/em/text()')
    print(prices_list)
    for u in range(15):
        prices_list.append(0)
    # 获取用户评论量
    detail_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        'cookie': 'SECKEY_ABVK=ixgOEINPMdoruxdvzhVekH2RDQ+UyFQ9yLWWH7d+B/g=; BMAP_SECKEY=aVX7rcMHAXJL76ICtRNadIGOMZ_cN6Wv4Vjf_PAutoH_PJmcwN7kkKb8tnaOcttmS0RZs3MzeiZuI1at5nq35p4GfXm173-SMLkohyv_jB-fh59f3w3RA-oaOfNaMAa2AIHnBXa4LqYyuzcxowhBi-QqvvyR9G5840g5mHFGOTjuZtrPJuLZonVLezf3_SV8; QN1=00006300306c4f3add705437; QN300=s=baidu; QN99=8865; QunarGlobal=10.68.38.173_d63949a_1875ea7deff_-5a1d|1680922030948; QN205=s=baidu; QN277=s=baidu; QN601=2cc661fe7ec382d30e93998fee27fbc3; QN269=A9520690D5B711EDB228FA163EE16C88; QN48=9e51ca74-11c3-4f17-a67b-7cbb8ddd1093; fid=a7c06760-7142-453f-88d2-9e4128d539d9; QN57=16809220377460.34514589154593756; ctt_june=1654604625968##iK3wWsgnahPwawPwas3nXP3wESDwXKHhXsoTW2ihWPX=WKvOWDjOWRTDaKvOiK3siK3saKjmaR2AasvnVR2mVuPwaUvt; ctf_june=1654604625968##iK3wWKt8auPwawPwasDOWK2AWRfGVKPOWS0IVK0IXSkRVDa8XKGRVR28aSaNiK3siK3saKjmaR2AasvnVR2NVuPwaUvt; ariaDefaultTheme=null; cs_june=59ce994d9abbfcb150e48c395047feadee27586b048818b4809afc260c5705ec6f5e2aaba5489363270918193206c4efecae5320c037b4706149249f2755a6fbb17c80df7eee7c02a9c1a6a5b97c117922eecca8546232252c8d1c06c5fb43b65a737ae180251ef5be23400b098dd8ca; QN271AC=register_pc; QN271SL=4e17148f379a5061f376bcd050769178; QN271RC=4e17148f379a5061f376bcd050769178; _q=U.mtxcdmg5240; csrfToken=iclPYpjqAyKx33wOTCCX2oZKvamjeAqe; _s=s_XNWL7OTFTU2OI6PKF3NKTWATG4; _t=28125323; _v=5vBlWNrjIG_vIZlBw02Re4VXV0Uj7wwV5S7s2sU3Vb4hB82-cqDUIJGT6-YqVzzePiL0cEftH-h0UNXR3oJ0oa3BZ52r3622obTSbBxpQinBqGnhnLIKaCQ0X7IM6oLadpjRsjNfHY2IhScu4GF9wDXTDbUh-De_lhk-qJZ3E6bQ; QN43=""; QN42=wdhc0134; _i=ueHd8pLGrXk7eEGA-rASgOTHnf0X; _vi=PHa1MzPInxMeRdUNsCEceG9v6UoGHh3l2mtQ352ds3F6SB95nE7ST7HKlB2mOGddRpkii3I4rg3rrbaEie2G_bU03ezqvcFUnWNIcwgBkEb8vv5gTt28_d-knUeStbmwFYU538iCs5Sb8I_fadI0Rn0O4Nbk8S2ahoLFyRxIEMUe; QN67=1366,215548; qunar-assist={"version":"20211215173359.925","show":false,"audio":false,"speed":"middle","zomm":1,"cursor":false,"pointer":false,"bigtext":false,"overead":false,"readscreen":false,"theme":"default"}; QN44=mtxcdmg5240; QN267=018029385250ef62882; QN58=1680953016498|1680953244385|6; Hm_lvt_15577700f8ecddb1a927813c81166ade=1680922038,1680953017,1680953245; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1680953245; QN271=b792a676-b435-40b1-aa3d-8fbbe5f37276; JSESSIONID=868A02F751A995F03832FB2F6CEC5555; __qt=v1|VTJGc2RHVmtYMStPL25rY210Q3luOTBBTFRWTEtFVWFrTEVrSi83M05HTzRuUUVjWEJtQ0VpUmp6ajNldHdRSzB3NXlIKy9VSE1vRWVRRDAzQ3NLY2p4Vy8xMEdNbkJtcnBYdEZTS0h6QndZMUlYN1RRUXlUYmpFSXVzWWlZR3phb1NaY0t4bEdmczJMWUtya29BdmxndlhTOEFZNGJaZGZOaU4ybUtiQkZWWUFGaDVRb0JlSnV5RURwWlRIa3Vo|1680953245264|VTJGc2RHVmtYMTltM0gzOXdEcVI3UExaTU4xNnlUVENtYjZuMjV4UHpITDhzaGY4SmdvczJPWGpmc3JqT3hNR0xVOE9vVTErb0xOYVljRm1MRnR1NlE9PQ==|VTJGc2RHVmtYMTh0M1JYT1NTMlByWFcvYVkyUS8yQVEzaUFRT0ZJREhQL2xsK1BZV1diRzhGRTNrQktZK0pCMVA3KzVFYWlpOVdKeWRSNXNJS1ZydU5IYjJqUnJPZzhqWUo4VVBUcVYzeFVWektOSHlYMlI5STVkbDR6a2R4a2RQa0pUZzRkZ1J5TjIwVTg2WVFKM1AyS09EZlUweVFhdkFHdkR4RS9ZZWJneE0rU2svUHA4SjdPd3ZyWWV4NkhxanNwUkJ0WWxUeUhsMWZzcGV6ZXlmandNckhrY2xnQWxyUmRaZkI3WjlmU2U2MmY1V1U4enJiYm84d3A2V2FuMkU4eCtnTFJ1UWZWRzdwQlNhZWUxUzZCNEVVZ1M2Z0pmZEsvd0FQK09pT3g0c0RqZzArZ0xMeS9rUDVBZXdzTFdhQ0hiTkRQVkVzR2RHR1l1WmMxVlBjZ01BemRESHdmUUd4UFZJMVA3ZGtvWkI3RzdlRWxMUkNkT3o5dTl2SytBUDg4NTdVSVNTaDMyQjJ6UjFtZWo2QXFJVlRtZlRBUnRPUHN5dnpEY3RZMkZCdU82K1pCRjNCQ3FlM0hRRXlnNUpLekNwZFZOMGI3SmJOSjR5YVR0bHBKejczNVJnYmMrcnpiZkhGRW55NWh6UVBralExM25ESGt6RTB3Y3E3ajlUNHAzUjM5VTJzbFJiMlFudlVKQXFMcGdmbmhZdkJaMUNYTnJCclZqbnVTZWpra0dRNXRDSzhuM25XKzVVUm5nZXZZU1U0UE1rMWxaUkZSZFAzNnA1UW14Z0ZaWG81VUpWYW45Z0dVTzloaUkxQk1BekZjOURYVll0dGVJRTVTMzFvcVBpb0Yyb282Q0drcTkxVFdhMDc2SWh2UE5RVlZ4QVUyUDZpN0cxRkpMbFJJQzVFU3VBdjlobzM2MVFjS1FKWFBWa2ZXcWtaeFl0b2lTYmQ0SldzYzJXTE5aTW1OUUZiUzc2QStURHY0QVdEbFlwTlpuQVgvaFZoMmJJZElv'
    }
    comment_list = [0 for j in range(15)]
    for k, deatil in enumerate(detail_list):
        detail_response = requests.get(url=baseurl + deatil, headers=detail_headers, proxies=proxy)
        # detail_response = requests.get(url = baseurl + deatil , headers= detail_headers)
        detail_html = etree.HTML(detail_response.text)
        comment_num = detail_html.xpath('//*[@id="mp-comments"]/div[1]/a/@href')
        if len(comment_num) > 0:
            sight_id = comment_num[0][comment_num[0].find('=') + 1:]
            comment_headers = {
                'cookie': 'SECKEY_ABVK=ixgOEINPMdoruxdvzhVekMsRIEY9RQ0FGvSXywgdYA4=; BMAP_SECKEY=aVX7rcMHAXJL76ICtRNadGUTxtgxepqMMrZFC_f8oCq0ganjoiyxyLNx3lP6EzFVwPTX4NAhYjZ5oz0U4u_6HAuwF7ZsrMS-73vP6IEc1JSydaFDezLlY3kFqcYs8GxLNrpKOoW8yIHk-kYkWt7ZbW0sNw4ik7piHcSDzl27fsy1cvZYtxarmQs0kPUMLhAc; QN1=00007f802eb44f3b19f0a0cf; QN71="MjIxLjIxMi4xMTYuMTU65ZOI5bCU5ruoOjE="; QN57=16809239736080.9202408331897802; QN269=2DAC06D1D5BC11EDA255FA163E1046EA; fid=19c96b4f-63cd-428e-b779-fc87b9fb5bad; QN99=1017; QunarGlobal=10.68.38.173_d63949a_1875ea7deff_-3227|1680923975967; QN601=c83b3b318830dd1b07fae87c304bfe21; QN48=21b74c4c-4259-4e42-9b6a-0f21abbbe544; QN83=qunar; ariaDefaultTheme=null; ctt_june=1654604625968##iK3waSt+WwPwawPwasXAaS3naPP8VDasXPfIVDfDERGGESaNaKDNERkTVRj8iK3siK3saKjmaR2=aSgnVKtnWhPwaUvt; QN271AC=register_pc; QN271SL=6bfba7427029c4e95d1a25906483ec07; QN271RC=6bfba7427029c4e95d1a25906483ec07; _q=U.mtxcdmg5240; csrfToken=fqwBmtdFchEfvaaYjWoqcrtcNStZlOye; _s=s_CDRGK4LYPM3ZUKLJUZBBCYLARU; _t=28125152; _v=--1Q4CaY_LxLfIQ4AJ4BVoCejEjbdZa6zoMBQ1ZXAqERduC15K-ZF53WUJan2qLyReHDAp5_UW3_QvWyMRq7M0IG0WE5Vje1pZy35W07uTf2y2dWN6x-pko0cCE_Bvuc2u8szIAgAgKYMKN1Ue_m5d6X4b_ltra5tNcd_YvkFTzS; QN43=""; QN42=wdhc0134; _i=ueHd8pLGrXk7e1SA-rFBq-xXQcoX; HN1=v1e57f8d12d27cd6492558871ea4e0da59; HN2=quuzgklcggsck; ctf_june=1654604625968##iK3waKt+WhPwawPwa=GIESj=a2P+asWRWDiRW2WRESaOX2DNWPEDa=j8XPD+iK3siK3saKjmaR2AaS28aRPnWhPwaUvt; cs_june=bf8999a10943685b35546b104009d2294743159cf8c9d9afcc5d2c68eb839ebd47d40cf81413188b9da632e2ab00f3af98f107f19447972581e328cacaed6a74b17c80df7eee7c02a9c1a6a5b97c11793a9d419bb91408934d897cb7fc7717145a737ae180251ef5be23400b098dd8ca; quinn=faca5969ce93612b2ba3f0004213263c423040f446c0fc425522523f15a5533c6914ac4e6e93f6438035fe7131ae0e68; qunar-assist={"version":"20211215173359.925","show":false,"audio":false,"speed":"middle","zomm":1,"cursor":false,"pointer":false,"bigtext":false,"overead":false,"readscreen":false,"theme":"default"}; QN44=mtxcdmg5240; Hm_lvt_15577700f8ecddb1a927813c81166ade=1680923974,1680939125,1680952873,1680954003; QN300=s=baidu; QN205=s=baidu; QN277=s=baidu; QN163=0; _vi=eSQ7UjCIKOOxl0bPHI2FOn3i5Q5Hs6OMURjDV2Uzo3hlG9_a1rg8PhAZllk-g3qaO4Fal04F5j25LNq24yPGCKMZgLVnozluZZsVQfECr53DcBu2mdlkqTFOh2qV3LBuAq6GKOaPWr_1XUdl5ZOmBI-dIbU7wZYJ3TMl9VhtRP8_; QN67=462631,1366,191223,191236,185916,189637,214043,406159,192159,40505; QN58=1680951246119|1680955100010|25; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1680955100; QN271=39d8dae1-fc21-45a1-90b9-997a5ef5e63f; __qt=v1|VTJGc2RHVmtYMSt1MHJLOFlvdFI5VXlrNW1HMnJHbkc3QnJKN0o0Mm9RNEQ4N0FBK0dza2h3a1B0dVhZYjBDZkt6ZFlrSnpkak5OdEhJajYyQks2SXFEcnB4UUkwazIxT3dtNi80VzV1NEttajd0TEtteGsvaXk5Ym9LZkNLZklWV21sWThmQ2plYzNLNU1FQXVweFdsenJOaFJvd0piRVpJQldsbUpDT244PQ==|1680955102360|VTJGc2RHVmtYMTlUWmZQT3F2S2JqVUV0VzhFZEtjd1pzbEhzZmhFUWdDeG5mTi83NnB2cm1aVUpHd2RKcVE1S3hyY3VlWSt3Tmsxd1M5NXdtU29VQ2c9PQ==|VTJGc2RHVmtYMTljajVWWnltdStmT2JyUURoa2hWT1FQK0tLTkR5S3R4UTdOd0hvZDNuZnAxUHJORUdrelN3ZGU0L1BkRXVqa2FpYjRYc2UrYmdOb2gxamtDaEtWRFptZVlQTlFxKzJIejZCUW1mTTZwRFExNiszcW5kbS9xa01uRUEydmhlL1h1Z0FpQ1RsUFNhM3U5U28zUytWbGpycFF2ek8yd3Y0ZGZKL3V1cnowVWw1d0lYT1FZZlozUHVocjJiQzd2K2RlK0VYc1EySXQxVEJpTVBBaVhFd2g2TU54b1krOElPV2dDQ0t0d2dOQkFzcnI1ZzRHL1BHTUxVVCtRRS9zUFhxaGFnRjU4MkRhaG13M1NlclM0S2dlajVlSDNpT28wUkRtbFhiNWF0dE1SVjBSOXRoN1RGQ2hOdG9zZzRtK3FBR0hwQmJucFo3eEVmOFpabHd6L0tSTHkxRjUycFVLN3hjank0cTEySjNCUEZ4WmJhRTd4Y0N2OWI0eWpFNjh0RkF0b1RCNkI0T2lnWlVKaDVtdGdNZHA2aEpjTmpRT2h2bEhuUWtWNFFTeVZBRHc5KzhMVWhUOER5Vk0zM3NpTXVUeXFzRFR3YXRXZlJrQ2p0YVdYNnNuZlBLRWk4ejdIZW5VbXhqdWI5aHpNU1ZvQnFHZlgwU0ZiUWc1L2NkcHM5d2s5S3FBaENoUy9wdTdFRWx2b2cxdUs1RTdDQjk3MFlWZXVjcklBd0lYSnhFaUFleHlvZ2ExVlptbmt5Y2tkTWJVKzNuaERrNnpGRUd2cnd4dnBGT0hlN0tJVVhBcHQxNFRUb2VLeDdCRnZtTDdiZXB0RHZXWHBrMHN0aXNtUnNsaDR3VnBEaS9zVGtHWVRYQlVNc2dSZGlwQ0J5R3p4V0NtVWRXSFd1dWU3ZndVQ0NvZ1V2WXZkTTNnYzhCMGNORWtXY085NG9YMjVoMUJZMVZZQkhCU2RRMU5HczdxM0M5VysyU1lnem85S0dGcU91ZzlLQWF4VnAy; JSESSIONID=D77A4CC0871188F3358D48EBC0CB191B; QN267=0143264395162e2d957',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
            }
            # comment_detail = requests.get('https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId=' +
            #                               str(sight_id) +'&index=1&page=1&pageSize=10&tagType=0', headers= comment_headers, proxies= proxy)
            comment_detail = requests.get('https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId=' +
                                          str(sight_id) + '&index=1&page=1&pageSize=10&tagType=0',
                                          headers=comment_headers)
            comment_json = comment_detail.json()
            comment_list[k] = comment_json['data']['commentCount']
        else:
            num = detail_html.xpath('/html/body/div[3]/div[2]/div[2]/div[4]/span[4]/a/text()')
            comment_list[k] = 0
        comment_url = 'https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId=1366&index=1&page=1&pageSize=10&tagType=0'

    print(comment_list)
    # print(comment_list)
    # 保存到csv文件
    for l in range(15):
        if comment_list[l] is not 0:
            comment_num = str(comment_list[l])[0:str(comment_list[l]).find('条')]
        else:
            comment_num = 0
        if len(name_list) < l:
            name = '  '
        else:
            name = name_list[l]
        if len(star_list) < l:
            star = ' '
        else:
            star = star_list[l]
        if len(address_list) < l:
            address = ' '
        else:
            address = address_list[l]
        if len(hot_list) < l:
            hot = ' '
        else:
            hot = hot_list[l][hot_list[l].find('度') + 1:]

        sales = sales_list[l]
        if len(prices_list) < l:
            prices = ' '
        else:
            prices = prices_list[l]
            # 将数据写入到csv文件中
        writer.writerow((name, star, address, hot,
                         sales, prices, comment_num))
    writer.writerow(["", "", '', '', '', '', ''])
    # 暂停1分钟，防止频繁访问，对方服务器将本机封掉
    time.sleep(60)

file.close()
