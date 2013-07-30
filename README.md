A scraper to collect information about the [Cinemateca](www.cinemateca.pt) program and an API to query for the information.

__Manually run the scraper__

go to cinemateca_scraper/cinemateca and run:

    scrapy crawl cinemateca -t ujson -a date="YYYY-MM-DD"
