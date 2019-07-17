# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import STestItem
import sys

print(sys.path)


class BaiduSpider(scrapy.Spider):
    name = 'variety_category'
    # allowed_domains = ['lab.scrapy.cn']
    start_urls = ['https://v.qq.com/channel/variety?listpage=1&channel=variety&sort=4&_all=1']
    '''
    如果要动态拼接路哟   要接受动态传入的参数
    此时要重写 start_request函数
    tag = getattr(self, "tag", None)
    '''

    def parse(self, response):
        py = PyQuery(response.text)

        type_list = py("body > div.mod_row_box >div >div.mod_list_filter").find(".filter_line")

        for filter_line in type_list.items():
            filter_label = filter_line(".filter_label").text()

            a_tag_list = filter_line.find("a.filter_item")

            for a_tag in a_tag_list.items():
                item = STestItem()
                item["label"] = filter_label
                item["name"] = a_tag.attr("_stat").split("_")[1]
                item["url"] = a_tag.attr("href")
                item["key"] = a_tag.attr("data-key")
                item["key_val"] = a_tag.attr("data-value")
                yield item


