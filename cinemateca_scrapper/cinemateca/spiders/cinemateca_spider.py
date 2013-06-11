from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from cinemateca.schedule import ScheduleItem
from datetime import date as libdate

class CinematecaSpider(BaseSpider):

    name = "cinemateca"
    allowed_domains = ["cinemateca.pt"]

    def __init__(self, date=libdate.today().strftime("%Y-%m-%d")):
        self.start_urls = ["http://www.cinemateca.pt/programacao.aspx?date=%s" % date]

    def parse_movies(self, div, schedule):
        items = []
        for movie in schedule.select('div[@class="%s"]' % div):
            title = movie.select('div[@class="infoTitleProg"]/text()').extract()[0]
            desc = ""
            for info in movie.select('div[@class="infoBiblio"]/text()').extract():
                desc += info.encode('utf8').strip(' \t\n\r')
                desc += '\n'
            for info in movie.select('div[@class="infoText"]/p/text()').extract():
                desc += info.encode('utf8').strip(' \t\n\r')
                desc += '\n'
            dates_locations = movie.select('div[@class="infoDate"]/text()').re('\d{,2}-\d{,2}-\d{4}, \d{,2}h\d{,2} \| .*')
            for date_location in dates_locations:
                item = ScheduleItem()
                date, location = date_location.split("|")
                item['date'] = date.encode('utf8').strip(' \t\n\r')
                item['title'] = title.encode('utf8').strip(' \t\n\r')
                item['location'] = location.encode('utf8').strip(' \t\n\r')
                item['desc'] = desc.strip(' \t\n\r')
                items.append(item)
                print item['date']
                print item['title']
                print item['location']
                print item['desc']
        return items

    def parse(self, response):
        items = []
        hxs = HtmlXPathSelector(response)
        schedule = hxs.select('//div[@class="sectionLayoutRight"]')
        items = self.parse_movies("infoDetail", schedule) + self.parse_movies("infoDetail hide", schedule)
        return items

