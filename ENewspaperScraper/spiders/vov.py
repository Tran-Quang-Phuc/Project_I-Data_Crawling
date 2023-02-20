import scrapy

from ENewspaperScraper.items import newsItem


class vovSpider(scrapy.Spider):
    name = 'vov'
    allowed_domains = ['vov.vn']
    start_urls = ['https://vov.vn/']

    def parse(self, response):
        article_links = response.xpath('//a[@class="vovvn-title"]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//div[@class="col-lg-2 col-md-4 col-6"]/div/h5/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        page_links = response.xpath('//ul[@class="pagination justify-content-center"]/li/a/@href').getall()
        for _ in page_links[1:4]:
            article_links = response.xpath('//a[@class="vovvn-title"]/@href').getall()
            for link in article_links:
                yield response.follow(link, callback=self.parse_article)

        category_links = response.xpath('//div[@class="row children-category"]/div/a/@href').getall()
        for link in category_links:
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        page_links = response.xpath('//ul[@class="pagination justify-content-center"]/li/a/@href').getall()
        for _ in page_links[1:4]:
            article_links = response.xpath('//a[@class="vovvn-title"]/@href').getall()
            for link in article_links:
                yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()
        news['docID'] = response.url[-11:-4]
        user = response.xpath('//div[@class="row article-author"]/div/text()').get()
        if user:
            news['user'] = user.split('/')[0]
        news['userID'] = None
        news['type'] = response.xpath('//meta[@property="article:section"]/@content').get()

        dateString = response.xpath('//meta[@property="article:published_time"]/@content').get()
        if dateString:
            dateString = dateString[:-6] + '.000' + '+07:00'
            news['createDate'] = dateString
            news['shortFormDate'] = dateString[:10]

        news['title'] = response.xpath('//meta[@name="title"]/@content').get()
        news['description'] = response.xpath('//meta[@name="description"]/@content').get()
        news['message'] = response.xpath('//div[@class="text-long"]/p//text()').getall()
        news['links_in_article'] = []
        news['picture'] = response.xpath('//div[@class="text-long"]/figure//img/@src').getall()

        yield news

    def getLinksInfo(self, selectors):
        pass
