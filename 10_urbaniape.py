from urllib import response
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector 
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
import re


def process_link(value):
    m = re.search(r"data-to-posting\('(.*?)'", value)
    print('**************************************************************')
    print(m)
    return m

class Department(Item):
    name = Field()
    address = Field()

class UrbaniaCrawler(CrawlSpider):
    name = 'Urbania'
    
    custom_settings = {
        "USER_AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "FEED_EXPORT_ENCODING": "UTF-8",
        "CLOSESPIDER_PAGECOUNT": 5 # Count of the number of pages that Scrapy visits.
    }

    download_delay = 1

    allowed_domains = ['urabnia.pe']

    start_urls = [  'https://urbania.pe/buscar/proyectos-propiedades-en-lima?page=1',
                    'https://urbania.pe/buscar/proyectos-propiedades-en-lima?page=2',
                    'https://urbania.pe/buscar/proyectos-propiedades-en-lima?page=3',
                    'https://urbania.pe/buscar/proyectos-propiedades-en-lima?page=4',
                    'https://urbania.pe/buscar/proyectos-propiedades-en-lima?page=5'
                ]


    rules = (
        Rule(LinkExtractor(tags = ('a', 'div'), attrs = ('href', 'data-to-posting'), process_value = process_link), follow = True, callback = 'parse_department' ),
    )

    def parse_department(self, response):
        sel = Selector(response)
        item = ItemLoader(Department(), sel)
        item.add_xpath('name', '//h2[@class="title"]/text()')
        item.add_xpath('address', '//div[@class="development-title-container"]/p/text()')

        yield item.load_item()

process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'urbania.json'
})
process.crawl(UrbaniaCrawler)
process.start()




        






