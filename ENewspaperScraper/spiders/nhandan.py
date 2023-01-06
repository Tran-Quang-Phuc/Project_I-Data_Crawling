import scrapy


class nhandanSpider(scrapy.Spider):
    name = 'nhandan.vn'
    allowed_domains = ['nhandan.vn']
    start_urls = ['https://nhandan.vn/']

    def parse(self, response):
        article_links = response.xpath('//h2[@class="story__heading"]/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//ul[@class="menu-1"]/li/a/@href').getall()
        for link in topic_links:
            response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//h3[@class="story__heading"]/a/@href').getall() \
                        + response.xpath('//h2[@class="story__heading"]/a/@href').getall() \
                        + response.xpath('//h5[@class="story__heading"]/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        cate_links = response.xpath('//ul[@class="list-news"]/li/h3/a/@href').getall()
        for link in cate_links:
            response.follow(link, callbacck=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//h3[@class="story__heading"]/a/@href').getall() \
                        + response.xpath('//h2[@class="story__heading"]/a/@href').getall() \
                        + response.xpath('//h5[@class="story__heading"]/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        pass
