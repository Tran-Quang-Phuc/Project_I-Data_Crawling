import scrapy


class tuoitreSpider(scrapy.Spider):
    name = 'tuoitre.vn'
    start_urls = ['https://tuoitre.vn/']

    def parse(self, response):
        article_links = response.xpath('//div[@class="box-content-title"]/h3/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//ul[@class="menu-nav"]/li/a/@href').getall()
        for link in topic_links:
            response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//div[@class="box-content-title"]/h3/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        category_links = response.xpath('//ul[@class="sub-category"]/li/a/@href').getall()
        for link in category_links:
            response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//div[@class="box-content-title"]//a[1]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        pass
    