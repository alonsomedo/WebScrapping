
from twisted.internet import reactor
from twisted.internet.task import LoopingCall 
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import Spider

class WeatherExtractor(Spider):
    name = "Crawler of Weather"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20,
        'LOG_ENABLED': True
    }

    start_urls = [
        "https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947",
        "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846",
        "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
    ]

    def parse(self, response):
        city = response.xpath('//a[class="header-city-link"]/h1/text()').get()
        current = response.xpath('//div[contains(@class, "cur-con-weather-card__panel")]//div[@class="temp"]/text()').get()
        real_feel = response.xpath('//div[contains(@class, "cur-con-weather-card__panel")]//div[@class="real-feel"]/text()').get()

        # Limpieza de datos
        city = city.replace('\n', '').replace('\r', '').strip()
        current = current.replace('°', '').replace('\n', '').replace('\r', '').strip()
        real_feel = real_feel.replace('RealFeel®', '').replace('°', '').replace('\n', '').replace('\r', '').strip()
        
        # Guardado de datos en un archivo
        f = open("./datos_clima_scrapy.csv", "a")
        f.write(city + "," + current + "," + real_feel + "\n")
        f.close()
        print(city)
        print(current)
        print(real_feel)
        print()

runner = CrawlerRunner()
task = LoopingCall(lambda: runner.crawl(WeatherExtractor)) 
task.start(20) 
reactor.run()