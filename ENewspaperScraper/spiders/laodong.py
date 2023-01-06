import scrapy


class laodongSpider(scrapy.Spider):
    name = 'laodong.vn'
    allowed_domains = ['laodong.vn']
    start_urls = ['https://laodong.vn/']

    def parse(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//li[@class="item"]/a/@href').getall() \
                      + response.xpath('//div[@class="blk"]/a/@href').getall()
        for link in topic_links:
            response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        cate_links = response.xpath('//h3/a[@class="item"]/@href').getall()
        for link in cate_links:
            response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        pass
    