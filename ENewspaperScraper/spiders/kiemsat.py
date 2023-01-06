import scrapy


class kiemsatSpider(scrapy.Spider):
    name = 'kiemsat'
    allowed_domains = ['kiemsat.vn']
    start_urls = ['https://kiemsat.vn/']

    def parse(self, response):
        article_links = response.xpath('//a[@class="title"]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//div[@class="khoi1100"]/a/@href').getall()
        for link in topic_links:
            response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//a[@class="title"]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        pass
    