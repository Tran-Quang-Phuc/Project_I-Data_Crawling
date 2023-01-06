import json

import scrapy

from ENewspaperScraper.items import newsItem


class article(scrapy.Spider):
    name = 'article'
    start_urls = ['https://vietnamnet.vn/yeu-cau-xac-minh-tai-san-bi-ke-bien-trong-vu-aic-2097637.html',
                  'https://vietnamnet.vn/quoc-hoi-phe-chuan-mien-nhiem-va-bo-nhiem-thanh-vien-chinh-phu-2097734.html']

    def parse(self, response):
        news = newsItem()

        news['docID'] = response.xpath('//div[@articletrackingv3="true"]/@articleid').get()

        user_link = response.xpath('//p[@class="newsFeature__author-info"]/span/a/@href').get()
        news['userID'] = user_link[-11:-5]

        news['type'] = response.xpath('//div[@class="breadcrumb-box__link "]/p/a[1]/@title').get()

        data = response.xpath('//script[@type="application/ld+json"]/text()').getall()[1]
        data = data.replace('\n', '')
        data_obj = json.loads(data)
        news['createDate'] = data_obj['datePublished']
        news['shortFormDate'] = data_obj['datePublished'][:10]

        news['title'] = response.xpath('//div[@class="newsFeature__header"]/h1/text()').get()
        news['message'] = response.xpath('//div[contains(@class, "maincontent")]//p//text()').getall()

        news['links_in_article'] = response.xpath('//div[contains(@class, "maincontent")]//p/a') \
            + response.xpath('//div[@class="related-news mb-25"]/ul/li/p/a') \
            + response.xpath('//div[@class="insert-wiki-content"]')

        news['picture'] = response.xpath('//div[contains(@class, "maincontent")]//figure/img/@src').getall()
        news['numLikes'] = 100
        news['numComments'] = 100
        news['numShares'] = 10

        yield news
