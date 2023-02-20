import json

import scrapy

from ENewspaperScraper.items import newsItem


class candSpider(scrapy.Spider):
    name = 'cand'
    allowed_domains = ['cand.com.vn']
    start_urls = ['https://cand.com.vn/']

    def parse(self, response):
        topic_links = response.xpath('//li[@class="parent-menu"]/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

        article_links = response.xpath('//div[@class="box-title"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_topic(self, response):
        cate_links = response.xpath('//div[@class="cate-main"]/a/@href').getall()
        for link in cate_links:
            yield response.follow(link, callback=self.parse_category)

        article_links = response.xpath('//div[@class="box-title"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_category(self, response):
        article_links = response.xpath('//div[@class="box-title"]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()

        news['docID'] = response.url[-7:-1]
        news['user'] = response.xpath('//div[@class="box-author uk-text-right uk-clearfix"]/strong/text()').get()
        news['userID'] = None
        news['type'] = response.xpath('//ul[@class="uk-breadcrumb"]/li/a/text()').get()

        data = response.xpath('//script[@type="application/ld+json"]/text()').getall()[-2]
        data = data.replace('\n', '')
        data_obj = json.loads(data)
        if data_obj['datePublished']:
            dateString = self._reformatDateString(data_obj['datePublished'])
            news['createDate'] = dateString
            news['shortFormDate'] = dateString.split("T")[0]

        news['title'] = response.xpath('//h1/text()').get()
        news['description'] = response.xpath('//div[@class="box-des-detail this-one"]/p/text()').get()
        news['message'] = response.xpath('//div[@class="detail-content-body"]/p/text()').getall()

        link_selectors = response.xpath('//div[@class="contref simplebox thumbnail"]/ul/li/a') \
            + response.xpath('//div[@class="contref simplebox vertical"]/ul/li/a')
        news['links_in_article'] = self._getLinksInfo(link_selectors)

        news['picture'] = response.xpath('//div[@class="detail-content-body"]/figure/img/@src').getall()

        yield news

    @staticmethod
    def _reformatDateString(dateString):
        # 1/12/2023 7:56:00 AM
        date_component = dateString.split('/')
        month = date_component[0]
        if len(month) == 1:
            month = '0' + month
        day = date_component[1]
        if len(day) == 1:
            day = '0' + day
        date_component = date_component[2].split(' ')
        year = date_component[0]
        time = date_component[1]
        if date_component[2] == 'PM':
            time = time.split(':', 1)
            hour = str(int(time[0]) + 12)
            if hour == '24':
                hour = '12'
            time = hour + ':' + time[1]

        dateString = year + '-' + month + '-' + day + 'T' + time + '.000' + '+07:00'
        return dateString

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
