import scrapy

from ENewspaperScraper.items import newsItem


class nldSpider(scrapy.Spider):
    name = 'nld'
    allowed_domains = ['nld.com.vn']
    start_urls = ['https://nld.com.vn/']

    def parse(self, response):
        article_links = response.xpath('//div[contains(@class, "news-item")]//a[1]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//ul[@class="menu-top clearfix"]/li/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//div[@class="news-info"]//a[1]/@href').getall() \
                        + response.xpath('//ul[@class="list-video"]/li//a[1]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        cate_links = response.xpath('//ul[@class="sub-cate"]/li//a/@href').getall()
        for link in cate_links:
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//div[@class="news-info"]//a[1]/@href').getall() \
                        + response.xpath('//ul[@class="list-video"]/li//a[1]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()

        news['docID'] = response.xpath('//meta[@property="dable:item_id"]/@content').get()
        user = response.xpath('//meta[@property="dable:author"]/@content').get()
        if user:
            news['user'] = user.split(': ')[-1]
        news['userID'] = None
        news['type'] = response.xpath('//meta[@property="article:section"]/@content').get()

        dateString = response.xpath('//meta[@itemprop="datePublished"]/@content').get()
        if dateString:
            dateString = dateString[:-6] + '.000' + '+07:00'
            news['createDate'] = dateString
            news['shortFormDate'] = dateString[:10]

        news['title'] = response.xpath('//meta[@property="og:title"]/@content').get()
        news['description'] = response.xpath('//meta[@name="description"]/@content').get()
        news['message'] = response.xpath('//div[@class="content-news-detail old-news"]/p//text()').getall()

        link_selectors = response.xpath('//div[@class="content-news-detail old-news"]/p/a') \
            + response.xpath('//div[contains(@class, "news-relation-bottom")]/ul[@class="list-item"]/li/a[1]')
        news['links_in_article'] = self._getLinksInfo(link_selectors)

        news['picture'] = response.xpath('//div[@class="content-news-detail old-news"]/div[@type="Photo"]//img/@src').getall()

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
    