import scrapy


class baochinhphuSpider(scrapy.Spider):
    name = 'baochinhphu'
    allowed_domains = ['baochinhphu.vn']
    start_urls = ['https://baochinhphu.vn/']

    def parse(self, response):
        article_links = response.xpath('//h3/a/@href').getall() + response.xpath('h2/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//div[@class="header__menu"]/ul/li/a/@href').getall()[0:-1]
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//div[@class="box-stream-item"]/a/@href').getall()  \
                       + response.xpath('//div[contains(@class, "box-category-item")]//a/@href').getall()  \
                       + response.xpath('//div[contains(@class, "box-item")]//a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        sub_topic_links = response.xpath('//ul[@class="sub-category"]/li/a/@href').getall()
        for link in sub_topic_links:
            yield response.follow(link, callback=self.parse_sub_topic)

    def parse_sub_topic(self, response):
        article_links = response.xpath('//div[@class="box-stream-item"]/a/@href').getall() \
                        + response.xpath('//div[contains(@class, "box-category-item")]//a/@href').getall() \
                        + response.xpath('//div[contains(@class, "box-item")]//a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        pass
