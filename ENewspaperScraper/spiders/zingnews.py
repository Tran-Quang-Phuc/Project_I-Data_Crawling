import scrapy

from ENewspaperScraper.items import newsItem


class zingnewsSpider(scrapy.Spider):
    name = 'zingnews'
    allowed_domains = ['zingnews.vn']
    custom_settings = {'CONCURRENT_REQUESTS': 2}
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
        news = newsItem()

        news['docID'] = response.xpath('//article/@article-id').get()
        news['user'] = response.xpath('//p[@class="author"]/text()').get()
        news['userID'] = None
        news['type'] = response.xpath('//p[@class="the-article-category"]/a/@title').get()
        dateString = response.xpath('//meta[@property="article:published_time"]/@content').get()
        if dateString:
            dateString = dateString[:-5] + '.000' + '+07:00'
            news['createDate'] = dateString
            news['shortFormDate'] = dateString[:10]
        news['title'] = response.xpath('//meta[@property="og:title"]/@content').get()
        news['description'] = response.xpath('//meta[@name="description"]/@content').get()
        news['message'] = response.xpath('//div[@class="the-article-body"]/p//text()').getall()
        link_selectors = response.xpath('//div[@class="inner-article"]/a')
        news['links_in_article'] = self._getLinksInfo(link_selectors)
        news['picture'] = response.xpath('//div[@class="the-article-body"]//img/@data-src').getall()

        yield news

    @staticmethod
    def _getLinksInfo(selectors):
        links_in_article = []
        link = {}

        for selector in selectors:
            link['name'] = selector.xpath('./h2/text()').get()
            link['link'] = selector.xpath('./@href').get()
            link['description'] = selector.xpath('./p[@class="summary"]/text()').get()
            links_in_article.append(link.copy())

        return links_in_article
    