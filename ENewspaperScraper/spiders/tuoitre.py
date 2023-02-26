import scrapy

from ENewspaperScraper.items import newsItem


class tuoitreSpider(scrapy.Spider):
    name = 'tuoitre'
    allowed_domains = ['tuoitre.vn']
    start_urls = ['https://tuoitre.vn/']

    def parse(self, response):
        topic_links = response.xpath('//ul[@class="menu-nav"]/li/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

        article_links = response.xpath('//div[@class="box-content-title"]/h3/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_topic(self, response):
        category_links = response.xpath('//ul[@class="sub-category"]/li/a/@href').getall()
        for link in category_links:
            yield response.follow(link, callback=self.parse_category)

        article_links = response.xpath('//div[@class="box-content-title"]/h3/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_category(self, response):
        article_links = response.xpath('//div[@class="box-content-title"]//a[1]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()

        news['docID'] = response.xpath('//input[@id="hdNewsId"]/@value').get()
        news['user'] = response.xpath('//div[@class="author-info"]/a/@title').get()
        news['userID'] = None
        news['type'] = response.xpath('//meta[@property="article:section"]/@content').get()
        dateString = response.xpath("//meta[@name='pubdate']/@content").get()
        if dateString:
            dateString = dateString[:-6] + '.000' + '+07:00'
            news['createDate'] = dateString
            news['shortFormDate'] = dateString[:10]

        news['title'] = response.xpath('//meta[@name="title"]/@content').get()
        news['description'] = response.xpath('//meta[@name="description"]/@content').get()
        news['message'] = response.xpath('//div[@data-role="content"]/p//text()').getall()
        link_selectors = response.xpath('//div[@data-role="content"]/p//a') \
            + response.xpath('//div[@type="RelatedOneNews"]')
        news['links_in_article'] = self.getLinksInfo(link_selectors)
        news['picture'] = response.xpath('//div[@data-role="content"]/figure//img/@src').getall()

        yield news

    def getLinksInfo(self, selectors):
        links_in_article = []
        link = {}

        for selector in selectors:
            if selector.xpath('./@href').get():
                link['name'] = selector.xpath('./@title').get()
                link['link'] = selector.xpath('./@href').get()
                link['description'] = None
                links_in_article.append(link.copy())
            else:
                link['name'] = selector.xpath('./a[2]/text()').get()
                link['link'] = selector.xpath('./a/@href').get()
                link['description'] = selector.xpath('./p/text()').get()
                links_in_article.append(link.copy())

        return links_in_article
    