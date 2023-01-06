import scrapy
import json

from ENewspaperScraper.items import newsItem


class vietnamnetSpider(scrapy.Spider):

    name = 'vietnamnet'
    allowed_domains = ['vietnamnet.vn']
    start_urls = ['https://vietnamnet.vn/']

    def parse(self, response):
        article_links = response.xpath('//div[@class="horizontalPost-content"]/h3/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//ul[@class="menu datautm-menu"]/li/a/@href').getall()[1:]
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//h3[contains(@class, "vnn-title")]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        cate_links = response.xpath("//div[@class='breadcrumb-box__content']/ul/li/a/@href").getall()
        for link in cate_links:
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//h3[contains(@class, "vnn-title")]/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        article_links = response.xpath('//h4/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()

        news['docID'] = response.xpath('//div[@articletrackingv3="true"]/@articleid').get()

        user_link = response.xpath('//p[@class="newsFeature__author-info"]/span/a/@href').get()
        if user_link:
            news['userID'] = user_link[-11:-5]

        news['type'] = response.xpath('//div[@class="breadcrumb-box__link "]/p/a[1]/@title').get()

        data = response.xpath('//script[@type="application/ld+json"]/text()').getall()[1]
        data = data.replace('\n', '')
        data_obj = json.loads(data)
        dateString = data_obj['datePublished'][:-7] + '000'
        news['createDate'] = dateString
        news['shortFormDate'] = dateString[:10]

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
