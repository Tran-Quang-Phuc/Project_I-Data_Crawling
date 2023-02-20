import scrapy

from ENewspaperScraper.items import newsItem


class thanhnienSpider(scrapy.Spider):
    name = 'thanhnien'
    allowed_domains = ['thanhnien.vn']
    start_urls = ['https://thanhnien.vn/']

    def parse(self, response):
        topic_links = response.xpath('//ul[@class="menu-nav"]/li/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

        article_links = response.xpath('//h3/a/@href').getall()
        for link in article_links:
            if link != "javascript:;":
                yield response.follow(link, callback=self.parse_article)

    def parse_topic(self, response):
        cate_links = response.xpath('//div[@class="swiper-wrapper"]/a/@href').getall()
        for link in cate_links:
            yield response.follow(link, callback=self.parse_category)

        article_links = response.xpath('//h3/a/@href').getall() + response.xpath('//h2/a/@href').getall()
        for link in article_links:
            if link != "javascript:;":
                yield response.follow(link, callback=self.parse_article)

    def parse_category(self, response):
        article_links = response.xpath('//h3/a/@href').getall() + response.xpath('//h2/a/@href').getall()
        for link in article_links:
            if link != "javascript:;":
                yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()

        news['docID'] = response.xpath('//meta[@property="dable:item_id"]/@content').get()
        news['user'] = response.xpath('//meta[@property="dable:author"]/@content').get()
        if news['user']:
            user_link = response.xpath('//div[@class="author-info"]//a/@href').get()
            if user_link:
                news['userID'] = user_link[-10: -4]
            else:
                news['userID'] = None
        else:
            news['user'] = None
            news['userID'] = None

        news['type'] = response.xpath('//div[@class="detail-cate"]/a/@title').get()
        dateString = response.xpath('//meta[@itemprop="datePublished"]/@content').get()
        if dateString:
            dateString = dateString + '.000' + '+07:00'
            news['createDate'] = dateString
            news['shortFormDate'] = dateString[:10]
        news['title'] = response.xpath('//title/text()').get()
        news['description'] = response.xpath('//meta[@name="description"]/@content').get()
        news['message'] = response.xpath('//div[@data-role="content"]/p//text()').getall()

        link_selectors = response.xpath('//h2[@class="detail-sapo"]/a') \
            + response.xpath('//div[@data-role="content"]/p/a') \
            + response.xpath('//div[@class="detail__related"]//div[@class="box-category-content"]')
        news['links_in_article'] = self._getLinksInfo(link_selectors)

        news['picture'] = response.xpath('//figure//img/@src').getall()

        yield news

    @staticmethod
    def _getLinksInfo(selectors):
        links_in_article = []
        link = {}

        for selector in selectors:
            if selector.xpath('./@href'):
                link['name'] = selector.xpath('./@title').get()
                link['link'] = selector.xpath('./@href').get()
                link['description'] = None
                links_in_article.append(link.copy())
            else:
                link['name'] = selector.xpath('./h3/a/@title').get()
                link['link'] = selector.xpath('./h3/a/@href').get()
                link['description'] = selector.xpath('./p/text()').get()
                links_in_article.append(link.copy())

        return links_in_article
    