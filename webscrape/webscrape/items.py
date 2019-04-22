# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    artist = scrapy.Field()
    rank = scrapy.Field()
    date_ = scrapy.Field()
    last_week_rank = scrapy.Field()
    peak_rank = scrapy.Field()
    weeks_on_chart = scrapy.Field() 