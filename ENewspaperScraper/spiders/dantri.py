import json

import scrapy

from ENewspaperScraper.items import newsItem


class dantriSpider(scrapy.Spider):
    name = 'dantri'
    allowed_domains = ['dantri.com.vn']
    start_urls = ['https://dantri.com.vn/']

    def parse(self, response):
        article_links =  response.xpath('//h3[@class="article-title"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//li[@class="has-child"]/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//h3[@class="article-title"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        cate_links = response.xpath('//ol[@class="menu-second child"]/li/a/@href').getall()
        for link in cate_links:
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//h3[@class="article-title"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()

        news['docID'] = response.xpath('//div[@data-module="article-audio"]/@data-article-id').get()
        news['user'] = response.xpath('//div[@class="author-name"]/a/b/text()').get()
        news['userID'] = response.xpath('//div[@class="author-name"]/a/@href').get()[-7:-4]
        news['type'] = response.xpath('//ul[@class="breadcrumbs"]/li/a/@title').get()

        data = response.xpath('//script[@type="application/ld+json"]/text()').getall()[-2]
        data = data.replace('\n', '')
        data_obj = json.loads(data)
        dateString = data_obj['datePublished']
        if dateString:
            dateString = dateString[:-6] + '.000000' + dateString[-6:]
            news['createDate'] = dateString
            news['shortFormDate'] = dateString[:10]

        news['title'] = response.xpath('//h1/text()').get()
        news['description'] = response.xpath('//h2[@class="singular-sapo"]/text()').get()
        news['message'] = response.xpath('//div[@class="singular-content"]/p//text()').getall()

        link_selectors = response.xpath('//div[@class="singular-content"]/p/a') \
            + response.xpath('//article[@class="article-related"]/article/div[@class="article-content"]')
        news['links_in_article'] = self.getLinksInfo(link_selectors)

        news['picture'] = response.xpath('//div[@class="singular-content"]/figure//img[1]/@src').getall()

        yield news

    def getLinksInfo(self, selectors):
        links_in_article = []
        link = {}

        for selector in selectors:
            if selector.xpath('./@href').get():
                link['name'] = selector.xpath('./text()').get()
                link['link'] = selector.xpath('./@href').get()
                link['description'] = None
                links_in_article.append(link.copy())
            else:
                link['name'] = selector.xpath('.//a[1]/text()').get()
                link['link'] = selector.xpath('.//a[1]/@href').get()
                link['description'] = selector.xpath('.//a[2]/text()').get()
                links_in_article.append(link.copy())

        return links_in_article
