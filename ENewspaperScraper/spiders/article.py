import scrapy

from ENewspaperScraper.items import newsItem


class candSpider(scrapy.Spider):
    name = 'article'
    start_urls = [
        'https://nhandan.vn/thu-tuong-pham-minh-chinh-du-le-phat-lenh-lam-hang-dau-xuan-quy-mao-tai-cang-tan-cang-cat-lai-post736479.html'
    ]

    def parse(self, response):
        news = newsItem()

        news['docID'] = response.xpath('//meta[@property="dable:item_id"]/@content').get()
        news['user'] = response.xpath('//meta[@property="dable:author"]/@content').get()
        news['userID'] = None
        news['type'] = response.xpath('//meta[@property="article:section"]/@content').get()

        dateString = response.xpath('//meta[@itemprop="datePublished"]/@content').get()[:-6] + '.000' + '+07:00'
        news['createDate'] = dateString
        news['shortFormDate'] = dateString[:10]

        news['title'] = response.xpath('//title/text()').get()
        news['description'] = response.xpath('//meta[@name="description"]/@content').get()
        news['message'] = response.xpath('//div[@class="article__body cms-body"]/p//text()').getall()

        link_selectors = response.xpath('//div[@class="related-news"]//article//a')
        news['links_in_article'] = self.getLinksInfo(link_selectors)

        news['picture'] = response.xpath(
            '//div[@class="main-col content-col"]/table[@class="picture"]//img/@src').getall() \
            + response.xpath('//table[@class="picture"]//img/@data-src').getall()

        yield news

    def getLinksInfo(self, selectors):
        links_in_article = []
        link = {}

        for selector in selectors:
            link['name'] = selector.xpath('./@title').get()
            link['link'] = selector.xpath('./@href').get()
            link['description'] = None
            links_in_article.append(link.copy())

        return links_in_article
