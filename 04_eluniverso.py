from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector 
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup


class News(Item):
    _index = Field()
    title = Field()
    description = Field()

class ElUniversoSpider(Spider):
    name = "My Second Spider"
    custom_settings = {
        "USER_AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    start_urls = ['https://www.eluniverso.com/deportes/']

    def parse(self, response):
        # Using Scrappy

        sel = Selector(response)
        news = sel.xpath("//div[contains(@class,'content-feed')]/ul/li")
        
        for ix,new in enumerate(news):
            item = ItemLoader(News(), new)
            item.add_value("_index", ix) 
            item.add_xpath("title",".//h2/a/text()")
            item.add_xpath("description",".//p/text()")

            yield item.load_item()

process = CrawlerProcess({
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'eluniverso.csv'
})
process.crawl(ElUniversoSpider)
process.start()
    