# -*- coding: utf-8 -*-
import scrapy


class TencentTvItemsSpider(scrapy.Spider):
    name = "tencent_tv_items"
    allowed_domains = ["qq.com"]
    start_urls = ['http://qq.com/']

    def parse(self, response):
        pass
