# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import TencentMovieCategoryItem
import pymysql
import pymysql.cursors
import pypinyin

class TencentMovieCategoriesSpider(scrapy.Spider):
    name = "tencent_movie_categories"
    allowed_domains = ["qq.com"]
    #MOVIE
    #start_urls = ['https://v.qq.com/channel/movie?listpage=1&channel=movie&sort=18&_all=1']
    #TV
    #start_urls = ['https://v.qq.com/channel/tv?listpage=1&channel=tv&sort=18&_all=1']
    #variety
    start_urls = ['https://v.qq.com/channel/variety?listpage=1&channel=variety&sort=4&_all=1']
    def parse(self, response):
        py = PyQuery(response.text)

        type_list = py("body > div.mod_row_box >div >div.mod_list_filter").find(".filter_line")


        for filter_line in type_list.items():
            filter_label = filter_line(".filter_label").text()

            a_tag_list = filter_line.find("a.filter_item")

            for a_tag in a_tag_list.items():
                item = TencentMovieCategoryItem()
                item["label"] = filter_label
                item["name"] = a_tag.attr("_stat").split("_")[1]
                item["url"] = a_tag.attr("href")
                if a_tag.attr("data-key") == 'year':
                    item["key"] = 'iyear'
                else:
                    item["key"] = a_tag.attr("data-key")
                item["key_val"] = a_tag.attr("data-value")


                #return
                yield item
