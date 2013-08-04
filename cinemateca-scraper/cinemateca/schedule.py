from scrapy.item import Item, Field

class ScheduleItem(Item):
    title = Field()
    date = Field()
    location = Field()
    director = Field()
    actors = Field()
    country = Field()
    year = Field()
    duration = Field()
    desc = Field()

