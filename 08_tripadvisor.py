from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector 
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class Review(Item):
    title = Field()
    score = Field()
    content = Field()
    autor = Field()

class TripAdvisor(CrawlSpider):
    name = 'TripAdvisor'
    custom_settings = {
        "USER_AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        #"FEED_EXPORT_ENCODING": "utf-8",
        "CLOSESPIDER_PAGECOUNT": 30 # Count of the number of pages that Scrapy visits.
    }

    download_delay = 1

    allowed_domains = ['tripadvisor.com.pe']

    start_urls = ["https://www.tripadvisor.com.pe/Hotels-g15221234-San_Isidro_Lima_Region-Hotels.html"]

    rules = (
        Rule(LinkExtractor(r'-oa\d+'), follow = True), # Pagination of Hotels
        Rule(LinkExtractor(r'/Hotel_Review-', restrict_xpaths=["//div[@id='taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0']//a[@data-clicksource='HotelName']"]), follow = True), # Detail of Hotel 
        Rule(LinkExtractor(r'-or\d+-'), follow = True), # Pagination of comments
        Rule(LinkExtractor(r'/Profile/', 
                            restrict_xpaths = ["//div[@data-test-target='reviews-tab']//a[@class='ui_header_link bPvDb']"]), 
                            follow = True, callback='parse_review') # Detail of profile user
    )

    def get_score(self, text):
        score = text.split('_')[-1]
        return score


    def parse_review(self, response):
        sel = Selector(response)
        reviews = sel.xpath("//div[@id='content']/div/div")

        autor = sel.xpath("//h1/span/text()").get()

        for ix, review in enumerate(reviews):
            item = ItemLoader(Review(), review)
            item.add_value('autor', autor)
            item.add_xpath('title', ".//div[@class= 'fpXkH b _a eCoog']/text()")
            item.add_xpath('score', ".//div[@class='cncQp eCoog']/span[contains(@class, 'ui_bubble_rating')]/@class", MapCompose(self.get_score))
            item.add_xpath('content', ".//q/text()")
            
            yield item.load_item()

process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'tripadvisor_reviews.json'
})
process.crawl(TripAdvisor)
process.start()