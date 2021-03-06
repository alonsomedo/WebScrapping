from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector 
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class Hotel(Item):
    name = Field()
    score = Field()
    desciption = Field()
    amenities = Field()

class TripAdvisor(CrawlSpider):
    name = "TripAdvisorHotels"
    custom_settings = {
        #"USER_AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_FIELDS': ['name', 'score', 'description', 'amenities'],
        'CONCURRENT_REQUESTS': 10,
        'DOWNLOADER_MIDDLEWARES': { # pip install Scrapy-UserAgents
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },
        'USER_AGENTS': [
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
            # chrome
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
            # chrome
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',  # firefox
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
            # chrome
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
            # chrome
        ]
    }

    start_urls = ['https://www.tripadvisor.com.pe/Hotels-g15221234-San_Isidro_Lima_Region-Hotels.html']
    
    # Range between 0.5 * download_delay and 1.5 * download_delay
    download_delay = 2

    # follow: the links of Hotel_Review, should i follow them? True or False
    rules = (
            Rule(
            LinkExtractor(
                allow = r'/Hotel_Review-'
            ), follow = True, callback = 'parse_hotel'
        ),
    )

    def parse_start_url(self, response):
        sel = Selector(response)
        hoteles = sel.xpath('//div[@class="prw_rup prw_meta_hsx_listing_name listing-title"]')
        print("Numero de hoteles", len(hoteles))
         

    def round_score_to_upper(self, text):
        score = str(round(int(text[0])))
        return score


    def parse_hotel(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)
        item.add_xpath('name', "//h1[@id='HEADING']/text()") 
        item.add_xpath('score', "//span[@class='bvcwU P']/text()", MapCompose(self.round_score_to_upper)) 
        item.add_xpath('desciption', "//div[contains(@class, 'duhwe _T bOlcm bWqJN Ci')]/div/text()")
        item.add_xpath('amenities', "//div[contains(@class, 'bUmsU f ME H3 _c')]/text()")  

        yield item.load_item()
 
process = CrawlerProcess({
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'tripadvisor.csv'
})    
process.crawl(TripAdvisor)
process.start()
