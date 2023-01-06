import scrapy


class candSpider(scrapy.Spider):
    name = 'cand.com'
    allowed_domains = ['cand.com.vn']
    start_urls = ['https://cand.com.vn/']

    def parse(self, response):
        article_links = response.xpath('//div[@class="box-title"]/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//li[@class="parent-menu"]/a/@href').getall()
        for link in topic_links:
            response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//div[@class="cate-main"]/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)
        cate_links = response.xpath('//div[@class="cate-main"]/a/@href').getall()
        for link in cate_links:
            response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//div[@class="box-title"]/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        pass
