from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from cinemateca.schedule import ScheduleItem

class CinematecaSpider(BaseSpider):
    name = "Cinemateca"
    allowed_domains = ["cinemateca.pt"]
    start_urls = ["http://www.cinemateca.pt/programacao.aspx?date=2013-06-14"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        schedule = hxs.select('//div[@class="sectionLayoutRight"]')
        items = []
        for movie in schedule.select('div[@class="infoDetail hide"]'):
            title = movie.select('div[@class="infoTitleProg"]/text()').extract()[0]
            print title
            dates = movie.select('div[@class="infoDate"]/text()').re('\d{,2}-\d{,2}-\d{4}, \d{,2}h\d{,2}')
            for date in dates:
                print date
                item = ScheduleItem()
                item['date'] = date
                item['title'] = title
                item['location'] = "location"
                item['desc'] = "desc"
                items.append(item)
        return items

