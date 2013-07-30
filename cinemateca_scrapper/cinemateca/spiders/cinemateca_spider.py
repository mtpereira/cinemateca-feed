from pytz import timezone
import pytz

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from cinemateca.schedule import ScheduleItem
from datetime import date, datetime

class CinematecaSpider(BaseSpider):

    name = "cinemateca"
    allowed_domains = ["cinemateca.pt"]

    def __init__(self, date=date.today().strftime("%Y-%m-%d")):
        self.start_urls = ["http://www.cinemateca.pt/programacao.aspx?date=%s" % date]

    def parse_movies(self, div, schedule):
        items = []
        localtz = timezone('Europe/Lisbon');

        for movie in schedule.select('div[@class="%s"]' % div):
            title = movie.select('div[@class="infoTitleProg"]/text()').extract()[0]
            desc = ""
            for info in movie.select('div[@class="infoBiblio"]/text()').extract():
                desc += info.strip(' \t\n\r')
                desc += '\n'
            for info in movie.select('div[@class="infoText"]/p/text()').extract():
                desc += info.strip(' \t\n\r')
                desc += '\n'
            dates_locations = movie.select('div[@class="infoDate"]/text()').re('\d{,2}-\d{,2}-\d{4}, \d{,2}h\d{,2} \| .*')
            for date_location in dates_locations:
                item = ScheduleItem()
                
                # dates are stored in Lisbon timezone
                date, location = date_location.split("|")
                date_obj = datetime.strptime(date.strip(' \t\n\r'), '%d-%m-%Y, %Hh%M')
                date_obj_aware = localtz.localize(date_obj); 
                
                #item['datetime'] = date_obj.strftime('%Y-%m-%d %H:%M')
                item['date'] = date_obj_aware
                item['title'] = title.strip(' \t\n\r')
                item['location'] = location.strip(' \t\n\r')
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

