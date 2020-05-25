# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentVarietyListItem(scrapy.Item):
    '''
            下面是具体的一个variety的所有列表信息
    '''

    variety_title = scrapy.Field()
    variety_url = scrapy.Field()
    variety_image = scrapy.Field()
    parent_id = scrapy.Field()
    parent_title = scrapy.Field()
    date = scrapy.Field()
    create_time = scrapy.Field()
