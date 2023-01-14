import scrapy


class CarSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['https://car.autohome.com.cn/price/brand-15.html']
    start_urls = ['https://car.autohome.com.cn/price/brand-15.html']

    def parse(self, response):
        print("================================================")
        name_list = response.xpath("//div[@class='main-title']/a/text()")
        price_list = response.xpath("//span[@class='font-arial']/text()")
        print("车型名称\t\t\t\t\t车型价格")
        for i in range(len(name_list)):
            print(name_list[i].extract(),"\t\t\t\t\t",price_list[i].extract())


