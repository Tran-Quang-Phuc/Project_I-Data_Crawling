import scrapy

from ENewspaperScraper.items import newsItem


class baochinhphuSpider(scrapy.Spider):
    name = 'baochinhphu'
    allowed_domains = ['baochinhphu.vn']
    start_urls = ['https://baochinhphu.vn/']

    def parse(self, response):
        article_links = response.xpath('//h3/a/@href').getall() + response.xpath('h2/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//div[@class="header__menu"]/ul/li/a/@href').getall()[0:-1]
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//div[@class="box-stream-item"]/a/@href').getall()  \
                       + response.xpath('//div[contains(@class, "box-category-item")]//a/@href').getall()  \
                       + response.xpath('//div[contains(@class, "box-item")]//a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        sub_topic_links = response.xpath('//ul[@class="sub-category"]/li/a/@href').getall()
        for link in sub_topic_links:
            yield response.follow(link, callback=self.parse_sub_topic)

    def parse_sub_topic(self, response):
        article_links = response.xpath('//div[@class="box-stream-item"]/a/@href').getall() \
                        + response.xpath('//div[contains(@class, "box-category-item")]//a/@href').getall() \
                        + response.xpath('//div[contains(@class, "box-item")]//a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()

        news['docID'] = response.url[-22:-4]
        news['user'] = response.xpath('//p[@style="text-align: right;"]//text()').get()
        news['userID'] = None
        news['type'] = response.xpath('//div[@class="detail-breadcrumb"]/ul/li/a/@title').get()

        dateString = response.xpath('//meta[@property="article:published_time"]/@content').get()
        if dateString:
            dateString = dateString[:-6] + '.000000' + dateString[-6:]
            news['createDate'] = dateString
            news['shortFormDate'] = dateString[:10]

        news['title'] = response.xpath('//h1/text()').get()
        news['description'] = response.xpath('//meta[@name="description"]/@content').get()
        news['message'] = response.xpath('//div[@data-role="content"]/p//text()').getall()

        link_selectors = response.xpath('//div[@data-role="content"]/p/a') \
            + response.xpath('//a[@class="title link-callout"]')
        news['links_in_article'] = self._getLinksInfo(link_selectors)

        news['picture'] = response.xpath('//div[@data-role="content"]/figure//img[1]/@src').getall()

        yield news

    @staticmethod
    def _getLinksInfo(selectors):
        links_in_article = []
        link = {}

        for selector in selectors:
            link['name'] = selector.xpath('./text()').get()
            link['link'] = selector.xpath('./@href').get()
            link['description'] = None
            links_in_article.append(link.copy())

        return links_in_article
