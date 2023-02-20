import scrapy

from ENewspaperScraper.items import newsItem


class vtvSpider(scrapy.Spider):
    name = 'vtv'
    allowed_domains = ['vtv.vn']
    start_urls = ['https://vtv.vn/']

    def parse(self, response):
        article_links = response.xpath('//h2/a/@href').getall() \
                        + response.xpath('//h3/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//div[@class="menu_chinh"]/ul/li/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//li[@class="tlitem "]/h4/a/@href').getall() \
                        + response.xpath('//ul[@class="swiper-wrapper"]/li/a/@href').getall() \
                        + response.xpath('//li[contains(@class, "borderbox")]/a/@href').getall() \
                        + response.xpath('//h2/a/@href').getall() \
                        + response.xpath('//h3/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        cate_links = response.xpath('//div[@class="left fl"]/ul/li/a/@href').getall()
        for link in cate_links:
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//li[@class="tlitem "]/h4/a/@href').getall() \
                        + response.xpath('//ul[@class="swiper-wrapper"]/li/a/@href').getall() \
                        + response.xpath('//li[contains(@class, "borderbox")]/a/@href').getall() \
                        + response.xpath('//h2/a/@href').getall() \
                        + response.xpath('//h3/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()
        news['docID'] = response.url[-19:-4]
        news['user'] = None
        news['userID'] = None
        news['type'] = response.xpath('//meta[@property="article:section"]/@content').get()
        dateString = response.xpath("//meta[@name='pubdate']/@content").get()
        if dateString:
            dateString = dateString[:-6] + '.000' + '+07:00'
            news['createDate'] = dateString
            news['shortFormDate'] = dateString[:10]
        news['title'] = response.xpath('//meta[@property="og:title"]/@content').get()
        news['description'] = response.xpath('//meta[@property="og:description"]/@content').get()
        news['message'] = response.xpath('//div[@data-field="body"]/p//text()').getall()

        link_selectors = response.xpath('//div[@class="tinlienquan clearfix"]/ul/li/a') \
            + response.xpath('//div[@data-field="body"]/p/a')
        news['links_in_article'] = self._getLinksInfo(link_selectors)

        news['picture'] = response.xpath('//div[@data-field="body"]/div[@type="Photo"]//img/@src').getall()

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
