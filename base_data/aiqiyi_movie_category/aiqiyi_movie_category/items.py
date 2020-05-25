# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AiqiyiMovieCategoryItem(scrapy.Item):
    name = scrapy.Field()  # 剧情
    url = scrapy.Field()  #
    key = scrapy.Field()  # itype
    key_val = scrapy.Field()  # 100012
    label = scrapy.Field()  # 类型
    year = scrapy.Field()  #
