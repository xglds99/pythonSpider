import urllib.request

# url = 'https://www.baidu.com'
#
# # url的组成
# # 请求对象的定制可以解决ua反爬
#
# headers = {
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44'
# }
#
# request = urllib.request.Request(url,headers = headers)
# response = urllib.request.urlopen(request)
#
# content = response.read().decode('utf-8')
# print(content)


#
# count = 1
# while True:
#     total = count
#     stolen = 0
#     for i in range(5):
#         if (total - 1) % 5 != 0:
#             break
#         stolen += (total - 1) // 5
#         total = (total - 1) // 5 * 4
#     else:
#         if total % 5 == 1 and stolen == (total - 1) // 5 * 4:
#             print("至少有" % count)
#             break
#     count += 1
#
# print(count)
# beans = 1  # 第一个同学开始时拿到的豆子数
# while True:
#     # 五个人分别操作
#     for i in range(5):
#         if i == 0:
#             beans = beans * 5 + 1  # 第一个同学的操作
#         else:
#             if beans % 5 != 1:  # 如果不能均分，则说明前面的同学拿错了
#                 break
#             beans = beans // 5 * 4  # 其他同学的操作
#     else:  # 如果没有break，说明每个同学都操作成功了
#         if beans % 5 == 1:  # 最后一次均分出现多余一个的情况
#             print(beans - 1)  # 最少的豆子数
#             break
#     # 豆子数加1，重新开始
#     beans += 1
# print(1)
x = 0
while True:
    if (x + 1) % 5 == 0 and \
       (x + 1) * 5 + 1 % 5 == 0 and \
       ((x + 1) * 5 + 1) * 5 + 1 % 5 == 0 and \
       (((x + 1) * 5 + 1) * 5 + 1) * 5 + 1 % 5 == 0:
        break
    x += 1
print((((x + 1) * 5 + 1) * 5 + 1) * 5 + 1)
