# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import AiqiyiMovieCategoryItem
from urllib import parse
from .. import db

class AqyMovieCategorySpider(scrapy.Spider):
    name = "aqy_movie_category"
    allowed_domains = ["iqiyi.com"]
    start_urls = ['https://list.iqiyi.com/www/1/-------------11-1-1-iqiyi--.html']

    def parse(self, response):
        self.connect_mysql()
        self.cursor.execute("select * from movie_category")
        data = self.cursor.fetchall()
        dict = {}
        for it in data:
            dict[it['name']] = ['', '']
            dict[it['name']][0] = it['key']
            dict[it['name']][1] = it['key_val']
        print("-------------------------")
        py = PyQuery(response.text)
        type_list = py("#block-B  .category-content  .category-class.category-class2 .category-list")
        for index in range(type_list.length):
            if index > 0  and index < type_list.length -1:
                item = AiqiyiMovieCategoryItem()
                item['label'] = py(type_list[index])(".selected .category-text").text()
                filter_item = py(type_list[index])(".category-item")
                for filter in filter_item.items():
                    id = filter.attr("data-id")
                    if id!=None:
                        item['url'] = 'https://list.iqiyi.com/www/1/' + str(id) + '-------------11-1-1-iqiyi--.html',
                        item['name'] = filter(".category-text").text()
                        if dict.get(item['name']):
                            item['key'] = dict.get(item['name'])[0]
                            item['key_val'] = dict.get(item['name'])[1]
                        else:
                            item['key'] = ""
                            item['key_val'] = ""
                        yield item



    def connect_mysql(self):  # 连接数据库
        self.connect = db.mysqlConnect
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
