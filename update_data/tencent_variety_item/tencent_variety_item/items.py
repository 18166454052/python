# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentVarietyItem(scrapy.Item):
    '''
            下面是具体的一个综艺variety的信息
    '''
    variety_url = scrapy.Field()
    variety_image = scrapy.Field()
    variety_title = scrapy.Field()
    variety_desc = scrapy.Field()
    offset = scrapy.Field()
    exclusive = scrapy.Field()
    itype = scrapy.Field()
    iarea = scrapy.Field()
    iyear = scrapy.Field()
    ipay = scrapy.Field()
    order = scrapy.Field()
    key = scrapy.Field()
    key_val = scrapy.Field()
    type = scrapy.Field()
    pinyin = scrapy.Field()
    py = scrapy.Field()
    create_time = scrapy.Field()