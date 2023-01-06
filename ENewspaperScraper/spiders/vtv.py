import scrapy


class vtvSpider(scrapy.Spider):
    name = 'vtv.vn'
    allowed_domains = ['vtv.vn']
    start_urls = ['https://vtv.vn/']

    def parse(self, response):
        article_links = response.xpath('//h2/a/@href').getall() \
                        + response.xpath('//h3/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//div[@class="menu_chinh"]/ul/li/a/@href').getall()
        for link in topic_links:
            response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//li[@class="tlitem "]/h4/a/@href').getall() \
                        + response.xpath('//ul[@class="swiper-wrapper"]/li/a/@href').getall() \
                        + response.xpath('//li[contains(@class, "borderbox")]/a/@href').getall() \
                        + response.xpath('//h2/a/@href').getall() \
                        + response.xpath('//h3/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        cate_links = response.xpath('//div[@class="left fl"]/ul/li/a/@href').getall()
        for link in cate_links:
            response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//li[@class="tlitem "]/h4/a/@href').getall() \
                        + response.xpath('//ul[@class="swiper-wrapper"]/li/a/@href').getall() \
                        + response.xpath('//li[contains(@class, "borderbox")]/a/@href').getall() \
                        + response.xpath('//h2/a/@href').getall() \
                        + response.xpath('//h3/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        pass
    