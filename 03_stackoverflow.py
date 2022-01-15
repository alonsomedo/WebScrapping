from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector 
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


class Question(Item):
    id = Field()
    title = Field()
    #description = Field()

class StackOverflowSpider(Spider):
    name = "FirstSpider"
    custom_settings = {
        "USER_AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }

    start_urls = ['https://stackoverflow.com/questions']

    def parse(self, response):
        sel = Selector(response)
        questions = sel.xpath("//div[@id='questions']//div[@class='question-summary']")

        i=0
        for question in questions:
            item = ItemLoader(Question(), question)
            item.add_xpath("title",".//h3/a/text()") # We use dot (.) because it has to be a relative position from "question".
            #item.add_xpath("description",".//div[@class='excerpt']/text()") 
            item.add_value('id', i) # To add a value directly to a property with a defined value
            i += 1
            yield item.load_item()

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(StackOverflowSpider) 
    process.start()

# If we want to run the script without main , we need to use the following sentence in the terminal.
# scrapy runspider 03_stackoverflow.py -o stackoverflow.csv -t csv

