# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class STestItem(scrapy.Item):
    # 下面是movie 分类的信息
    name = scrapy.Field()  # 剧情
    url = scrapy.Field()   #
    key = scrapy.Field()  # itype
    key_val = scrapy.Field()  # 100012
    label = scrapy.Field()  # 类型

class MovieItem(scrapy.Item):
    '''
        下面是具体的一个movie的信息
    '''
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
    charge = scrapy.Field()
    key = scrapy.Field()
    key_val = scrapy.Field()
    pinyin = scrapy.Field()
    py = scrapy.Field()


class TvItem(scrapy.Item):
    '''
        下面是具体的一个tv的信息
    '''
    tv_url = scrapy.Field()
    tv_image = scrapy.Field()
    tv_title = scrapy.Field()
    tv_desc = scrapy.Field()
    tv_all = scrapy.Field()
    tv_caption = scrapy.Field()
    offset = scrapy.Field()
    feature = scrapy.Field()
    iarea = scrapy.Field()
    year = scrapy.Field()
    pay = scrapy.Field()
    key = scrapy.Field()
    key_val = scrapy.Field()
    type = scrapy.Field()
    create_time = scrapy.Field()
    pinyin = scrapy.Field()
    py = scrapy.Field()

class TvList(scrapy.Item):
    '''
        下面是具体的一个tv的所有列表信息
    '''
    tv_num = scrapy.Field()
    tv_title = scrapy.Field()
    tv_url = scrapy.Field()
    parent_id = scrapy.Field()
    parent_title = scrapy.Field()
    is_trail_notice = scrapy.Field()
    create_time = scrapy.Field()
    tv_all = scrapy.Field()


class VarietyItem(scrapy.Item):
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


class VarietyList(scrapy.Item):
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


class CartoonItem(scrapy.Item):
    '''
        下面是具体的一个variety的所有列表信息
    '''

    cartoon_url = scrapy.Field()
    cartoon_image = scrapy.Field()
    cartoon_title = scrapy.Field()
    cartoon_desc = scrapy.Field()
    cartoon_all = scrapy.Field()
    cartoon_caption = scrapy.Field()
    offset = scrapy.Field()
    itype = scrapy.Field()
    iarea = scrapy.Field()
    iyear = scrapy.Field()
    ipay = scrapy.Field()
    plot_aspect = scrapy.Field()
    language = scrapy.Field()
    key = scrapy.Field()
    key_val = scrapy.Field()
    type = scrapy.Field()
    px = scrapy.Field()
    pinyin = scrapy.Field()
    py = scrapy.Field()
    source = scrapy.Field()
    create_time = scrapy.Field()

class CartoonList(scrapy.Item):
    '''
        下面是具体的一个cartoon的所有列表信息
    '''
    cartoon_num = scrapy.Field()
    cartoon_title = scrapy.Field()
    cartoon_url = scrapy.Field()
    parent_id = scrapy.Field()
    parent_title = scrapy.Field()
    is_trail_notice = scrapy.Field()
    create_time = scrapy.Field()
    cartoon_all = scrapy.Field()