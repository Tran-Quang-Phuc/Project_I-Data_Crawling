import scrapy
from scrapy.crawler import CrawlerProcess


class TfhSpider(scrapy.Spider):
    name = '24h.com'
    allowed_domains = ['24h.com.vn']
    start_urls = ['https://www.24h.com.vn/']

    def parse(self, response):
        article_links = response.xpath('//div[@class="bxDnC mrB10" or @class="bxDoC" or @class="bxTrtmC"]//a/@href')
        for link in article_links:
            yield response.follow(link.get(), callback=self.parse_article)

        topic_links = response.xpath('//div[@class="tpMnRt tpMnRtx"]/ul/li/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_topic(self, response):
        topic_links = response.xpath('//div[@class="tpMnRt tpMnRtx"]/ul/li/a/@href').getall()
        for link in topic_links:
            yield response.follow(link, callback=self.parse_topic)

        article_links = response.xpath('//h3/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        sub_topic_links = response.xpath('//nav[@class="cate-24h-foot-menu-top pos-rel"]/ul/li/a/@href').getall()
        for link in sub_topic_links:
            yield response.follow(link, callback=self.parse_topic)

    def parse_sub_topic(self, response):
        article_links = response.xpath('//h3/a/@href').getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        article_links = response.xpath('//figcaption[@class="cate-24h-foot-home-latest-list__info"]/header/p/a/@href')
        for link in article_links:
            yield response.follow(link.get(), callback=self.parse_article)

    def parse_article(self, response):
        yield {
            'id': 12
        }


if __name__ == "__main__":
    news_scraper = CrawlerProcess()
    news_scraper.crawl(TfhSpider)
    news_scraper.start()
