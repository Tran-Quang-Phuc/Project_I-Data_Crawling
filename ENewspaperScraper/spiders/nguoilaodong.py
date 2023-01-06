import scrapy


class nldSpider(scrapy.Spider):
    name = 'nld.com'
    allowed_domains = ['nld.com.vn']
    start_urls = ['https://nld.com.vn/']

    def parse(self, response):
        article_links = response.xpath('//div[contains(@class, "news-item")]//a[1]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//ul[@class="menu-top clearfix"]/li/a/@href').getall()
        for link in topic_links:
            response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//div[@class="news-info"]//a[1]/@href').getall() \
                        + response.xpath('//ul[@class="list-video"]/li//a[1]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        cate_links = response.xpath('//ul[@class="sub-cate"]/li//a/@href').getall()
        for link in cate_links:
            response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//div[@class="news-info"]//a[1]/@href').getall() \
                        + response.xpath('//ul[@class="list-video"]/li//a[1]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        pass
    