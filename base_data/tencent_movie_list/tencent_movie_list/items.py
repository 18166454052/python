# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentMovieListItem(scrapy.Item):
    movie_url = scrapy.Field()
    movie_score = scrapy.Field()
    movie_image = scrapy.Field()
    movie_title = scrapy.Field()
    movie_desc = scrapy.Field()
    offset = scrapy.Field()
    itype = scrapy.Field()
    iarea = scrapy.Field()
    characteristic = scrapy.Field()
    year = scrapy.Field()
    iyear = scrapy.Field()
    order = scrapy.Field()
    charge = scrapy.Field()
    key = scrapy.Field()
    key_val = scrapy.Field()
    pinyin = scrapy.Field()
    py = scrapy.Field()
