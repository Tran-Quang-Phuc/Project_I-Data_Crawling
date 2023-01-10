import scrapy
from scrapy.crawler import CrawlerProcess

from ENewspaperScraper.items import newsItem


class vnexpressSpider(scrapy.Spider):
    name = 'vnexpress'
    # custom_settings = {'CLOSESPIDER_PAGECOUNT': 100}
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/']

    def parse(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        topic_links = response.xpath('//nav[@class="main-nav"]/ul[1]/li/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        category_links = response.xpath('//ul[@class="ul-nav-folder"]/li/a/@href').getall()
        for link in category_links:
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        article_links = response.xpath('//article//a[1]/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        news = newsItem()

        news['docID'] = response.xpath('//meta[@name="tt_article_id"]/@content').get()
        news['user'] = response.xpath('//article[@class="fck_detail "]/p[last()]//text()').get()
        news['userID'] = None
        news['type'] = response.xpath('//ul[@class="breadcrumb"]/li/a/@title').get()

        dateString = response.xpath('//meta[@itemprop="dateCreated"]/@content').get()
        if dateString:
            dateString = dateString[:-6] + '.000000' + dateString[-6:]
            news['createDate'] = dateString
            news['shortFormDate'] = dateString[:10]

        news['title'] = response.xpath('//h1[@class="title-detail"]/text()').get()
        news['message'] = response.xpath('//article[@class="fck_detail "]/p//text()').getall()

        link_selecters = response.xpath('//article[@class="fck_detail "]/p/a') \
            + response.xpath('//article[@class="item-news"]')  # not in response?
        news['links_in_article'] = self.getLinksInfo(link_selecters)

        news['picture'] = response.xpath('//article[@class="fck_detail "]//img/@data-src').getall()

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


if __name__ == "__main__":
    news_crawler = CrawlerProcess()
    news_crawler.crawl(vnexpressSpider)
    news_crawler.start()
