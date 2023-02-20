from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

spider_names = ['vtv', 'vov', 'vnexpress', 'vietnamnet', 'tuoitre', 'thanhnien',
                'nhandan', 'nld', 'laodong', 'kiemsat', 'dantri', 'cand',
                'thoibaotaichinh', 'baochinhphu', 'zingnews']


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    for spider_name in spider_names:
        process.crawl(spider_name)

    process.start()
