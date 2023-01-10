import json

import scrapy
from scrapy.settings.default_settings import USER_AGENT

from ENewspaperScraper.items import newsItem


class vnexpressSpider(scrapy.Spider):
    name = 'article'

    def start_requests(self):
        urls = ['https://thoibaotaichinhvietnam.vn/quy-hoach-tong-the-quoc-gia-can-phu-hop-voi-nguon-luc-120016.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers={'User-Agent': USER_AGENT})

    def parse(self, response):
        news = newsItem()

        data = response.xpath('//script[@type="application/ld+json"][last()]/text()').get()
        data = data.replace('\n', '')
        data_obj = json.loads(data)

        news['docID'] = response.url[-11:-5]
        news['user'] = data_obj['author']['name'].replace(' Thời báo Tài chính Việt Nam', '')
        news['userID'] = None
        news['type'] = response.xpath('//div[@class="catname c-blue"]/a/@title').get()

        dateString = data_obj['datePublished']
        if dateString:
            news['createDate'] = dateString[:-6] + '.000000' + dateString[-6:]
            news['shortFormDate'] = dateString[:10]

        news['title'] = data_obj['headline']
        news['description'] = data_obj['description']
        news['message'] = response.xpath('//div[@class="post-content __MASTERCMS_CONTENT"]/p//text()').getall()

        link_selectors = []
        news['links_in_article'] = self.getLinksInfo(link_selectors)

        news['picture'] = response.xpath('//div[@class="post-content __MASTERCMS_CONTENT"]//img/@src').getall()

        yield news

    def getLinksInfo(self, selectors):
        links_in_article = []
        link = {}

        for selector in selectors:
            if selector.xpath('./@href'):
                link['name'] = selector.xpath('./text()').get()
                link['link'] = selector.xpath('./@href').get()
                link['description'] = None
                links_in_article.append(link.copy())
            else:
                link['name'] = selector.xpath('.//a[1]/@title').get()
                link['link'] = selector.xpath('.//a[1]/@href').get()
                link['description'] = selector.xpath('/p[@class="description"]/text()').get()
                links_in_article.append(link.copy())

        return links_in_article
