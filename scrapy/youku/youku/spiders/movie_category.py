# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import CategoryItem
import sys

print(sys.path)


class BaiduSpider(scrapy.Spider):
    name = 'movie_category'
    # allowed_domains = ['lab.scrapy.cn']
    start_urls = ['https://list.youku.com/category/show/c_96.html?spm=a2ha1.12701310.app.5~5!2~5!2~5~5~DL~DD~A!2']

    def parse(self, response):
        py = PyQuery(response.text)

        type_list = py("body > div.mod_row_box >div >div.mod_list_filter").find(".filter_line")

        for filter_line in type_list.items():
            filter_label = filter_line(".filter_label").text()

            a_tag_list = filter_line.find("a.filter_item")

            for a_tag in a_tag_list.items():
                item = CategoryItem()
                item["label"] = filter_label
                item["name"] = a_tag.attr("_stat").split("_")[1]
                item["url"] = a_tag.attr("href")
                item["key"] = a_tag.attr("data-key")
                item["key_val"] = a_tag.attr("data-value")

                yield item
