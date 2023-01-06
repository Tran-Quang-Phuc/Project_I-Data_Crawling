import scrapy


class thanhnienSpider(scrapy.Spider):
    name = 'baothanhnien'
    allowed_domains = ['thanhnien.vn']
    start_urls = ['https://thanhnien.vn/']

    def parse(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//ul[@class="site-header__menu"]/li/a/@href').getall()
        for link in topic_links:
            response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        cate_links = response.xpath('//ol[@class="breadcrumb"]/li/a/@href').getall()
        for link in cate_links:
            response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        pass
    