from scrapy.item import Item, Field

class ScheduleItem(Item):
    title = Field()
    date = Field()
    location = Field()
    desc = Field()

