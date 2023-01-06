import scrapy


class zingnewsSpider(scrapy.Spider):
    name = 'zingnews.vn'
    allowed_domains = ['zingnews.vn']
    start_urls = ['https://zingnews.vn/']

    def parse(self, response):
        article_links = response.xpath('//p[@class="article-title"]/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//nav[@class="category-menu"]/ul/li/a/@href').getall()
        for link in topic_links:
            response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//p[@class="article-title"]/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        if response.url != 'https://lifestyle.zingnews.vn/':
            cate_links = response.xpath('//section[@id="category-header"]/ul/li/a/@href').getall()
            for link in cate_links:
                response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//p[@class="article-title"]/a/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        pass
    