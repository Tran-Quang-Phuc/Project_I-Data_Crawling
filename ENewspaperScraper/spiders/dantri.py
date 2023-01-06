import scrapy


class dantriSpider(scrapy.Spider):
    name = 'dantri'
    allowed_domains = ['dantri.com.vn']
    start_urls = ['https://dantri.com.vn/']

    def parse(self, response):
        article_links =  response.xpath('//h3[@class="article-title"]/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//li[@class="has-child"]/a/@href').getall()
        for link in topic_links:
            response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//h3[@class="article-title"]/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        cate_links = response.xpath('//ol[@class="menu-second child"]/li/a/@href').getall()
        for link in cate_links:
            response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//h3[@class="article-title"]/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        pass
