import scrapy

from ENewspaperScraper.items import newsItem


class vnexpressSpider(scrapy.Spider):
    name = 'vnexpress'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/']

    def parse(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//nav[@class="main-nav"]/ul[1]/li/a/@href').getall()
        for link in topic_links:
            response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

        category_links = response.xpath('//ul[@class="ul-nav-folder"]/li/a/@href').getall()
        for link in category_links:
            response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()

        news['docID'] = response.xpath('//meta[@name="tt_article_id"]/@content').get()
        news['user'] = response.xpath('//article[@class="fck_detail "]/p[last()]//text()').get()
        news['userID'] = None
        news['type'] = response.xpath('//ul[@class="breadcrumb"]/li/a/@title').get()

        dateString = response.xpath('//meta[@itemprop="dateCreated"]/@content').get()
        dateString = dateString[:-6] + '.000000'
        news['createDate'] = dateString
        news['shortFormDate'] = dateString[:10]
        news['title'] = response.xpath('//h1[@class="title-detail"]/text()').get()
        news['message'] = response.xpath('//article[@class="fck_detail "]/p//text()').getall()
        news['links_in_article'] = response.xpath('//article[@class="fck_detail "]/p/a')
    