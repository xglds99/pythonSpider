import scrapy


class TcSpider(scrapy.Spider):
    name = 'tc'
    allowed_domains = ['shanxian.58.com']
    start_urls = ['http://shanxian.58.com/']

    def parse(self, response):
        content = response.text
        print(content)
