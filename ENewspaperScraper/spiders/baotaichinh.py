import scrapy


class baotaichinhSpider(scrapy.Spider):
    name = 'thoibaotaichinhvietnam'
    allowed_domains = ['thoibaotaichinhvietnam.vn']
    start_urls = ['https://thoibaotaichinhvietnam.vn/']

    def parse(self, response):
        article_links = response.xpath('//article[@class="article"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('(//ul[@class="navbar-nav clearfix"])[1]/li/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//article[@class="article"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        sub_topic_links = response.xpath('//div[@class="breadcrumb-list active text-bold"]/span/a/@href').getall()
        for link in sub_topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_article(self, response):
        pass
