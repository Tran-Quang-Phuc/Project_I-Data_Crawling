import scrapy


class zingnewsSpider(scrapy.Spider):
    name = 'zingnews'
    allowed_domains = ['zingnews.vn']
    custom_settings = {'CLOSESPIDER_PAGECOUNT': 100}
    start_urls = ['https://zingnews.vn/']

    def parse(self, response):
        topic_links = response.xpath('//nav[@class="category-menu"]/ul/li/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

        article_links = response.xpath('//p[@class="article-title"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_topic(self, response):
        if response.url != 'https://lifestyle.zingnews.vn/':
            cate_links = response.xpath('//section[@id="category-header"]/ul/li/a/@href').getall()
            for link in cate_links:
                yield response.follow(link, callback=self.parse_category)

        article_links = response.xpath('//p[@class="article-title"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_category(self, response):
        article_links = response.xpath('//p[@class="article-title"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        pass
    