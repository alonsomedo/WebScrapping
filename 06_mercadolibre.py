from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector 
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class Article(Item):
    title = Field()
    price = Field()
    description = Field()


class MercadoLibreCrawler(CrawlSpider):
    name = 'MercadoLibre'
    custom_settings = {
        "USER_AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "FEED_EXPORT_ENCODING": "utf-8",
        "CLOSESPIDER_PAGECOUNT": 10 # Count of the number of pages that Scrapy visits.
    }

    download_delay = 1
    start_urls = ["https://listado.mercadolibre.com.pe/animales-mascotas/perros/"]
    # We do this to restrict our search spectre to certains domains. 
    allowed_domains = ['listado.mercadolibre.com.pe', 'articulo.mercadolibre.com.pe']

    rules = (
            # Pagination
            Rule(
                LinkExtractor(
                    allow=r'/_Desde_'
                ), follow=True
            ),
            # Detail of products
            Rule(
                LinkExtractor(
                    allow = r'/MPE-'
                ), follow = True, callback = 'parse_items'
            ),
        )

    def cleaning_text(self, text):
        clean_text = text.replace('\n', ' ').replace('\r', ' ').replace(',','').strip()
        return clean_text

    def clean_and_parse_price(self, text_price):
        clean_price = float(text_price.replace('.','').strip())
        return clean_price

    def parse_items(self, response):
        sel = Selector(response)
        item = ItemLoader(Article(), sel)
        item.add_xpath( "title",
                        "//h1[@class='ui-pdp-title']/text()",
                        MapCompose(self.cleaning_text)
                    )
        item.add_xpath( "description", 
                        "//div[@class='ui-pdp-description']/p/text()",
                        MapCompose(self.cleaning_text)
                    )
        item.add_xpath( "price",
                        "//div[@class='ui-pdp-price__second-line']//span[@class='price-tag-fraction']/text()",
                        MapCompose(self.clean_and_parse_price)
                    )

        yield item.load_item()

process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'mercadolibre.json'
})
process.crawl(MercadoLibreCrawler)
process.start()
