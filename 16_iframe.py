from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector 
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy import Request


class Dummy(Item):
    title = Field()
    title_iframe = Field()

class W3SchoolCrawler(Spider):
    name = 'w3s'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'REDIRECT_ENABLED': True # Parametro para activar los redirects (codigo 302)
    } 

    allowed_domains = ['w3schools.com']
    start_urls = ['https://www.w3schools.com/html/html_iframe.asp']
    
    download_delay = 2

    def parse(self, response):
        sel = Selector(response)
        title = sel.xpath('//div[@id="main"]//h1/span/text()').get()

        # We are going to use this variable to pass data from the father page to the iframe
        previous_data = {
            'title': title
        }

        iframe_url = sel.xpath('//div[@id="main"]//iframe[@width="99%"]/@src').get()
        iframe_url = "https://www.w3schools.com/html/" + iframe_url

        yield Request(
                iframe_url, 
                callback = self.parse_iframe, 
                meta = previous_data
            )

    def parse_iframe(self, response):
        item = ItemLoader(Dummy(), response)
        item.add_xpath('title_iframe', '//div[@id="main"]//h1/span/text()')
        item.add_value('title', response.meta.get('title'))
        yield item.load_item()     

    
process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'iframe.json'
})
process.crawl(W3SchoolCrawler)
process.start()

