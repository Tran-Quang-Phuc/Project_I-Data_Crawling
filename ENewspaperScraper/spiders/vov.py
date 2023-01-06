import scrapy


class vovSpider(scrapy.Spider):
    name = 'vov.vn'
    allowed_domains = ['vov.vn']
    start_urls = ['https://vov.vn/']

    def parse(self, response):
        article_links = response.xpath('//a[@class="vovvn-title"]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//div[@class="col-lg-2 col-md-4 col-6"]/div/h5/a/@href').getall()
        for link in topic_links:
            response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        page_links = response.xpath('//ul[@class="pagination justify-content-center"]/li/a/@href').getall()
        for page in page_links[1:4]:
            article_links = response.xpath('//a[@class="vovvn-title"]/@href').getall()
            for link in article_links:
                response.follow(link, callback=self.parse_article)

        category_links = response.xpath('//div[@class="row children-category"]/div/a/@href').getall()
        for link in category_links:
            response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        page_links = response.xpath('//ul[@class="pagination justify-content-center"]/li/a/@href').getall()
        for page in page_links[1:4]:
            article_links = response.xpath('//a[@class="vovvn-title"]/@href').getall()
            for link in article_links:
                response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        pass
