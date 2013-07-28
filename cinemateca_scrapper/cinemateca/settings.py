# Scrapy settings for cinemateca project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'cinemateca'

SPIDER_MODULES = ['cinemateca.spiders']
NEWSPIDER_MODULE = 'cinemateca.spiders'

ITEM_PIPELINES = ['scrapy_mongodb.MongoDBPipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cinemateca (+http://www.yourdomain.com)'

# ujson : exporter for utf8-encoded JSON
FEED_EXPORTERS = {'ujson' : 'cinemateca.exporters.UnicodeJsonLinesItemExporter'}

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'movies'
MONGODB_UNIQUE_KEY = 'date'