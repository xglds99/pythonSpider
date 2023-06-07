# 分析豆瓣唐探3的影评，生成词云
import requests
from stylecloud import gen_stylecloud
import jieba
import re
from bs4 import BeautifulSoup
headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
}
def jieba_cloud(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        word_list = jieba.cut(f.read(),cut_all=True)

        result = " ".join(word_list)
        # 制作中文词云
        icon_name = " "
        icon = "ciyun"
        pic = icon + '.png'
        gen_stylecloud(text=result, font_path='simsun.ttc', output_name=pic)
        return pic
def spider_comment(movie_id, page):
    comment_list = []
    with open("douban.txt", "a+", encoding='utf-8') as f:
        for i in range(1,page+1):

            url = 'https://movie.douban.com/subject/%s/comments?start=%s&limit=20&sort=new_score&status=P' \
                  % (movie_id, (i - 1) * 20)

            req = requests.get(url, headers=headers)
            req.encoding = 'utf-8'
            comments = re.findall('<span class="short">(.*)</span>', req.text)


            f.writelines('\n'.join(comments))
    print(comments)
if __name__ == '__main__':
    movie_id = '27619748'     #引号中的数字即为电影短评网址中的那几个数字，可以通过修改它来爬取其他电影的短评
    page = 10
    spider_comment(movie_id, page)
    jieba_cloud("douban.txt")
