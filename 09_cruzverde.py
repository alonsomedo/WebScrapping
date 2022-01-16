from urllib import response
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector 
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class Product(Item):
    name = Field()
    price = Field()

class CruzVerdeCrawler(CrawlSpider):
    name = 'CruzVerde'
    
    custom_settings = {
        "USER_AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "FEED_EXPORT_ENCODING": "UTF-8",
        "CLOSESPIDER_PAGECOUNT": 2 # Count of the number of pages that Scrapy visits.
    }

    download_delay = 1

    allowed_domains = ['cruzverde.cl']

    start_urls = ["https://www.cruzverde.cl/medicamentos/"]

    rules= (
        Rule(LinkExtractor(r'start=', tags = ('a', 'button'), attrs = ('href', 'data-url')), follow = True, callback = 'parse_product'),
    )

    def cleaning_text(self, text):
        clean_text = text.replace('\n', ' ').replace('\r', ' ').replace(',','').strip()
        return clean_text

    def clean_and_parse_price(self, text_price):
        price = text_price.replace('$','').replace('(Oferta)', '').replace('\n', ' ').replace('\r', ' ').strip()
        return price


    def parse_product(self, response):
        sel = Selector(response)
        products = sel.xpath('//div[@class="col-12 col-lg-4"]')

        for p in products:
            item = ItemLoader(Product(), p)
            item.add_xpath('name','.//div[@class="pdp-link"]/a/text()', MapCompose(self.cleaning_text))
            item.add_xpath('price','.//div[@class="price"]//span[@class="value"]/text()', MapCompose(self.clean_and_parse_price))
            yield item.load_item()

process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'cruzverde.json'
})    
process.crawl(CruzVerdeCrawler)
process.start()

