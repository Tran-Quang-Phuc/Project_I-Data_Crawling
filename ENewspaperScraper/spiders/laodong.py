import json

import scrapy

from ENewspaperScraper.items import newsItem


class laodongSpider(scrapy.Spider):
    name = 'laodong'
    allowed_domains = ['laodong.vn']
    start_urls = ['https://laodong.vn/']

    def parse(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//li[@class="item"]/a/@href').getall() \
                      + response.xpath('//div[@class="blk"]/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        cate_links = response.xpath('//h3/a[@class="item"]/@href').getall()
        for link in cate_links:
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()

        news['docID'] = response.xpath('//div[@ng-controller="ChiTietTinCtrl as vm"]/@articleid').get()
        news['user'] = response.xpath('//span[@class="authors"]/text()').get()
        news['userID'] = None
        news['type'] = response.xpath('//meta[@property="article:section"]/@content').get()

        data = response.xpath('//script[@type="application/ld+json"]/text()').get()
        data = data.replace('\n', '')
        data_obj = json.loads(data)
        dateString = data_obj[-1]['datePublished']
        if dateString:
            dateString = dateString[:-6] + '.000000' + '+07:00'
            news['createDate'] = dateString
            news['shortFormDate'] = dateString[:10]

        news['title'] = response.xpath('//meta[@property="og:title"]/@content').get()
        news['description'] = response.xpath('//meta[@property="og:description"]/@content').get()
        news['message'] = response.xpath('//div[@class="art-body"]/p//text()').getall()

        link_selectors = response.xpath('//div[@class="tin-lien-quan"]/div/a') \
            + response.xpath('//div[@class="chappeau"]/p/a') \
            + response.xpath('//div[@class="art-body"]/p/a')
        news['links_in_article'] = self.getLinksInfo(link_selectors)

        news['picture'] = response.xpath('//div[@class="art-body"]/figure/img/@src').getall()

        yield news

    def getLinksInfo(self, selectors):
        links_in_article = []
        link = {}

        for selector in selectors:
            link['name'] = selector.xpath('.//text()').get().replace('\r\n', '').strip()
            link['link'] = selector.xpath('./@href').get()
            link['description'] = None
            links_in_article.append(link.copy())

        return links_in_article
    