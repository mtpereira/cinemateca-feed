from pytz import timezone
import pytz
import re

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

            try:
              #realizador
              infoBiblio = movie.select('div[@class="infoBiblio"]/text()').extract()
              #0 - realizador
              director = infoBiblio[0].strip(' \t\n\r')
              #1 - actores
              actors = infoBiblio[1].strip(' \t\n\r')
              #2 - pais, data - tempo
              reg = re.compile(r'(?P<country>.*?),'
                r' +'
                r'(?P<year>\d{4})'
                r' +- +'
                r'(?P<duration>\d{,3})')
              temp = reg.match(infoBiblio[2])
              country = temp.group('country')
              year = int(temp.group('year'))
              duration = int(temp.group('duration'))

            except Exception, e:
              pass

            for info in movie.select('div[@class="infoText"]/p/text()').extract():
                desc += info.strip(' \t\n\r')
                desc += '\n'

            dates_locations = movie.select('div[@class="infoDate"]/text()').re('\d{,2}-\d{,2}-\d{4}, \d{,2}h\d{,2} \| .*')
            for date_location in dates_locations:
                item = ScheduleItem()

                # dates are stored in Lisbon utc
                date, location = date_location.split("|")
                date_obj = datetime.strptime(date.strip(' \t\n\r'), '%d-%m-%Y, %Hh%M')
                date_obj_aware = localtz.localize(date_obj);

                item['date'] = date_obj_aware
                item['title'] = title.strip(' \t\n\r')
                item['location'] = location.strip(' \t\n\r')

                try:
                  item['director'] = director
                  item['actors'] = actors
                  item['country'] = country
                  item['year'] = year
                  item['duration'] = duration
                except NameError:
                  pass

                item['desc'] = desc.strip(' \t\n\r')
                items.append(item)
        return items

    def parse(self, response):
        items = []
        hxs = HtmlXPathSelector(response)
        schedule = hxs.select('//div[@class="sectionLayoutRight"]')
        items = self.parse_movies("infoDetail", schedule) + self.parse_movies("infoDetail hide", schedule)
        return items

