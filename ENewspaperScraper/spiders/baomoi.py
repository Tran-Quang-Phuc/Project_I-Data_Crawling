import scrapy


class baomoiSpider(scrapy.Spider):
    name = 'baomoi'
    start_urls = ['https://baomoi.com/']

    def parse(self, response):
        pass

    def parse_article(self, response):
        pass
