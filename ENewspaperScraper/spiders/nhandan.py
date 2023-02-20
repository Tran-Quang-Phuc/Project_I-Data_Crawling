import scrapy

from ENewspaperScraper.items import newsItem


class nhandanSpider(scrapy.Spider):
    name = 'nhandan'
    allowed_domains = ['nhandan.vn']
    start_urls = ['https://nhandan.vn/']

    def parse(self, response):
        topic_links = response.xpath('//ul[@class="menu-1"]/li/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

        article_links = response.xpath('//h2[@class="story__heading"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_topic(self, response):
        cate_links = response.xpath('//ul[@class="list-news"]/li/h3/a/@href').getall()
        for link in cate_links:
            yield response.follow(link, callbacck=self.parse_category)

        article_links = response.xpath('//h3[@class="story__heading"]/a/@href').getall() \
            + response.xpath('//h2[@class="story__heading"]/a/@href').getall() \
            + response.xpath('//h5[@class="story__heading"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_category(self, response):
        article_links = response.xpath('//h3[@class="story__heading"]/a/@href').getall() \
                        + response.xpath('//h2[@class="story__heading"]/a/@href').getall() \
                        + response.xpath('//h5[@class="story__heading"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()

        news['docID'] = response.xpath('//meta[@property="dable:item_id"]/@content').get()
        news['user'] = response.xpath('//meta[@property="dable:author"]/@content').get()
        news['userID'] = None
        news['type'] = response.xpath('//meta[@property="article:section"]/@content').get()

        dateString = response.xpath('//meta[@itemprop="datePublished"]/@content').get()
        if dateString:
            dateString = dateString[:-6] + '.000' + '+07:00'
            news['createDate'] = dateString
            news['shortFormDate'] = dateString[:10]

        news['title'] = response.xpath('//title/text()').get()
        news['description'] = response.xpath('//meta[@name="description"]/@content').get()
        news['message'] = response.xpath('//div[@class="article__body cms-body"]/p//text()').getall()

        link_selectors = response.xpath('//div[@class="related-news"]//article//a')
        news['links_in_article'] = self._getLinksInfo(link_selectors)

        news['picture'] = response.xpath(
            '//div[@class="main-col content-col"]/table[@class="picture"]//img/@src').getall() \
            + response.xpath('//table[@class="picture"]//img/@data-src').getall()

        yield news

    @staticmethod
    def _getLinksInfo(selectors):
        links_in_article = []
        link = {}

        for selector in selectors:
            link['name'] = selector.xpath('./@title').get()
            link['link'] = selector.xpath('./@href').get()
            link['description'] = None
            links_in_article.append(link.copy())

        return links_in_article
