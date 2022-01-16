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
    content = Field()

class Review(Item):
    title = Field()
    score = Field()

class Video(Item):
    title = Field()
    publication_date = Field()

class IGNCrawler(CrawlSpider):
    name = 'IGN-LATAM'
    custom_settings = {
        "USER_AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        #"FEED_EXPORT_ENCODING": "utf-8",
        "CLOSESPIDER_PAGECOUNT": 30 # Count of the number of pages that Scrapy visits.
    }

    download_delay = 1

    allowed_domains = ['latam.ign.com']

    start_urls = ["https://latam.ign.com/se/?model=&q=ps5"]
 
    # We do this to restrict our search spectre to certains domains. 
    

    rules = (
        
        Rule(LinkExtractor(r'type='), follow = True), # Type (Article, Review , Video) - Horizontal
        
        Rule(LinkExtractor(r'&page=\d+'), follow = True), # Pagination - Horizontal , "\d+" means any number followed by = 
        
        Rule(LinkExtractor(r'/review/'), follow = True, callback='parse_review'), # Detail of Review - Vertical
        
        Rule(LinkExtractor(r'/video/'), follow = True, callback='parse_video'), # Detail of Video - Vertical
        
        Rule(LinkExtractor(r'/news/'), follow = True, callback='parse_news') # Detail of Article - Vertical
    )

    def parse_news(self, response):
        item = ItemLoader(Article(), response)
        item.add_xpath('title', "//h1[@id='id_title']/text()")
        item.add_xpath('content', "//div[@id='id_text']//*/text()") # Find all the sons and get the text of each one.
        
        yield item.load_item() 

    def parse_review(self, response):
        item = ItemLoader(Review(), response)
        item.add_xpath('title', "//div[@class='article-headline']/h1/text()")
        item.add_xpath('score', "//div[@class='article-review']//span[@class='side-wrapper side-wrapper hexagon-content']/text()")
        
        yield item.load_item() 

    def parse_video(self, response):
        item = ItemLoader(Video(), response)
        item.add_xpath('title', "//h1[@id='id_title']/text()")
        item.add_xpath('publication_date', "//span[@class='publish-date']/text()")

        yield item.load_item() 

process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'ignlatam.json'
})
process.crawl(IGNCrawler)
process.start()
