import json

import scrapy

from ENewspaperScraper.items import newsItem


class kiemsatSpider(scrapy.Spider):
    name = 'kiemsat'
    allowed_domains = ['kiemsat.vn']
    start_urls = ['https://kiemsat.vn/']

    def parse(self, response):
        article_links = response.xpath('//a[@class="title"]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//div[@class="khoi1100"]/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//a[@class="title"]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()

        news['docID'] = response.url[-10:-5]
        news['user'] = response.xpath('//div[@class="chuky"]/a/text()').get()
        news['userID'] = None
        news['type'] = 1

        data = response.xpath('//script[@type="application/ld+json"]/text()').getall()[-2]
        data = data.replace('\n', '')
        data_obj = json.loads(data)
        dateString = data_obj['datePublished']
        if dateString:
            dateString = dateString[:-1] + '.000000' + '+07:00'
            news['createDate'] = dateString
            news['shortFormDate'] = dateString[:10]

        news['title'] = response.xpath('//h1/text()').get()
        news['description'] = response.xpath('//div[@class="mota"]/h2/text()').get()
        news['message'] = response.xpath('//div[@class="noidung"]/p/text()').getall()

        link_selectors = response.xpath('//div[@class="lienquan"]/div') \
            + response.xpath('//div[@class="list_other"]//a')
        news['links_in_article'] = self.getLinksInfo(link_selectors)

        news['picture'] = response.xpath('//div[@class="noidung"]//img/@src').getall()

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
                link['name'] = selector.xpath('./h3/a/text()').get()
                link['link'] = selector.xpath('.//a[1]/@href').get()
                link['description'] = selector.xpath('.//div[@class="desc"]/text()').get()
                links_in_article.append(link.copy())

        return links_in_article
    