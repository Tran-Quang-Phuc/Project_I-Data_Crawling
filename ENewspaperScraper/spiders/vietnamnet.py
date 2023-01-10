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
        if data_obj['datePublished']:
            dateString = data_obj['datePublished'][:-7] + data_obj['datePublished'][-6:]
            news['createDate'] = dateString
            news['shortFormDate'] = dateString[:10]

        news['title'] = response.xpath('//div[@class="newsFeature__header"]/h1/text()').get()
        news['message'] = response.xpath('//div[contains(@class, "maincontent")]//p//text()').getall()

        link_selectors = response.xpath('//div[contains(@class, "maincontent")]//p/a') \
            + response.xpath('//div[@class="related-news mb-25"]/ul/li/p/a') \
            + response.xpath('//div[@class="insert-wiki-content"]')
        news['links_in_article'] = self.getLinksInfo(link_selectors)

        news['picture'] = response.xpath('//div[contains(@class, "maincontent")]//figure/img/@src').getall()

        yield news

    def getLinksInfo(self, link_selectors):
        links_in_article = []
        link = {}
        for link_selector in link_selectors:
            # link_selector = Selector(text=link_selector)
            if link_selector.xpath('./@href').get():
                if link_selector.xpath('./@title').get():
                    link['name'] = link_selector.xpath('./@title').get()
                else:
                    link['name'] = link_selector.xpath('.//text()').get()
                link['link'] = link_selector.xpath('./@href').get()
                link['description'] = None
                links_in_article.append(link.copy())
            else:
                link['name'] = link_selector.xpath('./h3/a/text()').get()
                link['link'] = link_selector.xpath('./h3/a/@href').get()
                link['description'] = link_selector.xpath('./div[@class="insert-wiki-description"]/text()').get()
                links_in_article.append(link.copy())

        return links_in_article

