from urllib import response
import scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector 
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


usename = open('./credentials.txt').readline().split(',')[0]
password = open('./credentials.txt').readline().split(',')[1]

class LoginGithub(Spider):
    name = 'Github Login'
    start_urls = ['https://github.com/login']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata = {
                'login': usename,
                'password': password
            },
            callback = self.after_login
        )

    def after_login(self, response):
        # We need to make an artifice , a forced request to go to the repositories lists
        request = scrapy.Request(
            'https://github.com/alonsomedo?tab=repositories',
            callback=self.parse_repositories
        )
        
        yield request

    def parse_repositories(self, response):
        sel = Selector(response)
        repositories = sel.xpath('//h3[@class="wb-break-all"]/a/text()')
        for repo in repositories:
            print(repo.get())


process = CrawlerProcess()
process.crawl(LoginGithub)
process.start()